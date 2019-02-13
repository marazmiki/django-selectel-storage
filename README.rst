=======================
django-selectel-storage
=======================


.. image:: https://travis-ci.org/marazmiki/django-selectel-storage.svg?branch=branch
     :target: https://travis-ci.org/marazmiki/django-selectel-storage
     :alt: Travis CI building status

.. image:: https://coveralls.io/repos/github/marazmiki/django-selectel-storage/badge.svg?branch=master
     :target: https://coveralls.io/github/marazmiki/django-selectel-storage?branch=master
     :alt: Code coverage status

.. image:: https://badge.fury.io/py/django-selectel-storage.svg
     :target: http://badge.fury.io/py/django-selectel-storage
     :alt: PyPI release

.. image:: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg
     :target: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg?branch=novodel
     :alt: Supported Python versions

.. image:: https://readthedocs.org/projects/django-selectel-storage/badge/?version=latest
     :target: https://django-selectel-storage.readthedocs.io/ru/latest/?badge=latest
     :alt: Documentation Status


This application allows you easily save media and static files into Selectel cloud storage.


Installation
------------

1. Install the package

.. code:: bash

    pip install django-selectel-storage


2. Add to your settings module:

.. code:: python

    DEFAULT_FILE_STORAGE = 'django_selectel_storage.storage.SelectelStorage'
    SELECTEL_STORAGES = {
        'default': {
            'USERNAME': 'xxxx_user1',
            'PASSWORD': 'secret',
            'CONTAINER_NAME': 'bucket',
        },
        'yet-another-schema': {
            'USERNAME': 'yyyy_user2',
            'PASSWORD': 'mystery',
            'CONTAINER_NAME': 'box',

        },
    }

If you have assigned custom domain with your selectel container, you need add
the `SELECTEL_CONTAINER_NAME` attribute (trailing slash not matters)

.. code:: python

    SELECTEL_CONTAINER_URL = 'http://your.domain/'


Caveats
-------

* In python 3.x ``ContentFile`` with text mode content (not binary one) will causes ``TypeError`` due ``requests`` restrictions
