@echo off
echo Starting installation and setup...

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python не установлен! Пожалуйста, установите Python 3.8 или выше.
    echo Скачать можно с https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Создаем и активируем виртуальное окружение
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Обновляем pip
echo Updating pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости
echo Installing requirements...
pip install -r requirements.txt

REM Проверяем успешность установки
if errorlevel 1 (
    echo Ошибка при установке зависимостей!
    pause
    exit /b 1
)

echo Installation completed successfully!
echo Starting the application...

REM Запускаем приложение
python main.py

REM Если приложение закрылось с ошибкой, показываем сообщение
if errorlevel 1 (
    echo Произошла ошибка при запуске приложения!
    pause
)

deactivate