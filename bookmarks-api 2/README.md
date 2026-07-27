# bookmarks-api

Простое API для хранения закладок (URL, заголовок, теги, избранное) на FastAPI с MongoDB.

## Возможности

- Создание закладки
- Получение списка закладок с фильтром по избранному и тегу
- Получение закладки по ID
- Обновление закладки
- Удаление закладки
- Проверка состояния сервиса через `/health`

## Технологии

- Python 3.11+
- FastAPI
- Motor
- MongoDB
- Uvicorn

## Эндпоинты

- `GET /health`
- `POST /api/v1/bookmarks`
- `GET /api/v1/bookmarks`
- `GET /api/v1/bookmarks/{bookmark_id}`
- `PATCH /api/v1/bookmarks/{bookmark_id}`
- `DELETE /api/v1/bookmarks/{bookmark_id}`

## Формат закладки

Пример ответа:

```json
{
  "id": "66b8f2f3d1b2e3a4c5d6e7f8",
  "url": "https://example.com/article",
  "title": "Интересная статья",
  "tags": ["reading", "devops"],
  "favorite": false,
  "created_at": "2026-07-24T06:23:00Z",
  "updated_at": "2026-07-24T06:23:00Z"
}
```

## Локальный запуск

Настрой окружение, зависимости, MongoDB и `.env` самостоятельно — см. `requirements.txt` и `.env.example` как отправную точку.
