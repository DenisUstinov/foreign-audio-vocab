import shutil
from gtts import gTTS
from pydub import AudioSegment
import os
from typing import List


class TextToVoiceConverter:
    """
    Класс для конвертации текста в речь и создания аудиофайлов.

    Args:
        translations (List[str]): Список строк с переводами для обработки.
        delimiter (str, optional): Разделитель между словами в переводах. По умолчанию ':'
        langs (str, optional): Строка с языковыми кодами, разделенными двоеточием, например, 'en:ru'. По умолчанию 'en:ru'.
        delay (int, optional): Задержка между аудиофайлами в миллисекундах. По умолчанию 1.
        tmp_dir (str, optional): Путь к временной директории для сохранения временных файлов. По умолчанию 'tmp'.
    """

    def __init__(self, translations: List[str], delimiter: str = ':', langs: str = 'en:ru', delay: int = 1,
                 tmp_dir: str = 'tmp'):
        self.translations = translations
        self.delimiter = delimiter
        self.langs = langs
        self.delay = delay
        self.audio_files = []
        self.tmp_dir = tmp_dir

        if not os.path.exists(tmp_dir):
            os.makedirs(self.tmp_dir)

    def convert_to_audio(self, text: str, lang: str, filename: str) -> None:
        """
        Преобразует текст в аудиофайл с заданным языком и сохраняет его.

        Args:
            text (str): Текст для преобразования в речь.
            lang (str): Языковой код для преобразования, например, 'en'.
            filename (str): Путь для сохранения аудиофайла.

        Returns:
            None
        """
        try:
            tts = gTTS(text, lang=lang)
            tts.save(filename)
        except Exception as e:
            print(f"Ошибка при преобразовании текста '{text}' в аудио: {e}")

    def create_combined_audio(self, audio1_path: str, audio2_path: str, output_path: str) -> None:
        """
        Объединяет два аудиофайла в один общий аудиофайл.

        Args:
            audio1_path (str): Путь к первому аудиофайлу.
            audio2_path (str): Путь к второму аудиофайлу.
            output_path (str): Путь для сохранения объединенного аудиофайла.

        Returns:
            None
        """
        try:
            os.system(f'ffmpeg -i {audio1_path} -i {audio2_path} -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[outa]" -map "[outa]" {output_path}')
        except Exception as e:
            print(f"Ошибка при создании объединенного аудио: {e}")

    def combine_audio_files(self) -> None:
        """
        Объединяет все аудиофайлы из списка в один общий аудиофайл с заданными задержками.

        Returns:
            None
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
        Удаляет временные аудиофайлы и временную директорию.

        Returns:
            None
        """
        try:
            shutil.rmtree(self.tmp_dir)
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")

    def process_translations(self) -> None:
        """
        Обрабатывает переводы, создает аудиофайлы, объединяет их и удаляет временные файлы.

        Returns:
            None
        """
        for idx, translation in enumerate(self.translations, start=1):
            words = translation.split(self.delimiter)
            if len(words) != 2:
                print(f"Неверный формат перевода для записи {idx}: {translation}. Пропуск...")
                continue

            word1, word2 = words

            combined_output_path = os.path.join(self.tmp_dir, f'{word1.replace(" ", "_")}.mp3')

            # Проверяем, существует ли файл по указанному пути
            if os.path.isfile(combined_output_path):
                print(f"Файл {combined_output_path} уже существует. Пропуск...")
            else:
                audio1_path = os.path.join(self.tmp_dir, 'temp_1.mp3')
                audio2_path = os.path.join(self.tmp_dir, 'temp_2.mp3')

                lang1, lang2 = self.langs.split(self.delimiter)

                self.convert_to_audio(word1, lang1, audio1_path)
                self.convert_to_audio(word2, lang2, audio2_path)

                self.create_combined_audio(audio1_path, audio2_path, combined_output_path)

                # Удаляем временные аудиофайлы после объединения
                os.remove(audio1_path)
                os.remove(audio2_path)

            self.audio_files.append(combined_output_path)
