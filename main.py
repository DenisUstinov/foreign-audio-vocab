from foreign_audio_vocab.text_to_voice_converter import TextToVoiceConverter


def read_file_lines(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


if __name__ == "__main__":
    # Замените 'translations.txt' на путь к вашему файлу с переводами
    input_file = 'translations.txt'

    # Считываем переводы из файла
    translations = read_file_lines(input_file)

    # Параметры для создания экземпляра TextToVoiceConverter
    delimiter = ':'
    langs = 'en:ru'
    delay = 2

    # Создание экземпляра класса TextToVoiceConverter с заданными параметрами и считанными переводами
    converter = TextToVoiceConverter(translations, delimiter, langs, delay)

    try:
        converter.process_translations()  # Создание промежуточных аудиофайлов
        converter.combine_audio_files()  # Создание конечного аудио файла
        converter.remove_old_audio_files()  # Удаление временных файлов
        print("Обработка завершена.")
    except Exception as e:
        print(f"Произошла ошибка при обработке: {e}")
