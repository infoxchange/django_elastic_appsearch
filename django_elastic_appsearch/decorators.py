from contextlib import ContextDecorator

from django.db.models.signals import post_save, post_delete
from django.conf import settings

from django_elastic_appsearch.signals import post_save_receiver
from django_elastic_appsearch.signals import post_delete_receiver


class disable_auto_indexing(ContextDecorator):
    """Context decorator to disable auto indexing signals.

    Can be used as a context manager:
    >>> with disable_auto_indexing('Model'):
    >>>     obj.save()

    Can be used as a method decorator:
    >>> @disable_auto_indexing('Model')
    >>> some_operation()
    """

    def __init__(self, model):
        self.model = model
        # This should use get_app_config()
        # But then can't easily test..
        self.auto_indexing = getattr(
            settings, 'APPSEARCH_AUTOINDEXING_ENABLED', False
        )

    def __enter__(self):
        """Disable post save/delete signals."""
        post_save.disconnect(
            post_save_receiver,
            sender=self.model
        )
        post_delete.disconnect(
            post_delete_receiver,
            sender=self.model
        )

    def __exit__(self, exc_type, exc_value, traceback):
        """Re-enable post save/delete signals."""

        if not self.auto_indexing:
            return

        post_save.connect(
            post_save_receiver,
            sender=self.model
        )
        post_delete.connect(
            post_delete_receiver,
            sender=self.model
        )
