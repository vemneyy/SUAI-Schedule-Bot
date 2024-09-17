# database.py

import asyncpg
from datetime import datetime
from utils import DAY_OF_WEEK_MAPPING, is_odd_week

pool = None


async def init_db_pool(config):
    global pool
    pool = await asyncpg.create_pool(**config)


async def fetch_groups_by_course(course_id):
    global pool
    async with pool.acquire() as conn:
        groups = await conn.fetch(
            "SELECT group_id FROM public.groups WHERE course_id = $1 ORDER BY group_id ASC", int(course_id)
        )
        return [record['group_id'] for record in groups]


async def fetch_schedule(user_id, day_offset=0, week_kind=None):
    global pool
#    from datetime import datetime

#    target_date = datetime.now()
    from datetime import datetime, timedelta

    target_date = datetime.now() + timedelta(days=day_offset)

    weekday_name_en = target_date.strftime('%A')
    weekday_name = DAY_OF_WEEK_MAPPING.get(weekday_name_en)

    # Определяем week_kind на основе target_date
    if not week_kind:
        week_kind = is_odd_week(target_date)

    # Получаем данные о группе пользователя
    async with pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT group_id FROM public.users WHERE id = $1", user_id)

        if not user_data or not user_data['group_id']:
            return None, None

        group_id = user_data['group_id']

        # Запрос на получение расписания для текущей группы и дня
        query = '''
            SELECT s.id, s.group_id, s.lesson_number, s.subject, s.classroom, s.week_kind, lt.start_time, lt.end_time
            FROM public.schedule s
            JOIN public.lessontimes lt ON s.lesson_number = lt.lesson_number AND s.unit = lt.unit
            WHERE s.group_id = $1
            AND s.day_of_week = $2
            AND (s.week_kind = $3 OR s.week_kind IS NULL)
            ORDER BY s.lesson_number ASC
        '''
        schedule_data = await conn.fetch(query, group_id, weekday_name, week_kind)

    return schedule_data, target_date


async def fetch_teachers_for_schedule(schedule_id):
    global pool
    query = '''
        SELECT t.full_name
        FROM public.scheduleteachers st
        JOIN public.teachers t ON st.teacher_id = t.teacher_id
        WHERE st.schedule_id = $1
    '''
    async with pool.acquire() as conn:
        teachers = await conn.fetch(query, schedule_id)
    return [teacher['full_name'] for teacher in teachers]


async def fetch_lesson_times(unit):
    global pool
    async with pool.acquire() as conn:
        lesson_times = await conn.fetch(
            "SELECT lesson_number, start_time, end_time FROM public.lessontimes WHERE unit = $1 ORDER BY lesson_number",
            int(unit)
        )
    return lesson_times


async def log_user_action(user, course_id=None, group_id=None):
    global pool
    last_active_time = datetime.now()
    is_premium = user.is_premium if user.is_premium is not None else False

    async with pool.acquire() as conn:
        user_data = await conn.fetchrow("SELECT id FROM public.users WHERE id = $1", user.id)

        if user_data:
            await conn.execute('''
                UPDATE public.users
                SET username = $2, first_name = $3, last_name = $4, last_active_time = $5,
                    course_id = COALESCE($6, course_id), group_id = COALESCE($7, group_id),
                    language_code = $8, is_premium = $9
                WHERE id = $1
            ''', user.id, user.username, user.first_name, user.last_name, last_active_time,
                               course_id, group_id, user.language_code, is_premium)
        else:
            await conn.execute('''
                INSERT INTO public.users (id, username, first_name, last_name, last_active_time,
                                          course_id, group_id, language_code, is_premium)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ''', user.id, user.username, user.first_name, user.last_name, last_active_time,
                               course_id, group_id, user.language_code, is_premium)
