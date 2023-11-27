from config import config
import psycopg2

class DBManager:


    def create_db(self, db_name, params):
        """Метод создания базы данных"""

        connection = psycopg2.connect(dbname="postgres", **params)
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
        except psycopg2.ProgrammingError:
            pass
        cursor.close()
        connection.close()

    def create_tables(self, db_name, params):
        """Создание таблиц в БД о компаниях и их вакансиях"""

        conn = psycopg2.connect(dbname=db_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                   CREATE TABLE companies (
                       id_company SERIAL PRIMARY KEY,   
                       company_name VARCHAR(255),
                       open_vacancies VARCHAR(255) NOT NULL,
                       url_vacancies TEXT);
               """)


            cur.execute("""
                   CREATE TABLE vacancies (
                       id_vacancy SERIAL PRIMARY KEY,
                       company_id INT REFERENCES companies(id_company),
                       vacancy_name VARCHAR(255),
                       salary INT,
                       vacancy_url TEXT);
               """)

        conn.commit()
        conn.close()

    def save_data_to_db(self, company, vacancies, db_name, params):
        """Наполнение таблиц основными полями"""

        conn = psycopg2.connect(dbname=db_name, **params)

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO companies (company_name, open_vacancies, url_vacancies)
                VALUES (%s, %s, %s) RETURNING id_company
                """,
                (company['name'], company['open_vacancies'], company['url_vacancies']))

            company_id = cur.fetchone()
            for vacancy in vacancies:
                cur.execute(
                        """
                        INSERT INTO vacancies (company_id, vacancy_name, salary, vacancy_url)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (company_id, vacancy["name"], vacancy['salary'], vacancy["url"]))

        conn.commit()
        conn.close()

    def database_connect(self):

        db_params = config()
        with psycopg2.connect(dbname="hh", **db_params) as connection:
            return connection

    def close_connection(self):

        connection = self.database_connect()
        connection.close()

    def get_companies_and_vacancies_count(self):
        """Получает общее число компаний и вакансий"""

        cur = self.database_connect().cursor()
        cur.execute(
            """
            SELECT companies.company_name, COUNT(vacancies.vacancy_name) FROM companies
            INNER JOIN vacancies ON companies.id_company=vacancies.company_id
            GROUP BY companies.company_name""")
        data = cur.fetchall()
        return data

    def get_all_vacancies(self):
        """Получает информаццию о вакансии"""

        cur = self.database_connect().cursor()
        cur.execute(
            """
            SELECT vacancy_name, salary, vacancy_url FROM vacancies""")
        data = cur.fetchall()
        return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по списку вакансий"""

        cur = self.database_connect().cursor()
        cur.execute(
            """
            SELECT AVG(salary) FROM vacancies""")
        data = cur.fetchall()
        return data

    def get_vacancies_with_higher_salary(self):
        """Получает вакансии с наибольшей зарплатой"""

        cur = self.database_connect().cursor()
        cur.execute(
            """
            SELECT * FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies) """)
        data = cur.fetchall()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """Получает название вакансий по ключевому слову"""

        cur = self.database_connect().cursor()
        cur.execute(
            f"""
            SELECT * FROM vacancies
            WHERE vacancies.vacancy_name LIKE '%{keyword}%' """)
        data = cur.fetchall()
        return data
