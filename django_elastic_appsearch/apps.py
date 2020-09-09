"""Django App Search config."""

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class DjangoAppSearchConfig(AppConfig):
    """Config for the Django App Search app."""

    name = 'django_elastic_appsearch'
    verbose_name = 'Django Elastic App Search'

    def __init__(self, *args, **kwargs):
        """Initialise the config."""
        if not hasattr(settings, 'APPSEARCH_HOST'):
            raise ImproperlyConfigured(
                "You must specify the `APPSEARCH_HOST` in your settings."
            )
        if not hasattr(settings, 'APPSEARCH_API_KEY'):
            raise ImproperlyConfigured(
                "You must specify the `APPSEARCH_API_KEY` in your settings."
            )

        if settings.APPSEARCH_HOST:
            self.api_v1_base_endpoint = settings.APPSEARCH_HOST + '/api/as/v1'
        else:
            self.api_v1_base_endpoint = None

        self.api_key = settings.APPSEARCH_API_KEY

        self.use_https = getattr(settings, 'APPSEARCH_USE_HTTPS', True)

        self.chunk_size = getattr(settings, 'APPSEARCH_CHUNK_SIZE', 100)

        self.enabled = getattr(settings, 'APPSEARCH_INDEXING_ENABLED', True)

        # Don't try to index documents to app search if
        # APPSEARCH_HOST or APPSEARCH_API_KEY is set to None
        if self.api_v1_base_endpoint is None or self.api_key is None:
            self.enabled = False

        super().__init__(*args, **kwargs)
