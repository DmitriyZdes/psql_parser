import requests

def get_company(company):
    """Получает название компании по API с hh.ru"""

    url = "https://api.hh.ru/employers"
    params = {"text": company}
    response = requests.get(url, params=params)
    value = response.json()
    return {
        "name": value["items"][0]["name"],
        "open_vacancies": value["items"][0]["open_vacancies"],
        "url_vacancies": value["items"][0]["vacancies_url"]
    }

def get_vacancies(url):
    """Получает список вакансий компании по url"""

    response = requests.get(url)
    raw_vacancies = response.json().get("items")
    vacancies = []
    if raw_vacancies:
        for vacancy in raw_vacancies:
            vacancies.append(
                {
                    "name": vacancy["name"],
                    "salary": vacancy["salary"]["from"] if vacancy["salary"] else 0,
                    "url": vacancy["alternate_url"]
                }
            )
    return vacancies
