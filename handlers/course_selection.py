# handlers/course_selection.py

from aiogram import types
from aiogram import F
from aiogram.types import BotCommand, BotCommandScopeDefault

from loader import dp, bot
from keyboards import get_course_setter, get_group_buttons, get_today_week_keyboard
from database import fetch_groups_by_course, log_user_action


@dp.callback_query(F.data.startswith("set_course_"))
async def callbacks_course(callback: types.CallbackQuery):
    action = int(callback.data.split("_")[2])

    await log_user_action(callback.from_user, course_id=action)

    groups = await fetch_groups_by_course(action)

    await callback.message.delete()

    if groups:
        group_buttons = get_group_buttons(groups, action)
        await callback.message.answer("Выбери свою группу:", reply_markup=group_buttons)
    else:
        await callback.message.answer("Группы не найдены для этого курса.")

    await callback.answer()


@dp.callback_query(F.data.startswith("select_group_"))
async def callback_select_group(callback: types.CallbackQuery):
    group_id = int(callback.data.split("_")[2])
    await callback.message.delete()
    usercommands = [
        BotCommand(command="week", description="Расписание на неделю"),
        BotCommand(command="today", description="Расписание на сегодня"),
        BotCommand(command="tommorow", description="Расписание на завтра"),
        BotCommand(command="change", description="Сменить группу"),
        BotCommand(command="calls", description="Расписание звонков"),
        BotCommand(command="list", description="Вывести список команд")
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

    await log_user_action(callback.from_user, group_id=group_id)

    await callback.message.answer(f"Вы успешно выбрали группу C{group_id}.\n\n"
                                  "Основные команды бота:\n"
                                  "/week — Расписание на неделю\n"
                                  "/today — Расписание на сегодня\n"
                                  "/tommorow — Расписание на завтра\n"
                                  "/change — Сменить группу\n"
                                  "/calls — Расписание звонков\n"
                                  "/list — Вывести список команд",
                                  reply_markup=get_today_week_keyboard())


@dp.callback_query(F.data == "back_to_course")
async def callback_back_to_course(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выбери свой курс!", reply_markup=get_course_setter())
    await callback.answer()
