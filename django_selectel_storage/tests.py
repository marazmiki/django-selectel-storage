# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import test
from django.core.files.base import ContentFile
from django_selectel_storage.storage import SelectelStorage, SelectelStaticStorage


class Test(test.TestCase):
    def setUp(self):
        self.storage = SelectelStorage()

    def test_get(self):
        self.storage.save('hello.txt', ContentFile('Hey\nhey\n\hey'))
        print(self.storage.get('hello.txt'))
        self.storage.delete('hello.txt')

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
