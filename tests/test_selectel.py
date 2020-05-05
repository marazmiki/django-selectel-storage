import io
import uuid

import pytest
import requests

from django_selectel_storage import selectel, utils


@pytest.mark.parametrize(
    argnames='delta, expected',
    argvalues=[
        (-10, True),
        (0, True),
        (10, True),
        (selectel.Auth.THRESHOLD + 10, False),
    ],
    ids=[
        'a negative timedelta',
        'a nullable timedelta',
        'a positive timedelta less than a thresh hold value',
        'a positive timedelta greather than a thresh hold value'
    ]
)
def test_auth_is_expired(delta, expected):
    auth = selectel.Auth(requests=None, config=None)
    auth.update_expires(delta)
    assert auth.is_expired() is expected


@pytest.mark.parametrize(
    argnames='delta, expected',
    argvalues=[
        (-10, True),
        (0, True),
        (10, True),
        (selectel.Auth.THRESHOLD + 10, False),
        (None, True),
    ],
    ids=[
        'a negative timedelta',
        'a nullable timedelta',
        'a positive timedelta less than a thresh hold value',
        'a positive timedelta greater than a thresh hold value',
        'empty storage_url'
    ]
)
def test_auth_renew_if_expired(delta, expected, monkeypatch):
    def patched_authenticate(self):
        raise SystemError()

    monkeypatch.setattr(selectel.Auth, 'authenticate', patched_authenticate)

    auth = selectel.Auth(requests=None, config=None)
    auth.storage_url = 'https://example.com/'

    if delta is None:
        auth.storage_url = ''
    else:
        auth.update_expires(delta)

    if expected:
        with pytest.raises(SystemError):
            auth.renew_if_need()
    else:
        auth.renew_if_need()


def test_build_url(monkeypatch):
    def patched_authenticate(self):
        self.storage_url = 'https://example.com/'
        self.update_expires(100500)

    auth = selectel.Auth(requests=None, config={
        'CONTAINER': 'bucket'
    })
    monkeypatch.setattr(selectel.Auth, 'authenticate', patched_authenticate)

    auth.renew_if_need()
    assert (
        auth.build_url('index.html') == 'https://example.com/bucket/index.html'
    )


def test_send_me_file():
    container = selectel.Container(
        config=utils.read_config([], {})
    )
    identifier = str(uuid.uuid4())

    filename = 'send_me_file-' + identifier + '.txt'
    contents = b'This is content of ' + filename.encode()

    public_upload_link = container.send_me_file(filename, len(contents))

    assert public_upload_link == container.build_url(filename)

    resp = requests.put(public_upload_link, io.BytesIO(contents))
    assert resp.status_code == 201

    resp = requests.get(public_upload_link)
    assert resp.content == contents
