from telebot import types

keyboard_week = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']


def week_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    for i in range(0, 6, 2):
        keyboard.add(types.InlineKeyboardButton(text=keyboard_week[i], callback_data=keyboard_week[i]), types.InlineKeyboardButton(text=keyboard_week[i+1], callback_data=keyboard_week[i+1]))

    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='week_back'))
    return keyboard

def group_keyboard(current_week):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton('ЧС', callback_data='Числитель')
    button2 = types.InlineKeyboardButton('ЗН', callback_data='Знаменатель')
    button3 = types.InlineKeyboardButton('Текущая неделя', callback_data=current_week)

    keyboard.add(button1, button2, button3)

    return keyboard

def day_keyboard(current_week):
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton('Назад', callback_data=current_week)

    keyboard.add(button1)

    return keyboard

def groups_keyboard(group):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for i in range(0, len(group)):
        keyboard.add(types.KeyboardButton(group[i]))

    return keyboard

