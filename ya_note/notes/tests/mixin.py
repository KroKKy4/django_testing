from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


class CustomTestCase(TestCase):

    @classmethod
    def setUpTestData(cls, client_form_content=False):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug='note-slug',
            author=cls.author,
        )
        if client_form_content:
            cls.author_client = Client()
            cls.author_client.force_login(cls.author)
            cls.reader_client = Client()
            cls.reader_client.force_login(cls.reader)
            cls.form_data = {
                'title': 'Новый заголовок',
                'text': 'Новый текст',
                'slug': 'new-slug'
            }
