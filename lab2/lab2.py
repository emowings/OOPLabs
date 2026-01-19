import tkinter as tk
from tkinter import ttk
from math import pow


class InvestmentGrowthCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор роста инвестиций в акции")
        self.root.geometry("450x500")
        self.root.configure(bg="#f0f4f8")

        # Среднегодовая ожидаемая доходность акций (в %)
        self.expected_returns = {
            "1 год": {"до 300 тыс.": 9.5, "300–800 тыс.": 10.0, "800 тыс.–2 млн": 10.5, "свыше 2 млн": 11.0},
            "3 года": {"до 300 тыс.": 10.0, "300–800 тыс.": 10.8, "800 тыс.–2 млн": 11.3, "свыше 2 млн": 11.8},
            "5 лет": {"до 300 тыс.": 10.5, "300–800 тыс.": 11.2, "800 тыс.–2 млн": 11.8, "свыше 2 млн": 12.5},
            "7 лет": {"до 300 тыс.": 11.0, "300–800 тыс.": 11.7, "800 тыс.–2 млн": 12.3, "свыше 2 млн": 13.0},
            "10 лет": {"до 300 тыс.": 11.5, "300–800 тыс.": 12.2, "800 тыс.–2 млн": 12.8, "свыше 2 млн": 13.5},
            "15+ лет": {"до 300 тыс.": 12.0, "300–800 тыс.": 12.7, "800 тыс.–2 млн": 13.3, "свыше 2 млн": 14.0}
        }

        # Частота реинвестирования дивидендов (примерно соответствует периодам)
        self.reinvest_freq = {
            "Без реинвестирования": 1,
            "Ежегодно": 1,
            "Ежеквартально": 4,
            "Ежемесячно": 12,
            "Ежедневно": 365
        }

        self.create_interface()

    def create_interface(self):
        frame = tk.Frame(self.root, bg="#f0f4f8")
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame, text="Начальная сумма инвестиций (руб)", bg="#f0f4f8", font=("Arial", 11)).pack(anchor="w", pady=(10,0))
        self.initial_entry = ttk.Entry(frame, width=25)
        self.initial_entry.pack(pady=5)
        self.initial_entry.insert(0, "150000")

        tk.Label(frame, text="Горизонт инвестирования", bg="#f0f4f8", font=("Arial", 11)).pack(anchor="w", pady=(15,0))
        self.horizon_var = tk.StringVar(value="5 лет")
        ttk.Combobox(frame, textvariable=self.horizon_var, 
                     values=list(self.expected_returns.keys()), 
                     state="readonly", width=22).pack(pady=5)

        tk.Label(frame, text="Частота реинвестирования дивидендов", bg="#f0f4f8", font=("Arial", 11)).pack(anchor="w", pady=(15,0))
        self.reinvest_var = tk.StringVar(value="Ежеквартально")
        ttk.Combobox(frame, textvariable=self.reinvest_var,
                     values=list(self.reinvest_freq.keys()),
                     state="readonly", width=22).pack(pady=5)

        tk.Label(frame, text="Дивидендная доходность (годовая, %)", bg="#f0f4f8", font=("Arial", 11)).pack(anchor="w", pady=(15,0))
        self.dividend_entry = ttk.Entry(frame, width=25)
        self.dividend_entry.pack(pady=5)
        self.dividend_entry.insert(0, "4.5")

        # Кнопка расчёта
        ttk.Button(frame, text="Рассчитать ожидаемый результат", command=self.compute_growth).pack(pady=25)

        # Результат
        self.result_text = tk.Text(frame, height=12, width=50, wrap="word", font=("Consolas", 10), bg="#ffffff", relief="flat", bd=1)
        self.result_text.pack(pady=10, fill="x")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

    def compute_growth(self):
        try:
            initial = float(self.initial_entry.get().replace(" ", "").replace(",", "."))
            horizon = self.horizon_var.get()
            reinvest_type = self.reinvest_var.get()
            div_yield = float(self.dividend_entry.get().replace(" ", "").replace(",", "."))

            if initial < 30000:
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, "Минимальная сумма инвестиций — 30 000 ₽")
                self.result_text.config(fg="red")
                return

            # Определение категории суммы
            if initial < 300000:
                category = "до 300 тыс."
            elif initial <= 800000:
                category = "300–800 тыс."
            elif initial <= 2000000:
                category = "800 тыс.–2 млн"
            else:
                category = "свыше 2 млн"

            # Среднегодовая ожидаемая доходность (включая рост цены и дивиденды)
            r = self.expected_returns[horizon][category]  # в %

            # Длительность в годах
            years = {"1 год": 1, "3 года": 3, "5 лет": 5, "7 лет": 7, "10 лет": 10, "15+ лет": 15}[horizon]

            # Частота реинвестирования
            m = self.reinvest_freq[reinvest_type]

            # Дивидендная доходность в расчётах (часть общей доходности)
            div_rate = div_yield / 100

            # Эффективная доходность с реинвестированием
            if reinvest_type == "Без реинвестирования":
                # Только рост цены без реинвестирования дивидендов
                final = initial * (1 + (r / 100 - div_rate) * years)
                profit = final - initial
                effective = (r - div_yield)
            else:
                # Полная капитализация (рост + реинвестированные дивиденды)
                rate_per_period = (r / 100) / m
                periods = m * years
                final = initial * pow(1 + rate_per_period, periods)
                profit = final - initial
                effective = (pow(1 + rate_per_period, periods) - 1) * 100 / years

            # Формируем красивый вывод
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Категория суммы: {category}\n")
            self.result_text.insert(tk.END, f"Горизонт: {horizon}\n")
            self.result_text.insert(tk.END, f"Ожидаемая доходность: {r:.2f} % годовых\n")
            self.result_text.insert(tk.END, f"Дивидендная доходность: {div_yield:.2f} %\n")
            self.result_text.insert(tk.END, f"Реинвестирование: {reinvest_type}\n")
            self.result_text.insert(tk.END, f"Периодов в год: {m}\n")
            self.result_text.insert(tk.END, "─" * 38 + "\n")
            self.result_text.insert(tk.END, f"Начальная сумма:   {initial:,.0f} ₽\n")
            self.result_text.insert(tk.END, f"Ожидаемая прибыль:  {profit:,.0f} ₽\n")
            self.result_text.insert(tk.END, f"Итоговая стоимость: {final:,.0f} ₽\n")
            self.result_text.insert(tk.END, f"Эффективная доходность: {effective:.2f} % годовых\n")

            self.result_text.config(fg="#006400")  # тёмно-зелёный для успеха

        except ValueError:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Ошибка ввода: проверьте числа")
            self.result_text.config(fg="red")
        except Exception as e:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Ошибка: {str(e)}")
            self.result_text.config(fg="red")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = InvestmentGrowthCalculator()
    calc.run()
