import requests

from datetime import datetime, timedelta
from logging import getLogger as get_logger


log = get_logger('selectel')
now = datetime.now


# get, put_stream, remove, info, list
# info -- content-length
class Auth:
    THRESHOLD = 300
    AUTH_URL = 'https://auth.selcdn.ru/'

    def __init__(self, requests):
        self.requests = requests
        self.token = ''
        self.storage_url = ''
        self.expires = now()

    def is_expired(self):
        return (self.expires - now()).total_seconds() < self.THRESHOLD

    def renew_if_need(self):
        if self.is_expired():
            self.authenticate()

    def update_expires(self, delta):
        self.expires = now() + timedelta(seconds=int(delta))

    def update_auth_token(self, new_token):
        self.requests.headers.update({'X-Auth-Token': new_token})
        self.token = new_token

    def authenticate(self):
        log.debug('Need to authentificate with %s:%s', self.user, self.key)
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

    def make_request(self, http_method, path, data=None):
        self.renew_if_need()
        url = self.build_url(path)
        handler = getattr(self.requests, http_method)

        resp = handler(url, data=data)  # type: requests.Response
        resp.raise_for_status()


class Container:
    def __init__(self):
        self.requests = self.get_requests()  # type: requests.Session
        self.auth = Auth(self.requests)
        self.container = 'todo'

    def get_requests(self):
        return requests.Session()

    def build_url(self, key):
        return '{storage_url}/{container_name}{key}'.format(
            storage_url=self.auth.storage_url,
            container_name=self.container,
            key=key,
        )

    def get(self, key):
        url = "%s/%s%s" % (self.auth.storage, container, path)
        r = self.session.get(url, headers=headers, verify=True)
        r.raise_for_status()
        return r.content

    def save(self, key, content):
        return self.auth.make_request

    def delete(self, key):
        pass

    def size(self, key):
        try:
            return self.container.info(self._name(name))['content-length']
        except requests.exceptions.HTTPError:
            raise IOError('Unable get size for %s' % name)

    def exists(self, key):
        pass

    def list(self):
        pass
