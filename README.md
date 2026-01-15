# Flask API для сайта объявлений

## Примеры запросов

### 1. **Регистрация пользователя** (`POST /register`)

Регистрирует нового пользователя с email и паролем.

#### Запрос
```bash
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"email": "newuser@example.com", "password": "password123"}'
```
#### Ответ
```bash
{
    "message": "User registered successfully!"
}
```

### 2. Логин пользователя (POST /login)

Авторизует пользователя и возвращает JWT токен.

#### Запрос
```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"email": "newuser@example.com", "password": "password123"}'
```
#### Ответ
```bash
{
    "access_token": "your-jwt-token"
}
```

### 3. Создание объявления (POST /ads)

Создает новое объявление. Требуется авторизация.

#### Запрос
```bash
curl -X POST http://127.0.0.1:5000/ads \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your-jwt-token>" \
-d '{"title": "Продам велосипед", "description": "Новый велосипед в отличном состоянии."}'
```
#### Ответ
```bash
{
    "message": "Ad created successfully!"
}
```

### 4. Получение объявления по ID (GET /ads/{ad_id})

Получает информацию об объявлении по его ID.

#### Запрос
```bash
curl -X GET http://127.0.0.1:5000/ads/1 \
-H "Authorization: Bearer <your-jwt-token>"
```
#### Ответ
```bash
{
    "id": 1,
    "title": "Продам велосипед",
    "description": "Новый велосипед в отличном состоянии.",
    "created_at": "2026-01-15T12:00:00",
    "owner_id": 1
}
```

### 5. Удаление объявления (DELETE /ads/{ad_id})

Удаляет объявление с указанным ID. Требуется авторизация.

#### Запрос
```bash
curl -X DELETE http://127.0.0.1:5000/ads/1 \
-H "Authorization: Bearer <your-jwt-token>"
```
#### Ответ
```bash
{
    "message": "Ad deleted successfully!"
}
```

#### Запрос
### 6. Тестирование без авторизации (POST /ads)

Попытка создать объявление без токена (неавторизованный запрос).

#### Запрос
```bash
curl -X POST http://127.0.0.1:5000/ads \
-H "Content-Type: application/json" \
-d '{"title": "Без авторизации", "description": "Попытка создать объявление без токена."}'
```
#### Ответ
```bash
{
    "msg": "Missing Authorization Header"
}
```