import os
import time

def add_date_to_file(filepath):
    """
    Добавляет дату создания к имени файла.
    Возвращает: (успешно: bool, сообщение: str)
    """
    if not os.path.isfile(filepath):
        return False, f"Файл '{filepath}' не существует."

    try:
        stat = os.stat(filepath)
        creation_time = stat.st_ctime
        creation_date = time.strftime("%Y-%m-%d", time.localtime(creation_time))

        directory, filename = os.path.split(filepath)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}_{creation_date}{ext}"
        new_filepath = os.path.join(directory, new_filename)

        if os.path.exists(new_filepath):
            return False, f"Не переименовано: файл уже существует — {new_filepath}"

        os.rename(filepath, new_filepath)
        return True, f"Файл переименован: {filepath} → {new_filepath}"

    except Exception as e:
        return False, f"Ошибка при обработке '{filepath}': {e}"


def process_folder(folder_path, recursive=False):
    """
    Обрабатывает все файлы в папке (рекурсивно или нет).
    Возвращает: список сообщений.
    """
    messages = []
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                success, msg = add_date_to_file(filepath)
                messages.append(msg)
    else:
        for item in os.listdir(folder_path):
            filepath = os.path.join(folder_path, item)
            if os.path.isfile(filepath):
                success, msg = add_date_to_file(filepath)
                messages.append(msg)
    return messages


def rename_file_with_date(file_path, folder_path, recursive=False):
    """
    Главная функция: обрабатывает один файл + всю папку.
    Возвращает: (успешно: bool, сообщение: str)
    """
    messages = []

    success, msg = add_date_to_file(file_path)
    messages.append(msg)

    folder_msgs = process_folder(folder_path, recursive)
    messages.extend(folder_msgs)

    all_success = all("Ошибка" not in msg and "не переименовано" not in msg for msg in messages)
    return all_success, "\n".join(messages)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='rename', description="Добавляет дату создания к имени файла")
    parser.add_argument("file", help="файл для переименования")
    parser.add_argument("folder", help="папка для обработки")
    parser.add_argument("--recursive", action="store_true", help="рекурсивно")

    args = parser.parse_args()

    success, message = rename_file_with_date(args.file, args.folder, args.recursive)
    if message:
        if success:
            print(message)
        else:
            print(message, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()