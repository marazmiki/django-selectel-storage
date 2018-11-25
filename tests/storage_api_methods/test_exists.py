import uuid


def test_exists_returns_false_when_the_file_does_not_exist(selectel_storage):
    non_existing_file = '{0}/non-exist.txt'.format(uuid.uuid4())
    assert not selectel_storage.exists(non_existing_file)


def test_exists_returns_true_when_the_file_exists(
        selectel_storage,
        create_file
):
    existing_file = create_file('exists.txt', 'Yup, it\'s exists!')
    assert selectel_storage.exists(existing_file)
