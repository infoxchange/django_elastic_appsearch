#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for the ORM methods."""

from django.utils import timezone
from django_elastic_appsearch import serialisers
from elastic_app_search import Client
from elastic_enterprise_search import AppSearch

from example.models import Car
from example.serialisers import CarSerialiser

from .base import BaseElasticAppSearchClientTestCase


class TestORM(BaseElasticAppSearchClientTestCase):
    """Test Django Elastic App Search ORM functions."""

    def setUp(self):
        """Setup the patches and test data."""
        super().setUp()
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

    def test_get_appsearch_client(self):
        """Test `get_appsearch_client` class method."""
        client = Car.objects.first().get_appsearch_client()
        self.assertIsInstance(client, Client)

    def test_get_enterprise_search_appsearch_client(self):
        """Test `get_enterprise_search_appsearch_client` class method."""
        client = Car.objects.first().get_enterprise_search_appsearch_client()
        self.assertIsInstance(client, AppSearch)

    def test_model_object_index(self):
        """Test indexing a model object to appsearch."""
        car = Car.objects.first()
        car.index_to_appsearch()
        self.assertEqual(self.client_index.call_count, 1)

    def test_model_object_update(self):
        """Test indexing a model object to appsearch as an update operation."""
        car = Car.objects.first()
        car.index_to_appsearch(update_only=True)
        self.assertEqual(self.client_update.call_count, 1)

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

    def test_queryset_update(self):
        """Test indexing a queryset to appsearch as an update operation."""
        car = Car.objects.all()
        car.index_to_appsearch(update_only=True)
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents
        self.assertEqual(self.client_update.call_count, 5)

    def test_queryset_delete(self):
        """Test deleting a queryset from appsearch."""
        car = Car.objects.all()
        car.delete_from_appsearch()
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents
        self.assertEqual(self.client_destroy.call_count, 5)

    def test_set_appsearch_serialiser_class(self):
        """Test classmethod to set an appsearch serialiser class."""

        # Define a test serialiser class.
        class TestSerialiserClass(serialisers.AppSearchSerialiser):
            test_field = serialisers.Field()

        # Set the new serialiser class to the Car model.
        Car.set_appsearch_serialiser_class(TestSerialiserClass)

        # Test if its set successfully
        serialiser_class = Car.get_appsearch_serialiser_class()
        self.assertEqual(serialiser_class, TestSerialiserClass)

        # Reset it back to original
        Car.set_appsearch_serialiser_class(CarSerialiser)

    def test_set_appsearch_engine_name(self):
        """Test classmethod to set an appsearch engine name for a model."""

        # Get the current engine name and store it
        original_engine_name = Car.get_appsearch_engine_name()

        # Set a new app search engine name
        Car.set_appsearch_engine_name('test_cars')

        # Test if its set successfully
        engine_name = Car.get_appsearch_engine_name()
        self.assertEqual(engine_name, 'test_cars')

        # Reset it back to the original
        Car.set_appsearch_engine_name(original_engine_name)
