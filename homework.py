from typing import ClassVar, Dict
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
# в других классах pytest тоже не даёт поменять duration

    def get_message(self) -> str:
        """получить информационное сообщение о тренировке."""
        return (
            f'Тип тренировки: {self.training_type};'
            f' Длительность: {"{:.3f}".format(self.duration)} ч.;'
            f' Дистанция: {"{:.3f}".format(self.distance)} км;'
            f' Ср. скорость: {"{:.3f}".format(self.speed)} км/ч;'
            f' Потрачено ккал: {"{:.3f}".format(self.calories)}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM: ClassVar = 1000
    LEN_STEP: ClassVar = 0.65
# с использованием ClassVar действительно производит верные расчеты :)

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'не переопределен метод get_spent_calories в классе '
            f'{self.__class__.__name__}'
        )

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
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20
    MINUTES_IN_HOUR: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_1 * self.get_mean_speed()
             - self.COEFF_CALORIE_2)
            * self.weight / self.M_IN_KM
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float
    COEFF_CALORIE_1: ClassVar = 0.035
    COEFF_CALORIE_2: ClassVar = 0.029
    MINUTES_IN_HOUR: ClassVar = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.COEFF_CALORIE_1 * self.weight
             + (self.get_mean_speed()**2 // self.height)
             * self.COEFF_CALORIE_2 * self.weight)
            * self.duration * self.MINUTES_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int
    LEN_STEP: ClassVar = 1.38
    COEFF_CALORIE_1: ClassVar = 1.1
    COEFF_CALORIE_2: ClassVar = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2 * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train_styles: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in train_styles.keys():
        return train_styles.get(workout_type)(*data)
    else:
        raise KeyError('нужного ключа нет в словаре train_styles')


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
