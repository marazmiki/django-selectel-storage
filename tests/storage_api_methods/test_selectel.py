import pytest

from django_selectel_storage import selectel


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
    ],
    ids=[
        'a negative timedelta',
        'a nullable timedelta',
        'a positive timedelta less than a thresh hold value',
        'a positive timedelta greather than a thresh hold value'
    ]
)
def test_auth_renew_if_expired(delta, expected, monkeypatch):
    def patched_authenticate(self):
        raise SystemError()

    monkeypatch.setattr(selectel.Auth, 'authenticate', patched_authenticate)

    auth = selectel.Auth(requests=None, config=None)
    auth.update_expires(delta)

    if expected:
        with pytest.raises(SystemError):
            auth.renew_if_need()
    else:
        auth.renew_if_need()
