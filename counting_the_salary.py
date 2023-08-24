import requests
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable


def calculating_the_number_vacancies_hh(language):
    list_the_number_of_vacancies = []
    list_of_vacancies = []
    page = 0
    pages_number = 3
    while page < pages_number:
        url = 'https://api.hh.ru/vacancies/'
        payload = {
            "text": f'{language}',
            "area": 1,
            "page": f'{page}',
        }
        response = requests.get(url, params=payload)
        response.raise_for_status()
        information_about_vacancies = response.json()
        page += 1
        list_of_vacancies.append(information_about_vacancies)
        number_of_vacancies = information_about_vacancies['found']
        list_the_number_of_vacancies.append(number_of_vacancies)
    return list_the_number_of_vacancies, list_of_vacancies


def predict_rub_salary_for_hh(list_of_vacancies):
    average_salary = []
    for number in range(len(list_of_vacancies)):
        for vacancy in list_of_vacancies[number]['items']:
            if vacancy['salary'] is None or vacancy['salary']['currency'] != 'RUR':
                average_salary.append(None)
            else:
                if vacancy['salary']['from'] and vacancy['salary']['to']:
                    salary = (vacancy['salary']['from'] + vacancy['salary']['to']) / 2
                elif vacancy['salary']['from']:
                    salary = vacancy['salary']['from'] * 1.2
                elif vacancy['salary']['to']:
                    salary = vacancy['salary']['to'] * 0.8
                else:
                    salary = None
                average_salary.append(salary)
    return average_salary


def calculating_the_number_vacancies_sj(language):
    load_dotenv()
    super_job_secret_key = os.getenv("SECRET_KEY")
    list_the_number_of_vacancies = []
    list_of_vacancies = []
    page = 0
    pages_number = 3
    while page < pages_number:
        url = 'https://api.superjob.ru/2.0/vacancies/'
        headers = {
            "X-Api-App-Id": super_job_secret_key,
        }
        params = {
            'town': "Москва",
            'keyword': f'{language}',
            "page": f'{page}',
        }
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        information_about_vacancies = response.json()
        page += 1
        list_of_vacancies.append(information_about_vacancies)
        number_of_vacancies = information_about_vacancies['total']
        list_the_number_of_vacancies.append(number_of_vacancies)
    return list_the_number_of_vacancies, list_of_vacancies


def predict_rub_salary_for_sj(list_of_vacancies):
    average_salary = []
    for number in range(len(list_of_vacancies)):
        for vacancy in list_of_vacancies[number]['objects']:
            if vacancy['payment_from'] and vacancy['payment_to']:
                salary = (vacancy['payment_from'] + vacancy['payment_to']) / 2
            elif vacancy['payment_from']:
                salary = vacancy['payment_from'] * 1.2
            elif vacancy['payment_to']:
                salary = vacancy['payment_to'] * 0.8
            else:
                salary = None
            average_salary.append(salary)
    return average_salary


def computation_work_for_vacancies(average_salary):
    vacancies_processed = 0
    specified_salary = []
    list_jobs_with_salary = []
    statistical_average_salary = []
    for amount_of_money in average_salary:
        if amount_of_money is not None:
            specified_salary.append(amount_of_money)
            vacancies_processed += amount_of_money
    jobs_with_salary = (len(specified_salary))
    list_jobs_with_salary.append(jobs_with_salary)
    average_salary_the_specialty = vacancies_processed / jobs_with_salary
    statistical_average_salary.append(int(average_salary_the_specialty))
    return statistical_average_salary, list_jobs_with_salary


def main():
    programming_languages = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'CSS', 'C#', 'C']
    salary_table_sj = [
        ['SuperJob Moscow'],
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in programming_languages:
        list_the_number_of_vacancies, list_of_vacancies = calculating_the_number_vacancies_sj(language)
        average_salary = predict_rub_salary_for_sj(list_of_vacancies)
        statistical_average_salary, list_jobs_with_salary = computation_work_for_vacancies(average_salary)
        salary_table_sj.append(
            [language, list_the_number_of_vacancies[0], list_jobs_with_salary[0], statistical_average_salary[0]]
        )
    table_superjob = AsciiTable(salary_table_sj)
    print(table_superjob.table)

    salary_table_hh = [
        ['HeadHunter Moscow'],
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language in programming_languages:
        list_the_number_of_vacancies, list_of_vacancies = calculating_the_number_vacancies_hh(language)
        average_salary = predict_rub_salary_for_hh(list_of_vacancies)
        statistical_average_salary, list_jobs_with_salary = computation_work_for_vacancies(average_salary)
        salary_table_hh.append(
            [language, list_the_number_of_vacancies[0], list_jobs_with_salary[0], statistical_average_salary[0]]
        )
    table_headhunter = AsciiTable(salary_table_hh)
    print(table_headhunter.table)


if __name__ == "__main__":
    main()
