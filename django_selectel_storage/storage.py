import os

import requests

from django.core.files import base, storage

from .selectel import Container
from .utils import read_config


MAX_RETRIES = 3
POOL_CONNECTIONS = 50
POOL_MAXSIZE = 50


class SelectelStorage(storage.Storage):
    def __init__(self, *args, **kwargs):
        self.config = read_config(args, kwargs)
        self.container = Container()

    def _open(self, name, mode='rb'):
        return base.ContentFile(self.container.open(name))

    def _save(self, name, content):
        self.container.save(name, content)
        return name

    def delete(self, name):
        self.container.delete(name)

    def exists(self, name):
        return self.container.exists(name)

    def listdir(self, path):
        items = self.container.list(path)
        return (
            [],
            [i[len(path):].lstrip('/') for i in items.keys()
             if len(i) > len(path)]
        )

    def size(self, name):
        return self.container.size(name)

    def url(self, name):
        base_url = self.get_container_url()
        if base_url:
            base_url = base_url.rstrip('/')
        else:
            base_url = '{netloc}/{container}'.format(
                netloc=self.auth.storage,
                container=self.get_container_name()
            )
        return os.path.join(base_url.rstrip('/'),  name.lstrip('/'))


class SelectelStaticStorage(SelectelStorage):
    pass
