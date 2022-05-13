from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
# по поводу замечания на счет имени переменной duration:
# pytest требует именно такое имя, иначе тест не проходит

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {"{:.3f}".format(self.duration)} ч.;'
            f' Дистанция: {"{:.3f}".format(self.distance)} км;'
            f' Ср. скорость: {"{:.3f}".format(self.speed)} км/ч;'
            f' Потрачено ккал: {"{:.3f}".format(self.calories)}.'
        )


class Training:
    """Базовый класс тренировки."""
# здесь столкнулся с проблемой при использовании @dataclass:
# при использовании неправильно расчитывалось расстояние в классе Swimming
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
        raise NotImplementedError('не переопределен метод get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration, self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20
    minutes_in_hour: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.coeff_calorie_1 * self.get_mean_speed()
             - self.coeff_calorie_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.minutes_in_hour
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029
    minutes_in_hour: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action,
                         duration,
                         weight)
        self.height = height
# правильно ли я понял, что декоратор @dataclass не применить
# ко всем классам? не получалось вынести константу LEN_STEP
# в тело родительского класса,
# т.к. впоследствии у дочерних классов возникала ошибка, что
# аргумент не по умолчанию следует за аргументом по умолчанию
# таким образом, я не мог задать свойство height в классе SportsWalking)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return (
            (self.coeff_calorie_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.coeff_calorie_2 * self.weight)
            * self.duration * self.minutes_in_hour
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):
        super().__init__(action,
                         duration,
                         weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.coeff_calorie_1)
            * self.coeff_calorie_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {
        Swimming: 'SWM',
        Running: 'RUN',
        SportsWalking: 'WLK'
    }

    if workout_type == dictionary[Swimming]:
        return Swimming(*data)
    elif workout_type == dictionary[Running]:
        return Running(*data)
    elif workout_type == dictionary[SportsWalking]:
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
