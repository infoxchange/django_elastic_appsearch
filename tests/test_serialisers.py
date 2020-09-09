#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for serialisers."""

from django.test import TestCase
from django.utils import timezone

from django_elastic_appsearch.decorators import disable_auto_indexing

from example.models import Car
from example.serialisers import CarSerialiser


class TestAppSearchSerialiser(TestCase):
    """Test serialisers."""

    @disable_auto_indexing(Car)
    def test_app_search_serialiser(self):
        """Test the `AppSearchSerialiser`."""

        timezone_now = timezone.now()
        # Create a car
        car = Car(
            make='Toyota',
            model='Corolla',
            year_manufactured=timezone_now
        )
        car.save()

        # Instantiate a serialiser object with the new car object
        car_serialiser = CarSerialiser(car)
        data = car_serialiser.data

        # Test if the Car is serialised as expected
        self.assertEqual(data.get('id'), car.get_appsearch_document_id())
        self.assertEqual(data.get('object_type'), 'Car')
        self.assertEqual(data.get('make'), 'Toyota')
        self.assertEqual(data.get('model'), 'Corolla')
        self.assertEqual(data.get('verbose_name'), 'Toyota Corolla')
        self.assertEqual(data.get('year_manufactured'), timezone_now)
