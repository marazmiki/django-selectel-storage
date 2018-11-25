import os
import uuid


def test_not_failed_when_deleting_a_non_existing_file(selectel_storage):
    non_existing_file = os.path.join(str(uuid.uuid4()), 'non-exists.txt')
    selectel_storage.delete(non_existing_file)


def test_delete_actually_works(selectel_storage, create_file):
    existing_file = create_file('DELETE_ME.txt', 'Please, delete me!')

    assert selectel_storage.exists(existing_file)

    selectel_storage.delete(existing_file)

    assert not selectel_storage.exists(existing_file)
