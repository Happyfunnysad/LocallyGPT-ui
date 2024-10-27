#!/bin/bash

echo "Запуск GPT Chat Client..."

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "Виртуальное окружение не найдено!"
    echo "Пожалуйста, сначала запустите install_and_run.sh"
    read -p "Нажмите Enter для выхода"
    exit 1
fi

# Активация виртуального окружения
source venv/bin/activate

# Запуск приложения
python3 main.py

# Проверка ошибок
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при запуске приложения!"
    echo "Проверьте, что все зависимости установлены корректно."
    echo "Попробуйте запустить install_and_run.sh для переустановки."
    read -p "Нажмите Enter для выхода"
fi

deactivate
