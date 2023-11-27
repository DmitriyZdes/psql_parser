from parser import get_vacancies, get_company
from dbmanager import DBManager
from config import config

def main():

# config для подключения к БД
    params = config()
    db_manager = DBManager()# создать объект класса DBManager
    db_manager.create_db("hh", params)
    db_manager.create_tables("hh", params)
    list_companies = ["Lamoda tech", "ВТБ", "Альфа-банк", "Пятерочка", "Перекресток", "МТС", "Мегафон", "Магнит", "Ростелеком", "Почта России"]
    for company in list_companies:
        company_info = get_company(company)
        company_vacancies = get_vacancies(company_info["url_vacancies"])
        db_manager.save_data_to_db(company_info, company_vacancies, "hh", params)

    while True:

        user_input = input(
            "Введите 1, чтобы получить список всех компаний и количество вакансий у каждой компании\n"
            "Введите 2, чтобы получить список всех вакансий с указанием названия компании, "
            "названия вакансии и зарплаты и ссылки на вакансию\n"
            "Введите 3, чтобы получить среднюю зарплату по вакансиям\n"
            "Введите 4, чтобы получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
            "Введите 5, чтобы получить список всех вакансий, в названии которых содержатся переданные в метод слова\n"
            "Введите Стоп, чтобы завершить работу\n"
        )

        if user_input == "Стоп":
            break
        elif user_input == '1':
            print(db_manager.get_companies_and_vacancies_count())
            print()
        elif user_input == '2':
            print(db_manager.get_all_vacancies())
            print()
        elif user_input == '3':
            print(db_manager.get_avg_salary())
            print()
        elif user_input == '4':
            print(db_manager.get_vacancies_with_higher_salary())
            print()
        elif user_input == '5':
            keyword = input('Введите ключевое слово: ')
            print(db_manager.get_vacancies_with_keyword(keyword))
            print()
        else:
            print('Неправильный запрос')
    db_manager.close_connection()

main()

