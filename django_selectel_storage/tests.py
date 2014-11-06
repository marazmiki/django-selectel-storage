# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.files.base import ContentFile
from django_selectel_storage.storage import SelectelStorage
from django.utils import six
import uuid
import requests


LAZY_FOX = 'The *quick* brown fox jumps over the lazy dog'
EMPTY_GIF = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\xf0\x01\x00' \
            b'\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x0a\x00\x00' \
            b'\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02' \
            b'\x44\x01\x00\x3b'


class ExistingFile(object):
    def __init__(self, test_case, fn, cnt, file_class=ContentFile):
        self.test = test_case
        self.filename = self.test.session_id + '_' + fn
        self.content = file_class(cnt)

    def __enter__(self):
        self.test.storage.save(self.filename, self.content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.test.storage.delete(self.filename)


class TestBase(test.TestCase):
    def setUp(self):
        self.storage = SelectelStorage()
        self.session_id = uuid.uuid4().hex

    def existing_file(self, filename, content=''):
        return ExistingFile(self, filename, content)


class TestListDirMethod(TestBase):
    """
    Tests for `listdir` storage method
    """

    def test_listdir_empty(self):
        # Create unique directory to avoid race conditions during
        # concurrent test running
        self.storage.container.storage.session.put(
            url='{storage}/{container}{path}'.format(
                storage=self.storage.container.storage.auth.storage,
                container=self.storage.container.name,
                path=self.session_id
            ),
            headers={
                'Content-Type': 'application/directory'
            })
        self.assertEquals(
            first=([], []),
            second=self.storage.listdir('/' + self.session_id)
        )

    def test_listdir_non_empty(self):
        with self.existing_file('file.img') as f:
            dirs, files = self.storage.listdir('/')
            self.assertIn('/' + f.filename, files)


class TestExistsMethod(TestBase):
    """
    Tests for `exists` storage method
    """
    def test_exists_not(self):
        filename = self.session_id + '_non_exists.txt'
        self.assertFalse(self.storage.exists(filename))

    def test_exists_yes(self):
        with self.existing_file('file.img') as f:
            self.assertTrue(self.storage.exists(f.filename))


class TestDeleteMethod(TestBase):
    """
    Tests for `exists` storage method
    """
    def test_delete_non_exists(self):
        self.storage.delete(self.session_id + '_non_exists.txt')

    def test_delete_exists(self):
        with self.existing_file('exists.txt') as f:
            self.assertTrue(self.storage.exists(f.filename))
            self.storage.delete(f.filename)
            self.assertFalse(self.storage.exists(f.filename))


class TestUrlMethod(TestBase):
    """
    Tests for `url` storage method
    """
    def test_url_with_container_default_name(self):
        self.assertEquals(
            self.storage.get_base_url() + '/index.html',
            self.storage.url('index.html')
        )

    def test_container_custom_name(self):
        url = 'https://selectel.com'
        with self.settings(SELECTEL_CONTAINER_URL=url):
            storage = SelectelStorage()
            self.assertEquals(url, storage.get_base_url())


class TestSizeMethod(TestBase):
    """
    Tests for `url` storage method
    """
    def test_size_for_non_existing_file(self):
        def raise_exception():
            self.storage.size(self.session_id + '_non_exists.txt')
        self.assertRaises(requests.exceptions.HTTPError, raise_exception)

    def test_zero_size_file(self):
        with self.existing_file('zero_size.txt') as f:
            self.assertEquals(0, self.storage.size(f.filename))

    def test_size_binary_file(self):

        with self.existing_file('empty.gif', content=EMPTY_GIF) as f:
            self.assertEquals(len(EMPTY_GIF), self.storage.size(f.filename))

    def test_size_text_file(self):
        if six.PY3:
            self.skipTest('Does not work in py3')

        with self.existing_file('README.md', content=LAZY_FOX) as f:
            self.assertEquals(len(LAZY_FOX), self.storage.size(f.filename))


class TestOpenMethod(TestBase):
    """
    Tests for `_open` storage method
    """
    def test_get_binary_file(self):
        with self.existing_file('empty.gif', content=EMPTY_GIF) as f:
            content = self.storage._open(f.filename, 'rb')
            self.assertEquals(first=EMPTY_GIF,
                              second=content.read())

    def test_get_text_mode(self):
        if six.PY3:
            self.skipTest('Does not work in py3')

        with self.existing_file('file.txt', content=LAZY_FOX) as f:
            content = self.storage._open(f.filename, 'r')
            self.assertEquals(first=LAZY_FOX,
                              second=content.read())

    # def get_auth(self, **kwargs):
    # def get_key(self, **kwargs):
    # def get_container_name(self, **kwargs):
    # def get_container_url(self, **kwargs):
    # def get_requests_adapter(self):
    # def mount_requests_adapter(self, prefix, adapter):
    # *def get_base_url(self):
    # def _name(self, name):
    # def _open(self, name, mode='rb'):
    # def _save(self, name, content):
    #
    #
    # *def delete(self, name):
    # *def exists(self, name):
    # *def listdir(self, path):
    # *def size(self, name):
    # *def url(self, name):
