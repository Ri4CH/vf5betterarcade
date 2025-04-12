import re
import random
import os
import sys
import subprocess
import tempfile
import atexit
import shutil
from collections import deque

# Режим без консоли
IS_COMPILED = getattr(sys, 'frozen', False)
SUPPRESS_OUTPUT = True  # Отключаем все сообщения

# Настройка путей
CURRENT_DIR = os.path.dirname(sys.executable if IS_COMPILED else os.path.abspath(__file__))
FILE_PATH = os.path.join(CURRENT_DIR, r"mods\Better Arcade Mode\rom\game_score.txt")
EXE_PATH = os.path.join(CURRENT_DIR, "VFREVO.exe")

WORDS = ['AKI', 'SAR', 'LAU', 'SHU', 'JEF', 'PAI', 'JAK', 'KAG', 'LIO', 'WOL',
         'AOI', 'LEI', 'VAN', 'BRA', 'GOH', 'MON', 'MSK', 'KRT', 'TAK', 'TE2']


class SilentWordReplacer:
    def __init__(self):
        self.pattern = re.compile(r'\b(' + '|'.join(WORDS) + r')\b')
        self.used_replacements = deque(maxlen=len(WORDS))

    def get_replacement(self, original_word):
        possible = [w for w in WORDS if w != original_word and w not in self.used_replacements]
        if possible:
            replacement = random.choice(possible)
        else:
            replacement = self.used_replacements.popleft() if self.used_replacements else original_word

        if replacement != original_word:
            self.used_replacements.append(replacement)
        return replacement


def process_file_silently():
    replacer = SilentWordReplacer()
    try:
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as tmp:
            with open(FILE_PATH, 'r', encoding='utf-8') as src:
                for i, line in enumerate(src):
                    if 81 <= i < 112:
                        line = replacer.pattern.sub(
                            lambda m: replacer.get_replacement(m.group(0)),
                            line
                        )
                    tmp.write(line)

            shutil.move(tmp.name, FILE_PATH)
        return True
    except Exception:
        return False


def run_exe_silently():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        subprocess.Popen(
            [EXE_PATH],
            cwd=CURRENT_DIR,
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=True
        )
        return True
    except Exception:
        return False


def main():
    # Очистка временных файлов PyInstaller
    if hasattr(sys, '_MEIPASS'):
        atexit.register(lambda: shutil.rmtree(sys._MEIPASS, ignore_errors=True))

    process_file_silently()
    run_exe_silently()


if __name__ == "__main__":
    main()