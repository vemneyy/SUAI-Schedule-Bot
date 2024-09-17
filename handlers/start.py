# handlers/start.py

from aiogram import types
from aiogram.filters.command import Command

from loader import dp
from keyboards import get_course_setter

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, выбери свой курс!", reply_markup=get_course_setter())
