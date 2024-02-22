from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

from .const_urls import (ADD, DELETE, DETAIL, EDIT, HOME, LIST, LOGIN, LOGOUT,
                         SIGNUP, SUCCESS)

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.auth_user = User.objects.create(username='auth_user')
        cls.auth_user_client = Client()
        cls.auth_user_client.force_login(cls.auth_user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )

    def test_pages_availability_for_anonymous_user(self):
        urls = (
            HOME,
            LOGIN,
            LOGOUT,
            SIGNUP,
        )
        for name in urls:
            with self.subTest():
                url = reverse(name)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_auth_user(self):
        urls = (
            LIST,
            SUCCESS,
            ADD,
        )
        for name in urls:
            with self.subTest():
                url = reverse(name)
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_different_users(self):
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.auth_user_client, HTTPStatus.NOT_FOUND),
        )
        urls = (
            DETAIL,
            EDIT,
            DELETE,
        )
        for user, status in users_statuses:
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirects(self):
        login_url = reverse(LOGIN)
        urls = (
            (LIST, None),
            (SUCCESS, None),
            (ADD, None),
            (DETAIL, (self.note.slug,)),
            (EDIT, (self.note.slug,)),
            (DELETE, (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest():
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
