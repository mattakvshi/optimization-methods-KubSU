import math as mt
import matplotlib.pyplot as plt
import numpy as np

class FibonacciMethod:
    def __init__(self, func, interval, epsilon=0.5, n=10):
        """
        Класс для метода Фибоначчи поиска минимума функции на заданном интервале.

        Args:
            func (str): Строковое представление функции.
            interval (list): Интервал для поиска минимума [a, b].
            epsilon (float): Точность поиска минимума.
            n (int): Количество чисел Фибоначчи для метода.

        Attributes:
            func (str): Строковое представление функции.
            interval (list): Интервал для поиска минимума [a, b].
            epsilon (float): Точность поиска минимума.
            n (int): Количество чисел Фибоначчи для метода.
            fib_list (list): Список чисел Фибоначчи.
        """
        self.func = func
        self.interval = interval
        self.epsilon = epsilon
        self.n = n
        self.fib_list = self._calculate_fibonacci_numbers()

    def _calculate_fibonacci_numbers(self):
        """
        Вычисляет числа Фибоначчи до заданного количества n.
        """
        fib_list = [1, 1]
        for i in range(2, self.n):
            fib_list.append(fib_list[i - 1] + fib_list[i - 2])
        return fib_list

    def _function(self, x):
        """
        Вычисляет значение функции для заданного x.
        """
        return eval(self.func)

    def calculate_lambda_mu(self, l, i):
        """
        Рассчитывает значения lambda_i и mu_i для заданного интервала и итерации.
        """
        n = len(self.fib_list)
        lambda_i = l[0] + ((self.fib_list[(n - 1) - i - 1] / self.fib_list[(n - 1) - i + 1]) * (l[1] - l[0]))
        mu_i = l[0] + ((self.fib_list[(n - 1) - i] / self.fib_list[(n - 1) - i + 1]) * (l[1] - l[0]))
        return lambda_i, mu_i


    def calculate_new_interval(self, lambda_i, mu_i, l):
        """
        Переопределяет интервал неопределённости на основе lambda_i и mu_i.
        """
        f_lambda_i = self._function(lambda_i)
        f_mu_i = self._function(mu_i)
        return [lambda_i, l[1]] if f_lambda_i > f_mu_i else [l[0], mu_i]

    def calculate_accuracy(self, l):
        """
        Рассчитывает точность текущего интервала неопределённости.
        """
        return abs(l[1] - l[0]) < self.epsilon

    def find_minimum(self):
        """
        Находит минимум функции на заданном интервале с использованием метода Фибоначчи.
        """
        l = self.interval
        i = 1
        while not self.calculate_accuracy(l):
            lambda_i, mu_i = self.calculate_lambda_mu(l, i)
            l = self.calculate_new_interval(lambda_i, mu_i, l)
            i += 1

        min_point = (l[1] + l[0]) / 2  # Находим середину последнего интервала
        min_value = self._function(min_point)
        self.interval = l 
        return min_point, min_value, i - 1  # Возвращаем также количество итераций

    def plot_function(self):
        """
        Строит график функции и отмечает найденный минимум.
        """
        x_range = np.linspace(self.interval[0], self.interval[1], 1000)
        plt.plot(x_range, [self._function(x) for x in x_range], label="f(x)", color="orange")
        min_x, min_y, iterations = self.find_minimum()
        plt.scatter(min_x, min_y, color="red", s=20, label="Minimum")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.show()



def main():
    func = "3*x**2 - x + 4"
    interval = [-4, 6]
    fibonacci = FibonacciMethod(func, interval)

    print("Отчет по работе метода:")
    print("-----------------------------------------")
    print("Исходные данные: ")
    print("Функция: " + func)
    print("Интервал: " + str(interval))
    print("Точность: " + str(fibonacci.epsilon))
    print("Количество чисел Фибоначчи: " + str(fibonacci.n))
    print("Начальное k: 0")
    print("-----------------------------------------")

    min_x, min_y, iterations = fibonacci.find_minimum()

    print("\nВыходные данные:")
    print("Интервал: " + str(fibonacci.interval))
    print("Точка минимума: " + str(min_x))
    print("Значение функции в точке минимума: " + str(min_y))
    print("Конечное k: " + str(iterations))
    print("Точность (epsilon): " + str(abs(fibonacci.interval[1] - fibonacci.interval[0])))
    print("-----------------------------------------")

    fibonacci.plot_function()


if __name__ == "__main__":
    main()