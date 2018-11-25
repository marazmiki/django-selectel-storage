def test_get_zero_length_str(selectel_storage, create_file):
    file = create_file('zero.txt', content='')
    content = selectel_storage._open(file, 'r')
    assert content.read() == b''


def test_get_zero_length_byte(selectel_storage, create_file):
    file = create_file('zero.txt', content=b'')

    content = selectel_storage._open(file, 'r')
    assert content.read() == b''


def test_get_binary_file(selectel_storage, create_file, empty_gif):
    file = create_file('empty.gif', content=empty_gif)
    assert selectel_storage._open(file, 'rb').read() == empty_gif


def test_get_text_mode(selectel_storage, create_file, lazy_fox):
    file = create_file('file.txt', content=lazy_fox)
    assert selectel_storage._open(file, 'r').read() == lazy_fox.encode('UTF-8')
