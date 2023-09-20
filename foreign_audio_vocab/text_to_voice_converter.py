import shutil

from gtts import gTTS
from pydub import AudioSegment
import os
from typing import List


class TextToVoiceConverter:
    """
    Класс для преобразования текстовых переводов в аудиофайлы.

    Параметры:
    - translations (List[str]): Список переводов в формате 'слово:перевод'.
    - delimiter (str): Разделитель между словом и переводом (по умолчанию ':').
    - langs (str): Языковые коды через разделитель (по умолчанию 'en:ru').
    - delay (int): Задержка между определениями в секундах (по умолчанию 1).
    - audio_files (set): Набор созданных промежуточных аудио файлов (по умолчанию [])
    """
    def __init__(self, translations: List[str], delimiter: str = ':', langs: str = 'en:ru', delay: int = 1):
        self.translations = translations
        self.delimiter = delimiter
        self.langs = langs
        self.delay = delay
        self.audio_files = []

        if not os.path.exists('tmp'):
            os.makedirs('tmp')

    def convert_to_audio(self, text: str, lang: str, filename: str) -> None:
        """
        Преобразование текста в аудио и сохранение в файл.

        Параметры:
        - text (str): Текст для преобразования.
        - lang (str): Языковой код.
        - filename (str): Путь к файлу для сохранения аудио.
        """
        try:
            tts = gTTS(text, lang=lang)
            tts.save(filename)
        except Exception as e:
            print(f"Ошибка при преобразовании текста '{text}' в аудио: {e}")

    def create_combined_audio(self, audio1_path: str, audio2_path: str, output_path: str) -> None:
        """
        Создание объединенного аудиофайла путем конкатенации двух аудиофайлов.

        Параметры:
        - audio1_path (str): Путь к первому аудиофайлу.
        - audio2_path (str): Путь ко второму аудиофайлу.
        - output_path (str): Путь для сохранения объединенного аудиофайла.
        """
        try:
            os.system(f'ffmpeg -i {audio1_path} -i {audio2_path} -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[outa]" -map "[outa]" {output_path}')
        except Exception as e:
            print(f"Ошибка при создании объединенного аудио: {e}")

    def create_silence_audio(self, duration: int, output_path: str) -> None:
        """
        Создание пустого аудиофайла указанной длительности.

        Параметры:
        - duration (int): Длительность пустого аудиофайла в секундах.
        - output_path (str): Путь для сохранения пустого аудиофайла.
        """
        try:
            silence_audio = AudioSegment.silent(duration=duration * 1000)
            silence_audio.export(output_path, format="mp3")
        except Exception as e:
            print(f"Ошибка при создании пустого аудио: {e}")

    def combine_audio_files(self) -> None:
        """
        Объединение аудиофайлов из списка в один большой файл с паузами.
        """
        output_path = 'combined_output.mp3'
        try:
            combined_audio = AudioSegment.silent(duration=0)
            for filename in self.audio_files:
                audio = AudioSegment.from_mp3(filename)
                combined_audio += audio
                if filename != self.audio_files[-1]:
                    delay_audio = AudioSegment.silent(duration=self.delay * 1000)
                    combined_audio += delay_audio

            combined_audio.export(output_path, format="mp3")
        except Exception as e:
            print(f"Ошибка при объединении аудиофайлов: {e}")

    def remove_old_audio_files(self) -> None:
        """
        Удаление временных аудиофайлов tmp.
        """
        try:
            shutil.rmtree('tmp')
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")

    def process_translations(self) -> None:
        """
        Обработка переводов и создание объединенных аудиофайлов.
        """

        for idx, translation in enumerate(self.translations, start=1):
            words = translation.split(self.delimiter)
            if len(words) != 2:
                print(f"Неверный формат перевода для записи {idx}: {translation}. Пропуск...")
                continue

            word1, word2 = words
            lang1, lang2 = self.langs.split(self.delimiter)

            audio1_path = os.path.join('tmp', 'temp_1.mp3')
            audio2_path = os.path.join('tmp', 'temp_2.mp3')

            self.convert_to_audio(word1, lang1, audio1_path)
            self.create_silence_audio(self.delay, audio2_path)
            self.convert_to_audio(word2, lang2, audio2_path)

            combined_output_path = os.path.join('tmp', f'{word1.replace(" ", "_")}.mp3')

            # Проверяем, существует ли файл по указанному пути
            if os.path.isfile(combined_output_path):
                print(f"Файл {combined_output_path} уже существует. Пропуск...")
            else:
                # Создаем объединенный аудиофайл, только если его нет
                self.create_combined_audio(audio1_path, audio2_path, combined_output_path)
                self.audio_files.append(combined_output_path)

            os.remove(audio1_path)
            os.remove(audio2_path)
