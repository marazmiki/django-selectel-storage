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
    settings.SELECTEL_STORAGES['default']['CUSTOM_DOMAIN'] = url
    sel_storage = storage.SelectelStorage()
    assert url == sel_storage.url('' + appendix)


@pytest.mark.parametrize('custom_domain, expected_url', [
    pytest.param('one.com', 'https://one.com/photo.jpg', id='no schema'),
    pytest.param('http://two.com', 'http://two.com/photo.jpg', id='http'),
    pytest.param('https://three/', 'https://three/photo.jpg', id='https'),
])
def test_get_base_url_custom_domain(custom_domain, expected_url, settings):
    settings.SELECTEL_STORAGES['default']['CUSTOM_DOMAIN'] = custom_domain
    assert expected_url == storage.SelectelStorage().url('photo.jpg')
