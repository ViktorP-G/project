import shutil
import os
import sys

def copy_file(file_path, folder_path, overwrite=False):
    """
    Копирует файл в указанную папку.
    Возвращает: (успешно: bool, сообщение: str)
    """
    if not os.path.isfile(file_path):
        return False, f"Файл '{file_path}' не найден."

    if not os.path.isdir(folder_path):
        return False, f"Папка '{folder_path}' не существует."

    filename = os.path.basename(file_path)
    destination = os.path.join(folder_path, filename)

    if os.path.exists(destination) and not overwrite:
        return False, f"Файл '{destination}' уже существует. Используйте overwrite=True для перезаписи."

    try:
        shutil.copy2(file_path, destination)
        return True, f"Файл успешно скопирован: {file_path} → {destination}"
    except Exception as e:
        return False, f"Ошибка при копировании: {e}"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog='copy',
        description="Копирует файл в указанную папку. Защищает от случайной перезаписи",
    )
    parser.add_argument("file", help="путь к файлу")
    parser.add_argument("folder", help="путь к папке")
    parser.add_argument("--overwrite", action="store_true", help="разрешить перезапись")

    args = parser.parse_args()

    success, message = copy_file(args.file, args.folder, args.overwrite)
    if success:
        print(message)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
