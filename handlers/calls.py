# handlers/calls.py

from aiogram import types
from aiogram.filters.command import Command

from loader import dp
from database import fetch_lesson_times

@dp.message(Command("calls"))
async def cmd_calls(message: types.Message):
    from database import pool
    async with pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT group_id FROM public.users WHERE id = $1", message.from_user.id)

        if not user_data or not user_data['group_id']:
            await message.answer("Группа не выбрана.")
            return

        group_id = user_data['group_id']

        group_data = await conn.fetchrow("SELECT unit FROM public.groups WHERE group_id = $1", group_id)
        if not group_data or not group_data['unit']:
            await message.answer("Не удалось найти информацию о корпусе для вашей группы.")
            return

        unit = group_data['unit']

        lesson_times = await fetch_lesson_times(unit)

        if lesson_times:
            timetable = f"<b>Расписание пар:</b>\n"
            for record in lesson_times:
                start_time = record['start_time'].strftime('%H:%M')
                end_time = record['end_time'].strftime('%H:%M')
                timetable += f"{record['lesson_number']} пара: {start_time}-{end_time}\n"

            await message.answer(timetable, parse_mode="html")
        else:
            await message.answer(f"Расписание звонков отсутствует для корпуса {unit}.")
