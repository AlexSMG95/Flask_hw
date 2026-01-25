# aiohttp API для сайта объявлений

REST API для доски объявлений, построенный на **aiohttp** с асинхронной архитектурой.

## Технологии

- **aiohttp 3.9.1** - асинхронный веб-фреймворк
- **SQLAlchemy 2.0.25** - async ORM с type hints
- **aiosqlite 0.19.0** - асинхронный драйвер для SQLite
- **bcrypt 4.1.2** - безопасное хеширование паролей
- **PyJWT 2.8.0** - JWT аутентификация

## Структура проекта

```
aiohttp_hw/
├── app.py              # Основное приложение
├── config.py           # Конфигурация
├── database.py         # Async database engine
├── models.py           # Модели данных (User, Ad)
├── routes.py           # Регистрация маршрутов
├── handlers/
│   ├── auth.py         # Регистрация и логин
│   └── ads.py          # CRUD для объявлений
├── middlewares/
│   └── jwt_auth.py     # JWT middleware
├── utils/
│   ├── password.py     # Async bcrypt
│   └── jwt_utils.py    # JWT утилиты
└── requirements.txt
```

## Установка и запуск

### 1. Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Запуск приложения

```bash
python app.py
```

Приложение запустится на `http://0.0.0.0:8080`

## API Endpoints

### 1. Регистрация пользователя (`POST /register`)

Регистрирует нового пользователя с email и паролем.

#### Запрос
```bash
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

#### Ответ
```json
{
    "message": "User registered successfully!"
}
```

#### Возможные ошибки
- **400** - Email already exists!
- **400** - Email and password are required

---

### 2. Логин пользователя (`POST /login`)

Авторизует пользователя и возвращает JWT токен.

#### Запрос
```bash
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

#### Ответ
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Возможные ошибки
- **401** - Invalid credentials
- **400** - Email and password are required

---

### 3. Создание объявления (`POST /ads`)

Создает новое объявление. **Требуется авторизация** (JWT токен).

#### Запрос
```bash
curl -X POST http://localhost:8080/ads \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"title": "Продам велосипед", "description": "Новый велосипед в отличном состоянии."}'
```

#### Ответ
```json
{
    "message": "Ad created successfully!"
}
```

#### Возможные ошибки
- **401** - Missing Authorization Header
- **401** - Token has expired
- **401** - Invalid token
- **400** - Title and description are required

---

### 4. Получение объявления (`GET /ads/{id}`)

Получает информацию об объявлении по его ID. Авторизация не требуется.

#### Запрос
```bash
curl -X GET http://localhost:8080/ads/1
```

#### Ответ
```json
{
    "id": 1,
    "title": "Продам велосипед",
    "description": "Новый велосипед в отличном состоянии.",
    "created_at": "2026-01-23T12:00:00.123456",
    "owner_id": 1
}
```

#### Возможные ошибки
- **404** - Ad not found
- **400** - Invalid ad ID

---

### 5. Обновление объявления (`PUT /ads/{id}`)

Редактирует информацию об объявлении. **Только владелец** может редактировать.

#### Запрос
```bash
curl -X PUT http://localhost:8080/ads/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"title": "Продам новый велосипед", "description": "Велосипед практически не использовался."}'
```

#### Ответ
```json
{
    "message": "Ad updated successfully!"
}
```

#### Возможные ошибки
- **401** - Missing Authorization Header / Token has expired / Invalid token
- **403** - You are not authorized to update this ad
- **404** - Ad not found

---

### 6. Удаление объявления (`DELETE /ads/{id}`)

Удаляет объявление. **Только владелец** может удалять.

#### Запрос
```bash
curl -X DELETE http://localhost:8080/ads/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

#### Ответ
```json
{
    "message": "Ad deleted successfully!"
}
```

#### Возможные ошибки
- **401** - Missing Authorization Header / Token has expired / Invalid token
- **403** - You are not authorized to delete this ad
- **404** - Ad not found

---

## Полный пример использования

```bash
# 1. Регистрация пользователя
curl -X POST http://localhost:8080/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# 2. Логин и сохранение токена
TOKEN=$(curl -s -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# 3. Создание объявления
curl -X POST http://localhost:8080/ads \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Продам велосипед", "description": "Горный велосипед 21 скорость"}'

# 4. Получение объявления
curl -X GET http://localhost:8080/ads/1

# 5. Обновление объявления
curl -X PUT http://localhost:8080/ads/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Продам горный велосипед"}'

# 6. Удаление объявления
curl -X DELETE http://localhost:8080/ads/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Тестирование без авторизации

Попытка создать объявление без токена вернет ошибку:

```bash
curl -X POST http://localhost:8080/ads \
  -H "Content-Type: application/json" \
  -d '{"title": "Без авторизации", "description": "Попытка без токена"}'
```

#### Ответ
```json
{
    "message": "Missing Authorization Header"
}
```

## Конфигурация

Параметры можно настроить через переменные окружения:

```bash
export JWT_SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite+aiosqlite:///site.db"
```

Или создать файл `.env`:

```env
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA_SECONDS=3600
HOST=0.0.0.0
PORT=8080
```

## Модели данных

### User
- `id` - уникальный идентификатор
- `email` - email (уникальный)
- `password` - хешированный пароль (bcrypt)

### Ad
- `id` - уникальный идентификатор
- `title` - заголовок (до 100 символов)
- `description` - описание
- `created_at` - дата создания (автоматически)
- `owner_id` - ID владельца (внешний ключ на User)

## Безопасность

- Пароли хешируются с помощью **bcrypt**
- JWT токены с временем жизни 1 час (по умолчанию)
- Проверка владельца при изменении/удалении объявлений
- Защита от SQL-инъекций через SQLAlchemy ORM

## Производительность

Благодаря асинхронной архитектуре:
- Поддержка тысяч одновременных соединений
- Эффективное использование ресурсов
- Неблокирующие I/O операции

## Разработка

### Запуск с логированием SQL

В `database.py` установлен `echo=True` для отладки SQL запросов.

### Структура async кода

Все обработчики используют `async/await`:
- `await request.json()` - чтение тела запроса
- `async with session` - управление транзакциями
- `await session.execute()` - выполнение запросов

## Лицензия

Учебный проект
