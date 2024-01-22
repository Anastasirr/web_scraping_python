import requests
import json
from bs4 import BeautifulSoup
import fake_headers


def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='microsoftedge')
    return headers_gen.generate()


url = 'https://spb.hh.ru/search/vacancy'
params = {
    'area': (1, 2),
    'text': 'python django flask',
}

main_response = requests.get(url, params=params, headers=gen_headers()).text
main_soup = BeautifulSoup(main_response, 'lxml')

vacancies = main_soup.find_all('div', class_='vacancy-serp-item__layout')

parsed_vacancies = []

for vacancy in vacancies:
    title = vacancy.find('span', class_='serp-item__title').text
    address = vacancy.find('div', {'data-qa': "vacancy-serp__vacancy-address"}).text
    city = address.split(',')[0].strip()
    company = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-employer"}).text.replace(u'\xa0', '')
    salary_el = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
    salary = salary_el.text.replace(u'\u202F', '') if salary_el else 'Не указано'

    link = vacancy.find('a', class_='bloko-link')['href']

    parsed_vacancies.append({
        'Vacancy': title,
        'Company': company,
        'Address': city,
        'Salary': salary,
        'link': link,
    })

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_vacancies, f, ensure_ascii=False, indent=4)

