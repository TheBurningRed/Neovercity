def get_cats_info(path: str) -> list[dict]:
    cats = []

    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    cat_id, name, age = line.split(',')
                    cats.append({
                        "id": cat_id,
                        "name": name,
                        "age": age
                    })
                except ValueError:
                    # Пропускаємо рядки з неправильним форматом
                    continue
    except FileNotFoundError:
        print(f"Файл '{path}' не знайдено.")
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")

    return cats

cats_info = get_cats_info("py_hw_04_02.txt")
print(cats_info)
