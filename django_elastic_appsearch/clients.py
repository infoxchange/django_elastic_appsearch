"""Django App Search Client utilities."""

from django.apps import apps
from elastic_app_search import Client


def get_api_v1_client():
    """Return the app search client."""
    config = apps.get_app_config('django_elastic_appsearch')

    base_endpoint = config.api_v1_base_endpoint
    api_key = config.api_key
    use_https = config.use_https

    return Client(
        api_key=api_key,
        base_endpoint=base_endpoint,
        use_https=use_https
    )
