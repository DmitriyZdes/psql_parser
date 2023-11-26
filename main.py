from parser import get_vacancies, get_company
from dbmanager import DBManager

def main():

# config для подключения к БД
    db_manager = DBManager()# создать объект класса DBManager
    db_manager.create_db()
    db_manager.create_tables("postgres", params)
    list_companies = ["Lamoda tech"]
    for company in list_companies:
        company_info = get_company(company)
        company_vacancies = get_vacancies(company_info["url_vacancies"])
        db_manager.save_data_to_db(company_info, company_vacancies)

    # распечатать каждый метод dbmanager из задания
