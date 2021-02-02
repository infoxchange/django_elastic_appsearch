"""ORM features for Elastic App Search."""

from django.apps import apps
from django.db import models

from django_elastic_appsearch.clients import get_api_v1_client
from django_elastic_appsearch.slicer import slice_queryset


class AppSearchQuerySet(models.QuerySet):
    """A queryset that supports Elastic App Search functions."""

    def _get_sliced_queryset(self):
        """Return the sliced queryset."""
        chunk_size = apps.get_app_config('django_elastic_appsearch').chunk_size
        return slice_queryset(self, chunk_size)

    def delete_from_appsearch(self):
        """Delete from appsearch."""
        responses = []
        if self and apps.get_app_config('django_elastic_appsearch').enabled:
            for (_, engine_name) in self.first().get_appsearch_serialiser_engine_pairs():
                client = self.first().get_appsearch_client()
                slices = self._get_sliced_queryset()
                for queryset in slices:
                    responses += client.destroy_documents(
                        engine_name,
                        [item.get_appsearch_document_id() for item in queryset]
                    )

        return responses

    def index_to_appsearch(self, update_only=False):
        """Index the queryset."""
        responses = []
        if self and apps.get_app_config('django_elastic_appsearch').enabled:
            for (_, engine_name) in self.first().get_appsearch_serialiser_engine_pairs():
                client = self.first().get_appsearch_client()
                slices = self._get_sliced_queryset()
                for queryset in slices:
                    if update_only:
                        responses += client.update_documents(
                            engine_name,
                            [item.serialise_for_appsearch(engine_name) for item in queryset]
                        )
                    else:
                        responses += client.index_documents(
                            engine_name,
                            [item.serialise_for_appsearch(engine_name) for item in queryset]
                        )

        return responses


class BaseAppSearchModel(models.Model):
    """
    Base class for AppSearchModel and AppSearchMultiEngineModel.

    Implements operations that interact with app search for both.
    """

    objects = AppSearchQuerySet.as_manager()

    class Meta:
        """Meta options for the app search model."""

        abstract = True

    @classmethod
    def get_appsearch_client(cls):
        """Get the App Search client."""
        return get_api_v1_client()

    def get_appsearch_document_id(self):
        """Get the unique document ID."""
        return "{}_{}".format(type(self).__name__, self.pk)

    def _destroy_document(self, engine_name):
        """Destroys document in specified engine."""
        return self.get_appsearch_client().destroy_documents(engine_name, [self.get_appsearch_document_id()])

    def _index_to_engine(self, engine_name, update_only):
        """Index to specified engine."""
        if update_only:
            return self.get_appsearch_client().update_documents(
                engine_name, self._serialise_for_appsearch()
            )
        else:
            return self.get_appsearch_client().index_documents(
                engine_name, self._serialise_for_appsearch()
            )

    def _serialise_for_appsearch(self, engine_name=None):
        """
        Serialise for app search.

        Args:
            engine_name (str): Optional, only serialise for the specified engine.

        Returns:
        list of serialiser output: List of the document serialised with the available
            serialisers in order, or the serialiser for the specified engine.
        """
        _pairs = self.get_appsearch_serialiser_engine_pairs()
        if engine_name is not None:
            _pairs = [pair for pair in _pairs if pair[1] == engine_name]

        return [serialiser(self).data for (serialiser, _) in _pairs]

    def _index_to_appsearch(self, update_only=False):
        """
        Indexes to all specified app search engines.

        Args:
            update_only (bool): Update rather than index the documents. Defaults to false.

        Returns:
            list of app search responses: responses from app search by engine, in order
        """
        if apps.get_app_config("django_elastic_appsearch").enabled:
            return [self._index_to_engine(engine_name, update_only) for (_, engine_name)
                    in self.get_appsearch_serialiser_engine_pairs()]
        return []

    def _delete_from_appsearch(self):
        """
        Delete from all specified app search engines.

        Returns:
            list of app search responses: responses from app search by engine, in order
        """
        if apps.get_app_config("django_elastic_appsearch").enabled:
            return [self._destroy_document(engine_name) for (_, engine_name)
                    in self.get_appsearch_serialiser_engine_pairs()]
        return []


class AppSearchModel(BaseAppSearchModel):
    """A model that integrates with Elastic App Search."""

    class Meta:
        """Meta options for the app search model."""

        abstract = True

    @classmethod
    def get_appsearch_serialiser_class(cls):
        """Get the app search serialiser class."""
        return cls.AppsearchMeta.appsearch_serialiser_class

    @classmethod
    def get_appsearch_engine_name(cls):
        """Get the app search engine name that maps to this model."""
        return cls.AppsearchMeta.appsearch_engine_name or cls.__name__

    @classmethod
    def get_appsearch_serialiser_engine_pairs(cls):
        """
        Get the serialisers and engines.

        Returns:
        list of (class, string): List of pairs of app search serialisers and engine names
            to be used together.
        """
        return [(cls.get_appsearch_serialiser_class(), cls.get_appsearch_engine_name())]

    @classmethod
    def set_appsearch_serialiser_class(cls, serialiser_class):
        """Set the app search serialiser class."""
        cls.AppsearchMeta.appsearch_serialiser_class = serialiser_class

    @classmethod
    def set_appsearch_engine_name(cls, engine_name):
        """Set the app search engine name that maps to this model."""
        cls.AppsearchMeta.appsearch_engine_name = engine_name

    def serialise_for_appsearch(self, engine_name=None):
        """Serialise the instance for appsearch."""
        return super()._serialise_for_appsearch(engine_name=(engine_name or self.get_appsearch_engine_name()))[0]

    def index_to_appsearch(self, update_only=False):
        """Index the object to appsearch."""
        response = super()._index_to_appsearch(update_only=update_only)
        return response[0] if response else None

    def delete_from_appsearch(self):
        """Delete the object from appsearch."""
        response = super()._delete_from_appsearch()
        return response[0] if response else None


class AppSearchMultiEngineModel(BaseAppSearchModel):
    """A model that integrates with multiple Elastic App Search engines."""

    class Meta:
        """Meta options for the multi engine app search model."""

        abstract = True

    @classmethod
    def set_appsearch_serialiser_engine_pairs(cls, pairs):
        """
        Set the serialisers and engines.

        Args:
            pairs (list of (class, string)): List of pairs of app search serialisers and engine names
            to be used together.
        """
        cls.AppsearchMeta.appsearch_serialiser_engine_pairs = pairs

    @classmethod
    def get_appsearch_serialiser_engine_pairs(cls):
        """
        Get the serialisers and engines.

        Returns:
        list of (class, string): List of pairs of app search serialisers and engine names
            to be used together.
        """
        return cls.AppsearchMeta.appsearch_serialiser_engine_pairs

    def serialise_for_appsearch(self, engine_name=None):
        """Serialise the instance for appsearch."""
        return super()._serialise_for_appsearch(engine_name=engine_name)

    def index_to_appsearch(self, update_only=False):
        """Index the object to appsearch."""
        return super()._index_to_appsearch(update_only=update_only)

    def delete_from_appsearch(self):
        """Delete the object from appsearch."""
        return super()._delete_from_appsearch()
