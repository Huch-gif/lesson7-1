





import requests



def get_vacancies(text="python разработчик", pages=2):

  """

  Получает вакансии с hh.ru по текстовому запросу.

  """

  all_descriptions = []



  for page in range(pages):

    response = requests.get("https://api.hh.ru/vacancies", params={

      "text": text,

      "area": 1, # Москва

      "page": page,

      "per_page": 20

    })



    data = response.json()

    for vacancy in data['items']:

      vacancy_detail = requests.get(vacancy['url']).json()

      desc = vacancy_detail.get('description', '')

      all_descriptions.append(desc)



  return all_descriptions



import spacy

from collections import Counter



nlp = spacy.load("ru_core_news_md")



def extract_keywords(texts):

  """

  Извлекает ключевые существительные и глаголы из текста.

  """

  keywords = []



  for text in texts:

    doc = nlp(text)

    for token in doc:

      if token.pos_ in ["NOUN", "VERB"] and not token.is_stop:

        keywords.append(token.lemma_.lower())



  return Counter(keywords).most_common(50)



def compare_with_resume(resume_text, job_keywords):

  resume_doc = nlp(resume_text.lower())

  resume_tokens = {token.lemma_ for token in resume_doc if token.pos_ in ['NOUN', 'VERB']}



  present = []

  missing = []



  for word, freq in job_keywords:

    if word in resume_tokens:

      present.append((word, freq))

    else:

      missing.append((word, freq))



  return present, missing



if __name__ == "__main__":

  query = input("Введите вакансию для анализа (например, python разработчик): ")

  print("📥 Получение вакансий...")

  texts = get_vacancies(query, pages=2)



  print("🔍 Извлечение популярных навыков...")

  top_skills = extract_keywords(texts)



  print("📄 Вставьте текст вашего резюме:")

  resume = ""

  while True:

    line = input()

    if not line.strip():

      break

    resume += line + "\n"



  present, missing = compare_with_resume(resume, top_skills)



  print("\n✅ Навыки, которые у вас уже есть:")

  for skill, freq in present:

    print(f"{skill} (встречается в {freq} вакансиях)")



  print("\n❌ Навыки, которых не хватает:")

  for skill, freq in missing:

    print(f"{skill} (встречается в {freq} вакансиях)")