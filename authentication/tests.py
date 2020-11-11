from sqlite3 import IntegrityError

from django.db.backends import sqlite3
from django.test import TestCase
# Create your tests here.
from rest_framework.test import APIRequestFactory
from authentication.models import CustomUser
from django.db import IntegrityError
from authentication.views import ObtainTokenPairView


class UserAPI(TestCase):

    def test_add_duplicate_user(self):
        user1 = CustomUser.objects.create_user(username='SameUser',
                                              email='test@test.com', password='12345678')
        try:
            CustomUser.objects.create_user(username='SameUser',
                                              email='test@test.com', password='12345678')
            self.fail("Integrity Error")
        except IntegrityError:
            pass


    def test_long_name(self):

        user = CustomUser.objects.create_user(username='toolongggggggggggggggggggggggggggggggggggggggggg'
                                                       'ggggggggggggggggggggggggggggggggggggggggggggggggggggg'
                                                       'ggggggggggggggggggggggggggggggggggggggggggggggggggggg'
                                                       'ggggggggggggggggggggggggggggggggggggggggggggggggggggg'
                                                       'ggggggggggggggggggggggggggggggggggggggggggggggggggggg'
                                                       'ggggggggggggggggggggggggggggggggggggggggggggggggggggg!',
                                               email='test@test.com', password='12345678')

    def test_logingIn(self):
        user = CustomUser.objects.create_user(username='LoginUser',
                                               email='test@test.com', password='12345678')
        valid_paylod = {
            'username': 'LoginUser',
            'password': '12345678'
        }
        factory = APIRequestFactory()
        request_url = 'token/obtain/'
        request = factory.post(request_url, valid_paylod, format='json')
        view = ObtainTokenPairView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

