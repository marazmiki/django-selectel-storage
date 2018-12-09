import requests
from django.conf import settings

from .exceptions import (
    EmptyContainerName,
    EmptyPassword,
    EmptyUsername,
    InvalidSchema,
    SelectelException,
)

try:
    from urllib import parse as urlparse   # PY3
except ImportError:
    import urlparse                        # PY2


MAX_RETRIES = 3
POOL_CONNECTIONS = 50
POOL_MAXSIZE = 50

KNOWN_OPTS = (
    'max_retries',
    'pool_conns',
    'pool_maxsize'
)


def extract(opts, key, default=None, cast=None):
    if key not in opts:
        return default
    return cast(opts[key][0]) if cast is not None else opts[key][0]


def empty_username():
    raise EmptyUsername('An username should be given to access the '
                        'Selectel cloud storage')


def empty_password():
    raise EmptyPassword('A password should be given to access the'
                        'Selectel cloud storage')


def empty_container_name():
    raise EmptyContainerName('Looks like both username and password are '
                             'given, but container name seems to be empty')


def parse_dsn(string):
    bits = urlparse.urlparse(string)  # type: urlparse.ParseResult

    if bits.scheme.lower() != 'selectel':
        raise InvalidSchema('The only supported schema here is "selectel://"')

    if not bits.hostname:
        empty_container_name()

    if bits.hostname and bits.netloc.count(':') == 1:
        if bits.password is None and bits.username is None:
            empty_container_name()

        if not bits.password:
            empty_password()

        if not bits.username:
            empty_username()

    if not bits.username:
        empty_username()

    if not bits.password:
        empty_password()

    username = bits.username
    password = bits.password

    custom_domain = bits.hostname
    container = bits.path.strip('/')

    if bits.path in ['', '/']:
        custom_domain = None
        container = bits.hostname

    options = urlparse.parse_qs(bits.query)

    return {
        'USERNAME': username,
        'PASSWORD': password,
        'CONTAINER': container,
        'CUSTOM_DOMAIN': custom_domain,
        'OPTIONS': {
            'MAX_RETRIES': extract(
                opts=options,
                key='max_retries',
                cast=int,
                default=MAX_RETRIES
            ),
            'POOL_CONNECTIONS': extract(
                opts=options,
                key='pool_conns',
                cast=int,
                default=POOL_CONNECTIONS
            ),
            'POOL_MAXSIZE': extract(
                opts=options,
                key='pool_maxsize',
                cast=int,
                default=POOL_MAXSIZE
            ),
            'REQUESTS_FACTORY': extract(
                opts=options,
                key='requests_factory',
                cast=str,
                default='django_selectel_storage.utils.requests_factory'
            )
        }
    }


def read_config(args, kwargs):
    detected_schema = None

    # Case 1: Storage() with no args and kwargs
    if not args and not kwargs:
        detected_schema = 'default'

    # Case 2: the only positional argument: a data source string
    # like Storage("selectel://user:pass@name") or a schema name
    # like Storage("schema-name")
    if len(args) == 1 and not kwargs:
        try:
            return parse_dsn(args[0])
        except SelectelException:
            detected_schema = args[0]

    # Case 3: Using the "default" schema when there is not "dsn=" keyword arg.
    if kwargs.get('dsn') is None and all((
        'container' not in kwargs,
        'username' not in kwargs,
        'password' not in kwargs
    )):
        detected_schema = args[0] if args else 'default'

    # Case 4: Storage(storage='default')   default schema, the same as 1)
    if 'storage' in kwargs:
        detected_schema = kwargs['storage']

    if detected_schema is not None:
        return settings.SELECTEL_STORAGES[detected_schema]

    # 5. Storage(dsn='selectel://user:pass@container')
    if 'dsn' in kwargs:
        return parse_dsn(kwargs['dsn'])

    if all((
        'container' in kwargs,
        'username' in kwargs,
        'password' in kwargs
    )):
        dsn_format = 'selectel://{username}:{password}@{container}'
        if 'custom_domain'in kwargs:
            dsn_format = (
                'selectel://{username}:{password}@{custom_domain}/{container}'
            )
        if 'options' in kwargs:
            dsn_format += '/?'
        return parse_dsn(dsn_format.format(**kwargs))
    # 7. Storage(container='container', user='...', password='', options=None)


def requests_factory(config):
    return requests.Session()

# def get_requests_adapter(self, **kwargs):
#     return requests.adapters.HTTPAdapter(
#         max_retries=setting('SELECTEL_MAX_RETRIES',
#                             MAX_RETRIES),
#         pool_connections=setting('SELECTEL_POOL_CONNECTIONS',
#                                  POOL_CONNECTIONS),
#         pool_maxsize=setting('SELECTEL_POOL_MAXSIZE',
#                              POOL_MAXSIZE))
#
# def setup_requests_adapter(self, **kwargs):
#     adapter = self.get_requests_adapter(**kwargs)
#     self.mount_requests_adapter('http://', adapter)
#     self.mount_requests_adapter('https://', adapter)
#
# def mount_requests_adapter(self, prefix, adapter):
#     self.container.storage.session.mount(prefix, adapter)
