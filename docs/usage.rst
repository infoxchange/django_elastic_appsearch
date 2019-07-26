=====
Usage
=====

To use Django Elastic App Search in a project, add it to your `INSTALLED_APPS`:

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
