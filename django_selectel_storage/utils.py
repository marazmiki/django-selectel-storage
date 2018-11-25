import requests

try:
    from urllib.parse import parse_qs, urlparse   # PY3
except ImportError:
    from urlparse import parse_qs, urlparse       # PY2


MAX_RETRIES = 3
POOL_CONNECTIONS = 50
POOL_MAXSIZE = 50


def extract(opts, key, default=None, cast=None):
    if key not in opts:
        return default
    return cast(opts[key][0]) if cast is not None else opts[key][0]


def parse_dsn(string):
    bits = urlparse(string)  # type:
    if bits.scheme.lower() != 'selectel':
        raise ValueError('The only supported schema here is "selectel://"')

    username = bits.username
    password = bits.password
    container = bits.hostname

    options = parse_qs(bits.query)

    return {
        'USERNAME': username,
        'PASSWORD': password,
        'CONTAINER': container,
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
            'PUBLIC_NAME': extract(
                opts=options,
                key='public_name',
                cast=str,
                default=None,
            )
        }
    }


def read_config(args, kwargs):
    if not len(args) and not kwargs:
        pass  # no arguments - using defaults
    if any((
            len(args) == 1 and not kwargs,
            kwargs.get('dsn') is not None,
    )):
        pass  # parse dsn

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
