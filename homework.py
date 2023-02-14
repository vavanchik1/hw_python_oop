from typing import List
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = ((self.action * self.LEN_STEP) / self.M_IN_KM)
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_mess = InfoMessage(self.__class__.__name__,
                                self.duration,
                                self.get_distance(),
                                self.get_mean_speed(),
                                self.get_spent_calories())
        return info_mess


class Running(Training):
    """Тренировка: бег."""
    CAL_MULT: int = 18
    CAL_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CAL_MULT * self.get_mean_speed()
                + self.CAL_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_MULT: float = 0.035
    CAL_MULT1: float = 0.029
    KM_H_IN_M_S: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.heigt = height

    def get_spent_calories(self) -> float:
        return ((self.CAL_MULT * self.weight
                + ((self.get_mean_speed() * self.KM_H_IN_M_S) ** 2
                 / (self.heigt / self.CM_IN_M))
                * self.CAL_MULT1 * self.weight)
                * (self.duration * self.MIN_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    CAL_SHIFT: float = 1.1
    CAL_MULT: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CAL_SHIFT)
                * self.CAL_MULT * self.weight * self.duration)

    def get_distance(self) -> float:
        return ((self.action * self.LEN_STEP) / self.M_IN_KM)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    data_workout: dict[str, Training] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming}
    if workout_type not in data_workout:
        raise ValueError('Неподдерживаемый тип тренировки: {workout_type}')
    return data_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
