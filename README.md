## api_yamdb

### О проекте

*Проект предоставляет API-интерфейс для сбора и хранения отзывов и 
комментариев пользователей на произведения творчества людей.
Произведения имеют категорию и жанр. Пользователи могут оставить произведению
отзыв и оценку (не более одного). Другие пользователи могут прокомментировать
этот отзыв. Добавлять отзывы, комментарии и ставить оценки могут только 
аутентифицированные пользователи.
Интерфейс написан в соответствии с парадигмой REST API в рамках 
прохождения обучения в Яндекс-Практикум.*

### Установка и запуск проекта

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AntAresWeb/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 api_yamdb/manage.py runserver
```

### Заполнение базы данных тестовыми данными из csv-файлов в static/data
python api_yamdb/manage.py import_csv

### Примеры

# Получение списка всех произведений

http://127.0.0.1:8000/api/v1/titles/

Получить список всех объектов. Права доступа: Доступно без токена

Response samples

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
]
}

# Добавление произведения

http://127.0.0.1:8000/api/v1/titles/

Добавить новое произведение.  
Права доступа: Администратор.  
Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).  
При добавлении нового произведения требуется указать уже существующие категорию и жанр.  

Request samples
`
{  
  "name": "string",  
  "year": 0,  
  "description": "string",  
  "genre": [  
     "string"  
  ],  
  "category": "string"  
}
`

Response samples
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
