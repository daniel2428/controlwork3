import flet as ft
from db import main_db


def main(page: ft.Page):
    page.title = 'Shop List'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    task_list = ft.Column(spacing=10)
    filter_type = "all"

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, bought in main_db.get_tasks(filter_type):
            task_list.controls.append(create_task_row(task_id, task_text, bought))
        page.update()

    def create_task_row(task_id, task_text, bought):
        task_field = ft.TextField(value=task_text, expand=True, dense=True, read_only=True)
        in_work = ft.Checkbox(
            label="Нужно купить",
            value=(bought == 1),
            tristate=False,
            on_change=lambda e: toggle_in_work(task_id, e.control.value)
        )

        task_done = ft.Checkbox(
            label="Куплено",
            value=(bought == 2),
            tristate=False,
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )
        
        def enable_edit(e):
            task_field.read_only = False
            page.update()

        def save_edit(e):
            main_db.update_task_db(task_id, new_task=task_field.value)
            task_field.read_only = True
            page.update()



        return ft.Row([
            task_done,
            task_field,
            in_work,
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_edit),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value.strip():
            task_id = main_db.add_task_db(task_input.value.strip())
            task_list.controls.append(create_task_row(task_id, task_input.value.strip(), 0))
            task_input.value = ""
            page.update()

    def toggle_task(task_id, is_bought):
        status = 2 if is_bought else 0
        main_db.update_task_db(task_id, bought=status)
        load_tasks()

    def toggle_in_work(task_id, is_in_work):
        if is_in_work:
            main_db.update_task_status(task_id, 1)
        else:
            main_db.update_task_status(task_id, 0) 
        load_tasks()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    def bought_count():
        bought_tasks = main_db.get_tasks("bought")
        all_tasks = main_db.get_tasks()
        if all_tasks:
            return len(bought_tasks) / len(all_tasks) * 100
        
        return 0
    
    def clean_bought(e):
        main_db.delete_bought_tasks()
        load_tasks()


    task_input = ft.TextField(hint_text='Добавьте товар', expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD)

    filter_buttons = ft.Row([
        ft.ElevatedButton("Очистить куплинные", on_click=clean_bought),
        ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
        ft.ElevatedButton("Куплинные", on_click=lambda e: set_filter("bought")),
        ft.ElevatedButton("Нужно купить", on_click=lambda e: set_filter("need_bought")),
        ft.ElevatedButton("Не куплинные", on_click=lambda e: set_filter("not_bought")),
    ], alignment=ft.MainAxisAlignment.CENTER)

    content = ft.Container(
        content=ft.Column([
            ft.Row([task_input, add_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            filter_buttons,
            ft.Text(f"Процент купленных продуктов: {bought_count():.2f}%", size=16),
            ft.Divider(),
            task_list
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=20,
        alignment=ft.alignment.center
    )

    background_image = ft.Image(
        src='image.png',
        fit=ft.ImageFit.FILL,
        width=page.width,
        height=page.height
    )

    background = ft.Stack([background_image, content])

    def on_resize(e):
        background_image.width = page.width
        background_image.height = page.height
        page.update()

    page.on_resize = on_resize
    page.add(background)

    load_tasks()


if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main)