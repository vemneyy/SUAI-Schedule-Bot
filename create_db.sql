-- Создание таблицы teachers
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL
);

-- Создание таблицы lessontimes
CREATE TABLE lessontimes (
    time_id SERIAL PRIMARY KEY,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    unit INT NULL,
    lesson_number INT NOT NULL
);

-- Создание таблицы groups
CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    course_id INT NULL,
    unit INT NULL
);

-- Создание таблицы schedule
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    group_id INT NULL,
    day_of_week TEXT NOT NULL,
    lesson_number INT NOT NULL,
    subject TEXT NOT NULL,
    classroom TEXT NULL,
    week_kind TEXT NULL,
    is_change BOOLEAN DEFAULT FALSE,
    change_date DATE NULL,
    unit INT NULL,
    CONSTRAINT schedule_week_kind_check CHECK (week_kind IN ('odd', 'even'))
);

-- Добавление внешних ключей в таблицу schedule
ALTER TABLE schedule
    ADD CONSTRAINT schedule_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id),
    ADD CONSTRAINT schedule_lesson_number_fkey FOREIGN KEY (lesson_number) REFERENCES lessontimes(time_id);

-- Создание таблицы scheduleteachers
CREATE TABLE scheduleteachers (
    schedule_id INT NOT NULL,
    teacher_id INT NOT NULL,
    subgroup INT NOT NULL,
    PRIMARY KEY (schedule_id, teacher_id, subgroup),
    CONSTRAINT scheduleteachers_schedule_id_fkey FOREIGN KEY (schedule_id) REFERENCES schedule(id),
    CONSTRAINT scheduleteachers_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- Создание таблицы users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NULL,
    language_code TEXT NULL,
    is_premium BOOLEAN NULL,
    group_id INT NULL,
    course_id INT NULL,
    last_active_time TIMESTAMP NULL,
    CONSTRAINT users_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(group_id)
);
