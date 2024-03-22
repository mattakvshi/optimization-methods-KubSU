import math
import matplotlib.pyplot as plt
import numpy as np

class GoldenSectionMethod:
    def __init__(self, func, interval, epsilon):
        """
        Инициализация метода золотого сечения.

        Args:
            func: Функция, для которой ищется минимум.
            interval: Интервал, в котором происходит поиск минимума.
            epsilon: Точность поиска.
        """
        self.func = func
        self.interval = interval
        self.epsilon = epsilon
        self.num_1 = (3 - math.sqrt(5)) / 2
        self.num_2 = 1 - self.num_1
        self.k = 0
        self.count_n_for = 0
        self.n = 0

    def function(self, x):
        """Вычисление значения функции в точке x."""
        return 3 * x ** 2 - x + 4

    def y_z(self):
        """Нахождение новых значений y и z."""
        y = self.interval[0] + self.num_1 * (self.interval[1] - self.interval[0])
        z = self.interval[0] + self.interval[1] - y
        return y, z

    def fy_fz(self, y, z):
        """Вычисление значений функции в точках y и z и обновление интервала."""
        fy = self.function(y)
        fz = self.function(z)
        if fy <= fz:
            self.interval[1] = z
            y_new = self.interval[0] + self.interval[1] - y
            z_new = y
        else:
            self.interval[0] = y
            y_new = z
            z_new = self.interval[0] + self.interval[1] - z
        if self.count_n_for == 0:
            self.n = 2 * (self.k + 1)
            self.count_n_for += 1
        else:
            self.n += 1
            self.count_n_for += 1
        return y_new, z_new

    def accuracy(self):
        """Проверка достижения требуемой точности."""
        return math.fabs(self.interval[1] - self.interval[0]) < self.epsilon

    def optimize(self):
        """Основной метод оптимизации."""
        y, z = self.y_z()
        while not self.accuracy():
            y, z = self.fy_fz(y, z)
            self.k += 1
            if(self.k == self.n-3):
                break

    def print_results(self):
        """Вывод результатов поиска минимума в консоль."""

        print("\nОтчёт по работе метода:")
        print("\n-------------------------------------")
        print("\nНа вход принимает:")
        print("Исходная функция: 3x^2 - x + 4")
        print("Интервал неопределенности:", self.interval)
        print("Точность epsilon:", self.epsilon)
        print("Сама функция: 3x^2 - x + 4")
        print("Начальное k:", self.k)
        print("\n-------------------------------------")

        self.optimize()

        print("\nПолучаем:")
        print("Точка min:", (self.interval[1] - self.interval[0]) / 2)
        print("Значение функции в точке min:", self.function((self.interval[1] - self.interval[0]) / 2))
        print("Интервал, в котором находится точка min(конечный интервал):", self.interval)
        print("Индекс конечного интервала n:", self.n)
        print("Сходимость:", math.pow(self.num_2, self.n - 1))
        print("Конечное k:", self.k)
        print("Точность (по отношению к epsilon):", math.fabs(self.interval[1] - self.interval[0]))
        print("\n-------------------------------------")

    def plot_graph(self):
        """Построение графика функции с отмеченным минимумом."""
        x_range = np.linspace(-10, 10, 1000)
        plt.plot(x_range, [self.function(x) for x in x_range], label='f(x)', color="orange")
        plt.scatter((self.interval[1] + self.interval[0]) / 2, self.function((self.interval[1] + self.interval[0]) / 2),
                    color='red', s=20, label='Минимум')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()


if __name__ == "__main__":
    method = GoldenSectionMethod(func=lambda x: 3 * x ** 2 - x + 4, interval=[-4, 6], epsilon=0.5)
    method.print_results()
    method.plot_graph()