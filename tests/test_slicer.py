#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for the queryset slicer."""

from django.test import TestCase
from django.utils import timezone

from django_elastic_appsearch.slicer import slice_queryset
from django_elastic_appsearch.decorators import disable_auto_indexing

from example.models import Car


class TestSlicer(TestCase):
    """Test Queryset slicer."""

    @disable_auto_indexing(Car)
    def setUp(self, *args, **kwargs):
        """Add the test cars."""
        # Create 22 cars
        for i in range(0, 22):
            timezone_now = timezone.now()
            # Create a car
            car = Car(
                make='Make {}'.format(i),
                model='Model {}'.format(i),
                year_manufactured=timezone_now
            )
            car.save()

    def test_slice_queryset(self):
        """Test if the `slice_queryset` works as expected."""
        # Get a queryset of all 22 cars
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

    def test_slicing_queryset_smaller_than_chunk_size(self):
        """Test if slicing a queryset smaller than the specified chunk size."""
        # Get a queryset of all 22 cars
        queryset = Car.objects.all()
        self.assertEqual(queryset.count(), 22)

        # Slice the queryset into chunks of 30
        slices = slice_queryset(queryset, 30)

        # First slice should have all 22 cars
        for queryset in slices:
            self.assertEqual(queryset.count(), 22)
