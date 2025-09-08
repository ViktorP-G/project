import flet as ft
from core.copy import copy_file
from core.delet import delete_file_and_folder
from core.rename import rename_file_with_date


def show_main_menu(page):
    page.clean()
    page.add(
        ft.Text("🔧 File Tools", size=28, weight="bold", text_align="center"),
        ft.Divider(),
        ft.ElevatedButton("📄 Копировать", on_click=lambda _: show_operation_ui(page, "copy"), width=250),
        ft.ElevatedButton("🗑️ Удалить", on_click=lambda _: show_operation_ui(page, "delete"), width=250),
        ft.ElevatedButton("📅 Переименовать", on_click=lambda _: show_operation_ui(page, "rename"), width=250),
    )
    page.update()


def show_operation_ui(page, operation):
    config = {
        "copy": {
            "title": "📄 Копирование",
            "icon": "📄",
            "func": copy_file,
            "args": ["file", "folder", "overwrite"],
            "checkbox": ("Перезаписать", False),
            "button_color": ft.colors.BLUE
        },
        "delete": {
            "title": "🗑️ Удаление",
            "icon": "🗑️",
            "func": delete_file_and_folder,
            "args": ["file", "folder", "quiet"],
            "checkbox": ("Тихий режим", False),
            "button_color": ft.colors.RED
        },
        "rename": {
            "title": "📅 Переименование",
            "icon": "📅",
            "func": rename_file_with_date,
            "args": ["file", "folder", "recursive"],
            "checkbox": ("Рекурсивно", False),
            "button_color": ft.colors.GREEN
        }
    }

    op_config = config[operation]
    file_picker = ft.FilePicker()
    folder_picker = ft.FilePicker()
    page.overlay.extend([file_picker, folder_picker])

    src_text = ft.Text("Файл: не выбран", size=12, color=ft.colors.GREY)
    dst_text = ft.Text("Папка: не выбрана", size=12, color=ft.colors.GREY)
    checkbox = ft.Checkbox(label=op_config["checkbox"][0], value=op_config["checkbox"][1])

    def pick_file(_):
        file_picker.pick_files()

    def pick_folder(_):
        folder_picker.get_directory_path()

    def execute(_):
        page.clean()
        show_main_menu(page)
        page.add(ft.Text(op_config["title"], size=20, weight="bold"))

        if not getattr(file_picker, 'result', None) or not file_picker.result.files:
            show_result(page, "❌ Выберите файл!", False)
            return
        if not getattr(folder_picker, 'result', None) or not folder_picker.result.path:
            show_result(page, "❌ Выберите папку!", False)
            return

        try:
            file_path = file_picker.result.files[0].path
            folder_path = folder_picker.result.path
            args = [file_path, folder_path, checkbox.value]
            success, message = op_config["func"](*args)

            # Для тихого режима не показываем сообщение
            if operation == "delete" and checkbox.value:
                show_result(page, "✅ Операция выполнена", True)
            else:
                show_result(page, message, success)
        except Exception as e:
            show_result(page, f"❌ Ошибка: {e}", False)

    def on_file_result(e):
        if e.files:
            src_text.value = f"Файл: {e.files[0].name}"
            src_text.color = ft.colors.BLUE
        page.update()

    def on_folder_result(e):
        if e.path:
            dst_text.value = f"Папка: {e.path.split('/')[-1]}"
            dst_text.color = ft.colors.BLUE
        page.update()

    file_picker.on_result = on_file_result
    folder_picker.on_result = on_folder_result

    page.clean()
    page.add(
        ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: show_main_menu(page)),
        ft.Text(op_config["title"], size=20, weight="bold"),
        ft.ElevatedButton("Выбрать файл", on_click=pick_file),
        src_text,
        ft.ElevatedButton("Выбрать папку", on_click=pick_folder),
        dst_text,
        checkbox,
        ft.ElevatedButton("Выполнить", on_click=execute,
                          bgcolor=op_config["button_color"],
                          color=ft.colors.WHITE),
    )
    page.update()


def show_result(page, message, is_success=True):
    color = ft.colors.GREEN if is_success else ft.colors.RED
    page.add(ft.Text(message, color=color, size=14))


def run_gui():
    def main(page: ft.Page):
        page.title = "File Tools"
        page.window_width = 800
        page.window_height = 600
        show_main_menu(page)

    ft.app(target=main)