#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for Django Elastic App Search settings configurations."""

from unittest.mock import patch

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
from django.test import override_settings

from django_elastic_appsearch.apps import DjangoAppSearchConfig

from example.models import Car

from .base import BaseElasticAppSearchClientTestCase


class TestDjangoElasticAppSearchSettings(BaseElasticAppSearchClientTestCase):
    """Test django_elastic_appsearch settings configurations."""

    def setUp(self):
        """Setup."""
        super().setUp()
        self.original_config = apps.get_app_config('django_elastic_appsearch')

    @override_settings()
    def test_appsearch_host_config_check(self):
        """Test `APPSEARCH_HOST` configuration check."""
        del settings.APPSEARCH_HOST
        with self.assertRaises(ImproperlyConfigured):
            DjangoAppSearchConfig(
                app_name=self.original_config.name,
                app_module=self.original_config.module
            )

    @override_settings()
    def test_appsearch_api_key_config_check(self):
        """Test `APPSEARCH_API_KEY` configuration check."""
        del settings.APPSEARCH_API_KEY
        with self.assertRaises(ImproperlyConfigured):
            DjangoAppSearchConfig(
                app_name=self.original_config.name,
                app_module=self.original_config.module
            )

    @override_settings(APPSEARCH_HOST=None)
    def test_appsearch_host_is_none(self):
        """Test setting None for `APPSEARCH_HOST` disables the app."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertFalse(config.enabled)
        self.assertIsNone(config.api_v1_base_endpoint)

    @override_settings(APPSEARCH_API_KEY=None)
    def test_appsearch_api_key_is_none(self):
        """Test setting None for `APPSEARCH_API_KEY` disables the app."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertFalse(config.enabled)

    @override_settings(APPSEARCH_USE_HTTPS=False)
    def test_appsearch_use_https_setting(self):
        """Test `APPSEARCH_USE_HTTPS` setting."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertFalse(config.use_https)

    @override_settings(APPSEARCH_CHUNK_SIZE=25)
    def test_appsearch_chunk_size_setting(self):
        """Test `APPSEARCH_CHUNK_SIZE` setting."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertEqual(config.chunk_size, 25)

    @override_settings()
    def test_appsearch_chunk_size_default(self):
        """Test when `APPSEARCH_CHUNK_SIZE` is not set, defaults to 100."""
        del settings.APPSEARCH_CHUNK_SIZE
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertEqual(config.chunk_size, 100)

    @override_settings(APPSEARCH_INDEXING_ENABLED=False)
    def test_appsearch_indexing_enabled_setting(self):
        """Test `APPSEARCH_INDEXING_ENABLED` setting."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertFalse(config.enabled)

    @override_settings(APPSEARCH_INDEXING_ENABLED=False)
    def test_disabling_indexing(self):
        """Test disabling app search indexing."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module,
        )
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
        with patch(
            'django_elastic_appsearch.orm.apps.get_app_config',
            autospec=True,
            return_value=config
        ):
            car = Car.objects.first()
            car.index_to_appsearch()
            car.delete_from_appsearch()

            car_queryset = Car.objects.all()
            car_queryset.index_to_appsearch()
            car_queryset.delete_from_appsearch()

            self.assertEqual(self.client_index.call_count, 0)
            self.assertEqual(self.client_destroy.call_count, 0)
