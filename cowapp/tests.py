import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client

from cowapp.models import Cow, Record


class BaseTestCase(TestCase):
    verbose = True

    def setUp(self):
        self.username = 'user1'
        self.user = User.objects.create(username=self.username, password=make_password('password'))
        self.client = Client()
        self.sign_in()

    def sign_in(self):
        self.assertTrue(self.client.login(username='user1', password='password'))

    def get_test(self, url, success=True, status_code=None):
        response = self.client.get(url)
        if self.verbose:
            print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def post_test(self, url, data, success=True, status_code=None):
        response = self.client.post(url, data=data)
        if self.verbose:
            print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 201 if success else 400)
        return response

    def put_test(self, url, data, success=True, status_code=None):
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        if self.verbose:
            print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def patch_test(self, url, data, success=True, status_code=None):
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        if self.verbose:
            print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def delete_test(self, url, status_code=None):
        response = self.client.delete(url)
        if self.verbose:
            print(response.status_code)
        self.assertEqual(response.status_code, status_code if status_code else 204)
        return response


class UserViewTest(BaseTestCase):
    def test_sign_up(self):
        self.post_test('/users/new/', dict(
            username='user',
            password='pasdoifjaowwef',
        ))
        user = User.objects.filter(username='user')
        self.assertTrue(user.exists())
        user = user.first()
        self.assertNotEqual(user.password, 'pasdoifjaowwef')

    def test_retrieve(self):
        self.get_test('/users/my/')

    def test_update_success(self):
        self.patch_test('/users/my/', dict(password='qwer1234'))

    def test_update_fail(self):
        errors = [
            dict(password='password'),
            dict(password='1234'),
            dict(username='ajowi3jf@231', password='ajowi3jf@231')
        ]
        for data in errors:
            self.patch_test('/users/my/', data, success=False)

    def test_delete(self):
        self.delete_test('/users/my/')
        self.assertFalse(User.objects.filter(username=self.username).exists())


class CowViewTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cow1 = Cow.objects.create(number='002-1023-1203-1', sex='female', birthday='2011-12-21', user=self.user)
        self.cow2 = Cow.objects.create(number='002-1241-1241-2', sex='male', user=self.user, deleted=True)

    def test_create(self):
        self.post_test('/cows/', dict(
            number='002-1231-1411-1',
            sex='female',
            birthday='2012-12-23',
            mother_number=self.cow1.number,
        ))
        self.assertTrue(Cow.objects.filter(number='002-1231-1411-1').exists())
        self.post_test('/cows/', dict(
            number='002-1231-1411-2',
            sex='female',
            mother_number=self.cow1.number,
        ))
        self.assertTrue(Cow.objects.filter(number='002-1231-1411-2').exists())

    def test_create_fail(self):
        errors = [
            dict(
                number='002-1023-1203-13',
                sex='female',
                mother_number=self.cow1.number,
            ),
            dict(
                number='002-1032223-1203-1',
                sex='female',
                mother_number=self.cow1.number,
            ),
            dict(
                number='00232301-211421121',
                sex='female',
                mother_number=self.cow1.number,
            ),
            dict(
                number='002-1023-1203-1',
                sex='fe32e',
                mother_number=self.cow1.number,
            ),
            dict(
                number='002-1023-1203-1',
                sex='female',
                mother_number='1241-2342-1-231',
            ),
            dict(
                number='002-1023-1203-1',
                sex='female',
                mother_number=self.cow1.number,
            ),
        ]
        for data in errors:
            self.post_test('/cows/', data, success=False)

    def test_list(self):
        response = self.get_test('/cows/')
        self.assertEqual(len(response.json()), 2)
        response = self.get_test('/cows/?deleted=True')
        self.assertEqual(len(response.json()), 1)

    def test_update(self):
        inputs = [
            dict(number='002-1231-1241-2'),
            dict(deleted=True),
        ]
        for data in inputs:
            self.patch_test(f'/cows/{self.cow1.id}/', data)

    def test_update_fail(self):
        errors = [
            dict(number='102-1231-1421-19'),
            dict(sex='females'),
            dict(birthday='1231-12-55'),
            dict(mother_number='124-1241-211212'),
        ]
        for data in errors:
            self.patch_test(f'/cows/{self.cow1.id}/', data, success=False)

    def test_destroy(self):
        self.delete_test(f'/cows/{self.cow1.id}/')
        self.assertFalse(Cow.objects.filter(number=self.cow1.number).exists())


class RecordViewTest(CowViewTest):
    def setUp(self):
        super().setUp()
        self.record1 = Record.objects.create(content='asdf', day='1230-12-22', cow=self.cow1, user=self.user)

    def test_create(self):
        self.post_test('/records/', dict(
            content='hhhhh',
            day='1031-03-11',
            cow=self.cow2.id,
        ))
        self.assertTrue(Record.objects.filter(content='hhhhh').exists())

    def test_create_fail(self):
        errors = [
            dict(
                day='1031-03-11',
                cow=self.cow2.id,
            ),
            dict(
                content='hhhhh',
                cow=self.cow2.id,
            ),
            dict(
                content='hhhhh',
                day='1031-03-11',
            ),
            dict(
                content='hhhhh',
                day='1031-33-11',
                cow=self.cow2.id,
            ),
            dict(
                content='hhhhh',
                day='1031-03-11',
                cow=13791,
            ),
        ]
        for data in errors:
            self.post_test('/records/', data, success=False)

    def test_list(self):
        response = self.get_test('/records/')
        self.assertEqual(len(response.json()), 1)
        response = self.get_test(f'/records/?cow={self.cow2.id}')
        self.assertEqual(len(response.json()), 0)

    def test_update(self):
        inputs = [
            dict(content='1231414'),
            dict(etc='145100jaoif'),
        ]
        for data in inputs:
            self.patch_test(f'/records/{self.record1.id}/', data)

    def test_update_fail(self):
        errors = [
            dict(content=None),
            dict(day='10141-241224-14'),
            dict(cow=1240124),
            dict(cow=None),
        ]
        for data in errors:
            self.patch_test(f'/records/{self.record1.id}/', data, success=False)
