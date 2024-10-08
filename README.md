# SUAI-Schedule-Bot

## Описание

**SUAI-Schedule-Bot** — это Telegram-бот для студентов ГУАП, который позволяет просматривать расписание занятий по выбранной группе. Бот предоставляет удобный интерфейс для просмотра расписания на сегодня, завтра или всю неделю, а также позволяет переключаться между неделями (числитель/знаменатель).

## Функциональность

- Выбор курса и группы
- Просмотр расписания на сегодня, завтра или неделю
- Переключение между неделями (числитель/знаменатель)
- Отображение расписания звонков
- Смена выбранной группы

## Установка

### Требования

- Python 3.7 или выше
- PostgreSQL база данных
- Аккаунт Telegram для создания бота и получения токена

### Шаги установки

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/vemneyy/SUAI-Schedule-Bot.git
   cd SUAI-Schedule-Bot
   ```

2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/MacOS
   venv\Scripts\activate  # Для Windows
   ```

3. **Установите необходимые зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте базу данных:**

   - Создайте базу данных PostgreSQL.
   - Выполните скрипт `create_db.sql`, чтобы создать необходимые таблицы и структуры в базе данных:

     ```bash
     psql -U your_db_user -d your_db_name -f create_db.sql
     ```

   - Обновите файл `config.py`, указав параметры подключения к базе данных:

     ```python
     DATABASE_CONFIG = {
         'user': 'your_db_user',
         'password': 'your_db_password',
         'database': 'your_db_name',
         'host': 'your_db_host',
         'port': 'your_db_port'  # Если отличается от стандартного 5432
     }
     ```

5. **Получите токен Telegram-бота:**

   - Создайте нового бота через [@BotFather](https://t.me/BotFather) в Telegram.
   - Получите токен и вставьте его в файл `config.py`:

     ```python
     BOT_TOKEN = "ваш_токен_бота"
     ```

6. **Запуск бота:**

   ```bash
   python main.py
   ```

## Структура проекта

- `main.py` — точка входа в приложение.
- `config.py` — файл с конфигурацией бота и базы данных.
- `loader.py` — инициализация бота и диспетчера.
- `utils.py` — вспомогательные функции и декораторы.
- `keyboards.py` — файлы с описанием клавиатур и кнопок.
- `database.py` — функции для работы с базой данных.
- `schedule_utils.py` — функции для генерации расписания.
- `handlers/` — пакет с обработчиками команд и сообщений.
  - `__init__.py` — инициализация обработчиков.
  - `start.py` — обработчик команды `/start`.
  - `change.py` — обработчик команды `/change` и связанных callback.
  - `list_commands.py` — обработчик команды `/list`.
  - `schedule.py` — обработчики команд `/today`, `/tommorow`, `/week` и связанных функций.
  - `calls.py` — обработчик команды `/calls`.
  - `course_selection.py` — обработчики выбора курса и группы.

## Использование

После запуска бота пользователи могут взаимодействовать с ним через следующие команды:

- `/start` — начать работу с ботом, выбрать курс и группу.
- `/today` — показать расписание на сегодня.
- `/tommorow` — показать расписание на завтра.
- `/week` — показать расписание на текущую неделю.
- `/change` — изменить выбранную группу.
- `/calls` — показать расписание звонков.
- `/list` — вывести список доступных команд.

Также бот предоставляет кнопки для быстрого доступа к основным функциям после выбора группы.

## Команды бота

- **/start** — Начать работу с ботом и выбрать группу.
- **/today** — Расписание на сегодня.
- **/tommorow** — Расписание на завтра.
- **/week** — Расписание на текущую неделю.
- **/change** — Сменить выбранную группу.
- **/calls** — Расписание звонков.
- **/list** — Список доступных команд.

## Пример использования

1. **Начало работы:**

   - Отправьте команду `/start`.
   - Выберите курс из предложенных вариантов.
   - Выберите свою группу из списка.

2. **Просмотр расписания:**

   - Используйте команды `/today`, `/tommorow` или `/week` для просмотра расписания.
   - Для переключения между неделями (числитель/знаменатель) используйте кнопку переключения в расписании недели.

3. **Смена группы:**

   - Отправьте команду `/change`.
   - Подтвердите намерение сменить группу.
   - Повторите процесс выбора курса и группы.

## Обработка ошибок

- Бот включает ограничение по количеству запросов от одного пользователя (анти-спам). Если вы отправляете слишком много запросов за короткое время, бот может игнорировать их.
- Если бот сообщает, что группа не выбрана, используйте команду `/start` или `/change` для выбора группы.
- В случае проблем с подключением к базе данных убедитесь, что параметры в `config.py` указаны верно и база данных доступна.

## Разработка и вклад

Если вы хотите внести свой вклад в развитие бота:

1. Форкните репозиторий.
2. Создайте новую ветку для вашей функции или исправления: `git checkout -b feature/YourFeature`.
3. Внесите изменения и закоммитьте их: `git commit -am 'Add some feature'`.
4. Запушьте ветку: `git push origin feature/YourFeature`.
5. Создайте Pull Request.

## Лицензия

Этот проект находится под лицензией **MIT** — подробности в файле [LICENSE](LICENSE).
