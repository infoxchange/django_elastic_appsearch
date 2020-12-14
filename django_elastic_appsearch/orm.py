"""ORM features for Elastic App Search."""

import warnings
from django.apps import apps
from django.db import models

from django_elastic_appsearch.clients import (
    get_api_v1_client,
    get_api_v1_enterprise_search_client
)
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
            engine_name = self.first().get_appsearch_engine_name()
            client = self.first().get_enterprise_search_appsearch_client()
            slices = self._get_sliced_queryset()
            for queryset in slices:
                client.delete_documents(
                    engine_name=engine_name,
                    body=[item.get_appsearch_document_id() for item in queryset]
                )

    def index_to_appsearch(self, update_only=False):
        """Index the queryset."""
        if self and apps.get_app_config('django_elastic_appsearch').enabled:
            engine_name = self.first().get_appsearch_engine_name()
            client = self.first().get_enterprise_search_appsearch_client()
            slices = self._get_sliced_queryset()
            for queryset in slices:
                if update_only:
                    client.put_documents(
                        engine_name=engine_name,
                        body=[item.serialise_for_appsearch() for item in queryset]
                    )
                else:
                    client.index_documents(
                        engine_name=engine_name,
                        body=[item.serialise_for_appsearch() for item in queryset]
                    )


class AppSearchModel(models.Model):
    """A model that integrates with Elastic App Search."""

    objects = AppSearchQuerySet.as_manager()

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
    def set_appsearch_serialiser_class(cls, serialiser_class):
        """Set the app search serialiser class."""
        cls.AppsearchMeta.appsearch_serialiser_class = serialiser_class

    @classmethod
    def set_appsearch_engine_name(cls, engine_name):
        """Set the app search engine name that maps to this model."""
        cls.AppsearchMeta.appsearch_engine_name = engine_name

    @classmethod
    def get_appsearch_client(cls):
        """Get the App Search client."""
        warnings.warn(
            "`get_appsearch_client` is deprecated and will be removed in a future "
            "release. Please configure your application to use "
            "`get_enterprise_search_appsearch_client` instead.",
            DeprecationWarning
        )
        return get_api_v1_client()

    @classmethod
    def get_enterprise_search_appsearch_client(cls):
        """Get the Enterprise Search appsearch client."""
        return get_api_v1_enterprise_search_client()

    def serialise_for_appsearch(self):
        """Serialise the instance for appsearch."""
        _serialiser = self.get_appsearch_serialiser_class()
        return _serialiser(self).data

    def get_appsearch_document_id(self):
        """Get the unique document ID."""
        return '{}_{}'.format(type(self).__name__, self.pk)

    def index_to_appsearch(self, update_only=False):
        """Index the object to appsearch."""
        if apps.get_app_config('django_elastic_appsearch').enabled:
            if update_only:
                self.get_enterprise_search_appsearch_client().put_documents(
                    engine_name=self.get_appsearch_engine_name(),
                    body=[self.serialise_for_appsearch()]
                )
            else:
                self.get_enterprise_search_appsearch_client().index_documents(
                    engine_name=self.get_appsearch_engine_name(),
                    body=[self.serialise_for_appsearch()]
                )

    def delete_from_appsearch(self):
        """Delete the object from appsearch."""
        if apps.get_app_config('django_elastic_appsearch').enabled:
            self.get_enterprise_search_appsearch_client().delete_documents(
                engine_name=self.get_appsearch_engine_name(),
                body=[self.get_appsearch_document_id()]
            )
