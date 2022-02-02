Physical Transformation Test Case

Web-сервис (REST API) для определения номера недели для переданной даты

Stack:

    python 3.10
    Django
    drf
    loguru

Deploy:

    https://egor187.pythonanywhere.com/weekday-resolver/

Логика работы:

    сервис на входе получает json {"date": "YYYY-MM-DD"} и возвращает json {"week_number": "integer"}

Пример:

    curl -X POST https://egor187.pythonanywhere.com/weekday-resolver/ -H 'Content-Type: application/json' -d '{"date":"2021-12-12"}'