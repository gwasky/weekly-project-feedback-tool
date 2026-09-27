import pytest
from django.conf import settings
from django.db import connection


def test_database_is_postgres():
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"


@pytest.mark.django_db
def test_database_connection_works():
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")

        assert cursor.fetchone() == (1,)


def test_secret_key_comes_from_environment():
    assert not settings.SECRET_KEY.startswith("django-insecure-")
    assert settings.SECRET_KEY != "change-me"
