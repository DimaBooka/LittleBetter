from django.test import Client, TestCase, RequestFactory
from finder.models import User, Query, Result
from json import loads
from finder.tasks import create_zip


class TestConnection(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    def test_start(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show(self):
        c = Client()
        response = c.post('/api/query/', {'query': 'cat', 'status': 0})
        self.assertEqual(response.status_code, 401)


class AuthorisationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('dima_dima', 'dimadima@dima.dima', 'tunnel777')
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()

    def contain(self, phrase, data):
        if phrase in data.decode():
            return True
        return False

    def test_autorithation(self):
        c = Client()
        username = 'dima_dima'

        c.login(username=username, password='tunnel777')
        response = c.get('/#/query')
        auth = self.contain(username, response.content)
        self.assertEqual(auth, True)

        c.logout()
        response = c.get('/#/query')
        auth = self.contain(username, response.content)
        self.assertEqual(auth, False)


class QueriesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('dima_dima', 'dimadima@dima.dima', 'tunnel777')
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()

        self.queries = list()
        for q in range(5):
            query = Query.objects.create(query='test' + str(q), author_id=self.user.id, status=0)
            self.queries.append(query)

    def contain(self, phrase, data, key):
        if phrase in loads(data.decode())[key]:
            return True
        return False

    def contain_with_list(self, phrase, data, key):
        if phrase in loads(data.decode())[0][key]:
            return True
        return False

    def test_get_query(self):
        c = Client()
        c.login(username='dima_dima', password='tunnel777')
        response = c.get('/api/query/')
        query = self.contain_with_list('test0', response.content, 'query')
        self.assertEqual(query, True)

    def test_create_query(self):
        c = Client()
        c.login(username='dima_dima', password='tunnel777')
        response = c.post('/api/query/', {'query': 'test600', 'status': 0})
        query = self.contain('test600', response.content, 'query')
        self.assertEqual(query, True)

    def test_delete_query(self):
        c = Client()
        c.login(username='dima_dima', password='tunnel777')
        response = c.get('/api/query/')
        id = loads(response.content.decode())[0]['id']
        c.delete('/api/query/%s/' % id)
        response = c.get('/api/query/%s/' % id)
        query = self.contain('Not found.', response.content, 'detail')
        self.assertEqual(query, True)


class SendToClientTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('dima_dima', 'dimadima@dima.dima', 'tunnel777')
        self.user.is_staff = True
        self.user.is_superuser = False
        self.user.save()
        self.query = Query.objects.create(query='test', author_id=self.user.id, status=0)

        self.result = Result.objects.create(query=self.query, url='https://www.google.com.ua/images/nav_logo242.png',
                                            spider='test', rang=1)
        create_zip(self.query.query, [self.result.url, ])

    def test_sendfile(self):
        c = Client()
        c.login(username='dima_dima', password='tunnel777')

        response = c.get('/download/test')
        self.assertEqual(response.status_code, 200)
