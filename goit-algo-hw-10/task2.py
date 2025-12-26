import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def f(x):
    return x ** 2

a = 0  # Нижня межа
b = 2  # Верхня межа

# --- Метод Монте-Карло ---

# Кількість випадкових точок
n_points = 10000

# Генеруємо випадкові x у діапазоні [a, b]
x_rand = np.random.uniform(a, b, n_points)

# Генеруємо випадкові y у діапазоні [0, f(b)], оскільки f(x) зростає на [0, 2]
y_max = f(b)
y_rand = np.random.uniform(0, y_max, n_points)

# Перевіряємо, які точки знаходяться під графіком
under_curve = y_rand < f(x_rand)

# Обчислюємо площу прямокутника та частку точок під кривою
rectangle_area = (b - a) * y_max
monte_carlo_result = rectangle_area * (np.sum(under_curve) / n_points)

# --- Перевірка за допомогою quad ---

quad_result, error = integrate.quad(f, a, b)

# --- Вивід результатів ---

print(f"Результат методу Монте-Карло ({n_points} точок): {monte_carlo_result}")
print(f"Результат функції quad (аналітичний): {quad_result}")
print(f"Абсолютна помилка: {abs(monte_carlo_result - quad_result)}")

# Візуалізація для наочності методу
plt.figure(figsize=(8, 6))
plt.scatter(x_rand[under_curve], y_rand[under_curve], color='green', s=1, alpha=0.5, label='Точки під кривою')
plt.scatter(x_rand[~under_curve], y_rand[~under_curve], color='red', s=1, alpha=0.3, label='Точки над кривою')

# Малювання самої функції
x = np.linspace(a - 0.5, b + 0.5, 400)
plt.plot(x, f(x), 'b', linewidth=2, label='f(x) = x^2')
plt.axvline(x=a, color='gray', linestyle='--')
plt.axvline(x=b, color='gray', linestyle='--')
plt.title(f'Метод Монте-Карло для f(x)=x^2\nРезультат: {monte_carlo_result:.4f}')
plt.legend()
plt.grid()
plt.show()
