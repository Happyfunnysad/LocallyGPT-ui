#!/bin/bash

echo "Starting installation and setup..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "Python3 не установлен!"
    echo "Для Ubuntu/Debian: sudo apt install python3"
    echo "Для macOS: brew install python3"
    exit 1
fi

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "pip3 не установлен!"
    echo "Для Ubuntu/Debian: sudo apt install python3-pip"
    echo "Для macOS: brew install pip3"
    exit 1
fi

# Создание и активация виртуального окружения
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Обновление pip
echo "Updating pip..."
pip install --upgrade pip

# Установка зависимостей
echo "Installing requirements..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Ошибка при установке зависимостей!"
    exit 1
fi

echo "Installation completed successfully!"
echo "Starting the application..."

# Запуск приложен��я
python3 main.py

# Проверка ошибок
if [ $? -ne 0 ]; then
    echo "Произошла ошибка при запуске приложения!"
    read -p "Нажмите Enter для выхода"
fi

deactivate
