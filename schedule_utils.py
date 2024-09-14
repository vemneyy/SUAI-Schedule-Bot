# schedule_utils.py

from database import fetch_teachers_for_schedule, fetch_schedule
from utils import DAY_OF_WEEK_MAPPING, is_odd_week

async def generate_day_schedule(schedule_data):
    response = ""
    lessons = {}

    # Сгруппируем данные по номеру пары и предмету
    for record in schedule_data:
        lesson_number = record['lesson_number']
        subject = record['subject']
        start_time = record['start_time'].strftime('%H:%M')
        end_time = record['end_time'].strftime('%H:%M')
        classroom = record['classroom']

        # Получаем преподавателей для данного расписания
        teachers = await fetch_teachers_for_schedule(record['id'])
        teacher_info = ", ".join(teachers)

        key = (lesson_number, subject, start_time, end_time)

        if key not in lessons:
            lessons[key] = {'classrooms': [], 'teachers': []}

        lessons[key]['classrooms'].append(classroom)
        lessons[key]['teachers'].append(teacher_info)

    # Формируем финальный вывод
    for (lesson_number, subject, start_time, end_time), details in lessons.items():
        classrooms = set(details['classrooms'])
        teachers = ", ".join(set(details['teachers']))

        classrooms_str = ", ".join(
            [f"Спортивный зал" if room == "Спортивный зал" else f"ауд.{room}" for room in classrooms]
        )

        response += f"{lesson_number} пара ({start_time} - {end_time}):\n"
        response += f"{subject}\n{classrooms_str}, {teachers}\n\n"

    return response

async def generate_week_schedule(user_id, week_kind):
    week_schedule = {}

    for day_offset in range(7):
        schedule_data, today = await fetch_schedule(user_id, day_offset=day_offset, week_kind=week_kind)
        weekday_name_en = today.strftime('%A')
        weekday_name = DAY_OF_WEEK_MAPPING.get(weekday_name_en)

        if not schedule_data:
            week_schedule[weekday_name] = f"<b>{weekday_name}</b>\nВыходной\n\n"
        else:
            day_schedule = await generate_day_schedule(schedule_data)
            week_schedule[weekday_name] = f"<b>{weekday_name}</b>\n\n{day_schedule}"

    response = f"<b>Расписание на неделю:</b>\n"
    response += f"Неделя: {'Числитель' if week_kind == 'odd' else 'Знаменатель'}\n\n"

    for day in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]:
        response += week_schedule.get(day, f"<b>{day}</b>\nВыходной\n\n")

    return response
