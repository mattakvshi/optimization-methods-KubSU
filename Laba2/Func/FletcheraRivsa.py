import math as mt
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_x_range() -> list[list[float]]:
    """
    Функция, которая создаёт диапазон для функции
    Args: отсутствует
    Return: список списков с точками
    """
    x_range = []
    step = 10 / 500
    for i in range(1000):
        x_range.append([-5 + (step * i), -5 + (step * i)])
    return x_range

def f(x_list: list[list[float]]) -> list[float]:
    """
    Функция двух переменных
    Args: x - список значений x
    Return: список значений функции
    """
    result = []
    for x in x_list:
        result.append([x[0]**2 + 8*(x[1]**2) + x[0]*x[1] + x[0]])
    return result

def grad_f(x: list[float]) -> list[float]:
    """
    Функция, которая считает градиент функции f
    Args: x - аргумент функции
    Return: список значений
    """
    return [2*x[0] + x[1] + 1, 16*x[1] + x[0]]

def norm_grad(grad: list[float]) -> float:
    """
    Функция, которая считает норму градиента
    Args: grad - градиент функции
    Return: значение нормы градиента функции
    """
    return mt.sqrt(grad[0]**2 + grad[1]**2)


def calculate_d(x: list[float], betta: float, d_0: list[float], flag: int) -> list[float]:
    """
    Функция, которая считает параметр d
    Args: x - список значений x; betta - аргумент бетта; d_0 - предыдущее значение d; flag - способ подсчёта нового d
    Return: новое значение d в виде списка
    """
    if flag == 1:
        return [-x for x in grad_f(x)]
    elif flag == 2:
        return np.array([-x for x in grad_f(x)]) + np.array(betta * np.array(d_0))
    else:
        print("Неверное значение флага! Флаг может быть 1 или 2!")


def calculate_betta(new_norm_grad: list[float], old_norm_grad: list[float]) -> float:
    """
    Функция, которая считает аргумент бетта
    Args: grad_new и grad_old - новая и старая норма градиента (от нового и старого х)
    Return: аргумент бетта
    """
    return (new_norm_grad**2) / (old_norm_grad**2)

def calculate_t(x_old: list[float], d: list[float]) -> float:
    """
    Функция, которая вычисляет значение t на какой-то итерации
    Args: x_old - список значений; d - коэффициент d
    Return: значение t
    """
    t = sp.symbols("t")  #объявляем символьную переменную
    expression_x_new = [x_old[0] + t * d[0], x_old[1] + t * d[1]]
    after_f = (expression_x_new[0]**2) + (8 * (expression_x_new[1]**2)) + (expression_x_new[0] * expression_x_new[1]) + expression_x_new[0]
    after_f_derivative = sp.diff(after_f, t)  #берём производную по t
    solution_t = sp.solve(after_f_derivative, t)  #решение уравнения производной = 0 для t
    return solution_t

def calculate_x_new(x_old: list[float], t: float, d: list[float]) -> list[float]:
    """
    Функция, которая вычисляет новое значение вектора x
    Args: x_old - предыдущее значение вектора x; t - коэффициент t; d - коэффициент d
    Return: новый вектор x
    """
    return np.array(x_old) + t * np.array(d)

def norm_between_x(x_old: list[float], x_new: list[float]) -> float:
    """
    Функция, которая вычисляет норму между новым и старым х
    Args: x_old и x_new - старый и новый х
    Return: значение нормы
    """
    return mt.sqrt((x_new[0] - x_old[0])**2 + (x_new[1] - x_old[1])**2)

def mod_between_f(x_old: list[float], x_new: list[float]) -> float:
    """
    Функция, которая вычисляет модуль между разницей новой и старой f
    Args: x_old и x_new - старый и новый х
    Return: значение модуля
    """
    return abs(f(x_new)[0][0] - f(x_old)[0][0])


# Создать списки для сохранения значений x и f(x)
x_history = []
f_history = []

x_0 = [1.5, 0.5]
epsilon_1 = 0.1
epsilon_2 = 0.15
m = 10
k = 0
old_norm_grad = 0
d_old = 0
flag = 0


while k < m:
    
    # Добавить текущее значение x и f(x) в историю
    x_history.append(x_0)
    f_history.append(f([x_0])[0][0])

    #шаг 3
    grad_x_0 = grad_f(x_0)
    #print(f"grad_x_0 = {grad_x_0}")
    #шаг 4
    norm_grad_x_0 = norm_grad(grad_x_0)
    
    if norm_grad_x_0 < epsilon_1:
        x_min = x_0
        f_min = f([x_min])
        break
    else:
        #шаг 5
        if k >= m:
            x_min = x_0
            f_min = f([x_min])
            break
        elif k == 0:
            #шаг 6
            d = calculate_d(x_0, None, None, 1)
        elif k > 0:
            #шаг 7
            betta = calculate_betta(norm_grad_x_0, old_norm_grad)
            #print(f"betta = {betta}")
            #шаг 8
            d = calculate_d(x_0, betta, d_old, 2)
        #print(f"d = {d}")
        #шаг 9
        t = calculate_t(x_0, d)
        #print(f"t = {t}")
        #шаг 10
        x_new = calculate_x_new(x_0, t, d)
        #print(f"x_new = {x_new}")
        #шаг 11
        between_x = norm_between_x(x_0, x_new)
        #print(f"between_x = {between_x}")
        between_f = mod_between_f([x_0], [x_new])
        #print(f"between_f = {between_f}")
        if between_x < epsilon_2 and between_f < epsilon_2:
            if flag == 1:
                flag = 2
                x_min = x_new
                f_min = f([x_min])
                break
            else:
                flag = 1
                x_0 = x_new
                old_norm_grad = norm_grad_x_0
                d_old = d
                k += 1
        else:
            x_0 = x_new
            old_norm_grad = norm_grad_x_0
            d_old = d
            k += 1

print(f"Координаты точки минимума: {x_min};\n f(x): {f_min};\n k: {k}")


# Изменить часть для построения графика
x_range = create_x_range()
x1_values = np.array([x_range[i][0] for i in range(len(x_range))])
x2_values = x1_values.copy()

x, y = np.meshgrid(x1_values, x2_values)
z = np.array(f(x_range))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection="3d")
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.6)
ax.scatter(x_min[0], x_min[1], f_min, color="red")

# Добавить отображение шагов минимизации
x_history = np.array(x_history)
f_history = np.array(f_history)
ax.plot(x_history[:, 0], x_history[:, 1], f_history, marker='o', color='blue')

plt.show()