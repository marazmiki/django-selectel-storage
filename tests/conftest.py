import os
import uuid

import pytest


def pytest_configure():
    """
    Create an MVP of a django test project
    """
    from django.conf import settings

    os.environ['SELECTEL_USERNAME'] = '9640_test'
    os.environ['SELECTEL_CONTAINER_NAME'] = 'test_django_selectel_storage'
    os.environ['SELECTEL_PASSWORD'] = '3lMUkJbFQp'

    username = os.getenv('SELECTEL_USERNAME')
    password = os.getenv('SELECTEL_PASSWORD')
    container = os.getenv('SELECTEL_CONTAINER_NAME')

    settings.configure(
        INSTALLED_APPS=['django_selectel_storage'],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':MEMORY:'
            }
        },
        SELECTEL_STORAGES={
            'default': {
                'USERNAME': username,
                'PASSWORD': password,
                'CONTAINER': container,
            },
            'customized': {
                'USERNAME': username,
                'PASSWORD': password,
                'CONTAINER': container,
            },
            'static': 'selectel://user'
        },
    )


@pytest.fixture(autouse=True)
def autouse_db(db):
    """
    Makes your test environment to initialize a database
    connection automatically for each test case
    """
    pass


@pytest.fixture
def selectel_storage(settings):
    """
    Creates a ``SelectelStorage`` instance to be used in test cases
    """
    from django_selectel_storage import storage
    return storage.SelectelStorage()


@pytest.fixture
def create_file(selectel_storage):
    """
    Creates a file with a unique prefix in the Selectel Cloud Storage
    container and then deletes it (the file) after a test case finished
    """
    from django.core.files.base import ContentFile
    from django.utils import six

    created_records = []

    def file_creator(filename, content=b'', prefix=''):
        if all((
            six.PY3,
            isinstance(content, six.text_type)
        )):
            content = content.encode('UTF-8')
        container = str(uuid.uuid4())
        key = os.path.join(prefix.lstrip('/') or container, filename)
        selectel_storage.save(key, ContentFile(content, key))
        created_records.append(key)
        return key

    yield file_creator

    for key in created_records:
        selectel_storage.delete(key)


@pytest.fixture
def empty_gif():
    """A 1x1 GIF image"""
    return (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\xf0\x01\x00'
        b'\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x00'
        b'\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02'
        b'\x44\x01\x00\x3b'
    )


@pytest.fixture
def lazy_fox():
    """Just a text string"""
    return 'The *quick* brown fox jumps over the lazy dog'
