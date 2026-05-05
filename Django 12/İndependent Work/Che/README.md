### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Надо создать `.env` в корне проекта:

```env
CLOUD_NAME=cloud_name
API_KEY=api_key
API_SECRET=api_secret
```

Из [cloudinary.com](https://cloudinary.com) взять эти данные

### 3. Установка Tailwind

```bash
python manage.py tailwind install
```

### 4. Миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 5. Запуск сервера

**Терминал 1 — Django:**
```bash
python manage.py runserver
```

**Терминал 2 — Tailwind:**
```bash
python manage.py tailwind start
```

### Для того чтобы зайти в адимику
1. Зайти за созданного cуперадмина в учетку
2. Нажать на аватарку, в появившимся menu есть кнопка `Админ панель`
