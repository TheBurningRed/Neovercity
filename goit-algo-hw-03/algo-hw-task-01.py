#!/usr/bin/env python3
import argparse
import os
import shutil
import sys
from pathlib import Path

"""
    Рекурсивно обходить src_dir, копіює файли в dst_root з розкладанням
    по підтеках за розширенням.
"""
def copy_and_sort_recursive(src_dir: Path, dst_root: Path) -> None:
    try:
        with os.scandir(src_dir) as it:
            for entry in it:
                entry_path = Path(entry.path)

                try:
                    # resolve() може зламатися на битих symlink-ах → ловимо окремо
                    if entry_path.resolve().is_relative_to(dst_root.resolve()):
                        continue
                except Exception:
                    # Якщо не змогли визначити, просто не фільтруємо
                    pass

                if entry.is_dir(follow_symlinks=False):
                    # Рекурсивний обхід піддиректорій
                    copy_and_sort_recursive(entry_path, dst_root)
                elif entry.is_file(follow_symlinks=False):
                    copy_single_file(entry_path, dst_root)
                else:
                    # Все інше (symlink-и, сокети тощо) ігноруємо
                    continue
    except PermissionError as e:
        print(f"Немає прав доступу до директорії: {src_dir} ({e})", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"Директорію не знайдено: {src_dir} ({e})", file=sys.stderr)
    except OSError as e:
        print(f"Помилка доступу до директорії: {src_dir} ({e})", file=sys.stderr)


def copy_single_file(src_file: Path, dst_root: Path) -> None:
    """
    Копіює один файл у піддиректорію в dst_root, яка названа за розширенням файлу.
    """
    try:
        ext = src_file.suffix.lower()
        if ext.startswith("."):
            ext = ext[1:]  # ".jpg" -> "jpg"

        if not ext:
            ext = "no_extension"

        dst_dir = dst_root / ext
        dst_dir.mkdir(parents=True, exist_ok=True)

        dst_file = dst_dir / src_file.name

        shutil.copy2(src_file, dst_file)
    except PermissionError as e:
        print(f"Немає прав для копіювання файлу: {src_file} ({e})", file=sys.stderr)
    except FileNotFoundError as e:
        print(f"Файл не знайдено під час копіювання: {src_file} ({e})", file=sys.stderr)
    except OSError as e:
        print(f"Помилка копіювання файлу: {src_file} ({e})", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли з вихідної директорії в нову, "
                    "сортує їх по піддиректоріях за розширенням файлів."
    )
    parser.add_argument(
        "src",
        help="Шлях до вихідної директорії"
    )
    parser.add_argument(
        "dst",
        nargs="?",
        default="dist",
        help="Шлях до директорії призначення (за замовчуванням: dist)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    src_dir = Path(args.src).resolve()
    dst_root = Path(args.dst).resolve()

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Вихідна директорія не існує або не є директорією: {src_dir}", file=sys.stderr)
        sys.exit(1)

    # Створюємо директорію призначення, якщо її немає
    try:
        dst_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Не вдалося створити директорію призначення: {dst_root} ({e})", file=sys.stderr)
        sys.exit(1)

    # Захист від рекурсії в саму себе, якщо dst лежить в src
    try:
        if dst_root.is_relative_to(src_dir):
            print("Директорія призначення не може бути всередині вихідної директорії.", file=sys.stderr)
            sys.exit(1)
    except AttributeError:
        # Для старих версій Python (<3.9) is_relative_to відсутній
        src_str = str(src_dir)
        dst_str = str(dst_root)
        if dst_str.startswith(src_str.rstrip(os.sep) + os.sep):
            print("Директорія призначення не може бути всередині вихідної директорії.", file=sys.stderr)
            sys.exit(1)

    copy_and_sort_recursive(src_dir, dst_root)
    print("Копіювання та сортування завершено.")


if __name__ == "__main__":
    main()
