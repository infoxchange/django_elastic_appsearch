"""Django App Search Client utilities."""

from django.apps import apps
from elastic_enterprise_search import AppSearch


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

    return AppSearch(url, bearer_auth=api_key, **config.extra_config_options)
