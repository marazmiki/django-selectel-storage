# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.files.storage import Storage as DjangoStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils import six
import io
import os
import selectel
import requests


def setting(name, default=None):
    return getattr(settings, name, default)


class SelectelStorage(DjangoStorage):
    def __init__(self, **kwargs):
        self.container = selectel.storage.Container(
            auth=self.get_auth(**kwargs),
            key=self.get_key(**kwargs),
            name=self.get_container_name())

        adapt = requests.adapters.HTTPAdapter(max_retries=3,
                                              pool_connections=50,
                                              pool_maxsize=50)
        self.container.storage.session.mount('http://', adapt)
        self.container.storage.session.mount('https://', adapt)

    def get_auth(self):
        return setting('SELECTEL_USERNAME')

    def get_key(self):
        return setting('SELECTEL_PASSWORD')

    def get_container_name(self):
        return setting('SELECTEL_CONTAINER_NAME')

    def get_container_url(self):
        return setting('SELECTEL_CONTAINER_URL')

    def get_requests_adapter(self):
        pass

    def mount_requests_adapter(self, prefix, adapter):
        self.container.storage.session.mount(prefix, adapter)

    def get_base_url(self):
        base_url = self.get_container_url()
        if base_url:
            return base_url
        else:
            return '{netloc}/{container}'.format(
                netloc=self.container.storage.auth.storage,
                container=self.get_container_name()
            )

    def _name(self, name):
        return '/' + name.lstrip('/')

    def _open(self, name, mode='rb'):
        return ContentFile(self.container.get(self._name(name)))

    def _save(self, name, content):
        if six.PY3:
            content = io.BytesIO(content.file)
        self.container.put_stream(self._name(name), content)
        return name

    def delete(self, name):
        self.container.remove(self._name(name), force=True)

    def exists(self, name):
        try:
            self.container.info(self._name(name))
            return True
        except selectel.storage.requests.exceptions.HTTPError:
            return False

    def listdir(self, path):
        return (
            [],
            self.container.list(self._name(path)).keys()
        )

    def size(self, name):
        return self.container.info(self._name(name))['content-length']

    def url(self, name):
        return os.path.join(self.get_base_url().rstrip('/'),  name.lstrip('/'))


class SelectelStaticStorage(SelectelStorage):
    container_name = setting('SWIFT_STATIC_CONTAINER_NAME')
    base_url = setting('SWIFT_STATIC_BASE_URL')
