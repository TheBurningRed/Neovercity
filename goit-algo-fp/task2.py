import turtle

def draw_pythagoras_tree(branch_length, level):
    """
    Рекурсивна функція для малювання дерева Піфагора.
    :param branch_length: довжина поточної гілки
    :param level: рівень рекурсії (глибина)
    """
    if level == 0:
        return

    # Малюємо основну гілку
    turtle.forward(branch_length)

    # Зберігаємо позицію та кут перед розгалуженням вліво
    turtle.left(45)
    draw_pythagoras_tree(branch_length * 0.7, level - 1)

    # Повертаємося до вузла та готуємося до розгалуження вправо
    turtle.right(90)
    draw_pythagoras_tree(branch_length * 0.7, level - 1)

    # Повертаємо черепашку у вихідний стан (кут і позиція)
    turtle.left(45)
    turtle.backward(branch_length)

def main():
    # Налаштування екрана
    screen = turtle.Screen()
    screen.title("Дерево Піфагора")

    # Налаштування швидкості та орієнтації
    turtle.speed("fastest")
    turtle.left(90)  # Повертаємо вгору, щоб дерево росло знизу вгору
    turtle.up()
    turtle.goto(0, -200) # Початкова точка
    turtle.down()
    turtle.color("darkgreen")

    try:
        recursion_level = int(input("Введіть рівень рекурсії (наприклад, 7): "))
        if recursion_level < 0:
            print("Будь ласка, введіть додатне число.")
            return

        # Виклик функції малювання
        draw_pythagoras_tree(100, recursion_level)

        print("Малювання завершено!")
        screen.mainloop()
    except ValueError:
        print("Помилка: потрібно ввести ціле число.")

if __name__ == "__main__":
    main()
