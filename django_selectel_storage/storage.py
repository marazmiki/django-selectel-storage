# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.files.storage import Storage as DjangoStorage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import selectel
import requests


MAX_RETRIES = 3
POOL_CONNECTIONS = 50
POOL_MAXSIZE = 50


def setting(name, default=None):
    return getattr(settings, name, default)


class SelectelStorage(DjangoStorage):
    def __init__(self, **kwargs):
        self.container = selectel.storage.Container(
            auth=self.get_auth(**kwargs),
            key=self.get_key(**kwargs),
            name=self.get_container_name(**kwargs))
        self.setup_requests_adapter(**kwargs)

    def get_auth(self, **kwargs):
        return setting('SELECTEL_USERNAME')

    def get_key(self, **kwargs):
        return setting('SELECTEL_PASSWORD')

    def get_container_name(self, **kwargs):
        return setting('SELECTEL_CONTAINER_NAME')

    def get_container_url(self, **kwargs):
        return setting('SELECTEL_CONTAINER_URL')

    def get_requests_adapter(self, **kwargs):
        return requests.adapters.HTTPAdapter(
            max_retries=setting('SELECTEL_MAX_RETRIES',
                                MAX_RETRIES),
            pool_connections=setting('SELECTEL_POOL_CONNECTIONS',
                                     POOL_CONNECTIONS),
            pool_maxsize=setting('SELECTEL_POOL_MAXSIZE',
                                 POOL_MAXSIZE))

    def setup_requests_adapter(self, **kwargs):
        adapter = self.get_requests_adapter(**kwargs)
        self.mount_requests_adapter('http://', adapter)
        self.mount_requests_adapter('https://', adapter)

    def mount_requests_adapter(self, prefix, adapter):
        self.container.storage.session.mount(prefix, adapter)

    def get_base_url(self):
        base_url = self.get_container_url()
        if base_url:
            return base_url.rstrip('/')
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
        # if six.PY3:
        #     self.container.put_stream_py3(self._name(name), content)
        # else:
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
            list(self.container.list(self._name(path)).keys())
        )

    def size(self, name):
        try:
            return self.container.info(self._name(name))['content-length']
        except requests.exceptions.HTTPError:
            raise IOError('Unable get size for %s' % name)

    def url(self, name):
        return os.path.join(self.get_base_url().rstrip('/'),  name.lstrip('/'))


class SelectelStaticStorage(SelectelStorage):
    container_name = setting('SELECTEL_STATIC_CONTAINER_NAME')
    base_url = setting('SELECTEL_STATIC_BASE_URL')
