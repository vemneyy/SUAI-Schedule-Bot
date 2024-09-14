# keyboards.py

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Функция для создания кнопок выбора группы с кнопкой "Назад"
def get_group_buttons(groups, course_id):
    buttons = []
    for i in range(0, len(groups), 3):
        buttons.append([types.InlineKeyboardButton(
            text=f"C{group_id}", callback_data=f"select_group_{group_id}"
        ) for group_id in groups[i:i + 3]])

    # Добавляем кнопку "Назад"
    buttons.append([types.InlineKeyboardButton(text="Назад", callback_data=f"back_to_course")])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Функция для создания обычной клавиатуры с кнопками "Сегодня" и "Неделя"
def get_today_week_keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="На сегодня"),
                types.KeyboardButton(text="На завтра")
            ],
            [
                types.KeyboardButton(text="На неделю")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard


# Клавиатура для подтверждения намерения смены группы
def get_confirm_change_keyboard():
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Да", callback_data="confirm_change")],
            [types.InlineKeyboardButton(text="Нет", callback_data="cancel_change")]
        ]
    )
    return keyboard


# Функция для создания кнопок выбора курса
def get_course_setter():
    buttons = [
        [
            types.InlineKeyboardButton(text="1 курс", callback_data="set_course_1"),
            types.InlineKeyboardButton(text="2 курс", callback_data="set_course_2")
        ],
        [
            types.InlineKeyboardButton(text="3 курс", callback_data="set_course_3"),
            types.InlineKeyboardButton(text="4 курс", callback_data="set_course_4")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


# Функция для создания inline-кнопки смены недели
def get_week_switch_keyboard(current_week_kind):
    new_week_kind = "odd" if current_week_kind == "even" else "even"
    button_text = "Переключить на Числитель" if current_week_kind == "even" else "Переключить на Знаменатель"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_text, callback_data=f"switch_week_{new_week_kind}")]
        ]
    )
    return keyboard
