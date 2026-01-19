import tkinter as tk
from tkinter import ttk


class NoteEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Заметки с предпросмотром")
        self.root.geometry("600x550")
        self.root.configure(bg="#f8f9fa")

        self.current_text = ""

        self.themes = {
            "Светлая": {"bg": "#ffffff", "fg": "#212529", "insert": "#0d6efd"},
            "Тёмная": {"bg": "#212529", "fg": "#f8f9fa", "insert": "#6c757d"},
            "Сепия": {"bg": "#fdf6e3", "fg": "#5d4037", "insert": "#8d6e63"},
            "Мятная": {"bg": "#e0f7fa", "fg": "#006064", "insert": "#009688"}
        }

        self.create_ui()
        self.root.mainloop()

    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Мои быстрые заметки", font=("Helvetica", 14, "bold")).pack(pady=(0, 10))

        ttk.Label(main_frame, text="Введите текст заметки:").pack(anchor="w")
        self.text_input = tk.Text(main_frame, height=8, width=60, wrap="word", font=("Arial", 11))
        self.text_input.pack(pady=5, fill="x")
        self.text_input.bind("<KeyRelease>", self.update_preview)

        ttk.Label(main_frame, text="Тема предпросмотра:").pack(anchor="w", pady=(15, 0))
        self.theme_var = tk.StringVar(value="Светлая")
        theme_combo = ttk.Combobox(
            main_frame,
            textvariable=self.theme_var,
            values=list(self.themes.keys()),
            state="readonly",
            width=25
        )
        theme_combo.pack(anchor="w", pady=5)
        theme_combo.bind("<<ComboboxSelected>>", self.apply_theme)

        self.bold_titles_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            main_frame,
            text="Выделять заголовки жирным (строки с #)",
            variable=self.bold_titles_var,
            command=self.update_preview  
        ).pack(anchor="w", pady=10)

        ttk.Label(main_frame, text="Предпросмотр заметки:", font=("Helvetica", 11, "bold")).pack(anchor="w", pady=(15, 5))
        self.preview_text = tk.Text(main_frame, height=10, width=60, wrap="word", font=("Arial", 11), state="disabled")
        self.preview_text.pack(fill="x", pady=5)

        clear_frame = ttk.Frame(main_frame)
        clear_frame.pack(pady=15, fill="x")
        ttk.Button(clear_frame, text="Очистить всё", command=self.clear_all, width=20).pack()

        self.apply_theme()  # начальная тема

    def update_preview(self, event=None):
        self.current_text = self.text_input.get("1.0", tk.END).strip()

        preview = self.current_text

        # Применяем форматирование заголовков только если чекбокс включён
        if self.bold_titles_var.get():
            lines = preview.split("\n")
            formatted_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("# "):
                    # Берём текст после # и делаем жирным
                    formatted_lines.append(f"**{stripped[2:].strip()}**")
                else:
                    formatted_lines.append(line)
            preview = "\n".join(formatted_lines)

        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", preview or "Начните вводить текст...")
        self.preview_text.config(state="disabled")

    def apply_theme(self, event=None):
        theme = self.themes[self.theme_var.get()]
        self.preview_text.config(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["insert"],
            state="normal"
        )
        self.preview_text.config(state="disabled")
        self.update_preview()  # обновляем текст при смене темы

    def clear_all(self):
        self.text_input.delete("1.0", tk.END)
        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", "Текст очищен")
        self.preview_text.config(state="disabled")
        self.update_preview()


def main():
    NoteEditor()


if __name__ == "__main__":
    main()
