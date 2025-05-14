# 🎟 Система бронирования мероприятий

## 📄 Описание проекта

Веб-приложение на Django для автоматизированного бронирования мероприятий (концерты, выставки, мастер-классы и т.п.).  
Проект демонстрирует:
- просмотр и фильтрацию событий  
- бронирование билетов  
- генерацию PDF с QR-кодом  
- отправку email  
- административную загрузку событий  
- импорт CSV  

---

## 🎯 Цели проекта

- Освоение Django как веб-фреймворка
- Практика MVC (MTV) подхода
- Работа с моделями, формами, авторизацией, изображениями, почтой
- Автоматизация рутины через админ-панель и массовый импорт

---

## 🧩 Основной функционал

### 👤 Пользователь:
- Просматривает список мероприятий `/`
- Фильтрует по дате, месту, жанру
- Смотрит детали события `/events/<id>/`
- Бронирует билет `/events/<id>/book/`
- Получает PDF-билет и email
- Может зарегистрироваться и войти
- Получает личный кабинет `/dashboard/`

---

## 👮 Кастомная админ-панель

📍 Доступна по адресу:  
```plaintext
/admin-panel/
```

🔐 Только для пользователей `is_staff`

### Возможности:
- ➕ Добавление мероприятий вручную через форму
- 📥 Массовая загрузка событий из `.csv` файла
- 🖼 Отображение обложек и всех полей в таблице
- 🧠 Автоматическое заполнение `available_tickets = capacity`

---

## 📥 CSV-импорт

Формат CSV-файла для загрузки мероприятий:

```csv
Название,Дата,Место,Жанр,Цена,Мест,Описание
Концерт группы "Лето",2025-06-18 19:00,Москва,Концерт,1200,150,Энергичный летний концерт на открытом воздухе.
...
```

Поддержка:
- UTF-8
- Разделитель: `,`
- Дата в формате `ГГГГ-ММ-ДД ЧЧ:ММ`

---

## 🖼 Поддержка обложек мероприятий

Каждое мероприятие может иметь изображение:
- Загрузка при добавлении
- Хранение в `/media/event_images/`
- Отображение в таблице админ-панели

---

## 📂 Архитектура проекта

```txt
event_booking/
├── manage.py
├── db.sqlite3
├── event_booking/
│   ├── settings.py
│   ├── urls.py
├── events/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py          # Форма событий и бронирования
│   ├── models.py         # Event, Booking
│   ├── urls.py
│   ├── views.py
│   ├── utils.py          # PDF, QR, Email
├── templates/
│   ├── base.html
│   ├── events/
│   │   ├── event_list.html
│   │   ├── event_detail.html
│   │   ├── booking_form.html
│   │   ├── booking_confirmation.html
│   │   ├── dashboard.html
│   │   └── admin_panel.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── media/
│   ├── event_images/
│   └── tickets/
```

---

## 🔐 Авторизация и маршруты

```txt
/                   — список мероприятий
/events/<id>/       — просмотр одного события
/events/<id>/book/  — форма бронирования
/register/          — регистрация
/accounts/login/    — вход
/accounts/logout/   — выход (POST)
/dashboard/         — личный кабинет
/admin-panel/       — Кастомная панель администратора
/admin/             — стандартная Django admin
```

---

## ⚙️ Установка и запуск

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Тестирование

```bash
python manage.py test
```

---

## ✉️ Email и PDF

- Генерация билета в PDF
- QR-код в файле
- Отправка по email

Настройка SMTP:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'example@mail.ru'
EMAIL_HOST_PASSWORD = 'пароль'
```

---

## 🧠 Возможности для расширения

- Подключение платёжных систем
- Telegram-бот для оповещений
- Расписание событий (cron / Celery)
- i18n мультиязычность
- Поиск, сортировка, экспорт Excel

---
