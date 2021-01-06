"""Example Django app models."""

from django.db import models
from django_elastic_appsearch.orm import AppSearchModel, AppSearchMultiEngineModel

from example.serialisers import CarSerialiser
from example.querysets import CustomQuerySet


class Car(AppSearchModel):
    """A car."""

    class AppsearchMeta:
        appsearch_engine_name = 'cars'
        appsearch_serialiser_class = CarSerialiser

    make = models.TextField()
    model = models.TextField()
    year_manufactured = models.DateTimeField()


class Truck(AppSearchMultiEngineModel):
    """A truck."""

    class AppsearchMeta:
        appsearch_serialiser_engine_pairs = [(CarSerialiser, "trucks")]

    make = models.TextField()
    model = models.TextField()
    year_manufactured = models.DateTimeField()


class Bus(Car):
    """A bus"""

    class AppsearchMeta:
        appsearch_engine_name = "bus"

    objects = CustomQuerySet.as_manager()
