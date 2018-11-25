import os
import pytest
from django_selectel_storage import storage


@pytest.fixture
def url():
    return os.getenv('SELECTEL_CONTAINER_URL', 'http://127.0.0.1/')


@pytest.mark.parametrize(
    argnames='appendix, arg',
    argvalues=[
        ('/index.html', 'index.html'),
    ],
)
def test_url(selectel_storage, appendix, arg):
    assert selectel_storage.url('').rstrip('/') + appendix \
           == selectel_storage.url(arg)


@pytest.mark.parametrize(
    argnames='appendix',
    argvalues=[
        '',
        '/',
        '////'
    ],
    ids=[
        'no trailing slashes',
        'one trailing slash',
        'multiple trailing slashes',
    ]
)
def test_get_base_url_trailing_slashes(url, settings, appendix):
    settings.SELECTEL_CONTAINER_URL = url + appendix
    sel_storage = storage.SelectelStorage()
    assert url == sel_storage.url('')
