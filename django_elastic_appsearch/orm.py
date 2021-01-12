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
        if self and apps.get_app_config('django_elastic_appsearch').enabled:
            for (_, engine_name) in self.first().get_appsearch_serialiser_engine_pairs():
                client = self.first().get_appsearch_client()
                slices = self._get_sliced_queryset()
                for queryset in slices:
                    client.destroy_documents(
                        engine_name,
                        [item.get_appsearch_document_id() for item in queryset]
                    )

    def index_to_appsearch(self, update_only=False):
        """Index the queryset."""
        if self and apps.get_app_config('django_elastic_appsearch').enabled:
            for (_, engine_name) in self.first().get_appsearch_serialiser_engine_pairs():
                client = self.first().get_appsearch_client()
                slices = self._get_sliced_queryset()
                for queryset in slices:
                    if update_only:
                        client.update_documents(
                            engine_name,
                            [item.serialise_for_appsearch(engine_name) for item in queryset]
                        )
                    else:
                        client.index_documents(
                            engine_name,
                            [item.serialise_for_appsearch(engine_name) for item in queryset]
                        )


class SuperAppSearchModel(models.Model):
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

    def index_to_appsearch(self, update_only=False):
        pass

    def serialise_for_appsearch(self, *args):
        pass

    @classmethod
    def get_appsearch_serialiser_engine_pairs(cls):
        pass

    def _destroy_document(self, engine_name):
        return self.get_appsearch_client().destroy_documents(engine_name, [self.get_appsearch_document_id()])

    def _index_to_engine(self, engine_name, update_only):
        if update_only:
            return self.get_appsearch_client().update_documents(
                engine_name, [self.serialise_for_appsearch()]
            )
        else:
            return self.get_appsearch_client().index_documents(
                engine_name, [self.serialise_for_appsearch()]
            )


class AppSearchModel(SuperAppSearchModel):
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
        return [(cls.get_appsearch_serialiser_class(), cls.get_appsearch_engine_name())]

    @classmethod
    def set_appsearch_serialiser_class(cls, serialiser_class):
        """Set the app search serialiser class."""
        cls.AppsearchMeta.appsearch_serialiser_class = serialiser_class

    @classmethod
    def set_appsearch_engine_name(cls, engine_name):
        """Set the app search engine name that maps to this model."""
        cls.AppsearchMeta.appsearch_engine_name = engine_name

    def serialise_for_appsearch(self, *args):
        """Serialise the instance for appsearch."""
        _serialiser = self.get_appsearch_serialiser_class()
        return _serialiser(self).data

    def index_to_appsearch(self, update_only=False):
        """Index the object to appsearch."""
        if apps.get_app_config("django_elastic_appsearch").enabled:
            self._index_to_engine(self.get_appsearch_engine_name(), update_only=update_only)

    def delete_from_appsearch(self):
        """Delete the object from appsearch."""
        if apps.get_app_config("django_elastic_appsearch").enabled:
            return self._destroy_document(self.get_appsearch_engine_name())


class AppSearchMultiEngineModel(SuperAppSearchModel):
    class Meta:
        """Meta options for the app search model."""

        abstract = True

    @classmethod
    def set_appsearch_serialiser_engine_pairs(cls, pairs):
        cls.AppsearchMeta.appsearch_serialiser_engine_pairs = pairs

    @classmethod
    def get_appsearch_serialiser_engine_pairs(cls):
        return cls.AppsearchMeta.appsearch_serialiser_engine_pairs

    def serialise_for_appsearch(self, engine_name=None):
        "Serialise the instance for appsearch."""
        _pairs = self.get_appsearch_serialiser_engine_pairs()
        if engine_name is not None:
            _pairs = [pair for pair in _pairs if pair[1] == engine_name]

        return [serialiser(self).data for (serialiser, _) in _pairs]

    def index_to_appsearch(self, update_only=False):
        """Index the object to appsearch."""
        if apps.get_app_config("django_elastic_appsearch").enabled:
            return [self._index_to_engine(engine_name, update_only) for (_, engine_name)
                    in self.get_appsearch_serialiser_engine_pairs()]

    def delete_from_appsearch(self):
        """Delete the object from appsearch."""

        if apps.get_app_config("django_elastic_appsearch").enabled:
            return [self._destroy_document(engine_name) for (_, engine_name)
                    in self.get_appsearch_serialiser_engine_pairs()]
