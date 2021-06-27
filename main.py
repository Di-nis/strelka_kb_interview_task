import re
import time
import csv
from selenium import webdriver
from datetime import datetime, date


driver = webdriver.Chrome(executable_path=".\\chromedriver.exe")


def get_page():
    driver.get("https://strelkamag.com/ru?format=news")


def click_on_the_button():
    driver.find_element_by_xpath("//span[@class='css-0 euxw5wz0']").click()


def close_browser():
    driver.close()
    driver.quit()


def find_news_header_with_city(data_news_header):

    pattern = r'.*Москв.*|.*Ижевск.*|.*Барселон.*'

    match = re.match(pattern, data_news_header)
    if match:
        return True
    return False


def create_date_from_parse(text):
    pattern = r'\d{2}\.\d{2}'
    match_string = re.match(pattern, str(text))

    date_from_parse = match_string.group(0)
    current_year = datetime.now().year

    lst_date = date_from_parse.split('.')
    date_to_csv = date(current_year, int(lst_date[1]), int(lst_date[0]))
    return date_to_csv


def find_data_news_header():

    data = {
        'title': '',
        'date': '',
        'url': ''
        }

    news = driver.find_elements_by_xpath(
        '//div[@class="c-grid__cell__item css-1jw941z e1f3t7p20"]')

    for one_news in news:
        title = one_news.find_element_by_xpath(
            './/h3[@class="css-1w27zk4 ejnprjw0"]'
        ).get_attribute('textContent')
        data['title'] = title

        if find_news_header_with_city(title):
            date_news = one_news.find_element_by_xpath(
                './/p[@class="css-o10g35 ejnprjw0"]'
            ).get_attribute('textContent')
            date = create_date_from_parse(date_news)
            data['date'] = date

            url = one_news.find_element_by_xpath(
                './/a[@class="css-1e2w7h3 e1q4zbhe0"]'
            ).get_attribute('href')
            data['url'] = url

            yield data


def write_csv(data):
    with open('parse_strelka_mag.csv',
              'a', encoding='utf-8',
              newline='') as file:
        fieldnames = ['ID', 'title', 'date', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if data['ID'] == 1:
            writer.writeheader()
        writer.writerow(data)


def main():
    id = 0
    count = 0
    lst_title = []

    get_page()
    while count < 50:
        gen = iter(find_data_news_header())
        while True:
            if count == 50:
                break
            try:
                data = next(gen)
                count += 1
                if data['title'] not in lst_title:
                    id += 1
                    data['ID'] = id
                    lst_title.append(data['title'])
                    write_csv(data)

            except StopIteration:
                break

        click_on_the_button()
        time.sleep(2)

    close_browser()


if __name__ == '__main__':
    main()
