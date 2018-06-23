import json

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase, Client


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1', password=make_password('password'))
        self.client = Client()
        self.sign_in()

    def sign_in(self):
        self.assertTrue(self.client.login(username='user1', password='password'))

    def get_test(self, url, success=True, status_code=None):
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def post_test(self, url, data, success=True, status_code=None):
        response = self.client.post(url, data=data)
        print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 201 if success else 400)
        return response

    def put_test(self, url, data, success=True, status_code=None):
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def patch_test(self, url, data, success=True, status_code=None):
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, status_code if status_code else 200 if success else 400)
        return response

    def delete_test(self, url, status_code=None):
        response = self.client.delete(url)
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

    def test_my_retrieve(self):
        self.get_test('/users/my/')

    def test_my_update_success(self):
        response = self.patch_test('/users/my/', dict(password='qwer1234'))

    def test_my_update_fail(self):
        errors = [
            dict(password='password'),
            dict(password='1234'),
            dict(username='ajowi3jf@231', password='ajowi3jf@231')
        ]
        for error_input in errors:
            response = self.patch_test('/users/my/', error_input, False)
            self.assertEqual(response.status_code, 400)

    def test_my_delete(self):
        response = self.delete_test('/users/my/')
