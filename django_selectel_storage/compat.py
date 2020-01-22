import sys

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

try:
    TEXT_TYPE = unicode
except NameError:
    TEXT_TYPE = str


def b(s):
    return s.encode('latin-1') if PY3 else s
