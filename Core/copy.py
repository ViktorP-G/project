import argparse
import shutil
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='copy',
        description="Копирует файл в указанную папку. Защищает от случайной перезаписи",
        epilog='''
Примеры:
  copy_file document.txt /tmp/
  copy_file data.csv /backup/ --overwrite

Поведение по умолчанию:
  - Если файл уже существует в папке — копирование отменяется.
  - Используйте --overwrite, чтобы разрешить перезапись.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("file", help="путь к файлу")
    parser.add_argument("folder", help="путь к папке")
    parser.add_argument("--overwrite",action="store_true",help="доступ к перезаписи файла")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        sys.stderr.write(f"файл '{args.file}' не найден.\n")
        sys.exit(1)

    if not os.path.isdir(args.folder):
        sys.stderr.write(f"Ошибка: папка '{args.folder}' не существует или это не папка.\n")
        sys.exit(1)

    filename = os.path.basename(args.file)
    destination = os.path.join(args.folder, filename)

    if os.path.exists(destination) and not args.overwrite:
        sys.stderr.write(f"Ошибка: файл назначения '{destination}' уже используется, используйте --overwrite для перезаписи.\n")
        sys.exit(1)

    try:
        shutil.copy2(args.file, destination)
        sys.stdout.write(f"Файл скопирован успешно из '{args.file}' в '{destination}'.\n")
    except Exception as e:
        sys.stderr.write(f"Ошибка при копировании: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
