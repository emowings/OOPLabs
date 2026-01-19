import abc
from datetime import timedelta


class TimeConverter(abc.ABC):
    """Абстрактный класс для преобразования времени"""
    @abc.abstractmethod
    def get_operation_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_symbol(self) -> str:
        pass

    @abc.abstractmethod
    def convert(self, total_seconds: int) -> int:
        """Преобразование общего количества секунд в нужную единицу"""
        pass


class ToSeconds(TimeConverter):
    def get_operation_name(self) -> str:
        return "Перевод в секунды"

    def get_symbol(self) -> str:
        return "сек"

    def convert(self, total_seconds: int) -> int:
        return total_seconds


class ToMinutes(TimeConverter):
    def get_operation_name(self) -> str:
        return "Перевод в минуты"

    def get_symbol(self) -> str:
        return "мин"

    def convert(self, total_seconds: int) -> int:
        return total_seconds // 60


class ToHours(TimeConverter):
    def get_operation_name(self) -> str:
        return "Перевод в часы"

    def get_symbol(self) -> str:
        return "ч"

    def convert(self, total_seconds: int) -> int:
        return total_seconds // 3600


class ToDays(TimeConverter):
    def get_operation_name(self) -> str:
        return "Перевод в дни"

    def get_symbol(self) -> str:
        return "дн"

    def convert(self, total_seconds: int) -> int:
        return total_seconds // 86400


class ToWeeks(TimeConverter):
    def get_operation_name(self) -> str:
        return "Перевод в недели"

    def get_symbol(self) -> str:
        return "нед"

    def convert(self, total_seconds: int) -> int:
        return total_seconds // 604800


class ToHumanReadable(TimeConverter):
    """Читаемый формат: дни, часы, минуты, секунды"""
    def get_operation_name(self) -> str:
        return "Человеко-читаемый формат"

    def get_symbol(self) -> str:
        return "≈"

    def convert(self, total_seconds: int) -> str:
        td = timedelta(seconds=total_seconds)
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        parts = []
        if days:
            parts.append(f"{days} дн")
        if hours:
            parts.append(f"{hours} ч")
        if minutes:
            parts.append(f"{minutes} мин")
        if seconds or not parts:
            parts.append(f"{seconds} сек")
        return " ".join(parts)


def read_duration() -> int:
    """Ввод количества времени в секундах с проверкой"""
    while True:
        try:
            raw = input("Введите количество секунд: ").strip()
            if not raw.isdigit():
                print("Нужно ввести только положительное целое число")
                continue
            seconds = int(raw)
            if seconds < 0:
                print("Время не может быть отрицательным")
                continue
            if seconds == 0:
                print("Нулевое время — это 0 во всех единицах")
            return seconds
        except ValueError:
            print("Введите корректное целое число")


def main():
    converters = [
        ToSeconds(),
        ToMinutes(),
        ToHours(),
        ToDays(),
        ToWeeks(),
        ToHumanReadable()
    ]

    print("Калькулятор анализа времени")
    print("Преобразует введённое количество секунд в разные единицы\n")

    total_seconds = read_duration()

    print(f"\nИсходное время: {total_seconds:,} секунд")
    print("─" * 45)

    for conv in converters:
        try:
            result = conv.convert(total_seconds)
            print(f"{conv.get_operation_name():<25} → {result} {conv.get_symbol()}")
        except Exception as e:
            print(f"{conv.get_operation_name():<25} → Ошибка: {e}")

    print("─" * 45)
    print("Повторить расчёт? (Enter = да, любой символ + Enter = выход)")
    if input().strip():
        print("До свидания!")
    else:
        main()


if __name__ == "__main__":
    main()
