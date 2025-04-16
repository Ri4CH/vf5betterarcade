import re
import random
import os
import sys
import subprocess
from collections import deque


def main():
    # Конфигурация
    WORDS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
             'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK']

    # Пути к файлам (проверяем оба возможных расположения)
    base_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'mods', 'Better Arcade Mode', 'rom', 'game_score.txt')
    exe_path = os.path.join(base_dir, 'VFREVO.exe')

    # Проверка существования файлов
    if not os.path.exists(file_path):
        print(f"Ошибка: Файл не найден: {file_path}")
        return
    if not os.path.exists(exe_path):
        print(f"Ошибка: VFREVO.exe не найден: {exe_path}")
        return

    # Инициализация замен
    pattern = re.compile(r'\b(' + '|'.join(WORDS) + r')\b')
    used_replacements = deque(maxlen=len(WORDS))

    def get_replacement(original):
        possible = [w for w in WORDS if w != original and w not in used_replacements]
        if possible:
            replacement = random.choice(possible)
            used_replacements.append(replacement)
            return replacement
        return original

    # Обработка файла
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Заменяем только строки 82-112 (индексы 81-111)
        for i in range(81, min(112, len(lines))):
            lines[i] = pattern.sub(lambda m: get_replacement(m.group(0)), lines[i])

        # Записываем изменения
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print("Файл успешно обработан. Замены выполнены.")

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return

    # Запуск VFREVO.exe
    try:
        subprocess.Popen([exe_path], cwd=base_dir)
        print("VFREVO.exe успешно запущен.")
    except Exception as e:
        print(f"Ошибка при запуске VFREVO.exe: {e}")


if __name__ == "__main__":
    main()
    # Оставляем окно открытым только при запуске из Python
    if not getattr(sys, 'frozen', False):
        input("Нажмите Enter для выхода...")