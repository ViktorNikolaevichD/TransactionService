# Руководство по запуску проекта без Docker

## Предварительные требования

Убедитесь, что у вас установлены следующие компоненты:
- Python 3.11

## Установка и настройка

1. **Открытие проекта**

Откройте проект в корневой директории

2. **Создание виртуального окружения**

Выполните следующую команду для создания виртуального окружения и активируйте его:
```bash
$ python -m venv venv
```

3. **Установка зависимостей**
```bash
$ pip install pip-tools
$ pip-sync ./requirements.txt
```

4. **Настройка переменных окружения**

В директории envs создайте файл .env.dev со следующим содержимым(пример):
```bash
DB_HOST="localhost"
DB_PORT=5432
DB_USER="postgres"
DB_PASS="1234"
DB_NAME="TransactionServiceDb"
JWT_SECRET_KEY="ugDIkmk2OuOaB3skY+rKEZ9/cYIm6oXT58tApbQAP60="
JWT_ALG="HS256"
SECRET_KEY="gfdmhghif38yrf9ew0jkf32"
```

5. **Настройка базы данных**

Создайте БД под управлением PostgreSQL с названием TransactionServiceDb и выполните команду:
```bash
$ alembic upgrade head
```

6. **Запуск проекта**

Запустите проект при помощи uvicorn(выполняйте это действие в директории ./src):
```bash
uvicorn main:app --reload
```

7. **Доступ к проекту**

Теперь документация к вашему проекту доступна по адресу http://127.0.0.1:8000/docs



# Руководство по запуску проекта с помощью Docker

## Предварительные требования

Убедитесь, что у вас установлены следующие компоненты:
- Python 3.11

## Установка и настройка

1. **Открытие проекта**

Откройте проект в корневой директории

2. **Настройка переменных окружения**

В директории envs создайте файл .env.dev со следующим содержимым(пример):
```bash
DB_HOST="db"
DB_PORT=5432
DB_USER="postgres"
DB_PASS="1234"
DB_NAME="TransactionServiceDb"
JWT_SECRET_KEY="ugDIkmk2OuOaB3skY+rKEZ9/cYIm6oXT58tApbQAP60="
JWT_ALG="HS256"
SECRET_KEY="gfdmhghif38yrf9ew0jkf32"
```

В корневой директории создайте файл .env со следующим содержимым(пример):
```bash
DB_USER="postgres"
DB_PASS="1234"
DB_NAME="TransactionServiceDb"
```

3. **Запуск контейнера**

Соберите проект:
```bash
$ docker-compose build
```
Запустите проект:
```bash
$ docker-compose up -d
```

4. **Доступ к проекту**

Теперь документация к вашему проекту доступна по адресу http://127.0.0.1:8000/docs

# email/пароли для теста
```bash
user: test@example.com/user
admin: admin@example.com/admin
```