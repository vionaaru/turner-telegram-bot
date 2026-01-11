# Engineering Context Map (агент-ориентированный)

Project: Telegram бот для приема заказов на токарные работы с CRM-системой
Repo root: d:\CursorProjects\order-TG-bot-self-CRM
Last updated: 2026-01-11
Primary owner/stakeholder: Сергей Акулов (serg-akulov)

## 0. Brief (copy-ready)
- What it is: Telegram бот для приема заказов на токарные/фрезерные работы с веб-CRM для управления
- Why it exists: Автоматизация приема заказов от клиентов с последующим управлением через веб-интерфейс
- Run in prod: systemctl start turner_bot (systemd) или docker-compose up -d
- Run locally: python bot.py (после настройки .env)
- Primary entry points: bot.py (бот), admin.php (CRM), install.sh (установка)
- Core flow: Клиент проходит опрос в боте → заказ сохраняется в БД → уведомление админу → управление через CRM
- Key risks/unknowns: Зависимость от Telegram API, хранение фото только через Telegram, отсутствие резервного копирования БД

## 1. Purpose and scope
- Product intent: Прием заказов на токарные работы через удобный чат-бот с возможностью прикрепления фото и чертежей, управление заказами через веб-интерфейс
- Non-goals / out of scope: Оплата через бота, интеграция с внешними CRM, мобильное приложение, мультиязычность
- Primary users/actors: Клиенты (через Telegram), администратор/токарь (через веб-CRM и Telegram)
@source: README.md[:150], bot.py[:50]

## 2. Architecture at a glance
- Components: Python бот (aiogram), PHP веб-интерфейс, MySQL база данных, системный сервис, Docker контейнеры
- Runtime topology (processes/containers/services): 1 Python процесс (бот), 1 MySQL процесс, 1 Apache/Nginx процесс (опционально для CRM), systemd сервис для автозапуска
- Platforms (OS, devices, cloud): Linux (Ubuntu 20.04+/Debian), VPS/VDS, локальная разработка на Windows/Linux
@source: docker-compose.yml[:43], install.sh[:137], Dockerfile[:32]

## 3. Core flows
Flow A: Прием заказа от клиента
- Trigger: Команда /start в Telegram боте
- Steps: 1) Машина состояний OrderForm (фото→тип→размеры→условия→срочность→комментарий) 2) Сохранение в orders таблицу 3) Уведомление админа с фото
- Outputs: Запись в БД, уведомление админа в Telegram
@source: bot.py[:372], schema.sql[:27], bot.py[254:279]

Flow B: Управление заказами через CRM
- Trigger: Вход в веб-админку admin.php
- Steps: 1) Аутентификация по паролю 2) Просмотр заказов из orders таблицы 3) Изменение статуса 4) Ответы клиентам через reply в боте
- Outputs: Обновление статуса в БД, уведомления клиентам через Telegram API
@source: admin.php[:300], bot.py[291:324]

## 4. Code map
- Source roots: / (корень проекта)
- Main modules and responsibilities:
  - bot.py: Основная логика бота, FSM машина состояний, обработчики команд и сообщений
  - admin.php: Веб-интерфейс CRM, управление заказами, просмотр фото через Telegram API
  - database.py: Работа с MySQL, CRUD операции для заказов и настроек
  - config.py: Загрузка переменных окружения из .env
  - install.sh: Автоматическая установка и настройка
- State machines / schedulers / pipelines: FSM OrderForm в bot.py (7 состояний: photo→work_type→dimensions→conditions→urgency→extra_q→comment)
@source: bot.py[24:31], database.py[:79], admin.php[:300]

## 5. Data and storage
- Data sources: Входящие сообщения Telegram, фото/файлы через Telegram API, настройки из bot_config таблицы
- Persistence (DB, files, caches): MySQL (orders, settings, bot_config таблицы), фото хранятся в Telegram (ссылки в БД)
- File/dir contracts (inputs/outputs): .env (конфиг), php_config.php (генерируется install.sh), schema.sql (структура БД)
@source: schema.sql[:60], config.py[:15], docker-entrypoint.sh[16:34]

## 6. Config and secrets
- Config files (paths and purpose): .env (токен бота, БД, пароли), php_config.php (конфиг для CRM), schema.sql (дефолтные тексты в bot_config)
- Env vars and defaults: BOT_TOKEN, DB_HOST/DB_USER/DB_PASS/DB_NAME, ADMIN_PANEL_PASSWORD, BOT_ADMIN_PASSWORD
- Secret handling: Хранение в .env, php_config.php генерируется автоматически, пароли в открытом виде (нет шифрования)
@source: config.py[:15], install.sh[44:52], docker-entrypoint.sh[16:24]

## 7. Build, run, test
- Build: pip install -r requirements.txt (для Python), копирование PHP файлов на веб-сервер
- Run: python bot.py (локально), systemctl start turner_bot (прод), docker-compose up (контейнеры)
- Test: Отсутствуют автоматические тесты, ручное тестирование через Telegram бота
- Lint/format: Отсутствует, Python код без форматирования
@source: install.sh[:137], docker-compose.yml[:43], requirements.txt[:6]

## 8. Dependencies and integrations
- External services/APIs: Telegram Bot API (поллинг через aiogram), Telegram File API (для фото)
- Third-party binaries/models: MySQL клиент через pymysql, cryptography (опционально)
- Hardware dependencies: VPS с Ubuntu/Debian, MySQL сервер, веб-сервер для PHP
@source: requirements.txt[:6], bot.py[7:8], admin.php[58:66]

## 9. Ops and observability
- Logging: Python logging.INFO в stdout, journalctl -u turner_bot для системного сервиса
- Metrics/tracing: Отсутствует, только базовые логи ошибок
- Health checks: Отсутствует, проверка через systemctl status turner_bot
@source: bot.py[17:18], install.sh[126:129]

## 10. Risks and tech debt
- Known risks: Фото хранятся только в Telegram (ограниченное время), отсутствие бэкапа БД, простой аутентификации в CRM
- Gaps in tests/docs: Отсутствие unit/functional тестов, минимальная документация, нет обработки ошибок БД
@source: bot.py[69:71], admin.php[34:36], schema.sql[37:60]

## 11. Open questions
- Q1: Как обрабатывать устаревшие фото в Telegram (файлы удаляются через время)?
- Q2: Возможность резервного копирования БД и восстановления?
- Q3: Масштабируемость при большом количестве заказов (один процесс бота)?

## 12. Evidence index (optional)
- @inferred: Архитектурные решения основаны на анализе кода, нет явной документации
- @source: bot.py[254:279]: Логика уведомления админа с фото