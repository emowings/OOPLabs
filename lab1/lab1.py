from typing import List
from dataclasses import dataclass


@dataclass
class Recipe:
    """Один рецепт в личной кулинарной книге"""
    dish_name: str          # название блюда
    source: str             # автор/сайт/книга
    prep_time: int          # время приготовления в минутах
    difficulty: str = "Средний"  # лёгкий / средний / сложный

    def to_txt_line(self) -> str:
        """Рецепт → строка для текстового файла"""
        safe_dish   = self.dish_name.replace('|', '\\|')
        safe_source = self.source.replace('|', '\\|')
        safe_diff   = self.difficulty.replace('|', '\\|')
        return f"{safe_dish}|{safe_source}|{self.prep_time}|{safe_diff}\n"

    @classmethod
    def from_txt_line(cls, line: str) -> 'Recipe':
        """Строка из файла → объект Recipe"""
        parts = line.strip().split('|')
        if len(parts) < 3:
            raise ValueError(f"Неверный формат строки: {line.strip()}")

        dish_name = parts[0].replace('\\|', '|')
        source    = parts[1].replace('\\|', '|')
        try:
            prep_time = int(parts[2])
        except ValueError:
            raise ValueError(f"Время приготовления не число: {parts[2]}")

        difficulty = parts[3].replace('\\|', '|') if len(parts) > 3 else "Средний"

        return cls(dish_name, source, prep_time, difficulty)

    def __str__(self) -> str:
        return f"«{self.dish_name}» — {self.source} ({self.prep_time} мин), сложность: {self.difficulty}"


class RecipeCollection:
    """Управление личной коллекцией рецептов"""
    def __init__(self):
        self.recipes: List[Recipe] = []

    def add_recipe(self, dish_name: str, source: str, prep_time: int, difficulty: str = "Средний"):
        recipe = Recipe(dish_name.strip(), source.strip(), prep_time, difficulty.strip())
        self.recipes.append(recipe)
        print(f"Рецепт добавлен: {recipe}")

    def add_recipe_from_input(self):
        print("\nДобавление нового рецепта")
        print("-" * 40)
        dish_name = input("Название блюда: ").strip()
        if not dish_name:
            print("Название обязательно")
            return

        source = input("Источник (автор/сайт/книга): ").strip()
        time_input = input("Время приготовления (мин): ").strip()

        try:
            prep_time = int(time_input)
            if prep_time < 5 or prep_time > 300:
                print("Время выглядит странно. Попробуйте ещё раз.")
                return
        except ValueError:
            print("Время — это число минут")
            return

        difficulty = input("Сложность (лёгкий/средний/сложный, Enter = средний): ").strip()
        difficulty = difficulty or "Средний"
        if difficulty not in ["лёгкий", "средний", "сложный"]:
            print("Сложность должна быть: лёгкий, средний или сложный")
            return

        self.add_recipe(dish_name, source, prep_time, difficulty)
        print("Рецепт сохранён!\n")

    def sort_recipes(self, by: str):
        if by == "dish":
            self.recipes.sort(key=lambda r: r.dish_name.lower())
            print("Отсортировано по названию блюда")
        elif by == "source":
            self.recipes.sort(key=lambda r: r.source.lower())
            print("Отсортировано по источнику")
        elif by == "time":
            self.recipes.sort(key=lambda r: r.prep_time)
            print("Отсортировано по времени приготовления")
        elif by == "difficulty":
            diff_order = {"лёгкий": 0, "средний": 1, "сложный": 2}
            self.recipes.sort(key=lambda r: diff_order.get(r.difficulty.lower(), 1))
            print("Отсортировано по сложности")
        else:
            print("Неизвестный критерий сортировки")

    def print_recipes(self):
        if not self.recipes:
            print("\nКоллекция рецептов пуста.")
            return

        print("\n" + "═" * 80)
        print(f"{'№':<3}  {'Блюдо':<30}  {'Источник':<25}  {'Время (мин)':<12}  {'Сложность':<15}")
        print("─" * 80)
        for i, r in enumerate(self.recipes, 1):
            print(f"{i:<3}  {r.dish_name:<30}  {r.source:<25}  {r.prep_time:<12}  {r.difficulty:<15}")
        print("═" * 80)

    def save_to_text(self, filename: str):
        """Выгрузка коллекции в текстовый файл"""
        if not filename.endswith('.txt'):
            filename += '.txt'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("БЛЮДО|ИСТОЧНИК|ВРЕМЯ|СЛОЖНОСТЬ\n")
                f.write("-" * 70 + "\n")
                for recipe in self.recipes:
                    f.write(recipe.to_txt_line())
            print(f"Коллекция рецептов сохранена в файл: {filename}")
        except Exception as e:
            print(f"Ошибка записи: {e}")

    def load_from_text(self, filename: str):
        """Загрузка коллекции из текстового файла"""
        if not filename.endswith('.txt'):
            filename += '.txt'
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            if not lines:
                print("Файл пустой")
                return

            data_lines = lines[2:] if len(lines) > 2 else lines
            loaded = []
            for line in data_lines:
                if not line.strip():
                    continue
                try:
                    recipe = Recipe.from_txt_line(line)
                    loaded.append(recipe)
                except ValueError as e:
                    print(f"Пропущена строка: {line.strip()} → {e}")
            self.recipes.extend(loaded)
            print(f"Загружено {len(loaded)} рецептов. Всего теперь: {len(self.recipes)}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
        except Exception as e:
            print(f"Ошибка чтения: {e}")


def main_loop():
    collection = RecipeCollection()

    while True:
        print("\n" + "═" * 50)
        print("   МОЯ КУЛИНАРНАЯ КНИГА")
        print("═" * 50)
        print(" 1 — Показать все рецепты")
        print(" 2 — Добавить рецепт")
        print(" 3 — Сортировать по названию блюда")
        print(" 4 — Сортировать по источнику")
        print(" 5 — Сортировать по времени приготовления")
        print(" 6 — Сортировать по сложности")
        print(" 7 — Сохранить в текстовый файл")
        print(" 8 — Загрузить из текстового файла")
        print(" 9 — Выход")
        print("─" * 50)

        choice = input("Выбор: ").strip()

        if choice == '1':
            collection.print_recipes()
        elif choice == '2':
            collection.add_recipe_from_input()
        elif choice == '3':
            collection.sort_recipes("dish")
            collection.print_recipes()
        elif choice == '4':
            collection.sort_recipes("source")
            collection.print_recipes()
        elif choice == '5':
            collection.sort_recipes("time")
            collection.print_recipes()
        elif choice == '6':
            collection.sort_recipes("difficulty")
            collection.print_recipes()
        elif choice == '7':
            fname = input("Имя файла (без .txt): ").strip() or "my_recipes"
            collection.save_to_text(fname)
        elif choice == '8':
            fname = input("Имя файла (без .txt): ").strip() or "my_recipes"
            collection.load_from_text(fname)
            collection.print_recipes()
        elif choice == '9':
            print("\nПриятного аппетита!")
            break
        else:
            print("Нет такого пункта.")

        input("\nEnter → продолжить...")


if __name__ == "__main__":
    main_loop()
