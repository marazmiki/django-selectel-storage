Configuration
=============

Here, we assume you already:

* `Have registered <https://kb.selectel.com/22063010.html>`_ an account on Selectel,
* `Spent some money <https://kb.selectel.com/27821850.html>`_ there,
* `Created a couple of containers <https://kb.selectel.com/23137040.html#BasicOverview-CreatingandConfiguringContainers>`_ and got credentials for it.

if you haven't yet, consider doing that right now.


A minimal installation
----------------------

To begin using Selectel storage as your storage, you should configure
your containers credentials:

.. code:: python

    SELECTEL_STORAGES = {
        'default': {
            'USERNAME': 'xxxx_user',
            'PASSWORD': 'p455w0rd',
            'CONTAINER': 'my-data',
        },
        'yet_another_storage': 'selectel://xxxx_user:p455w0rd2@another-container',
    }

As you already guessed, the dictionary means you can create as much configurations
as you want. Here, we have two schemas: ``default`` and ``yet_another_storage``.


**You're free to use any names for schema but strongly recommended to declare
a schema with name ``default``.**

Also, as you already guessed again, you can specify credentials either:

* As a dictionary with ``USERNAME``, ``PASSWORD`` or ``CONTAINER`` keys, or
* a URL-like string with schema ``selectel://``

Please see all available configuration options below.

.. attention::
    Credentials in examples above are hardcoded. It really sucks, don't
    do that in real life. Instead, you can store these variables in the
    environment and extract it out of there, for example, via awesome
    `python-decouple <https://pypi.org/project/python-decople/>`_ package.


Using django-selectel-storage as a default backend
--------------------------------------------------

If you want to use the storage by default, consider adding to your ``settings.py``:

.. code:: python

    DEFAULT_FILE_STORAGE = 'django_selectel_storage.storage.SelectelStorage'

in this case, the ``default`` schema will be implicitly used. Please make sure
you defined it before.


Storage initialization
----------------------

If you want to explicitly instantiate a storage, you should write something like that:

.. code:: python

    # models.py
    from django.db import models

    class Post(models.Model):
        photo = models.ImageField(storage=storage_instance)

Wondering, what ``storage_instance`` is? Well, it would be one of:

.. code:: python

    from django_selectel_storage.storage import SelectelStorage

    storage_instance = SelectelStorage()
    storage_instance = SelectelStorage('default')
    storage_instance = SelectelStorage(storage='default')

Please pay attention: the last three lines of code do the same thing: creates
a ``SelectelStorage`` instance with using ``default`` schema. Of course, you
can choose any different schema (if you've defined it of course):

.. code:: python

    storage_instance = SelectelStorage('yet_another_storage')
    storage_instance = SelectelStorage(storage='yet_another_storage')


We even create an instance via DSN (it's useful somewhere in ``./manage.py shell``, please don't do that in production):

.. code:: python

    storage_instance = SelectelStorage('selectel://user:password@container_name/')
    storage_instance = SelectelStorage(storage='selectel://user:password@container_name/')

An interesting gotcha here: if you specify a DSN (a string begins with ``selectel://``) as a first positional argument, it would
act like a dsn rather as ``storage=``



