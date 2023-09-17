# api_yamdb

![Static Badge](https://img.shields.io/badge/%D0%B1%D1%8D%D0%BA%D0%B5%D0%BD%D0%B4-django-blue)
![Static Badge](https://img.shields.io/badge/framework-django%20rest%20framework-blue)
![Static Badge](https://img.shields.io/badge/%D0%90%D1%83%D1%82%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-JWT%2Bdjoser-blue)

## Описание. Что это за проект, какую задачу он решает, в чём его польза

Проект YaMDb собирает отзывы пользователей на различные произведения.
В нем есть возможность добавлять, реадктировать и удалять свои произведения, отзывы к ним и комментарии к отзывам.
Так же есть возможность добавлять, реадктировать и удалить своего пользователя.

## Установка. Как развернуть проект на локальной машине

1. Клонируем репозиторий:

    ```bash
    git clone git@github.com:lanarkk/api_final_yatube.git
    ```

2. Развертываем виртуальное окружение:

    ```bash
    python3 -m venv env
    ```

3. Устанавливаем в venv:

    * Если у вас Linux/macOS

    ```bash
    source env/bin/activate
    ```

    * Если у вас windows

    ```bash
    source env/scripts/activate
    ```

4. Установить зависимости из файла requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

    ```bash
    python3 -m pip install --upgrade pip
    ```

5. Выполнить миграции:

    ```bash
    python3 manage.py migrate
    ```

6. Запустить проект:

    ```bash
    python3 manage.py runserver
    ```

## Примеры. Некоторые примеры запросов к API

### Получение списка всех произведений

Получить список всех объектов. Права доступа: Доступно без токена

GET <http://127.0.0.1:8000/api/v1/titles/>

'''json

{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
            "name": "string",
            "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
}

'''

### Получение списка всех отзывов

Получить список всех отзывов. Права доступа: Доступно без токена.

GET <http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/>

'''yaml

{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
    {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": "integer",
        "pub_date": "timestamp"
    }
]
}

'''

### Добавление комментария к отзыву

Добавить новый комментарий для отзыва. Права доступа: Аутентифицированные пользователи.

POST <http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/>

'''yaml
{
  "text": "string"
}
'''

Авторы: Максим Федякин, Лилия Костырева, Дмитрий Жадаев
GitHubs <https://github.com/lanarkk>, <https://github.com/jlell>, <https://github.com/dmitriizh>
