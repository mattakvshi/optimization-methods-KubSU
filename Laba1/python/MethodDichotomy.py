import math
import matplotlib.pyplot as plt
import numpy as np

class DichotomyMethod:
    """
    Класс, реализующий метод дихотомии для поиска минимума функции.
    """

    def __init__(self, function: callable, interval: list, sigma: float, epsilon: float):
        """
        Конструктор класса.

        :param function: целевая функция, для которой ищется минимум.
        :param interval: начальный интервал неопределенности.
        :param sigma: шаг поиска.
        :param epsilon: точность поиска.
        """
        self.function = function
        self.interval = interval
        self.sigma = sigma
        self.epsilon = epsilon
        self.k = 0
        self.n = 0

    def find_minimum(self):
        """
        Метод, реализующий поиск минимума функции методом дихотомии.

        :return: кортеж из точки минимума и количества итераций.
        """
        while not self.is_accurate():
            y, z = self.calculate_y_and_z()
            self.n = self.calculate_n(y, z)
            self.update_interval(y, z)
            self.k += 1

        return (self.calculate_minimum(), self.n)

    def calculate_y_and_z(self):
        """
        Метод, вычисляющий значения y и z.

        :return: кортеж из значений y и z.
        """
        y = (self.interval[0] + self.interval[1] - self.sigma) / 2
        z = (self.interval[0] + self.interval[1] + self.sigma) / 2
        return y, z

    def calculate_n(self, y: float, z: float):
        """
        Метод, вычисляющий индекс конечного интервала неопределенности.

        :param y: значение y.
        :param z: значение z.
        :return: индекс конечного интервала неопределенности.
        """
        if self.function([y])[0] <= self.function([z])[0]:
            self.interval[1] = z
        else:
            self.interval[0] = y
        return 2 * (self.k + 1)

    def update_interval(self, y: float, z: float):
        """
        Метод, обновляющий интервал неопределенности.

        :param y: значение y.
        :param z: значение z.
        """
        if self.function([y])[0] <= self.function([z])[0]:
            self.interval[1] = z
        else:
            self.interval[0] = y

    def is_accurate(self):
        """
        Метод, проверяющий точность поиска.

        :return: True, если точность достигнута, иначе False.
        """
        return math.fabs(self.interval[1] - self.interval[0]) < self.epsilon

    def calculate_minimum(self):
        """
        Метод, вычисляющий точку минимума.

        :return: точка минимума.
        """
        return (self.interval[1] + self.interval[0]) / 2

    def print_results(self, minimum: float, n: int):
        """
        Метод, выводящий результаты поиска в консоль.

        :param minimum: точка минимума.
        :param n: количество итераций.
        """
        print("Отчёт по работе метода:")
        print("---------------------------------------------")
        print("Исходная функция: 3x^2 - x + 4")
        print("Точка минимума:", minimum)
        print("Конечный интервал неопределенности:", self.interval)
        print("Значение функции в точке минимума:", self.function([minimum])[0])
        print("Индекс конечного интервала неопределённости:", n)
        print("Сходимость:", 1 / (math.pow(2, n)))
        print("Начальное k: 0")
        print("Конечное k:", self.k)
        print("Точность (по отношению к epsilon):", math.fabs(self.interval[1] - self.interval[0]))

    def functionForGraph(self, x_range):
        res = []
        for x in (x_range):
             res.append(3 * x ** 2 - x + 4)
        return res

    def plot_graph(self, minimum: float):
        """
        Метод, строящий график функции и отмечающий на нем точку минимума.

        :param minimum: точка минимума.
        """
        x_range = np.linspace(-10, 10, 1000)
        plt.plot(x_range, self.functionForGraph(x_range), label='f(x)', color='orange')
        plt.scatter(minimum, self.function([minimum])[0], color='red', s=20, label='Минимум')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()

def main():
    """
    Главная функция, создающая экземпляр класса DichotomyMethod и вызывающая методы для поиска минимума, вывода результатов и построения графика.
    """
    function = lambda x: [3 * math.pow(x[0], 2) - x[0] + 4]
    interval = [-4, 6]
    sigma = 0.2
    epsilon = 0.5

    dichotomy_method = DichotomyMethod(function, interval, sigma, epsilon)
    minimum, n = dichotomy_method.find_minimum()
    dichotomy_method.print_results(minimum, n)
    dichotomy_method.plot_graph(minimum)

if __name__ == '__main__':
    main()
