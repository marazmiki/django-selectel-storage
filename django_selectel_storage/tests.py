# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.files.base import ContentFile
from django_selectel_storage.storage import SelectelStorage
import uuid


class Test(test.TestCase):
    def setUp(self):
        self.storage = SelectelStorage()
        self.uniq = uuid.uuid4().hex

    def tearDown(self):
        for file_ in ['hello.txt', 'empty.gif', 'exists.txt', 'file.txt']:
            self.storage.delete(self._file(file_))

    def _file(self, file_):
        return self.uniq + '_' + file_

    def test_get_text_mode(self):
        code = 'Hey\nhey\n\hey'
        filename = self._file('hello.txt')
        self.storage.save(filename, ContentFile(code))
        content = self.storage._open(filename)
        self.assertEquals(code, content.read())

    def test_get_binary_mode(self):
        with open('django_selectel_storage/tests/empty.gif', 'rb') as fp:
            filename = self._file('empty.gif')
            self.storage.save(filename, fp)
            fp.seek(0)
            content = self.storage._open(filename, 'rb')
            self.assertEquals(fp.read(), content.read())

    def test_exists_not(self):
        filename = self._file('non_exists.txt')
        self.assertFalse(self.storage.exists(filename))

    def test_exists_yes(self):
        filename = self._file('exists.txt')
        self.storage.save(filename, ContentFile('Hey'))
        self.assertTrue(self.storage.exists(filename))

    def test_size_(self):
        filename = self._file('exists.txt')
        self.storage.save(filename, ContentFile('Hey'))
        self.assertEquals(3, self.storage.size(filename))

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

    def test_listdir_empty(self):
        self.assertEquals(([], []), self.storage.listdir('/'))

    def test_listdir_non_empty(self):
        filename = self._file('file.txt')
        self.storage.save(filename, ContentFile('Hey'))
        self.assertEquals(([], ['/' + filename]), self.storage.listdir('/'))
