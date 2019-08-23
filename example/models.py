"""Example Django app models."""

from datetime import datetime

from django.db import models
from django.test import TestCase

from django_elastic_appsearch.orm import AppSearchModel

from example.serialisers import CarSerialiser


class Car(AppSearchModel):
    """A car."""

    class AppsearchMeta:
        appsearch_engine_name = 'cars'
        appsearch_serialiser_class = CarSerialiser

    make = models.TextField()
    model = models.TextField()
    year_manufactured = models.DateTimeField()
