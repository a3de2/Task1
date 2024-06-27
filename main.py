from wsgiref.simple_server import make_server
import json
from datetime import datetime
import pytz

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/html')]
    start_response(status, headers)

    # Получение метода запроса
    method = environ['REQUEST_METHOD']

    # Получение запрашиваемого пути
    path = environ['PATH_INFO']

    if method == 'GET' and path.startswith('/'):
        # Обработка GET запроса для получения текущего времени в запрошенной зоне
        tz_name = path[1:] if len(path) > 1 else 'GMT'
        tz = pytz.timezone(tz_name)
        current_time = datetime.now(tz)
        return [str(current_time).encode()]

    elif method == 'POST' and path == '/api/v1/convert':
        # Обработка POST запроса для преобразования времени из одного часового пояса в другой
        content_length = int(environ.get('CONTENT_LENGTH', '0'))
        post_data = json.loads(environ['wsgi.input'].read(content_length))
        date_str = post_data.get('date', '')
        source_tz_name = post_data.get('tz', '')
        target_tz_name = post_data.get('target_tz', '')

        if date_str and source_tz_name and target_tz_name:
            source_tz = pytz.timezone(source_tz_name)
            target_tz = pytz.timezone(target_tz_name)
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            localized_date = source_tz.localize(date_obj)
            converted_date = localized_date.astimezone(target_tz)
            response_data = {'converted_date': str(converted_date)}
            return [json.dumps(response_data).encode()]

    elif method == 'POST' and path == '/api/v1/datediff':
        # Обработка POST запроса для вычисления разницы во времени между двумя датами
        content_length = int(environ.get('CONTENT_LENGTH', '0'))
        post_data = json.loads(environ['wsgi.input'].read(content_length))
        first_date = datetime.strptime(post_data['first_date'], '%m.%d.%Y %H:%M:%S')
        second_date = datetime.strptime(post_data['second_date'], '%I:%M%p %Y-%m-%d')
        first_tz = pytz.timezone(post_data['first_tz'])
        second_tz = pytz.timezone(post_data['second_tz'])

        # Calculate the time difference
        time_diff = second_date - first_date
        time_diff = time_diff.total_seconds() // 60  # Get the time difference in minutes

        response_data = {'time_difference_minutes': time_diff}

        return [json.dumps(response_data).encode()]

with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
