=======================
django-selectel-storage
=======================



.. image:: https://badge.fury.io/py/django-selectel-storage.svg
    :target: https://badge.fury.io/py/django-selectel-storage

.. image:: https://img.shields.io/pypi/l/django-selectel-storage
    :target: https://raw.githubusercontent.com/marazmiki/django-selectel-storage/master/LICENSE
    :alt: The project license

.. image:: https://travis-ci.org/marazmiki/django-selectel-storage.svg?branch=master
    :target: https://travis-ci.org/marazmiki/django-selectel-storage
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/marazmiki/django-selectel-storage/badge.svg?branch=master
    :target: https://coveralls.io/r/marazmiki/django-selectel-storage?branch=master
    :alt: Code coverage percentage

.. image:: https://pypip.in/wheel/django-selectel-storage/badge.svg
     :target: https://pypi.python.org/pypi/django-selectel-storage/
     :alt: Wheel Status

.. image:: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg
     :target: https://img.shields.io/pypi/pyversions/django-selectel-storage.svg
     :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/djversions/django-selectel-storage.svg
     :target: https://pypi.org/project/django-selectel-storage/
     :alt: Supported Django versions

.. image:: https://readthedocs.org/projects/django-selectel-storage/badge/?version=latest
     :target: https://django-ulogin.readthedocs.io/ru/latest/?badge=latest
     :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/f143275acdf249328a4968b62a94e100
   :alt: Codacy Badge
   :target: https://app.codacy.com/manual/marazmiki/django-selectel-storage?utm_source=github.com&utm_medium=referral&utm_content=marazmiki/django-selectel-storage&utm_campaign=Badge_Grade_Dashboard


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

Please see details in the `documentation <https://django-selectel-storage.readthedocs.io/en/latest/>`_.
