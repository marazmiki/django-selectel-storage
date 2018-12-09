from django.core.files import base, storage

from .selectel import Container
from .utils import read_config


class SelectelStorage(storage.Storage):
    def __init__(self, *args, **kwargs):
        self.config = read_config(args, kwargs)
        self.container = Container(self.config)

    def _open(self, name, mode='rb'):
        return base.ContentFile(self.container.open(name).read())

    def _save(self, name, content):
        self.container.save(name, content, metadata=None)
        return name

    def delete(self, name):
        self.container.delete(name)

    def exists(self, name):
        return self.container.exists(name)

    def listdir(self, path):
        dirs, files = set(), set()
        results = self.container.list(path)
        for key, metadata in results.items():
            bits = key[len(path):].lstrip('/').split('/')
            (dirs if len(bits) > 1 else files).add(bits[0])
        return list(dirs), list(files)

    def size(self, name):
        return self.container.size(name)

    def url(self, name):
        if not self.config.get('CUSTOM_DOMAIN'):
            return self.container.build_url(name)
        else:
            custom_domain = self.config['CUSTOM_DOMAIN'].rstrip('/')
            if not custom_domain.lower().startswith(('http://', 'https://')):
                custom_domain = 'https://{0}'.format(custom_domain)
            return '{custom_domain}/{name}'.format(
                custom_domain=custom_domain,
                name=name.strip('/'),
            )

    def save_with_metadata(self, name, content, metadata=None):
        self.container.save(name, content, metadata=metadata)
        return name


class SelectelStaticStorage(SelectelStorage):
    pass
