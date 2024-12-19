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

**GET:** http://127.0.0.1:5000/api/id/<short_link>/

<sub>Получить оригинальную ссылку, ассоциированную с короткой</sub>
```
{
"url": "string"
}
```
**POST:** http://127.0.0.1:5000/api/id/

<sub>Получение короткой ссылки для оригинальной (поле short_link опционально)</sub>
```
{
"url": "string",
"short_link": "string"
}
```

Полная спецификация представлена в openapi.yml. Для удобства можно воспользоваться онлайн-редактором Swagger Editor.

### Технологический стек :bulb:
Python, Flask, SQLAlchemy, WTForms
___  
#### Автор проекта:  
:small_orange_diamond: [Поташев Илья](https://github.com/PotashevIlya)  
