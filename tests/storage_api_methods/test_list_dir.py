import os
import uuid
import pytest


def test_listdir_not_found(selectel_storage):
    assert selectel_storage.listdir('_this_dir_does_not_exist/') == ([], [])


@pytest.mark.parametrize(
    argnames='var_name, expected_items',
    argvalues=[
        ('files', {'file.img', 'hello.pdf'}),
        ('dirs', set()),
    ],

    ids=['files', 'directories - always empty']
)
def test_listdir_works(
        selectel_storage,
        create_file,
        var_name,
        expected_items
):
    prefix = '{0}/listdir'.format(uuid.uuid4())
    root = 'test-list/'

    for f in ['file.img', 'hello.pdf', 'hello/image.png', 'hello/text.txt']:
        create_file(root + f, prefix=prefix)

    dirs, files = selectel_storage.listdir(os.path.join(prefix, root))

    assert {_ for _ in locals()[var_name]} == expected_items
