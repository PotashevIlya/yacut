# «YaCut»

## Описание проекта: 
YaCut - это сервис для ассоцииации длинных ссылок с короткими. Вы можете предложить свой вариант короткой ссылки или предоставть генерацию проекту. Проект доступен с веб-интерфесом и API. 

## Как запустить проект у себя:
1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/PotashevIlya/yacut
```

```
cd yacut
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
4. Создать .env файл и заполнить его по образцу .env.example
5. Создать таблицы БД
```
flask db upgrade
```
6. Запустить сервер
```
flask run
```

## Доступные эндпоинты для API:

**GET:** http://127.0.0.1:8000/charity_project/

<sub>Получить список всех проектов фонда.</sub>
```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2025-01-15T11:37:23.655Z",
    "close_date": "2025-01-15T11:37:23.655Z"
  }
]
```
**POST:** http://127.0.0.1:8000/donation/

<sub>Сделать пожертвование.</sub>
```
{
  "full_amount": 0,
  "comment": "string"
}
```

Полная спецификация будет доступна по ссылкам /docs или /redoc после запуска сервера

### Технологический стек :bulb:
Python, FastAPI, SQLAlchemy
___  
#### Автор проекта:  
:small_orange_diamond: [Поташев Илья](https://github.com/PotashevIlya)  
