import requests
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable


def calculates_the_number_vacancies_hh(language):
    vacancies_of_number = []
    information_about_vacancies = []
    page = 0
    while True:
        url = 'https://api.hh.ru/vacancies/'
        payload = {
            'text': language,
            'area': 1,
            'page': page,
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        page += 1
        information_about_vacancies.append(response.json())
        vacancies_of_number.append(response.json()['found'])
        if response.json()['pages'] <= page:
            break
    return vacancies_of_number, information_about_vacancies


def calculates_the_average_salaries_hh(information_about_vacancies):
    average_salaries = []
    for number, vacancy in enumerate(information_about_vacancies):
        for salary_information in vacancy['items']:
            if salary_information['salary'] is None or salary_information['salary']['currency'] != 'RUR':
                average_salaries.append(None)
            else:
                if salary_information['salary']['from'] and salary_information['salary']['to']:
                    salary = (salary_information['salary']['from'] + salary_information['salary']['to']) / 2
                elif salary_information['salary']['from']:
                    salary = salary_information['salary']['from'] * 1.2
                elif salary_information['salary']['to']:
                    salary = salary_information['salary']['to'] * 0.8
                else:
                    salary = None
                average_salaries.append(salary)
    return average_salaries


def calculates_the_number_vacancies_sj(language, super_job_secret_key):
    vacancies_of_number = []
    information_about_vacancies = []
    page = 0
    next_page = True
    while next_page:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            'X-Api-App-Id': super_job_secret_key,
        }
        params = {
            'town': 'Москва',
            'keyword': language,
            'page': page,
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        information_about_vacancies.append(response.json())
        vacancies_of_number.append(response.json()['total'])
        next_page_available = response.json()['more']
        next_page = next_page_available
        page += 1
    return vacancies_of_number, information_about_vacancies


def calculates_the_average_salaries_sj(information_about_vacancies):
    average_salaries = []
    for number, vacancy in enumerate(information_about_vacancies):
        for salary_information in vacancy['objects']:
            if salary_information['payment_from'] and salary_information['payment_to']:
                salary = (salary_information['payment_from'] + salary_information['payment_to']) / 2
            elif salary_information['payment_from']:
                salary = salary_information['payment_from'] * 1.2
            elif salary_information['payment_to']:
                salary = salary_information['payment_to'] * 0.8
            else:
                salary = None
            average_salaries.append(salary)
    return average_salaries


def calculation_of_processed_vacancies(average_salary):
    vacancies_processed = 0
    specified_salary = []
    jobs_with_salary = []
    statistical_average_salary = []
    for amount_of_money in average_salary:
        if amount_of_money is not None:
            specified_salary.append(amount_of_money)
            vacancies_processed += amount_of_money
    jobs_with_salary.append(len(specified_salary))
    average_salary_the_specialty = vacancies_processed / (len(specified_salary))
    statistical_average_salary.append(int(average_salary_the_specialty))
    return statistical_average_salary, jobs_with_salary


def main():
    load_dotenv()
    super_job_secret_key = os.getenv("SUPERJOB_TOKEN")
    programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'C']
    salary_table_sj = [
        ['SuperJob Moscow'],
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in programming_languages:
        vacancies_of_number, information_about_vacancies = calculates_the_number_vacancies_sj(language,
                                                                                              super_job_secret_key)
        average_salaries = calculates_the_average_salaries_sj(information_about_vacancies)
        statistical_average_salary, jobs_with_salary = calculation_of_processed_vacancies(average_salaries)
        salary_table_sj.append(
            [language, vacancies_of_number[0], jobs_with_salary[0], statistical_average_salary[0]]
        )
    table_superjob = AsciiTable(salary_table_sj)
    print(table_superjob.table)

    salary_table_hh = [
        ['HeadHunter Moscow'],
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in programming_languages:
        vacancies_of_number, information_about_vacancies = calculates_the_number_vacancies_hh(language)
        average_salaries = calculates_the_average_salaries_hh(information_about_vacancies)
        statistical_average_salary, jobs_with_salary = calculation_of_processed_vacancies(average_salaries)
        salary_table_hh.append(
            [language, vacancies_of_number[0], jobs_with_salary[0], statistical_average_salary[0]]
        )
    table_headhunter = AsciiTable(salary_table_hh)
    print(table_headhunter.table)


if __name__ == "__main__":
    main()
