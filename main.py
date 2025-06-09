import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Инициализируем переводчик
translator = Translator()

# Функция для получения случайного английского слова и его значения
def get_english_words():
    url = "https://randomword.com"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip()
        word_definition = soup.find("div", id="random_word_definition").text.strip()
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return None

# Функция для перевода текста на русский
def translate_text(text):
    try:
        translation = translator.translate(text, src='en', dest='ru')
        return translation.text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text  # Возвращаем оригинальный текст, если не удалось перевести

# Основная функция игры
def word_game():
    print("Добро пожаловать в игру!")
    while True:
        words = get_english_words()
        if not words:
            break

        english_word = words["english_word"]
        word_definition = words["word_definition"]

        # Переводим слово и его описание на русский
        russian_word = translate_text(english_word)
        russian_definition = translate_text(word_definition)

        print(f"\nЗначение слова: {russian_definition}")
        user_answer = input("Какое это слово? ").strip().lower()

        if user_answer == english_word.lower():
            print("Правильно! Молодец!")
        else:
            print(f"Неверно. Правильный ответ: {english_word} ({russian_word})")

        play_again = input("\nХотите сыграть ещё раз? (y/n): ").strip().lower()
        if play_again != "y":
            print("Спасибо за игру! До новых встреч!")
            break

# Запуск игры
word_game()



