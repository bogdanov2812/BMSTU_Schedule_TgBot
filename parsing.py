from urllib.request import urlopen
from bs4 import BeautifulSoup


import re


# Получаем код html страницы по заданному url
def get_html(url):
    response = urlopen(url)
    return response.read()

# Парсим страницу с группами и ищем совпадение с тем, что ввел пользователь
def parse_groups(html, group):
    soup = BeautifulSoup(html, features="html.parser")
    table_all = soup.find_all('a',  class_='btn')  # ищем все теги <а> в которых как раз и находятся названия групп
    groups = []

    for table in table_all:
        text = table.text.strip()
        if text == group:
            link = table.get('href')  # достаем данные из атрибута "href" в котором как раз и хранится ссылка на страницу с нужной группой
            return link
        elif re.findall(group, text):
            groups.append(text)
    return groups



# Парсим страницу группы для определения текущей недели
def parse_week(html):
    soup = BeautifulSoup(html, features="html.parser")
    name_week = soup.find('i')  # ищем первый тег <i> в котором находится название текущей недели (например: 16 неделя, знаменатель)
    return name_week.text


def list_to_string(list1):
    string1 = ''
    for i in range(0, len(list1)):
        list1[i] = " ".join(list1[i].values())
        string1 = string1 + list1[i] + '\n'
    return string1


def reform_week(week):
    if week == 'Числитель' or re.search('числитель', week):
        return 'chislitel'
    else:
        return 'znamenatel'


def parse_day(html, day, week):
    raspisanie = []  # список словарей в который мы будем записывать расписание на день (например: ({time: 10.30 - 12.00, predmet: Английский},{time: 12.00 - 13.35, predmet: Физкультура}))
    soup = BeautifulSoup(html, features="html.parser")
    table_all = soup.find_all('div', class_="col-md-6 hidden-xs")  # ищем теги <div> у которых class="col-md-6 hidden-xs", в них содержится вся информация на конкретный день
    week = reform_week(week)
    for table in table_all:

        if table.find_all('td')[0].text == day:  # ищем нужный нам день
            table_day = table.find_all('td')[4:]  # ищем внутренние теги <td> интересующего нам дня, в них и содержится распсание
            i = 0
            while i < len(table_day):
                if (table_day[i].text == '') \
                        or (week == 'chislitel' and str(table_day[i])[:22] == '<td class="text-info">') \
                        or (week == 'znamenatel' and str(table_day[i])[:25] == '<td class="text-success">'):

                    del table_day[i]
                else:
                    i += 1
            print(table_day)
            for i in range(0, len(table_day)-1):
                print(table_day[i].text)
                if (table_day[i].text[:1] == '0' or table_day[i].text[:1] == '1') and (table_day[i+1].text[:1] != '0' and table_day[i+1].text[:1] != '1'):
                    raspisanie.append({
                        'time': table_day[i].text,
                        'predmet': table_day[i + 1].text
                    })

            result = list_to_string(raspisanie)

            return result
