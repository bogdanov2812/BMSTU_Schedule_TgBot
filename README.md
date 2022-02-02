# Телеграмм-бот расписания МГТУ им. Н.Э.Баумана
### Что умеет этот бот:
+ Показ расписаня для любой группы в университете
+ Возможность выбора недели (числитель/знаменатель или текущая неделя)
+ Помощь с определением номера группы, если Вы вдруг забыли
### Команды бота:
+ /start - запуск бота
+ /help - инструкция по работе с ботом
### Использованные технологии:
+ API - pyTelegramBotAPI
+ Кэширование данных в БД с помощью PostgreSQL
+ HTML парсер - Beautiful soup
+ Deploy - Heroky

### Пример взаимодействия с ботом приведен на скриншотах ниже
#### Запуск бота при помощи команды /start
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/start.png)
#### Инструкции по работе с ботом /help
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/help.png)
#### Ввод группы и меню выбора недели
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/group_intro.png)
#### Меню выбора дня недели
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/group_chisl.png)
#### Выбор дня недели и вывод расписания
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/group_day.png)
#### Автоматический поиск похожих групп на основе введенных данных
![Alt text](https://github.com/bogdanov2812/Screenshots/blob/master/Telegram_Bots/BMSTU/group_search.png)
