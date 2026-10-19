#!/usr/bin/env bash
set -e

# Проверяем, существует ли venv
if [ ! -d "venv" ]; then
    echo "Ошибка: venv не найден. Сначала запустите ./install.sh"
    exit 1
fi

# Активируем venv
source venv/bin/activate

echo "Running tests..."
# Запускаем pytest с флагом -v (verbose) для подробного вывода
# Указываем путь к файлу с тестами относительно корня проекта
./venv/bin/python -m pytest src/analysis/tests.py -v