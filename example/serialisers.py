"""Example Django App Search Serialisers."""

from django_elastic_appsearch import serialisers


class CarSerialiser(serialisers.AppSearchSerialiser):
        """Car serialiser."""

        make = serialisers.StrField()
        model = serialisers.StrField()
        year_manufactured = serialisers.Field()
        verbose_name = serialisers.MethodField()

        def get_verbose_name(self, instance):
            """Verbose name of the car."""
            return '{} {}'.format(instance.make, instance.model)
