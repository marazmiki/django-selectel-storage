# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.files.base import ContentFile
from django_selectel_storage.storage import SelectelStorage


class Test(test.TestCase):
    def setUp(self):
        self.storage = SelectelStorage()

    def test_get_text_mode(self):
        code = 'Hey\nhey\n\hey'
        self.storage.save('hello.txt', ContentFile(code))
        content = self.storage._open('hello.txt')
        self.assertEquals(code, content.read())
        self.storage.delete('hello.txt')

    def test_get_binary_mode(self):
        with open('django_selectel_storage/tests/empty.gif', 'rb') as fp:
            self.storage.save('empty.gif', fp)
            fp.seek(0)
            content = self.storage._open('empty.gif', 'rb')

            self.assertEquals(fp.read(), content.read())
            self.storage.delete('empty.gif')

    def test_exists_not(self):
        self.assertFalse(self.storage.exists('non_exists.txt'))

    def test_exists_yes(self):
        self.storage.save('exists.txt', ContentFile('Hey'))
        self.assertTrue(self.storage.exists('exists.txt'))
        self.storage.delete('exists.txt')

    def test_size_(self):
        self.storage.save('exists.txt', ContentFile('Hey'))
        self.assertEquals(3, self.storage.size('exists.txt'))
        self.storage.delete('exists.txt')

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
        self.storage.save('file.txt', ContentFile('Hey'))
        self.assertEquals(([], ['/file.txt']), self.storage.listdir('/'))
