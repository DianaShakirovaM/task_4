# Система бронирования мест

Проект представляет собой REST API для бронирования переговорных комнат с возможностью:
- Просмотра доступных комнат
- Бронирования на выбранное время
- Управления бронированиями
- Получения уведомлений о бронировании
---
## Автор
**Диана Шакирова**  
[![GitHub](https://img.shields.io/badge/GitHub-DianaShakirovaM-black)](https://github.com/DianaShakirovaM)  
---
## Установка

### Технологии
- Backend: Django 3.2 + Django REST Framework
- Аутентификация: Djoser
- Celery + Redis
---
### Локальный запуск
1. Клонируйте репозиторий:
```bash
   git clone https://github.com/DianaShakirovaM/task_4.git
   cd task_4
```
2. Установите зависимости:
```bash
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
```
3. Примените миграции:
```bash
  python manage.py migrate
```
4. Запустите сервер:
```bash
  python manage.py runserver
```
5. Во втором терминале (для Celery):

```bash
celery -A config worker -l info --pool=solo
```
---
## Примеры запросов
### Бронировать комнату(требуется аутентификация):
```http
Content-Type: application/json
Authorization: Token ваш_токен
POST /api/rooms/1/booking/
```
### Получить свободные комнаты в указанный прожемуток времени
```http
GET /api/rooms/available/?start_time=22.01.2025 12:00&end_time=23.01.2025 12:00
```
