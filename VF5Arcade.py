import os
import sys
import random
from pathlib import Path


def get_base_path():
    """Определяет правильный базовый путь для EXE и скрипта."""
    if getattr(sys, 'frozen', False):
        # Если программа 'заморожена' (скомпилирована в EXE)
        return Path(sys.executable).parent
    else:
        # Обычный режим (запуск как скрипт)
        return Path(__file__).parent


# Исходный список слов
original_words = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL', 'AOI', 'LEI', 'VAN', 'BRA',
                  'GOH', 'MON', 'MSK', 'KRT', 'TAK']


def randomize_words():
    randomized = original_words.copy()
    random.shuffle(randomized)
    return randomized


def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {file_path}")
        return

    words = []
    current_word = ''
    for char in content:
        if char.isalnum() or char == '_':
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ''
            words.append(char)

    if current_word:
        words.append(current_word)

    randomized_words = randomize_words()
    current_index = 0

    processed_words = []
    for word in words:
        if word in original_words:
            replacement = randomized_words[current_index]
            processed_words.append(replacement)
            current_index += 1
            if current_index >= len(randomized_words):
                randomized_words = randomize_words()
                current_index = 0
        else:
            processed_words.append(word)

    new_content = ''.join(processed_words)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в файл: {file_path}")


def main():
    base_path = get_base_path()

    # Путь к файлу game_score.txt
    file_path = base_path / 'mods' / 'Better Arcade Mode' / 'rom' / 'game_score.txt'

    if file_path.exists():
        process_file(file_path)
    else:
        print(f"Файл не найден: {file_path}")
        print("Убедитесь, что EXE лежит в той же папке, где находится VFREVO.exe")

    # Путь к VFREVO.exe
    exe_path = base_path / 'VFREVO.exe'
    import subprocess
    if exe_path.exists():
        subprocess.Popen([exe_path], shell=True)  # Запускает без ожидания
    else:
        print(f"Ошибка: VFREVO.exe не найден в {base_path}")


if __name__ == '__main__':
    main()
