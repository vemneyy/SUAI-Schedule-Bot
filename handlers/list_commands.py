# handlers/list_commands.py

from aiogram import types
from aiogram.filters.command import Command

from loader import dp


@dp.message(Command("help"))
async def cmd_list(message: types.Message):
    await message.answer(
        "Список команд бота:\n"
        "/week - Показать расписание на неделю\n"
        "/today - Показать расписание на сегодня\n"
        "/tommorow - Показать на завтра\n"
        "/change - Изменить группу\n"
        "/calls - Вывести расписание звонков\n"
        "/help - вывести список команд"
    )
