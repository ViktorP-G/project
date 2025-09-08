import sys
import argparse
import os

def create_parser():
    parser = argparse.ArgumentParser(
        prog='mytool',
        description='🔧 Утилиты для работы с файлами',
        epilog='Используй: mytool <команда> --help',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')

    p_copy = subparsers.add_parser('copy', help='Копировать файл')
    p_copy.add_argument('file', help='Исходный файл')
    p_copy.add_argument('folder', help='Папка назначения')
    p_copy.add_argument('--overwrite', action='store_true', help='Разрешить перезапись')

    p_del = subparsers.add_parser('delete', help='Удалить файл и папку')
    p_del.add_argument('file', help='Файл для удаления')
    p_del.add_argument('folder', help='Папка для удаления')
    p_del.add_argument('--quiet', action='store_true', help='Без вывода')

    p_rename = subparsers.add_parser('rename', help='Добавить дату к имени')
    p_rename.add_argument('file', help='Файл для переименования')
    p_rename.add_argument('folder', help='Папка для обработки')
    p_rename.add_argument('--recursive', action='store_true', help='Рекурсивно')

    return parser


def run_copy(args):
    original_argv = sys.argv.copy()

    sys.argv = ['copy', args.file, args.folder]
    if args.overwrite:
        sys.argv.append('--overwrite')

    try:
        core_path = os.path.join(os.path.dirname(__file__), 'core')
        if core_path not in sys.path:
            sys.path.insert(0, core_path)

        from copy import main as copy_main
        copy_main()
    finally:
        sys.argv = original_argv


def run_delete(args):
    original_argv = sys.argv.copy()

    sys.argv = ['delet', args.file, args.folder]
    if args.quiet:
        sys.argv.append('--quiet')

    try:
        core_path = os.path.join(os.path.dirname(__file__), 'core')
        if core_path not in sys.path:
            sys.path.insert(0, core_path)

        from delet import delete_files
        delete_files()
    finally:
        sys.argv = original_argv


def run_rename(args):
    original_argv = sys.argv.copy()

    sys.argv = ['date', args.file, args.folder]
    if args.recursive:
        sys.argv.append('--recursive')

    try:
        core_path = os.path.join(os.path.dirname(__file__), 'core')
        if core_path not in sys.path:
            sys.path.insert(0, core_path)

        from date_renamer import data_create_filename
        data_create_filename()
    finally:
        sys.argv = original_argv


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == 'copy':
            run_copy(args)
        elif args.command == 'delete':
            run_delete(args)
        elif args.command == 'rename':
            run_rename(args)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()