import argparse
import os
import time


def data_create_filename():
    parser = argparse.ArgumentParser(
        prog='date',
        description="Команда добавляющая в название файла дату его создания.",
        epilog="""
        Описание:
          Скрипт добавляет дату создания файла в его имя: 
          'file.txt' → 'file_2024-06-15.txt'

        Примеры:
          add_date todo.txt ./notes
          add_date scan.jpg ./archive --recursive

        Примечание: работает корректно на Windows, где доступна дата создания.
        """,
    )

    parser.add_argument("data_file", help="Файл, которому нужно добавить дату создания в имя")
    parser.add_argument("data_folder", help="Папка, всем файлам в которой нужно добавить дату")
    parser.add_argument("--recursive", action="store_true", help="Обрабатывать подпапки рекурсивно")

    args = parser.parse_args()

    if not os.path.isfile(args.data_file):
        print(f"Ошибка: файл '{args.data_file}' не найден или не является файлом.")
        exit(1)
    if not os.path.isdir(args.data_folder):
        print(f"Ошибка: папка '{args.data_folder}' не найдена или не является папкой.")
        exit(1)

    add_date_to_file(args.data_file)
    process_folder(args.data_folder, args.recursive)


def process_folder(folder_path, recursive=False):
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                add_date_to_file(filepath)
    else:
        for item in os.listdir(folder_path):
            filepath = os.path.join(folder_path, item)
            if os.path.isfile(filepath):
                add_date_to_file(filepath)


def add_date_to_file(filepath):
    if not os.path.isfile(filepath):
        return
    try:
        stat = os.stat(filepath)
        creation_time = stat.st_ctime
        creation_date = time.strftime("%Y-%m-%d", time.localtime(creation_time))
        print(f" Дата создания файла '{filepath}': {creation_date}")

        directory, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)

        new_filename = f"{name}_{creation_date}{ext}"
        new_filepath = os.path.join(directory, new_filename)
        if os.path.exists(new_filepath):
            print(f"Не переименовано: файл уже существует — {new_filepath}")
        else:
            os.rename(filepath, new_filepath)
            print(f"Файл переименован: {filepath} в {new_filepath}")

    except Exception as e:
        print(f"Ошибка при обработке {filepath}: {e}")


if __name__ == "__main__":
    data_create_filename()