# Root Optimization
## README.md для бэкенд части
### ОСНОВНЫЕ ВОЗМОЖНОСТИ
- Построение маршрута: расчет расстояния и времени между точками
- Оптимизация порядка точек: автоматическое нахождение оптимальной последовательности
- Управление маршрутами: сохранение, получение, мягкое удаление
- Генерация случайных координат в заданной области
- JWT аутентификация

### ТЕХНОЛОГИЧЕСКИЙ СТЕК
- fastapi (>=0.135.1,<0.136.0)
- pydantic-settings (>=2.13.1,<3.0.0)
- sqlalchemy[asyncio] (>=2.0.48,<3.0.0)
- asyncpg (>=0.31.0,<0.32.0)
- uvicorn (>=0.42.0,<0.43.0)
- alembic (>=1.18.4,<2.0.0)
- bcrypt (>=5.0.0,<6.0.0)
- pyjwt (>=2.12.1,<3.0.0)
- geoalchemy2 (>=0.18.4,<0.19.0)
- httpx (>=0.28.1,<0.29.0)
- shapely (>=2.1.2,<3.0.0)

### УСТАНОВКА И ЗАПУСК
#### ПРЕДВАРИТЕЛЬНЫЕ ТРЕБОВАНИЯ
- Docker / Docker Compose
- Локальный PostgreSQL с PostGIS
- Запущенный OSRM сервер

#### НАЧАЛО РАБОТЫ
1. КЛОНИРОВАНИЕ РЕПОЗИТОРИЯ:
```bash
git clone https://github.com/leanleanlean96/route-optimization.git
cd route-optimization
```

2. НАСТРОЙКА ОКРУЖЕНИЯ (.env файл):
   1. База данных
   APP_CONFIG__DB__URL=postgresql+asyncpg://user:password@db:5432/route_db

   2. JWT
   APP_CONFIG__JWT__SECRET_KEY=your-secret-key
   APP_CONFIG__JWT__PUBLIC_KEY=your-public-key
   APP_CONFIG__JWT__ALGORITHM=HS256

   3. OSRM
   APP_CONFIG__OSRM__URL=http://osrm:5000

   4. Географические границы для генерации точек
   APP_CONFIG__GEO__MIN_LAT=48.0
   APP_CONFIG__GEO__MIN_LON=28.0
   APP_CONFIG__GEO__MAX_LAT=52.0
   APP_CONFIG__GEO__MAX_LON=40.0

   5. Опционально
   APP_CONFIG__DEBUG=True
   APP_CONFIG__DB__ECHO=False

3. ЗАПУСК ЧЕРЕЗ DOCKER COMPOSE:
```bash
docker-compose up -d
```
Сервис будет доступен: http://localhost:8080

### API ЭНДПОИНТЫ
Базовый префикс: /api

МАРШРУТЫ (/routes):
- POST: /routes/create - Создать и сохранить маршрут
- GET: /routes/{route_id} - Получить сохранённый маршрут по ID
- POST: /routes/metrics - Рассчитать метрики
- POST: /routes/optimize - Оптимизировать порядок точек
- POST: /routes/random-coordinates - Сгенерировать случайные точки


### ПОТОК ДАННЫХ
Запрос -> FastAPI роутер -> Pydantic схема -> Use Case -> Доменные сервисы/Репозитории 
-> Инфраструктура (OSRM/PostgreSQL) -> Ответ

### БАЗА ДАННЫХ
#### МИГРАЦИИ (Alembic):
- Автогенерация настроена через target_metadata = Base.metadata
- Кастомное именование констрейнтов

#### ТАБЛИЦЫ:
users:
  - id (PK)
  - name (VARCHAR 30)
  - email (UNIQUE)
  - is_active (BOOLEAN)

routes:
  - id (PK)
  - distance_m (FLOAT) - метры
  - duration_s (FLOAT) - секунды
  - geometry (GEOMETRY(LINESTRING, 4326))
  - is_deleted (BOOLEAN) - мягкое удаление
  - user_id (FK -> users.id)

КОМАНДЫ ДЛЯ МИГРАЦИЙ:
```bash
alembic revision --autogenerate -m "description"
```
```bash
alembic upgrade head
```
```bash
alembic downgrade -1
```

### КОНФИГУРАЦИЯ

#### КЛЮЧЕВЫЕ ПАРАМЕТРЫ
- APP_CONFIG__APP__NAME: Название приложения
- APP_CONFIG__APP__HOST: Хост (по умолчанию 0.0.0.0)
- APP_CONFIG__APP__PORT: Порт (по умолчанию 8080)
- APP_CONFIG__DB__URL: URL подключения к БД
- APP_CONFIG__JWT__SECRET_KEY: Секрет для JWT
- APP_CONFIG__JWT__ALGORITHM: Алгоритм шифрования (HS256/RS256)
- APP_CONFIG__OSRM__URL: URL OSRM сервера
- APP_CONFIG__GEO__MIN_LAT/MIN_LON/MAX_LAT/MAX_LON: Границы для генерации
- APP_CONFIG__DEBUG: Режим отладки
- APP_CONFIG__DB__ECHO: Логирование SQL запросов

### ОБРАБОТКА ОШИБОК
- 401: UnauthorizedException - Ошибка аутентификации
- 404: RouteNotFoundException - Маршрут не найден в БД
- 500: OsrmServiceException - Ошибка при запросе к OSRM
- 503: OsrmServiceUnavailableException - OSRM сервер недоступен