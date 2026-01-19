import tkinter as tk
from tkinter import ttk, messagebox
import abc


class NumberConverter(abc.ABC):
    """Абстрактный класс для преобразования числа в разные форматы"""
    @abc.abstractmethod
    def get_format_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_prefix(self) -> str:
        pass

    @abc.abstractmethod
    def convert(self, number: int) -> str:
        pass


class BinaryConverter(NumberConverter):
    def get_format_name(self) -> str:
        return "Двоичная система"

    def get_prefix(self) -> str:
        return "0b"

    def convert(self, number: int) -> str:
        return bin(number)[2:]  # без префикса 0b


class OctalConverter(NumberConverter):
    def get_format_name(self) -> str:
        return "Восьмеричная система"

    def get_prefix(self) -> str:
        return "0o"

    def convert(self, number: int) -> str:
        return oct(number)[2:]


class HexConverter(NumberConverter):
    def get_format_name(self) -> str:
        return "Шестнадцатеричная система"

    def get_prefix(self) -> str:
        return "0x"

    def convert(self, number: int) -> str:
        return hex(number)[2:].upper()


class PropertiesAnalyzer(NumberConverter):
    """Анализ свойств числа (чётность, сумма цифр и т.д.)"""
    def get_format_name(self) -> str:
        return "Анализ свойств"

    def get_prefix(self) -> str:
        return ""

    def convert(self, number: int) -> str:
        parity = "чётное" if number % 2 == 0 else "нечётное"
        digit_sum = sum(int(d) for d in str(abs(number)))
        sign = "положительное" if number > 0 else "отрицательное" if number < 0 else "ноль"
        return f"{sign}, {parity}, сумма цифр = {digit_sum}"


class NumberExplorerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Исследователь чисел")
        self.root.geometry("420x380")
        self.root.configure(bg="#f5f7fa")

        self.converters = [
            BinaryConverter(),
            OctalConverter(),
            HexConverter(),
            PropertiesAnalyzer()
        ]

        self.create_interface()
        self.root.mainloop()

    def create_interface(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Исследователь чисел", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))

        # Поле ввода числа
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", pady=10)

        ttk.Label(input_frame, text="Введите целое число:").pack(side="left", padx=5)
        self.number_var = tk.StringVar(value="42")
        ttk.Entry(input_frame, textvariable=self.number_var, width=15, justify="center").pack(side="left", padx=5)

        # Кнопка "Анализировать"
        ttk.Button(frame, text="Показать все преобразования", command=self.analyze_number).pack(pady=15)

        # Область результатов
        self.result_text = tk.Text(frame, height=12, width=45, wrap="word", font=("Consolas", 11), state="disabled")
        self.result_text.pack(pady=10, fill="both", expand=True)

        # Подсказка
        ttk.Label(frame, text="Поддерживаются положительные и отрицательные числа", foreground="gray").pack(pady=5)

    def analyze_number(self):
        try:
            num = int(self.number_var.get())

            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)

            self.result_text.insert(tk.END, f"Число: {num}\n")
            self.result_text.insert(tk.END, "─" * 40 + "\n")

            for conv in self.converters:
                try:
                    result = conv.convert(num)
                    prefix = conv.get_prefix()
                    name = conv.get_format_name()
                    self.result_text.insert(tk.END, f"{name:<25} → {prefix}{result}\n")
                except Exception as e:
                    self.result_text.insert(tk.END, f"{conv.get_format_name():<25} → Ошибка: {e}\n")

            self.result_text.config(state="disabled")

        except ValueError:
            messagebox.showerror("Ошибка ввода", "Введите корректное целое число!")
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", str(e))


def main():
    NumberExplorerGUI()


if __name__ == "__main__":
    main()
