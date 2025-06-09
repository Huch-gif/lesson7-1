from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def wait_for_user():
    input("Нажмите Enter, чтобы продолжить...")

def show_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for p in paragraphs:
        print(p.text)
        input("Нажмите Enter, чтобы продолжить чтение (или Ctrl+C для остановки).")

def list_related_links(browser):
    links = []
    link_elements = browser.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href and not(contains(@href, ':'))]")

    print("\nСвязанные статьи:")
    for i, link in enumerate(link_elements[:10], 1):  # берем первые 10 ссылок
        title = link.get_attribute("textContent")
        href = link.get_attribute("href")
        print(f"{i}. {title}")
        links.append((title, href))
    return links

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Убираем окно браузера, если нужно
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        while True:
            query = input("\nВведите ваш запрос (или 'выход' для завершения): ").strip()
            if query.lower() == 'выход':
                break

            search_url = f"https://ru.wikipedia.org/wiki/{query.replace('  ', '_')}"
            browser.get(search_url)
            time.sleep(2)  # Ждём загрузки страницы

            print(f"\nВы находитесь на странице: {browser.title}")

            while True:
                print("\nВыберите действие:")
                print("1. Показать параграфы статьи")
                print("2. Перейти к связанным страницам")
                print("3. Вернуться к новому поиску")
                print("4. Выйти из программы")

                choice = input("Ваш выбор: ").strip()

                if choice == "1":
                    show_paragraphs(browser)

                elif choice == "2":
                    related_links = list_related_links(browser)
                    if not related_links:
                        print("Связанных статей не найдено.")
                        continue

                    sub_choice = input("Введите номер статьи для перехода (или Enter, чтобы остаться): ")
                    if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(related_links):
                        title, url = related_links[int(sub_choice) - 1]
                        browser.get(url)
                        time.sleep(2)
                        print(f"\nВы перешли на страницу: {browser.title}")
                        # Теперь можно снова читать или выбирать новые ссылки
                    else:
                        print("Неверный выбор.")

                elif choice == "3":
                    break  # Возврат к новому поиску

                elif choice == "4":
                    print("Завершение работы...")
                    browser.quit()
                    return

                else:
                    print("Неверный ввод. Попробуйте снова.")

    finally:
        browser.quit()

if __name__ == "__main__":
    main()



