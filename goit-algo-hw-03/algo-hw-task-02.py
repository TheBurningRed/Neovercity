import turtle


def koch_segment(t, length, level):
    """Рекурсивно малює одну лінію Коха."""
    if level == 0:
        t.forward(length)
    else:
        length /= 3.0
        koch_segment(t, length, level - 1)
        t.left(60)
        koch_segment(t, length, level - 1)
        t.right(120)
        koch_segment(t, length, level - 1)
        t.left(60)
        koch_segment(t, length, level - 1)


def koch_snowflake(t, length, level):
    """Малює повну сніжинку Коха (3 сторони)."""
    for _ in range(3):
        koch_segment(t, length, level)
        t.right(120)


def main():
    # Ввід рівня рекурсії від користувача
    try:
        level = int(input("Введіть рівень рекурсії (0–6 рекомендовано): "))
        if level < 0:
            raise ValueError
    except ValueError:
        print("Некоректне значення. Використовую рівень 3.")
        level = 3

    # Базові налаштування екрану та «черепахи»
    screen = turtle.Screen()
    screen.title("Сніжинка Коха")
    screen.setup(width=800, height=800)

    t = turtle.Turtle()
    t.speed(0)          # Максимальна швидкість
    t.penup()
    # Трохи зсунемося вниз, щоб сніжинка влізла в екран
    t.goto(-250, 150)
    t.pendown()

    length = 500  # Довжина сторони базового трикутника
    koch_snowflake(t, length, level)

    t.hideturtle()
    screen.mainloop()


if __name__ == "__main__":
    main()
