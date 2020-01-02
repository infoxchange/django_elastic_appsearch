"""Serialisers for Django models -> Elastic App Search objects."""

# pylint:disable=unused-import
from serpy import Field, MethodField, Serializer, StrField  # noqa: F401


class AppSearchSerialiser(Serializer):
    """A base serialiser to serialise Django models to app search objects."""

    id = MethodField()
    object_type = MethodField()

    def get_id(self, instance):
        """Set model pk as the document id."""
        return instance.get_appsearch_document_id()

    def get_object_type(self, instance):
        """Set model name as the object type."""
        return type(instance).__name__

# pylint:enable=unused-import
