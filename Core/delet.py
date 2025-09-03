import argparse
import shutil
import os


def delete_files():
    parser = argparse.ArgumentParser(
        prog='delet',
        description="Удаляет файл и папку по указанным путям.",
        epilog='''
Примеры:
  del myfile.txt my_folder/
  del data.log temp/

Поведение:
  - Удаляет указанный файл и папку.
  - Если файл или папка не существует — выведет предупреждение.
  - Требуются права на удаление.
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("del_file", help="удаление файла")
    parser.add_argument("del_folder", help="удаление папки")
    parser.add_argument("--quiet", action="store_true", help="Не выводить сообщения")

    args = parser.parse_args()
    try:
        shutil.rmtree(args.del_folder)
        if not args.quiet:
            print(f"Папка {args.del_folder} успешно удалена.")
    except FileNotFoundError:
        if not args.quiet:
            print(f"Папка {args.del_folder} не найдена.")
    except PermissionError:
        if not args.quiet:
            print(f"Нет прав для удаления папки {args.del_folder}.")
    except Exception as e:
        if not args.quiet:
            print(f"Произошла ошибка при удалении папки {args.del_folder}: {e}.")

    try:
        os.remove(args.del_file)
        if not args.quiet:
            print(f"Файл {args.del_file} успешно удален.")
    except FileNotFoundError:
        if not args.quiet:
            print(f"Файл {args.del_file} не найден.")
    except PermissionError:
        if not args.quiet:
            print(f"Нет прав для удаления файла {args.del_file}.")
    except Exception as e:
        if not args.quiet:
            print(f"Произошла ошибка при удалении файла {args.del_file}: {e}.")


if __name__ == "__main__":
    delete_files()