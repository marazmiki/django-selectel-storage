=======================
django-selectel-storage
=======================


.. image:: https://badge.fury.io/py/django-selectel-storage.png
    :target: http://badge.fury.io/py/django-selectel-storage
    :alt:

.. image:: https://travis-ci.org/marazmiki/django-selectel-storage.png?branch=master
    :target: https://travis-ci.org/marazmiki/django-selectel-storage
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/marazmiki/django-selectel-storage/badge.png?branch=master
    :target: https://coveralls.io/r/marazmiki/django-selectel-storage?branch=master
    :alt: Code coverage percentage

.. image:: https://pypip.in/d/django-selectel-storage/badge.png
    :target: https://pypi.python.org/pypi/django-selectel-storage
    :alt: Latest version on PyPI

.. image:: https://pypip.in/wheel/django-selectel-storage/badge.svg
    :target: https://pypi.python.org/pypi/django-selectel-storage/
    :alt: Wheel Status

.. image:: https://pypip.in/py_versions/django-selectel-storage/badge.png
    :target: https://pypi.python.org/pypi/django-selectel-storage/
    :alt: Supported Python versions






This application allows you easily save media and static files into Selectel cloud storage.

Dependencies
------------

* `requests <http://docs.python-requests.org/en/latest/>`_ library
* `selectel-api <https://pypi.python.org/pypi/selectel-api>`_ by Kirill Goldshtein

Installation
------------

1. Install the package

.. code:: bash

    pip install django-selectel-storage


2. Add to your settings module:

.. code:: python

    DEFAULT_FILE_STORAGE = 'django_selectel_storage.storage.SelectelStorage'
    SELECTEL_USERNAME = 'xxxxxx' 
    SELECTEL_PASSWORD = 'container_password'
    SELECTEL_CONTAINER_NAME = 'container_name'

If you have assigned custom domain with your selectel container, you need add
the `SELECTEL_CONTAINER_NAME` attribute (trailing slash not matters)

.. code:: python

    SELECTEL_CONTAINER_URL = 'http://your.domain/'


Caveats
-------

* In python 3.x ``ContentFile`` with text mode content (not binary one) will causes ``TypeError`` due ``requests`` restrictions
