import telebot
import os

from telebot.types import Message, CallbackQuery

from parsing import *
from keyboards import *
from bigdata import *

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: Message):
    bot.send_message(message.chat.id, 'Добро пожаловать! \n'
                                      'Этот бот умеет показывать расписание занятий в МГТУ им. Н.Э.Баумана \n'
                                      'Чтобы воспользоваться им, просто отправьте боту через сообщение нужную Вам группу а затем из всплывающего меню выберите нужную неделю и день \n'
                                      'Если у вас возникают какие-либо трудности с работой бота, просто выберите команду /help и ознакомьтесь с правилами управления ботом')


@bot.message_handler(commands=['help'])
def help_command(message: Message):
    bot.send_message(message.chat.id, 'Справка \n'
                                      '\n'
                                      'Для того чтобы начать поиск расписания введите в поле "Сообщение..." название группы \n'
                                      'ВАЖНО!!! Название группы обязательно должно состоять из двух частей - факультета и номера группы, которые должны быть '
                                      'разделены между собой пробелом, тире или нижним подчеркиванием, например так:\n'
                                      'ИУ5-23Б \n'
                                      'иУ5 23Б \n'
                                      'иу5_23Б \n'
                                      'Поиск не чувствителен к регистру \n'
                                      'Если вы забыли указать букву в конце, ничего страшного в этом нет, бот найдет все совпадения и предложит их на выбор, '
                                      'если таковые будут иметься \n'
                                      '\n'
                                      'Если Вы все сделали правильно, то под названием группы появиться меню, в котором можно будет выбрать неделю ("ЧС" - нечетная, "ЗН" - четная) \n'
                                      'Далее будет предложено выбрать день недели, также присутствует кнопка "Назад", чтобы вернуться к предыдущему пункту')



@bot.callback_query_handler(func=lambda call: True)
def week_schedule(call: CallbackQuery):

    group = call.message.reply_to_message.text
    group = re.sub(r"[ _]", '-', group).upper()

    if call.data == 'week_back':

        current_week = parse_week(get_html('https://lks.bmstu.ru' + search_group(group)))
        bot.edit_message_text('Выберите неделю', chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=group_keyboard(current_week))

    elif call.data == 'ПН' or call.data == 'ВТ' or call.data == 'СР' or call.data == 'ЧТ' or call.data == 'ПТ' or call.data == 'СБ':
        day = call.data
        week = call.message.text
        schedule = search_schedule(group, week, day)
        if schedule is None:
            url = search_group(group)
            schedule = parse_day(get_html('https://lks.bmstu.ru' + url), day, week)
            insert_schedule(group, week, day, schedule)

        bot.edit_message_text(week + '\n' + day + '\n' + schedule, call.message.chat.id, call.message.message_id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=day_keyboard(week))

    else:
        week = call.data
        bot.edit_message_text(week, chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=week_keyboard())


@bot.message_handler(func=lambda message: True)
def group_auth(message: Message):

    group = message.text

    group = re.sub(r"[ _]", '-', group).upper()

    db_group_url = search_group(group)
    if db_group_url is None:
        coincident = parse_groups(get_html('https://lks.bmstu.ru/schedule/list'), group)
        if isinstance(coincident, list):
            if len(coincident) != 0:
                groups = ''
                for i in range(0, len(coincident)):
                    groups = groups + coincident[i] + '\n'
                bot.send_message(message.chat.id, 'Возможно вы имели ввиду: \n' + groups, reply_markup=groups_keyboard(coincident))
                return
            else:
                bot.send_message(message.chat.id, 'Проврьте введенные данные и повторите попытку')
                return

        else:
            db_group_url = coincident
            insert_group(group, db_group_url)

    current_week = parse_week(get_html('https://lks.bmstu.ru'+db_group_url))
    bot.send_message(message.chat.id, 'Выберите неделю', reply_markup=group_keyboard(current_week),
                     reply_to_message_id=message.message_id)


bot.polling(none_stop=True, timeout=60)
