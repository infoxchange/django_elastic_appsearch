=============================
Django Elastic App Search
=============================

.. image:: https://badge.fury.io/py/django_elastic_appsearch.svg
    :target: https://badge.fury.io/py/django_elastic_appsearch

.. image:: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch.svg?branch=master
    :target: https://travis-ci.org/CorrosiveKid/django_elastic_appsearch

.. image:: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/CorrosiveKid/django_elastic_appsearch

Integrate your Django Project with Elastic App Search with ease.

Documentation
-------------

The full documentation is at https://django_elastic_appsearch.readthedocs.io.

Quickstart
----------

Install Django Elastic App Search::

    pip install django_elastic_appsearch

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_elastic_appsearch',
        ...
    )

Add the Elastic App Search URL and Key to your settings module:

.. code-block:: python

    APPSEARCH_URL = 'https://appsearch.base.url'
    APPSEARCH_API_KEY = 'some_appsearch_api_token'

Configure the Django models you want to index to Elastic App Search. You can do this by inheriting from the `AppSearchModel`, and then setting some meta options.

`AppsearchMeta.appsearch_engine_name` - Defines which engine in your app search instance your model will be indexed to.

`AppsearchMeta.appsearch_serialiser_class` - Defines how your model object will be serialised when sent to your elastic app search instance. The serialiser and fields used here derives from `Serpy <https://serpy.readthedocs.io/>`_, and you can use any of the serpy features like method fields.

Example:

.. code-block:: python

    from django_elastic_appsearch.orm import AppSearchModel
    from django_elastic_appsearch import serialisers

    class CarSerialiser(serialisers.AppSearchSerialiser):
        full_name = serialisers.MethodField()
        make = serialisers.StrField()
        model = serialisers.StrField()
        manufactured_year = serialisers.Field()

        def get_full_name(self, instance):
            return '{} {}'.format(make, model)


    class Car(AppSearchModel):

        class AppsearchMeta:
            appsearch_engine_name = 'cars'
            appsearch_serialiser_class = CarSerialiser

        make = models.CharField(max_length=100)
        model = models.CharField(max_length=100)
        manufactured_year = models.CharField(max_length=4)

Then you can call `index_to_appsearch` and `delete_from_appsearch` from your model objects.

Send the car with id 25 to app search.

.. code-block:: python

    from mymodels import Car

    car = Car.objects.get(id=25)
    car.index_to_appsearch()

Delete the car with id 21 from app search.

.. code-block:: python

    from mymodels import Car

    car = Car.objects.get(id=21)
    car.delete_from_appsearch()

You can also call `index_to_appsearch` and `delete_from_appsearch` on QuerySets of `AppSearchModel`

Send all cars where the make is 'Toyota' to app search.

.. code-block:: python

    cars = Car.objects.filter(make='Toyota')
    cars.index_to_appsearch()

Delete all cars where the make is 'Saab' from app search

.. code-block:: python

    cars = Car.objects.filter(make='Saab')
    cars.delete_from_appsearch()

If you want to speficy custom managers which also has this functionality, you can inherit from `django_elastic_appsearch.orm.AppSearchQuerySet`

.. code-block:: python

    from django_elastic_appsearch.orm import AppSearchModel, AppSearchQuerySet

    class MyCustomQuerySetManager(AppSearchQuerySet):
        def my_custom_queryset_feature(self):
            # Do Something cool
            pass

    class MyCustomModel(AppSearchModel):
        field_1 = models.CharField(max_length=100)

        # Set the custom manager
        objects = MyCustomQuerySetManager.as_manager()


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
