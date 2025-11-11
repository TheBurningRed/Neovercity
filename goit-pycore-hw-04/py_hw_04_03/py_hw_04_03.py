#!/usr/bin/env python3
"""
Вивід дерева директорії з кольорами.
Використання:
    python tree_view.py /шлях/до/директорії
"""

from pathlib import Path
import sys
from colorama import init, Fore, Style

# Увімкнути підтримку кольорів у всіх ОС
init(autoreset=True)

DIR_COLOR = Style.BRIGHT + Fore.BLUE     # каталоги
FILE_COLOR = Fore.WHITE                  # файли
LINK_COLOR = Fore.CYAN                   # символічні лінки
ERR_COLOR = Fore.RED                     # помилки доступу тощо

BRANCH_MID = "├── "
BRANCH_END = "└── "
PIPE = "│   "
SPACE = "    "


def print_tree(root: Path) -> None:
    """
    Друкує дерево вмісту root.
    """
    def _safe_iterdir(p: Path):
        try:
            return list(p.iterdir())
        except PermissionError:
            print(ERR_COLOR + f"{SPACE}{BRANCH_END}[no permission]")
            return []
        except OSError as e:
            print(ERR_COLOR + f"{SPACE}{BRANCH_END}[os error: {e}]")
            return []

    def _format_name(p: Path) -> str:
        if p.is_symlink():
            # Показати куди посилається лінк
            try:
                target = p.resolve(strict=False)
            except Exception:
                target = "?"
            base = LINK_COLOR + p.name + Style.RESET_ALL
            return f"{base} -> {target}"
        if p.is_dir():
            return DIR_COLOR + p.name + Style.RESET_ALL + "/"
        return FILE_COLOR + p.name + Style.RESET_ALL

    def _walk(p: Path, prefix: str) -> None:
        entries = _safe_iterdir(p)
        # Сортуємо: спочатку каталоги, потім файли; лексикографічно
        entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        for i, child in enumerate(entries):
            connector = BRANCH_END if i == len(entries) - 1 else BRANCH_MID
            print(prefix + connector + _format_name(child))
            if child.is_dir():
                new_prefix = prefix + (SPACE if i == len(entries) - 1 else PIPE)
                _walk(child, new_prefix)

    # Заголовок
    if root.is_symlink():
        head = LINK_COLOR + root.name + Style.RESET_ALL
    elif root.is_dir():
        head = DIR_COLOR + root.name + Style.RESET_ALL + "/"
    else:
        head = FILE_COLOR + root.name + Style.RESET_ALL

    print(head)
    if root.is_dir():
        _walk(root, "")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Помилка: потрібно передати шлях до директорії.\n"
              "Приклад: python tree_view.py /path/to/dir")
        return 2

    path_str = argv[1]
    root = Path(path_str)

    if not root.exists():
        print(ERR_COLOR + f"Шлях не існує: {root}")
        return 1
    if not root.is_dir():
        print(ERR_COLOR + f"Це не директорія: {root}")
        return 1

    try:
        print_tree(root)
        return 0
    except KeyboardInterrupt:
        print("\nПерервано користувачем.")
        return 130
    except Exception as e:
        print(ERR_COLOR + f"Неочікувана помилка: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))