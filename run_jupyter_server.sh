#!/usr/bin/env bash
set -e

# 1. Проверяем, что мы находимся в корне проекта (где лежит папка venv)
if [ ! -d "venv" ]; then
    echo "Ошибка: папка venv не найдена в текущей директории!"
    echo "Убедитесь, что вы запускаете скрипт из корня проекта."
    exit 1
fi

# 2. Вызываем Jupyter напрямую из venv, игнорируя source и PATH
echo "Запуск Jupyter Notebook..."
./venv/bin/jupyter notebook --no-browser --port=8888