@echo off
echo Запуск GPT Chat Client...

REM Проверяем наличие виртуального окружения
if not exist "venv" (
    echo Виртуальное окружение не найдено!
    echo Пожалуйста, сначала запустите install_and_run.bat
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
call venv\Scripts\activate.bat

REM Запускаем приложение
python main.py

REM Если приложение закрылось с ошибкой
if errorlevel 1 (
    echo Произошла ошибка при запуске приложения!
    echo Проверьте, что все зависимости установлены корректно.
    echo Попробуйте запустить install_and_run.bat для переустановки.
    pause
)

deactivatea@echo off