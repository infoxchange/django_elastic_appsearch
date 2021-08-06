#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for the ORM methods."""

from django.utils import timezone
from django_elastic_appsearch import serialisers
from elastic_app_search import Client
from elastic_enterprise_search import AppSearch

from example.models import Car, Truck
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
        Car.set_appsearch_engine_name("test_cars")

        # Test if its set successfully
        engine_name = Car.get_appsearch_engine_name()
        self.assertEqual(engine_name, "test_cars")

        # Reset it back to the original
        Car.set_appsearch_engine_name(original_engine_name)

    def test_serialise_for_appsearch(self):
        car = Car.objects.first()
        self.assertEqual('Car_1', car.serialise_for_appsearch()['id'])


class TestMultipleEngineModel(BaseElasticAppSearchClientTestCase):

    class TestSerialiserClass(serialisers.AppSearchSerialiser):
        model = serialisers.Field()

    class OtherSerialiserClass(serialisers.AppSearchSerialiser):
        make = serialisers.Field()

    def setUp(self):
        """Setup the patches and test data."""
        super().setUp()
        # Create 22 trucks
        for i in range(0, 22):
            timezone_now = timezone.now()
            # Create a truck
            truck = Truck(
                make="Make {}".format(i),
                model="Model {}".format(i),
                year_manufactured=timezone_now,
            )
            truck.save()

        # Set the engines and serialisers on the Truck model.
        pairs = [
            (TestMultipleEngineModel.TestSerialiserClass, "test_cars"),
            (TestMultipleEngineModel.OtherSerialiserClass, "other_cars"),
        ]
        Truck.set_appsearch_serialiser_engine_pairs(pairs)

    def test_set_multiple_serialiser_engine_pairs(self):
        """Test classmethod to set serialiser and engine pairs"""

        # Test if its set successfully
        pairs = Truck.get_appsearch_serialiser_engine_pairs()
        self.assertEqual(pairs[0][0], TestMultipleEngineModel.TestSerialiserClass)
        self.assertEqual(pairs[0][1], "test_cars")
        self.assertEqual(pairs[1][0], TestMultipleEngineModel.OtherSerialiserClass)
        self.assertEqual(pairs[1][1], "other_cars")

    def test_serialise_for_appsearch(self):
        truck = Truck.objects.first().serialise_for_appsearch()
        self.assertEqual({'id': 'Truck_1', 'object_type': 'Truck', 'model': 'Model 0'}, truck[0])
        self.assertEqual({'id': 'Truck_1', 'object_type': 'Truck', 'make': 'Make 0'}, truck[1])

    def test_model_object_index(self):
        """Test indexing a model object to appsearch."""
        truck = Truck.objects.first()
        truck.index_to_appsearch()
        self.assertEqual(self.client_index.call_count, 2)

    def test_model_object_update(self):
        """Test indexing a model object to appsearch as an update operation."""
        truck = Truck.objects.first()
        truck.index_to_appsearch(update_only=True)
        self.assertEqual(self.client_update.call_count, 2)

    def test_model_object_delete(self):
        """Test deleting a model object from appsearch."""
        truck = Truck.objects.first()
        truck.delete_from_appsearch()
        self.assertEqual(self.client_destroy.call_count, 2)

    def test_queryset_index(self):
        """Test indexing a queryset to appsearch."""
        truck = Truck.objects.all()
        truck.index_to_appsearch()
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents, over 2 engines
        self.assertEqual(self.client_index.call_count, 10)

    def test_queryset_update(self):
        """Test indexing a queryset to appsearch as an update operation."""
        truck = Truck.objects.all()
        truck.index_to_appsearch(update_only=True)
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents, over 2 engines
        self.assertEqual(self.client_update.call_count, 10)

    def test_queryset_delete(self):
        """Test deleting a queryset from appsearch."""
        truck = Truck.objects.all()
        truck.delete_from_appsearch()
        # Note that the app search chunk size is set to 5 in `tests.settings`
        # Therefore you should see 5 calls to cover 22 documents, over 2 engines
        self.assertEqual(self.client_destroy.call_count, 10)
