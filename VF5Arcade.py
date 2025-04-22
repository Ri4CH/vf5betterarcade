import random
import re
import os
import subprocess
import sys


def randomize_names():
    original_words = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL', 'AOI', 'LEI', 'VAN', 'BRA',
                      'GOH', 'MON', 'MSK', 'KRT', 'TAK']
    randomized_words = original_words.copy()
    random.shuffle(randomized_words)

    file_path = os.path.join('mods', 'Better Arcade Mode', 'rom', 'game_score.txt')

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        words_and_nonwords = re.split(r'(\W+)', content)

        current_index = 0
        for i, token in enumerate(words_and_nonwords):
            if token.isalpha() and token in original_words:
                replacement = randomized_words[current_index % len(randomized_words)]
                words_and_nonwords[i] = replacement
                current_index += 1

        new_content = ''.join(words_and_nonwords)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print("New order:")
        print(randomized_words)
        return True
    except Exception as e:
        print(f"Error in file: {e}")
        return False


def main():
    if randomize_names():
        exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        exe_path = os.path.join(exe_dir, "VFREVO.exe")

        try:
            subprocess.Popen([exe_path], creationflags=subprocess.CREATE_NO_WINDOW)
            print(f"Launched {exe_path}")
        except Exception as e:
            print(f"error while launching VFREVO.exe: {e}")


if __name__ == "__main__":
    main()
