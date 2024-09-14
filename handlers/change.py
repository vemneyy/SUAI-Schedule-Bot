# handlers/change.py

from aiogram import types
from aiogram.filters.command import Command
from aiogram import F

from loader import dp
from keyboards import get_confirm_change_keyboard, get_today_week_keyboard, get_course_setter

@dp.message(Command("change"))
async def cmd_change(message: types.Message):
    await message.answer("Вы уверены, что хотите сменить группу?", reply_markup=get_confirm_change_keyboard())

@dp.callback_query(F.data == "confirm_change")
async def callback_confirm_change(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выбери свой курс!", reply_markup=get_course_setter())
    await callback.answer()

@dp.callback_query(F.data == "cancel_change")
async def callback_cancel_change(callback: types.CallbackQuery):
    from database import pool
    async with pool.acquire() as conn:
        user_data = await conn.fetchrow(
            "SELECT group_id FROM public.users WHERE id = $1", callback.from_user.id
        )

        if user_data and user_data['group_id']:
            group_id = user_data['group_id']
            await callback.message.answer(f"Текущая выбранная группа: C{group_id}\n\n"
                                          "Основные команды бота:\n"
                                          "/week - Показать расписание на неделю\n"
                                          "/today - Показать расписание на сегодня\n"
                                          "/tommorow - Показать на завтра\n"
                                          "/change - Изменить группу\n"
                                          "/calls - Вывести расписание звонков\n"
                                          "/list - вывести список команд",
                                          reply_markup=get_today_week_keyboard())
        else:
            await callback.message.answer("Отмена смены группы. Группа не выбрана.",
                                          reply_markup=types.ReplyKeyboardRemove())

        await callback.message.delete()
        await callback.answer()
