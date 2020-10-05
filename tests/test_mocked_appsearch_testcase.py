#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for `MockedAppSearchTestCase`."""

from django.test import TestCase
from django.utils import timezone
from django_elastic_appsearch.test import MockedAppSearchTestCase
from django_elastic_appsearch.decorators import disable_auto_indexing

from example.models import Car, Bus


class TestMockedAppSearchWithCustomQuerySetTestCase(MockedAppSearchTestCase, TestCase):
    """Test the `MockedAppSearchTestCase`."""

    def setUp(self, *args, **kwargs):
        """Load test data."""
        kwargs['queryset_class'] = 'example.querysets.CustomQuerySet.'
        super().setUp(*args, **kwargs)
        timezone_now = timezone.now()
        bus1 = Bus(
            make='Volvo',
            model='Volgren Optimus',
            year_manufactured=timezone_now
        )
        bus1.save()

    def test_mocked_index_queryset_to_appsearch(self):
        """Test indexing a queryset to App Search is mocked."""

        Bus.objects.all().index_to_appsearch()
        self.assertAppSearchQuerySetIndexCallCount(1)

    def test_mocked_delete_queryset_from_appsearch(self):
        """Test deleting a queryset from App Search is mocked."""

        Bus.objects.all().delete_from_appsearch()
        self.assertAppSearchQuerySetDeleteCallCount(1)


class TestMockedAppSearchTestCase(MockedAppSearchTestCase, TestCase):
    """Test the `MockedAppSearchTestCase`."""

    @disable_auto_indexing(Car)
    def setUp(self, *args, **kwargs):
        """Load test data."""
        super().setUp(*args, **kwargs)
        timezone_now = timezone.now()
        car1 = Car(
            make='Toyota',
            model='Corolla',
            year_manufactured=timezone_now
        )
        car1.save()
        car2 = Car(
            make='Peugeot',
            model='307',
            year_manufactured=timezone_now
        )
        car2.save()

    def test_mocked_index_model_object_to_appsearch(self):
        """Test indexing a model object to App Search is mocked."""

        car = Car.objects.first()
        car.index_to_appsearch()
        self.assertAppSearchModelIndexCallCount(1)

    def test_mocked_delete_model_object_from_appsearch(self):
        """Test deleting a model object from App Search is mocked."""

        car = Car.objects.first()
        car.delete_from_appsearch()
        self.assertAppSearchModelDeleteCallCount(1)

    def test_mocked_index_queryset_to_appsearch(self):
        """Test indexing a queryset to App Search is mocked."""

        Car.objects.all().index_to_appsearch()
        self.assertAppSearchQuerySetIndexCallCount(1)

    def test_mocked_delete_queryset_from_appsearch(self):
        """Test deleting a queryset from App Search is mocked."""

        Car.objects.all().delete_from_appsearch()
        self.assertAppSearchQuerySetDeleteCallCount(1)
