# handlers/schedule.py

from aiogram import types
from aiogram.filters.command import Command
from aiogram import F
from datetime import timedelta

from loader import dp, bot
from utils import rate_limit, is_odd_week, DAY_OF_WEEK_MAPPING
from database import fetch_schedule
from schedule_utils import generate_day_schedule, generate_week_schedule
from keyboards import get_week_switch_keyboard

MAX_REQUESTS = 2
TIME_WINDOW = timedelta(seconds=1)


@dp.message(F.text == "На сегодня")
async def today_command(message: types.Message):
    await cmd_today(message)


@dp.message(F.text == "На завтра")
async def tomorrow_command(message: types.Message):
    await cmd_tommorow(message)


@dp.message(F.text == "На неделю")
async def week_command(message: types.Message):
    await cmd_week(message)


@dp.message(Command("today"))
@rate_limit(limit=MAX_REQUESTS, time_window=TIME_WINDOW)
async def cmd_today(message: types.Message):
    user_id = message.from_user.id
    schedule_data, today = await fetch_schedule(user_id)
    weekday_name_en = today.strftime('%A')
    weekday_name = DAY_OF_WEEK_MAPPING.get(weekday_name_en)

    if not schedule_data:
        await message.answer("Сегодня у вас нет занятий.")
        return

    response = f"<b>Расписание на сегодня ({today.strftime('%d.%m')}):</b>\n"
    response += f"Неделя: {'Числитель' if is_odd_week() == 'odd' else 'Знаменатель'}\n"
    response += f"День недели: {weekday_name}\n\n"
    response += await generate_day_schedule(schedule_data)

    await message.answer(response, parse_mode="html")


@dp.message(Command("tommorow"))
@rate_limit(limit=MAX_REQUESTS, time_window=TIME_WINDOW)
async def cmd_tommorow(message: types.Message):
    user_id = message.from_user.id
    schedule_data, tomorrow = await fetch_schedule(user_id, day_offset=1)
    weekday_name_en = tomorrow.strftime('%A')
    weekday_name = DAY_OF_WEEK_MAPPING.get(weekday_name_en)

    if not schedule_data:
        await message.answer("Завтра у вас нет занятий.")
        return

    response = f"<b>Расписание на завтра ({tomorrow.strftime('%d.%m')}):</b>\n"
    response += f"Неделя: {'Числитель' if is_odd_week() == 'odd' else 'Знаменатель'}\n"
    response += f"День недели: {weekday_name}\n\n"
    response += await generate_day_schedule(schedule_data)

    await message.answer(response, parse_mode="html")


@dp.message(Command("week"))
@rate_limit(limit=MAX_REQUESTS, time_window=TIME_WINDOW)
async def cmd_week(message: types.Message):
    user_id = message.from_user.id

    current_week_kind = is_odd_week()

    response = await generate_week_schedule(user_id, current_week_kind)

    await message.answer(response, parse_mode="html", reply_markup=get_week_switch_keyboard(current_week_kind))


@dp.callback_query(F.data.startswith("switch_week_"))
async def callback_switch_week(callback: types.CallbackQuery):
    new_week_kind = callback.data.split("_")[2]
    user_id = callback.from_user.id

    response = await generate_week_schedule(user_id, new_week_kind)

    await callback.message.edit_text(response, parse_mode="html", reply_markup=get_week_switch_keyboard(new_week_kind))
    await callback.answer()
