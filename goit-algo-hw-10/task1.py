import pulp

# Ліміти ресурсів
WATER_LIMIT = 100
SUGAR_LIMIT = 50
LEMON_JUICE_LIMIT = 30
FRUIT_PUREE_LIMIT = 40

# Витрати на одиницю Лимонаду
LEMONADE_WATER = 2
LEMONADE_SUGAR = 1
LEMONADE_JUICE = 1

# Витрати на одиницю Фруктового соку
JUICE_WATER = 1
JUICE_PUREE = 2

def main():
    # Ініціалізація моделі
    model = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

    # Визначення змінних
    lemonade = pulp.LpVariable('Lemonade', lowBound=0, cat='Integer')
    fruit_juice = pulp.LpVariable('Fruit_Juice', lowBound=0, cat='Integer')

    # Цільова функція: Максимізувати загальну кількість вироблених продуктів
    model += lemonade + fruit_juice, "Total_Production"

    # Обмеження ресурсів
    model += (LEMONADE_WATER * lemonade + JUICE_WATER * fruit_juice <= WATER_LIMIT,
              "Water_Constraint")
    model += LEMONADE_SUGAR * lemonade <= SUGAR_LIMIT, "Sugar_Constraint"
    model += LEMONADE_JUICE * lemonade <= LEMON_JUICE_LIMIT, "Lemon_Juice_Constraint"
    model += JUICE_PUREE * fruit_juice <= FRUIT_PUREE_LIMIT, "Fruit_Puree_Constraint"

    # Розв'язання моделі
    model.solve(pulp.PULP_CBC_CMD(msg=0))

    # Вивід результатів
    print(f"Статус: {pulp.LpStatus[model.status]}")
    print(f"Виробити Лимонаду: {int(lemonade.varValue)}")
    print(f"Виробити Фруктового соку: {int(fruit_juice.varValue)}")
    print(f"Загальна кількість продуктів: {int(pulp.value(model.objective))}")

if __name__ == "__main__":
    main()
