import requests

def get_company(company):

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

    response = requests.get(url)
    raw_vacancies = response.json().get("items")
    vacancies = []
    if raw_vacancies:
        for vacancy in raw_vacancies:
            vacancies.append(
                {
                    "name": vacancy["name"],
                    "salary": vacancy["salary"]["from"] if vacancy["salary"] else 0,
                    "url": vacancy["alternate_url"],
                    "company_name": vacancy["employer"]["name"]
                }
            )
    return vacancies

print(get_vacancies("https://api.hh.ru/vacancies?employer_id=9418714"))