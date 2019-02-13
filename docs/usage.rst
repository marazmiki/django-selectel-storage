Usage
=====


When using Django, in most cases, you don't need to use storage API
directly (of course, you can although), only through models, when
using ``FileField`` and ``ImageField.`` Like that:

.. code:: python

    # models.py
    class Photo(models.Model):
        file = models.ImageField()

    # somewhere else. Here, "photo" is a Photo instance.
    # you of course get it.
    with open('photo.jpg', 'rb') as fp:
        photo = Photo.objects.first()
        photo.save()


This code works regardless of a storage backend


Instancing
----------


.. code:: python

    class Photo(models.Model):
        photo = models.ImageField(storage=selectel_storage)

"But wait, what is ``selectel_storage`` here?" –– you ask. It's a good question.



.. code:: python

        # or
        photo = models.ImageField(storage=SelectelStorage(schema='default'))

        # or even:
        photo = models.ImageField(storage=SelectelStorage(
            username='',
            password='',
            container='',
        ))

        photo = models.ImageField(storage=SelectelStorage(
            'selectel://user:password@container-name/'
        ))


If you want to use all your data in the cloud, the better choice to make
the selectel storage default one (see configuration). In this case, you
can define your model this way:


.. code:: python

    from django.db import models

    class Photo(models.Model):
        photo = models.ImageField()  # no storage instance here
