import pytest

from django_selectel_storage.utils import parse_dsn


@pytest.mark.parametrize(
    argnames='dsn',
    argvalues=[
        ('selectel://container', ),
        ('selectel://john:example@container')
    ],
)
def test_parse_dsn(dsn):
    results = parse_dsn(dsn)
