=====
Usage
=====

To use Django Elastic App Search in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_elastic_appsearch.apps.DjangoAppSearchConfig',
        ...
    )

Add Django Elastic App Search's URL patterns:

.. code-block:: python

    from django_elastic_appsearch import urls as django_elastic_appsearch_urls


    urlpatterns = [
        ...
        url(r'^', include(django_elastic_appsearch_urls)),
        ...
    ]
