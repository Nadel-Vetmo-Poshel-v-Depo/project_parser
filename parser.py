import aiohttp
import asyncio
from database import save_vacancies, clear_vacancies, create_table

API_URL = "https://api.hh.ru/vacancies"

async def fetch_vacancies(session, keyword, page=0, per_page=20):
    params = {
        "text": keyword,
        "area": 113,
        "page": page,
        "per_page": per_page
    }

    async with session.get(API_URL, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Ошибка запроса: {response.status}")
            return {"items": []}


async def collect_vacancies(keyword="Python"):
    print("DEBUG: начало парсинга...")  # для отладки
    create_table()
    clear_vacancies()

    async with aiohttp.ClientSession() as session:
        all_vacancies = []

        for page in range(1):  # можно увеличить, если нужно больше страниц
            data = await fetch_vacancies(session, keyword, page)
            vacancies = data.get("items", [])
            print(f"Страница {page + 1}: найдено {len(vacancies)} вакансий")

            for item in vacancies:
                # title
                try:
                    title = item['name']
                except KeyError:
                    title = 'Без названия'

                # company
                try:
                    company = item['employer']['name']
                except (KeyError, TypeError):
                    company = 'Не указано'

                # city
                try:
                    city = item['area']['name']
                except (KeyError, TypeError):
                    city = 'Не указано'

                # salary
                try:
                    salary = f"{item['salary']['from']} - {item['salary']['to']} {item['salary']['currency']}"
                except (KeyError, TypeError):
                    salary = 'Не указана'

                # url
                url = item.get('alternate_url', '')

                all_vacancies.append({
                    "title": title,
                    "company": company,
                    "city": city,
                    "salary": salary,
                    "url": url,
                })

        save_vacancies(all_vacancies)
        print(f"✅ Сохранено {len(all_vacancies)} вакансий")