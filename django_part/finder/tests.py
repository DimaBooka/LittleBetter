from django.test.client import RequestFactory, Client
from .views import start, show
import unittest


class IndexTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_start(self):
        request = self.factory.get('/')
        response = start(request)
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        request = self.factory.get('/cat')
        response = show(request, query='cat')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
