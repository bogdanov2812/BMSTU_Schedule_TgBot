
import psycopg2
from psycopg2 import sql
import os

import re

keyboard_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']
db_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']

host = os.environ["HOST"]
user = os.environ["USER"]
password = os.environ["PASSWORD"]
dbname = os.environ["DATABASE"]


def reform_data(week, day):
    if week == 'Числитель' or re.search('числитель', week):
        week = 'chislitel'
    else:
        week = 'znamenatel'

    for i in range(0, len(db_week)):
        if day == keyboard_week[i]:
            day = db_week[i]

    return week, day


def insert_group(group, url):
    connection = psycopg2.connect(host=host, user=user, password=password, dbname=dbname, client_encoding='utf8')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO groups (name, url) VALUES (%s,%s)", (group, url))

    cursor.execute("SELECT id FROM groups WHERE name =%s", (group,))
    group_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO chislitel (group_id) VALUES (%s)", (group_id,))
    cursor.execute("INSERT INTO znamenatel (group_id) VALUES (%s)", (group_id,))
    connection.commit()
    connection.close()


def search_group(group):
    connection = psycopg2.connect(host=host, user=user, password=password, dbname=dbname, client_encoding='utf8')
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT url FROM groups WHERE name = %s', (group,))
        url = cursor.fetchone()[0]
    except Exception:
        url = None

    connection.close()
    return url


def search_schedule(group, week, day):
    week, day = reform_data(week, day)

    connection = psycopg2.connect(host=host, user=user, password=password, dbname=dbname, client_encoding='utf8')
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM groups WHERE name =%s", (group,))
    group_id = cursor.fetchone()[0]

    try:
        cursor.execute(sql.SQL('SELECT {} FROM {} WHERE group_id = %s').format(sql.Identifier(day), sql.Identifier(week)), (group_id,))
        raspisanie = cursor.fetchone()[0]
        print(raspisanie)
    except Exception:
        raspisanie = None

    return raspisanie


def insert_schedule(group, week, day, schedule):
    week, day = reform_data(week, day)

    connection = psycopg2.connect(host=host, user=user, password=password, dbname=dbname, client_encoding='utf8')
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM groups WHERE name =%s", (group,))
    group_id = cursor.fetchone()[0]

    cursor.execute(sql.SQL("UPDATE {} SET {} = %s WHERE group_id = %s").format(sql.Identifier(week), sql.Identifier(day)), (schedule, group_id))
    connection.commit()

    connection.close()



