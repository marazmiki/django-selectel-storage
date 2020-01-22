import io
import tempfile
import uuid

import pytest
from django.core.files import uploadedfile

from django_selectel_storage.compat import b


@pytest.fixture
def file_id():
    return str(uuid.uuid4())


@pytest.fixture
def simple_file():
    def inner(filename, content):
        fp = tempfile.NamedTemporaryFile(delete=False)
        fp.write(content)
        fp.flush()
        return fp
    return inner


@pytest.fixture
def in_memory_file():
    def inner(filename, content):
        return uploadedfile.InMemoryUploadedFile(
            file=io.BytesIO(content),
            field_name='test_field',
            name='_save_new_file.txt',
            content_type='text/plain',
            size=0,
            charset='utf8'
        )
    return inner


@pytest.fixture
def temporary_uploaded_file():
    def inner(filename, content):
        fp = uploadedfile.TemporaryUploadedFile(
            name=filename + '.tempfile',
            content_type='text/plain',
            size=0,
            charset='utf8',
        )
        fp.write(content)
        fp.flush()
        return fp
    return inner


parametrize = pytest.mark.parametrize(
    argnames='fixture_name',
    argvalues=[
        'simple_file',
        'in_memory_file',
        'temporary_uploaded_file',
    ]
)


@parametrize
def test_save_fileobj(selectel_storage, request, file_id, fixture_name):
    filename = 'save_new_file_{0}.txt'.format(file_id)
    content = b('test content one')

    fileobj = request.getfixturevalue(fixture_name)(filename, content)
    selectel_storage.save(filename, fileobj)

    with selectel_storage.open(filename) as f:
        f.seek(0)
        assert f.read() == content


@parametrize
def test_save_seeked_fileobj(selectel_storage, request, file_id, fixture_name):
    filename = 'save_new_file_{0}.txt'.format(file_id)
    content = b('test content one')

    fileobj = request.getfixturevalue(fixture_name)(filename, content)
    fileobj.seek(0)

    selectel_storage.save(filename, fileobj)

    with selectel_storage.open(filename) as f:
        assert f.read() == content
