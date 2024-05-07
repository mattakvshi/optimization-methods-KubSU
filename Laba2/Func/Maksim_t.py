
import numpy as np

def new_t(x: list[float]) -> float:
    return (2*x[0]*(2*x[0]+x[1]+1) + 16*x[1]*(16*x[1]+x[0]) + x[1]*(2*x[0]+x[1]+1) + x[0]*(16*x[1]+x[0]) + 2*x[0]+x[1]+1) / (2*((2*x[0]+x[1]+1)**2) + 16*((16*x[1]+x[0])**2) + 2*(2*x[0]+x[1]+1)*(16*x[1]+x[0]))

def grad(x: list[float]) -> list[float]:
    return [2*x[0]+x[1]+1, 16*x[1] + x[0]]

def norm_grad(grad: list[float]) -> float:
    return np.sqrt(grad[0]**2 + grad[1]**2)

def norm_x(new_x: list[float], old_x: list[float]) -> float:
    return np.sqrt((new_x[0]-old_x[0])**2 + (new_x[1]-old_x[1])**2)

def f(x: list[float]) -> float:
    return x[0]**2 + 8*(x[1]**2) + x[0]+x[1] + x[0]

def calc_new_x(old_x, t, grad):
    return [old_x[0] - t * grad[0], old_x[1] - t * grad[1]]

old_x = [-0.289, 0.007]
new_x = calc_new_x(old_x, new_t(old_x), grad(old_x))

print(f"grad = {grad(old_x)}")
print(f"norm_grad = {norm_grad(grad(old_x))}")
print(f"new_t = {new_t(old_x)}")
print(f"new_x = {calc_new_x(old_x, new_t(old_x), grad(old_x))}")
print(f"norm_x = {norm_x(new_x, old_x)}")
print(f"mod_f = {abs(f(new_x) - f(old_x))}")
print(f"f_min = {f(new_x)}")