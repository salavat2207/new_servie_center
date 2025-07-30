# 🔧 Сервисный центр Backend

FastAPI-бэкенд для системы сервисного центра:
обработка заявок, мастеров, товаров, категорий, цен и поддержка Telegram-бота.

---

## 🚀 Технологии

* FastAPI / Pydantic v1
* SQLAlchemy + Alembic
*  SQLite
* Redis
* Docker / Docker Compose
* Telegram Bot (aiogram)

---

## 📆 Функционал

* Авторизация для админов и редакторов
* Управление категориями, товарами, ценами по городам
* Telegram-бот с кнопками статуса заявки: Принято, В работе, Завершено
* API для фронта: меню, продукты, цены, заявки

---

## 📦 Установка

```bash
git clone https://github.com/yourname/service-center-backend.git
cd service-center-backend
cp .env.example .env
docker compose up --build
```



---

## 📃 Структура

```
app/
├── main.py
├── models.py
├── database.py
├── schemas.py
├── auth.py
├── routers/
│   ├── admin.py
│   └── requests.py
├── telegram_bot/
├── utils/
```

---

## 🔄 API

* `GET /menu` — все бренды, категории, модели
* `POST /requests` — оставить заявку
* `GET /admin/services` — список услуг с ценами
* `PATCH /admin/services/{id}/price` — изменение цены


---

## 🧳 Окружение


---

## 👤 Автор: @Салават Гибадуллин



**Stack:** FastAPI, SQLite, Docker, Telegram Bot
