import io
from datetime import datetime, timedelta
from logging import getLogger as get_logger

import requests
from django.utils.module_loading import import_string

from .compat import TEXT_TYPE

log = get_logger('selectel')
now = datetime.now


# get, put_stream, remove, info, list
# info -- content-length
class Auth:
    THRESHOLD = 300
    AUTH_URL = 'https://auth.selcdn.ru/'

    def __init__(self, config, requests):
        self.config = config
        self.requests = requests
        self.token = ''
        self.storage_url = ''
        self.expires = now()

    @property
    def user(self):
        return self.config['USERNAME']

    @property
    def key(self):
        return self.config['PASSWORD']

    @property
    def container_name(self):
        return self.config['CONTAINER']

    def build_url(self, key):
        self.renew_if_need()
        return '{storage_url}/{name}/{key}'.format(
            storage_url=self.storage_url.rstrip('/'),
            name=self.container_name.strip('/'),
            key=key.lstrip('/'),
        )

    def is_expired(self):
        return (self.expires - now()).total_seconds() < self.THRESHOLD

    def renew_if_need(self):
        if self.is_expired() or not self.storage_url:
            self.authenticate()

    def update_expires(self, delta):
        self.expires = now() + timedelta(seconds=int(delta))

    def update_auth_token(self, new_token):
        self.requests.headers.update({'X-Auth-Token': new_token})
        self.token = new_token

    def authenticate(self):
        log.debug('Need to authenticate with %s:%s', self.user, self.key)
        resp = self.requests.get(self.AUTH_URL, headers={
            'X-Auth-User': self.user,
            'X-Auth-Key': self.key
        })
        if resp.status_code != 204:
            log.debug('Got an unexpected response from auth: %s', resp.content)
            raise Exception("Selectel: Unexpected status code: %s" %
                            resp.status_code)
        self.storage_url = resp.headers['X-Storage-Url']
        self.update_expires(resp.headers['X-Expire-Auth-Token'])
        self.update_auth_token(resp.headers['X-Auth-Token'])

    def perform_request(self, http_method, key,
                        raise_exception=False, **kwargs):
        self.renew_if_need()
        resp = getattr(self.requests, http_method)(
            self.build_url(key),
            **kwargs
        )  # type: requests.Response
        if resp.status_code == 401:
            log.debug('Got an unexpected 401 error, reauthenticate.')
            self.authenticate()
            return self.perform_request(http_method, key, raise_exception,
                                        **kwargs)
        if raise_exception:
            resp.raise_for_status()
        return resp


class Container:
    def __init__(self, config):
        self.config = config
        self.requests = self.get_requests()  # type: requests.Session
        self.auth = Auth(self.config, self.requests)

    @property
    def name(self):
        return self.auth.container_name

    def get_requests(self):
        return import_string(self.config.get(
            'REQUESTS_FACTORY',
            'django_selectel_storage.utils.requests_factory'
        ))(self.config)

    def build_url(self, key):
        return self.auth.build_url(key)

    def perform_request(self, http_method, key,
                        raise_exception=False, **kwargs):
        return self.auth.perform_request(http_method, key,
                                         raise_exception=raise_exception,
                                         **kwargs)

    def open(self, key):
        return self.perform_request('get', key, raise_exception=True,
                                    stream=True).raw

    def save(self, key, content, metadata=None):
        self.perform_request('put', key, data=content, raise_exception=True)
        return key

    def delete(self, key):
        self.perform_request('delete', key, raise_exception=False)

    def size(self, key):
        try:
            resp = self.perform_request('head', key, raise_exception=True)
            return int(resp.headers['Content-Length'])
        except requests.exceptions.HTTPError:
            raise IOError('Failed to get file size of {}'.format(key))

    def exists(self, key):
        return self.perform_request('head', key).status_code == 200

    def list(self, key):
        return {
            x['name']: x for x in self.perform_request('get', '', params={
                'format': 'json',
                'prefix': key
            }).json()
        }

    def send_me_file(self, filename, size):
        headers = {
            'Content-Type': 'x-storage/sendmefile+inplace',
            'X-Object-Meta-Sendmefile-Max-Size': TEXT_TYPE(size),
            'X-Object-Meta-Sendmefile-Disable-Web': 'yes',
            'X-Object-Meta-Sendmefile-Allow-Overwrite': 'no',
            'X-Object-Meta-Sendmefile-Ignore-Filename': 'yes',
            'X-Filename': '/' + TEXT_TYPE(filename),
        }
        self.perform_request('put', filename, data=io.BytesIO(),
                             headers=headers, raise_exception=True)
        return self.build_url(filename)
