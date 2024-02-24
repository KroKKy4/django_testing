from datetime import date

import pytest
from django.conf import settings
from django.utils import timezone

from news.forms import CommentForm
from news.pytest_tests.conftest import URL

pytestmark = pytest.mark.django_db


def test_news_count_order(client, news_list):
    response = client.get(URL.home)
    news = list(response.context['object_list'])
    assert isinstance(news[0].date, date)
    assert news == sorted(
        news, key=lambda x: x.date, reverse=True
    )


def test_news_count_on_home_page(client, news_list):
    response = client.get(URL.home)
    news = list(response.context['object_list'])
    assert len(news) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_comments_order(client, news, comments_list):
    response = client.get(URL.detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = list(news.comment_set.all())
    assert isinstance(all_comments[0].created, timezone.datetime)
    assert all_comments == sorted(all_comments, key=lambda x: x.created)


def test_admin_has_form(admin_client, news):
    admin_response = admin_client.get(URL.detail)
    assert ('form' in admin_response.context)
    assert isinstance(admin_response.context['form'], CommentForm)


def test_anonymous_hasnt_form(client, news):
    response = client.get(URL.detail)
    assert 'form' not in response.context
