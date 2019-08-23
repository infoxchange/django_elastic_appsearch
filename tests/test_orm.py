#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for the ORM methods."""

from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

from example.models import Car


class TestORM(TestCase):
    """Test Django Elastic App Search ORM functions."""

    def setUp(self):
        """Setup the patches and test data."""
        super().setUp()
        client_index = patch('elastic_app_search.Client.index_documents')
        client_destroy = patch('elastic_app_search.Client.destroy_documents')

        self.client_index = client_index.start()
        self.client_destroy = client_destroy.start()

        self.addCleanup(client_index.stop)
        self.addCleanup(client_destroy.stop)

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

    def test_model_object_index(self):
        """Test indexing a model object to appsearch."""
        car = Car.objects.first()
        car.index_to_appsearch()
        self.assertEqual(self.client_index.call_count, 1)

    def test_model_object_delete(self):
        """Test deleting a model object from appsearch."""
        car = Car.objects.first()
        car.delete_from_appsearch()
        self.assertEqual(self.client_destroy.call_count, 1)

    def test_queryset_index(self):
        """Test indexing a queryset to appsearch."""
        car = Car.objects.all()
        car.index_to_appsearch()
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents
        self.assertEqual(self.client_index.call_count, 5)

    def test_queryset_delete(self):
        """Test deleting a queryset from appsearch."""
        car = Car.objects.all()
        car.delete_from_appsearch()
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents
        self.assertEqual(self.client_destroy.call_count, 5)
