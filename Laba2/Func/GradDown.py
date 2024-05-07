import numpy as np
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
    return np.sqrt(grad[0]**2 + grad[1]**2)

def calculate_t(x: list[float]) -> float:
    """
    Функция, которая вычисляет значение t на какой-то итерации
    Args: x - аргумент
    Return: значение t
    """
    return (2*x[0]*(2*x[0]+x[1]+1) + 16*x[1]*(16*x[1]+x[0]) + x[1]*(2*x[0]+x[1]+1) + x[0]*(16*x[1]+x[0]) + 2*x[0]+x[1]+1) / (2*((2*x[0]+x[1]+1)**2) + 16*((16*x[1]+x[0])**2) + 2*(2*x[0]+x[1]+1)*(16*x[1]+x[0]))

def calculate_new_x(x_old: list[float], t: float) -> list[float]:
    """
    Функция, которая вычисляет новое значение х
    Args: x - значение старого x; t - значение t
    Return: новое значение x
    """
    return [x_old[0] - t * grad_f(x_old)[0], x_old[1] - t * grad_f(x_old)[1]]

def norm_between_x(x_old: list[float], x_new: list[float]) -> float:
    """
    Функция, которая вычисляет норму между новым и старым х
    Args: x_old и x_new - старый и новый х
    Return: значение нормы
    """
    return np.sqrt((x_new[0] - x_old[0])**2 + (x_new[1] - x_old[1])**2)

def mod_between_f(x_old: list[float], x_new: list[float]) -> float:
    """
    Функция, которая вычисляет модуль между разницей новой и старой f
    Args: x_old и x_new - старый и новый х
    Return: значение модуля
    """
    return abs(f([x_new])[0][0] - f([x_old])[0][0])


# Создать списки для сохранения значений x и f(x)
x_history = []
f_history = []

x_0 = [1.5, 0.5]
epsilon_1 = 0.1
epsilon_2 = 0.15
m = 10
k = 0
flag = 0

while k < m:

    # Добавить текущее значение x и f(x) в историю
    x_history.append(x_0)
    f_history.append(f([x_0])[0][0])

    #шаг 3
    grad_f_x_0 = grad_f(x_0)
    #шаг 4
    norm_grad_f_x_0 = norm_grad(grad_f_x_0)
    if norm_grad_f_x_0 < epsilon_1:
        x_min = x_0
        f_min = f([x_min])
        break
    else:
        #шаг 5
        if k >= m:
            x_min = x_0
            f_min = f([x_min])
            break
        else:
            #шаг 6
            t = calculate_t(x_0)
            #шаг 7
            x_new = calculate_new_x(x_0, t)
            #шаг 8
            between_x = norm_between_x(x_0, x_new)
            between_f = mod_between_f(x_0, x_new)
            if between_x < epsilon_2 and between_f < epsilon_2:
                if flag == 1:
                    flag = 2
                    x_min = x_0
                    f_min = f([x_min])
                    break
                else:
                    flag = 1
                    x_0 = x_new
                    k += 1
            else:
                x_0 = x_new
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