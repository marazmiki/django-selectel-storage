import pytest
from pytest import param as p

from django_selectel_storage import exceptions as exs
from django_selectel_storage.storage import SelectelStorage
from django_selectel_storage.utils import parse_dsn

OPTS = {
    'MAX_RETRIES': 3,
    'POOL_CONNECTIONS': 50,
    'POOL_MAXSIZE': 50,
    'REQUESTS_FACTORY': 'django_selectel_storage.utils.requests_factory',
}


@pytest.mark.parametrize('dsn, exc', [
    p('s3://', exs.InvalidSchema,
      id='invalid schema'),
    p('selectel://', exs.EmptyContainerName,
      id='empty credentials'),
    p('selectel://container', exs.EmptyUsername,
      id='no username and password provided'),
    p('selectel://user@container', exs.EmptyPassword,
      id='no password provided'),
    p('selectel://user:@container', exs.EmptyPassword,
      id='an empty password provided'),
    p('selectel://:password@container', exs.EmptyUsername,
      id='an empty username provided'),
    p('selectel://user:password', exs.EmptyContainerName,
      id='a container name not provided'),
    p('selectel://user:password@', exs.EmptyContainerName,
      id='a container name is empty'),
])
def test_parse_dsn_exceptions(dsn, exc):
    with pytest.raises(exc) as actual_ex:
        parse_dsn(dsn)
        assert isinstance(actual_ex, exc)


@pytest.mark.parametrize('dsn, expected_pairs', [
    p('selectel://usr:pwd@container', {
        'USERNAME': 'usr',
        'PASSWORD': 'pwd',
        'CONTAINER': 'container'},
      id='no trailing slashes'),
    p('selectel://john:example@container/', {
        'USERNAME': 'john',
        'PASSWORD': 'example',
        'CONTAINER': 'container'},
      id='there is a trailing slash'),
    p('selectel://john:example@custom.domain.com/my-container',  {
        'USERNAME': 'john',
        'PASSWORD': 'example',
        'CONTAINER': 'my-container',
        'CUSTOM_DOMAIN': 'custom.domain.com'
    }, id='a custom domain given')
])
def test_parse_dsn(dsn, expected_pairs):
        results = parse_dsn(dsn)
        for k, v in expected_pairs.items():
            assert results[k] == v


@pytest.mark.parametrize('args, kwargs, expected', [
    pytest.param([], {}, 'default',
                 id='no args presented'),
    pytest.param(['default'], {}, 'default',
                 id='the only positional arg looking like a schema name'),
    pytest.param(['customized'], {}, 'customized',
                 id='the only positional arg is a non-default schema name'),
    pytest.param([], {'storage': 'default'}, 'default',
                 id='the only keyword argument storage='),
    # pytest.param(['selectel://user:pass@container'], {}, 'default',
    #              id='the only positional arg looking like a DSN'),
    pytest.param([], {'dsn': 'selectel://user:pass@container'}, {
        'CONTAINER': 'container',
        'USERNAME': 'user',
        'PASSWORD': 'pass',
        'CUSTOM_DOMAIN': None,
        'OPTIONS': OPTS,
    },
                 id='the keyword argument dsn='),
    pytest.param([], {'dsn': 'selectel://user:pass@ex.com/container'}, {
        'CONTAINER': 'container',
        'USERNAME': 'user',
        'PASSWORD': 'pass',
        'CUSTOM_DOMAIN': 'ex.com',
        'OPTIONS': OPTS,
    },
                 id='the keyword argument dsn= with a custom domain'),
    pytest.param([], {'container': 'container-mega',
                      'username': 'user',
                      'password': 'pass'}, {
        'CONTAINER': 'container-mega',
        'USERNAME': 'user',
        'PASSWORD': 'pass',
        'CUSTOM_DOMAIN': None,
        'OPTIONS': OPTS,
    },
                 id='a few keyword arguments'),
])
def test_parse_config(settings, args, kwargs, expected):
    settings.SELECTEL_STORAGES = {
        'default': {
            'USERNAME': 'john',
            'PASSWORD': 'secret',
            'CONTAINER': 'container-1',
        },
        'customized': {
            'USERNAME': 'jane',
            'PASSWORD': 'secret2',
            'CONTAINER': 'container-2',
        },
        'static': 'selectel://user'
    }
    storage = SelectelStorage(*args, **kwargs)
    conf = storage.config

    if isinstance(expected, str):
        assert conf == settings.SELECTEL_STORAGES[expected]
    else:
        assert conf == expected

    # 1. Storage()  # no args
    # 2. Storage('default') # the same as storage=default
    # 3. Storage(storage='default')  # default schema, the same as 1)
    # 4. Storage('selectel://user:pass@container') # the same as 5)
    # 5. Storage(dsn='selectel://user:pass@container')
    # 6. Storage(dsn='selectel://user:pass@example.com/container')
    # 7. Storage(container='container', user='...', password='', options=None)
