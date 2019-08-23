#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_elastic_appsearch
------------

Tests for `django_elastic_appsearch` models module.
"""

from datetime import datetime

from django.test import TestCase
from django_elastic_appsearch.test import MockedAppSearchTestCase

from example.models import Car


class TestORM(MockedAppSearchTestCase, TestCase):
    """Test the Django Elastic App Search ORM functions."""

    def setUp(self, *args, **kwargs):
        """Load test data."""
        super().setUp(*args, **kwargs)
        datetime_now = datetime.now()
        car1 = Car(
            make='Toyota',
            model='Corolla',
            year_manufactured=datetime_now
        )
        car1.save()
        car2 = Car(
            make='Peugeot',
            model='307',
            year_manufactured=datetime_now
        )
        car2.save()

    def test_index_model_object_to_appsearch(self):
        """Test indexing a model object to App Search."""

        car = Car.objects.first()
        car.index_to_appsearch()
        self.assertAppSearchModelIndexCallCount(1)

    def test_delete_model_object_from_appsearch(self):
        """Test deleting a model object from App Search."""

        car = Car.objects.first()
        car.delete_from_appsearch()
        self.assertAppSearchModelDeleteCallCount(1)

    def test_index_queryset_to_appsearch(self):
        """Test indexing a queryset to App Search."""

        Car.objects.all().index_to_appsearch()
        self.assertAppSearchQuerySetIndexCallCount(1)

    def test_delete_queryset_from_appsearch(self):
        """Test deleting a queryset from App Search."""

        Car.objects.all().delete_from_appsearch()
        self.assertAppSearchQuerySetDeleteCallCount(1)
