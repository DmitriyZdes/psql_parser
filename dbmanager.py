from config import config
import psycopg2

class DBManager:

    def database_connect(self):

        db_params = config()
        return db_params

    def create_db(self, db_name, params):

        connection = psycopg2.connect(dbname="postgres", **params)
        connection.autocommit = True
        cursor = connection.cursor()
        try:
            cursor.execute(f"DROP DATABASE {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name}")
        except psycopg2.ProgrammingError:
            pass
        cursor.close()
        connection.close()

    def create_tables(self, db_name, params):

        conn = psycopg2.connect(dbname=db_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                   CREATE TABLE companies (
                       company_name VARCHAR(255),
                       open_vacancies VARCHAR(255) NOT NULL,
                       url_vacancies TEXT,
               """)

        with conn.cursor() as cur:
            cur.execute("""
                   CREATE TABLE vacancies (
                       vacancy_name VARCHAR(255),
                       salary INT,
                       company_name VARCHAR(255) REFERENCES companies(company_name),
                       vacancy_url TEXT
               """)

        conn.commit()
        conn.close()

    def save_data_to_db(self, companies, vacancies):

        conn = psycopg2.connect(dbname=db_name, **params)

        with conn.cursor() as cur:
            for company in companies:
                cur.execute(
                    """
                    INSERT INTO companies (company_name, open_vacancies, url_vacancies)
                    VALUES (%s, %s, %s)
                    """,
                    (company['name'], company['open_vacancies'], company['url_vacancies']))

                for vacancy in vacancies:
                    cur.execute(
                        """
                        INSERT INTO vacancies (vacancy_name, salary, company_name, vacancy_url)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (vacancy["name"], vacancy['salary'], vacancy['company_name'], vacancy["url"]))

        conn.commit()
        conn.close()