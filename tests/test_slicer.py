#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for the queryset slicer."""

from datetime import datetime

from django.test import TestCase
from django_elastic_appsearch.slicer import slice_queryset

from example.models import Car


class TestSlicer(TestCase):
    """Test Queryset slicer."""

    def test_slice_queryset(self):
        """Test if the `slice_queryset` works as expected."""

        # Create 22 cars
        for i in range(0, 22):
            datetime_now = datetime.now()
            # Create a car
            car = Car(
                make='Make {}'.format(i),
                model='Model {}'.format(i),
                year_manufactured=datetime_now
            )
            car.save()

        # Get a queryset of all cars
        queryset = Car.objects.all()
        self.assertEqual(queryset.count(), 22)

        # Slice the queryset into chunks of 5
        slices = slice_queryset(queryset, 5)

        # First 4 chunks should have 5 cars in each queryset
        # and the last chunk should have 2 cars.
        for index, queryset in enumerate(slices):
            if index < 4:
                self.assertEqual(queryset.count(), 5)
            else:
                self.assertEqual(queryset.count(), 2)
