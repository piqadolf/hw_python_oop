from dataclasses import asdict, dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    MESSAGE: ClassVar[str] = ("Тип тренировки: {training_type}; "
                              "Длительность: {duration:.3f} ч.; "
                              "Дистанция: {distance:.3f} км; "
                              "Ср. скорость: {speed:.3f} км/ч; "
                              "Потрачено ккал: {calories:.3f}.")

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (self.MESSAGE.format(**asdict(self)))
        return message


''' Вы указали, что этот класс не является датаклассом.
    Но мне кажется, что несмотря на то, что сутью этого класса
    не является только хранение данных, его всё еще можно объявить
    датаклассом для упрощения написания кода'''


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    action: int
    duration: int
    weight: int

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WLK_FIRST_CALORIES_MULTUPLIER: ClassVar[float] = 0.035
    WLK_SECOND_CALORIES_MULTUPLIER: ClassVar[float] = 0.029
    M_IN_SEC_SPEED_MULTIPLIER: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100

    '''Тут вы указали, что эти данные не нужно здесь определять,
        Но тогда я не понимаю, как мне их определять. Ведь height
        не определяется в родительском классе, а значит тут один
        выход - переопределить метод __init__. Я сделал это с помощью
        датакласса для упрощения написания кода. Как мне поступить
        в этой ситуации правильнее?'''
    action: int
    duration: int
    weight: int
    height: int

    def __post_init__(self):
        self.height = self.height / self.CM_IN_M

    def get_spent_calories(self) -> float:
        return ((self.WLK_FIRST_CALORIES_MULTUPLIER * self.weight
                + ((self.get_mean_speed()
                   * self.M_IN_SEC_SPEED_MULTIPLIER)**2
                   / self.height) * self.WLK_SECOND_CALORIES_MULTUPLIER
                * self.weight) * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: ClassVar[float] = 1.38
    SWM_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    SPEED_MULTIPLIER: ClassVar[int] = 2

    action: int
    duration: int
    weight: int
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        return (self.count_pool * self.length_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_MEAN_SPEED_SHIFT)
                * self.SPEED_MULTIPLIER * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    training = training_type[workout_type](*data)
    return training


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
