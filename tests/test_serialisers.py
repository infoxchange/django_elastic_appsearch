#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for serialisers."""

from datetime import datetime

from django.test import TestCase

from example.models import Car
from example.serialisers import CarSerialiser


class TestAppSearchSerialiser(TestCase):
    """Test serialisers."""

    def test_app_search_serialiser(self):
        """Test the `AppSearchSerialiser`."""

        datetime_now = datetime.now()
        # Create a car
        car = Car(
            make='Toyota',
            model='Corolla',
            year_manufactured=datetime_now
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
        self.assertEqual(data.get('year_manufactured'), datetime_now)
