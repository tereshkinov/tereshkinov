import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


def f1(t, x, y):
    return 3 * x - y


def f2(t, x, y):
    return 4 * x - y


def euler_method_system(f1, f2, x0, y0, t0, t_end, dt):
    n_steps = int((t_end - t0) / dt)
    t_values = np.linspace(t0, t_end, n_steps + 1)
    x_values = np.zeros(n_steps + 1)
    y_values = np.zeros(n_steps + 1)
    x_values[0] = x0
    y_values[0] = y0
    for i in range(n_steps):
        t = t_values[i]
        x = x_values[i]
        y = y_values[i]
        x_values[i + 1] = x + dt * f1(t, x, y)
        y_values[i + 1] = y + dt * f2(t, x, y)
    return t_values, x_values, y_values


def trapezoidal_method_system(f1, f2, x0, y0, t0, t_end, dt):
    n_steps = int((t_end - t0) / dt)
    t_values = np.linspace(t0, t_end, n_steps + 1)
    x_values = np.zeros(n_steps + 1)
    y_values = np.zeros(n_steps + 1)
    x_values[0] = x0
    y_values[0] = y0

    for i in range(n_steps):
        t = t_values[i]
        x_n = x_values[i]
        y_n = y_values[i]
        def equations(vars):
            x_n1, y_n1 = vars
            eq1 = x_n1 - x_n - dt / 2 * (f1(t, x_n, y_n) + f1(t + dt, x_n1, y_n1))
            eq2 = y_n1 - y_n - dt / 2 * (f2(t, x_n, y_n) + f2(t + dt, x_n1, y_n1))
            return [eq1, eq2]

        x_pred = x_n + dt * f1(t, x_n, y_n)
        y_pred = y_n + dt * f2(t, x_n, y_n)
        solution = fsolve(equations, [x_pred, y_pred])
        x_values[i + 1], y_values[i + 1] = solution

    return t_values, x_values, y_values


def analytical(t0, t_end, dt):
    n_steps = int((t_end - t0) / dt)
    t_values = np.linspace(t0, t_end, n_steps + 1)
    x_values = (1 + 2 * t_values) * np.exp(t_values)
    y_values = (4 * t_values) * np.exp(t_values)
    return t_values, x_values, y_values


x0 = 1
y0 = 0
t0 = 0
t_end = 3
dt = 0.1

t_euler, x_euler, y_euler = euler_method_system(f1, f2, x0, y0, t0, t_end, dt)
t_trap, x_trap, y_trap = trapezoidal_method_system(f1, f2, x0, y0, t0, t_end, dt)
t_analyt, x_analyt, y_analyt = analytical(t0, t_end, dt)

plt.figure(num='tereshkinov1', figsize=(15, 10))

plt.subplot(3, 2, 1)
plt.plot(t_euler, x_euler, label='Метод Эйлера', color='red', linestyle='-.')
plt.plot(t_trap, x_trap, label='Метод трапеций', color='green')
plt.plot(t_analyt, x_analyt, label='Аналитическое решение', color='blue', linestyle='--')
plt.title('Сравнение решений для x(t)')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.legend()
plt.grid()

plt.subplot(3, 2, 2)
plt.plot(t_euler, y_euler, label='Метод Эйлера', color='red')
plt.plot(t_trap, y_trap, label='Метод трапеций', color='green')
plt.plot(t_analyt, y_analyt, label='Аналитическое решение', color='blue', linestyle='--')
plt.title('Сравнение решений для y(t)')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.legend()
plt.grid()

plt.subplot(3, 2, 3)
plt.plot(t_euler, x_analyt - x_euler, label='Невязка Эйлера', color='red')
plt.plot(t_trap, x_analyt - x_trap, label='Невязка трапеций', color='green')
plt.title('Невязки для x(t)')
plt.xlabel('t')
plt.ylabel('Ошибка')
plt.legend()
plt.grid()

plt.subplot(3, 2, 4)
plt.plot(t_euler, y_analyt - y_euler, label='Невязка Эйлера', color='red')
plt.plot(t_trap, y_analyt - y_trap, label='Невязка трапеций', color='green')
plt.title('Невязки для y(t)')
plt.xlabel('t')
plt.ylabel('Ошибка')
plt.legend()
plt.grid()

# Фазовые портреты
plt.subplot(3, 2, 5)
plt.plot(x_euler, y_euler, label='Метод Эйлера', color='red')
plt.plot(x_trap, y_trap, label='Метод трапеций', color='green')
plt.plot(x_analyt, y_analyt, label='Аналитическое решение', color='blue', linestyle='--')
plt.title('Фазовый портрет y(x)')
plt.xlabel('x(t)')
plt.ylabel('y(t)')
plt.legend()
plt.grid()


plt.figure(num='tereshkinov2', figsize=(12, 8))

steps = np.array([0.1, 0.05, 0.025, 0.0125, 0.00625])
euler_errors_x = []
trap_errors_x = []
euler_errors_y = []
trap_errors_y = []

for step in steps:
    _, x_e, y_e = euler_method_system(f1, f2, x0, y0, t0, t_end, step)
    _, x_t, y_t = trapezoidal_method_system(f1, f2, x0, y0, t0, t_end, step)
    _, x_a, y_a = analytical(t0, t_end, step)

    euler_errors_x.append(np.max(np.abs(x_a - x_e)))
    trap_errors_x.append(np.max(np.abs(x_a - x_t)))
    euler_errors_y.append(np.max(np.abs(y_a - y_e)))
    trap_errors_y.append(np.max(np.abs(y_a - y_t)))


# Линейная регрессия для определения наклона
def fit_slope(log_h, log_err):
    return np.polyfit(log_h, log_err, 1)[0]


log_steps = np.log10(steps)
slope_euler_x = fit_slope(log_steps, np.log10(euler_errors_x))
slope_trap_x = fit_slope(log_steps, np.log10(trap_errors_x))
slope_euler_y = fit_slope(log_steps, np.log10(euler_errors_y))
slope_trap_y = fit_slope(log_steps, np.log10(trap_errors_y))

# График
plt.loglog(steps, euler_errors_x, 'o-', color='red', label=f'Эйлер (x), наклон={slope_euler_x:.2f}')
plt.loglog(steps, trap_errors_x, 'o-', color='green', label=f'Трапеции (x), наклон={slope_trap_x:.2f}')
plt.loglog(steps, euler_errors_y, 's--', color='red', label=f'Эйлер (y), наклон={slope_euler_y:.2f}')
plt.loglog(steps, trap_errors_y, 's--', color='green', label=f'Трапеции (y), наклон={slope_trap_y:.2f}')

ideal_h = np.array([steps[0], steps[-1]])
plt.loglog(ideal_h, 0.1 * ideal_h ** 1, 'k:', label='Теор. наклон 1 (Эйлер)')
plt.loglog(ideal_h, 0.01 * ideal_h ** 2, 'k-.', label='Теор. наклон 2 (Трапеции)')

plt.title('Порядок точности методов')
plt.xlabel('log(Шаг)')
plt.ylabel('log(Максимальная ошибка)')
plt.legend()
plt.grid(True, which="both", ls="-")

for i, step in enumerate(steps):
    plt.text(step, euler_errors_x[i], f'h={step}', fontsize=8, ha='right')
    plt.text(step, trap_errors_x[i], f'h={step}', fontsize=8, ha='left')


plt.tight_layout()
plt.show()