# test_main.py
import unittest
from main import application

class TestApplication(unittest.TestCase):

    def test_get_current_time(self):
        environ = {'REQUEST_METHOD': 'GET', 'PATH_INFO': '/GMT'}
        response = application(environ, lambda status, headers: None)
        self.assertIsNotNone(response)
        self.assertTrue(response[0].startswith(b'20'))  # Checking if the response starts with '20'

    def test_convert_time(self):
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/api/v1/convert',
            'CONTENT_LENGTH': '29',
            'wsgi.input': '{"date": "2023-05-01 12:00:00", "tz": "Europe/London", "target_tz": "America/New_York"}'.encode()
        }
        response = application(environ, lambda status, headers: None)
        self.assertIsNotNone(response)

    def test_calculate_time_difference(self):
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/api/v1/datediff',
            'CONTENT_LENGTH': '94',
            'wsgi.input': '{"first_date": "05.01.2023 12:00:00", "second_date": "12:00PM 2023-05-01", "first_tz": "Europe/London", "second_tz": "America/New_York"}'.encode()
        }
        response = application(environ, lambda status, headers: None)
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()
