# gui.py

import flet as ft
from gpt import GptClient
import asyncio
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

# Константы для настройки внешнего вида
MESSAGE_WIDTH = 300
USER_MESSAGE_BG = ft.colors.BLUE_100
ASSISTANT_MESSAGE_BG = ft.colors.GREEN_100
ERROR_MESSAGE_BG = ft.colors.RED_100

async def main(page: ft.Page):
    page.title = "ChatGPT GUI"
    page.vertical_alignment = ft.CrossAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    # Инициализация GptClient
    gpt_client = GptClient()

    # Получаем список моделей из gpt.py
    model_list = gpt_client.get_models()
    selected_model = model_list[0]  # Модель по умолчанию

    # История сообщений
    conversation = []

    # Область отображения чата
    chat_display = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        auto_scroll=True
    )

    # Метка для отображения статистики
    stats_label = ft.Text(value="Символы: 0 | Слова: 0 | Токены: 0", color="black")

    # Загрузка индикатора
    loading_indicator = ft.ProgressRing(visible=False)

    def update_stats(e):
        user_input = input_field.value.strip()
        char_count = len(user_input)
        word_count = len(user_input.split())
        # Подсчет токенов (приблизительный, так как g4f не предоставляет токенизатор)
        token_count = len(user_input.encode('utf-8')) // 4  # Примерная оценка

        stats_label.value = f"Символы: {char_count} | Слова: {word_count} | Токены: {token_count}"
        page.update()

    async def on_model_change(e):
        nonlocal selected_model, conversation
        selected_model = model_dropdown.value
        conversation = []  # Сброс истории при смене модели
        chat_display.controls.clear()
        update_stats(None)
        await page.update_async()

    async def send_message_async(user_input):
        # Показываем индикатор загрузки
        loading_indicator.visible = True
        await page.update_async()

        # Добавляем сообщение пользователя в историю
        conversation.append({
            "role": "user",
            "content": user_input
        })

        # Получаем ответ ассистента
        response_text = await asyncio.to_thread(
            gpt_client.send_message, selected_model, conversation
        )

        # Скрываем индикатор загрузки
        loading_indicator.visible = False

        # Проверяем на наличие ошибки
        if response_text.startswith("Ошибка:"):
            # Отображаем сообщение об ошибке
            error_message = create_message_container(
                response_text, ft.alignment.center_left, ERROR_MESSAGE_BG
            )
            chat_display.controls.append(error_message)
            await page.update_async()
        else:
            # Добавляем ответ ассистента в область чата
            assistant_message = create_message_container(
                response_text, ft.alignment.center_left, ASSISTANT_MESSAGE_BG
            )
            chat_display.controls.append(assistant_message)
            await page.update_async()

            # Добавляем ответ ассистента в историю
            conversation.append({
                "role": "assistant",
                "content": response_text
            })

    async def on_submit(e):
        if isinstance(e, ft.KeyboardEvent) and e.key == "Enter" and not e.shift:
            user_input = input_field.value.strip()
            if not user_input:
                return  # Если ввод пустой, ничего не делаем

            # Добавляем сообщение пользователя в область чата
            user_message = create_message_container(
                user_input, ft.alignment.center_right, USER_MESSAGE_BG
            )
            chat_display.controls.append(user_message)
            await page.update_async()

            # Очищаем поле ввода и обновляем статистику
            input_field.value = ""
            update_stats(None)
            await page.update_async()

            # Запускаем асинхронную отправку сообщения
            await send_message_async(user_input)
        elif not isinstance(e, ft.KeyboardEvent):
            # Обработка нажатия кнопки "Отправить"
            await on_submit_button(e)
    def create_message_container(content, alignment, bgcolor):
        # Создаем контейнер для всего содержимого
        message_widgets = []
        
        # Проверяем, содержит ли сообщение таблицу
        if "| " in content and " |" in content:
            # Разбиваем контент на строки
            lines = content.split('\n')
            table_data = []
            in_table = False
            
            for line in lines:
                if line.strip().startswith('|') and line.strip().endswith('|'):
                    if not in_table:
                        in_table = True
                        table_data = []
                    # Обрабатываем строку таблицы
                    cells = [cell.strip() for cell in line.strip('|').split('|')]
                    table_data.append(cells)
                elif in_table:
                    # Создаем DataTable
                    if table_data:
                        data_table = ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text(header))
                                for header in table_data[0]
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[ft.DataCell(ft.Text(cell)) for cell in row]
                                )
                                for row in table_data[1:] if not all(c.startswith('-') for c in row)
                            ],
                        )
                        message_widgets.append(data_table)
                    in_table = False
                else:
                    # Добавляем обычный текст как Markdown
                    if line.strip():
                        message_widgets.append(
                            ft.Markdown(
                                line,
                                selectable=True,
                                extension_set="github",
                                code_style=ft.TextStyle(
                                    font_family="monospace",
                                    size=14,
                                ),
                            )
                        )
        else:
            # Если таблиц нет, используем обычный Markdown
            message_widgets.append(
                ft.Markdown(
                    content,
                    selectable=True,
                    extension_set="github",
                    code_style=ft.TextStyle(
                        font_family="monospace",
                        size=14,
                    ),
                )
            )

        return ft.Container(
            content=ft.Column(
                message_widgets,
                tight=True,
            ),
            alignment=alignment,
            bgcolor=bgcolor,
            padding=10,
            border_radius=ft.border_radius.all(10),
            width=min(len(content) * 8 + 20, MESSAGE_WIDTH),
            margin=ft.margin.symmetric(horizontal=20),
        )
    async def on_submit_button(e):
        user_input = input_field.value.strip()
        if not user_input:
            return  # Если ввод пустой, ничего не делаем

        # Добавляем сообщение пользователя в область чата
        user_message = create_message_container(
            user_input, ft.alignment.center_right, USER_MESSAGE_BG
        )
        chat_display.controls.append(user_message)
        await page.update_async()

        # Очищаем поле ввода и обновляем статистику
        input_field.value = ""
        update_stats(None)
        await page.update_async()

        # Запускаем асинхронную отправку сообщения
        await send_message_async(user_input)

    def clear_chat(e):
        conversation.clear()
        chat_display.controls.clear()
        page.update()

    # Заголовок
    title = ft.Text("ChatGPT GUI", size=30, weight="bold", color="blue")

    # Выпадающий список для выбора модели
    model_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(model) for model in model_list],
        value=selected_model,
        on_change=on_model_change
    )

    # Кнопка очистки чата
    clear_chat_button = ft.IconButton(
        icon=ft.icons.DELETE,
        tooltip="Очистить чат",
        on_click=clear_chat
    )

    # Поле ввода
    input_field = ft.TextField(
        hint_text="Введите ваше сообщение",
        border_color="blue",
        focused_border_color="darkblue",
        on_submit=on_submit,
        on_change=update_stats,
        expand=True,
        multiline=True,
        shift_enter=True
    )

    # Кнопка отправки
    submit_button = ft.ElevatedButton(
        text="Отправить",
        on_click=on_submit_button,
        bgcolor="blue",
        color="white"
    )

    # Строка ввода (поле ввода и кнопка)
    input_row = ft.Row(
        [input_field, submit_button],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Контейнер для строки ввода, статистики и индикатора загрузки
    input_container = ft.Column(
        [
            stats_label,
            input_row,
            loading_indicator
        ],
        spacing=5
    )

    # Верхняя панель с выбором модели и кнопкой очистки
    top_row = ft.Row(
        [model_dropdown, clear_chat_button],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    # Основной макет страницы
    page.add(
        ft.Column(
            [
                title,
                top_row,
                chat_display,
                input_container
            ],
            expand=True
        )
    )

    # Инициализация статистики
    update_stats(None)
