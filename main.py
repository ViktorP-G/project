import sys
import argparse
import os

core_path = os.path.join(os.path.dirname(__file__), 'core')
if core_path not in sys.path:
    sys.path.insert(0, core_path)

try:
    from copy import copy_file
    from delet import delete_file_and_folder
    from rename import rename_file_with_date
except ImportError as e:
    print(f"Ошибка импорта модулей из core: {e}", file=sys.stderr)
    sys.exit(1)


def create_parser():
    parser = argparse.ArgumentParser(
        prog='mytool',
        description='🔧 Утилиты для работы с файлами',
        epilog='Используй: mytool <команда> --help или mytool --gui для графического интерфейса',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--gui", action="store_true", help="Запустить графический интерфейс")

    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    p_copy = subparsers.add_parser('copy', help='Копировать файл')
    p_copy.add_argument('file', help='Исходный файл')
    p_copy.add_argument('folder', help='Папка назначения')
    p_copy.add_argument('--overwrite', action='store_true', help='Разрешить перезапись')

    p_del = subparsers.add_parser('delete', help='Удалить файл и папку')
    p_del.add_argument('file', help='Файл для удаления')
    p_del.add_argument('folder', help='Папка для удаления')
    p_del.add_argument('--quiet', action='store_true', help='Без вывода сообщений')

    p_rename = subparsers.add_parser('rename', help='Добавить дату к имени')
    p_rename.add_argument('file', help='Файл для переименования')
    p_rename.add_argument('folder', help='Папка для обработки')
    p_rename.add_argument('--recursive', action='store_true', help='Рекурсивно обработать подпапки')

    return parser


def run_copy(args):
    success, message = copy_file(args.file, args.folder, args.overwrite)
    if success:
        print(message)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)


def run_delete(args):
    success, message = delete_file_and_folder(args.file, args.folder, args.quiet)
    if success:
        print(message)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)


def run_rename(args):
    success, message = rename_file_with_date(args.file, args.folder, args.recursive)
    if success:
        print(message)
    else:
        print(message, file=sys.stderr)
        sys.exit(1)


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.gui:
        try:
            from interface import gui
            print("Запуск графического интерфейса...")
            gui.run_gui()
        except Exception as e:
            print(f"Ошибка запуска GUI: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        if args.command == 'copy':
            run_copy(args)
        elif args.command == 'delete':
            run_delete(args)
        elif args.command == 'rename':
            run_rename(args)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()