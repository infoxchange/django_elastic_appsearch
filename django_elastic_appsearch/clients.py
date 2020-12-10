"""Django App Search Client utilities."""

import warnings
from django.apps import apps
from elastic_app_search import Client
from elastic_enterprise_search import AppSearch


def get_api_v1_client():
    """Return the app search client."""
    warnings.warn(
        "`get_api_v1_client` is deprecated and will be removed in a future release. "
        "Please configure your application to use "
        "`get_api_v1_enterprise_search_client` instead.",
        DeprecationWarning
    )
    config = apps.get_app_config('django_elastic_appsearch')

    base_endpoint = config.api_v1_base_endpoint
    api_key = config.api_key
    use_https = config.use_https

    return Client(
        api_key=api_key,
        base_endpoint=base_endpoint,
        use_https=use_https
    )


def get_api_v1_enterprise_search_client():
    """Return the enterprise-search appsearch client."""
    config = apps.get_app_config('django_elastic_appsearch')

    appsearch_host = config.appsearch_host
    api_key = config.api_key
    use_https = config.use_https

    url = '{}://{}'.format(
        'https' if use_https else 'http',
        appsearch_host
    )

    return AppSearch(url, http_auth=api_key)
