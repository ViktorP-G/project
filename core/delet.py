import shutil
import os

def delete_file_and_folder(file_path, folder_path, quiet=False):
    """
    Удаляет файл и папку.
    Возвращает: (успешно: bool, сообщение: str)
    """
    messages = []


    try:
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            if not quiet:
                messages.append(f"Папка '{folder_path}' успешно удалена.")
        else:
            if not quiet:
                messages.append(f"Папка '{folder_path}' не найдена.")
    except PermissionError:
        messages.append(f"Нет прав для удаления папки '{folder_path}'.")
    except Exception as e:
        messages.append(f"Ошибка при удалении папки '{folder_path}': {e}")

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            if not quiet:
                messages.append(f"Файл '{file_path}' успешно удалён.")
        else:
            if not quiet:
                messages.append(f"Файл '{file_path}' не найден.")
    except PermissionError:
        messages.append(f"Нет прав для удаления файла '{file_path}'.")
    except Exception as e:
        messages.append(f"Ошибка при удалении файла '{file_path}': {e}")

    success = all("Ошибка" not in msg and "Нет прав" not in msg for msg in messages)
    return success, "\n".join(messages)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='delete', description="Удаляет файл и папку")
    parser.add_argument("file", help="файл для удаления")
    parser.add_argument("folder", help="папка для удаления")
    parser.add_argument("--quiet", action="store_true", help="без вывода сообщений")

    args = parser.parse_args()

    success, message = delete_file_and_folder(args.file, args.folder, args.quiet)
    if message:
        if success:
            print(message)
        else:
            print(message, file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()