#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for Django Elastic App Search settings configurations."""

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

from django_elastic_appsearch.apps import DjangoAppSearchConfig


class TestDjangoElasticAppSearchSettings(TestCase):
    """Test django_elastic_appsearch settings configurations."""

    def setUp(self):
        """Setup."""
        super().setUp()
        self.original_config = apps.get_app_config('django_elastic_appsearch')

    @override_settings()
    def test_appsearch_url_config_check(self):
        """Test `APPSEARCH_URL` configuration check."""
        del settings.APPSEARCH_URL
        with self.assertRaises(ImproperlyConfigured):
            config = DjangoAppSearchConfig(
                app_name=self.original_config.name,
                app_module=self.original_config.module
            )

    @override_settings()
    def test_appsearch_api_key_config_check(self):
        """Test `APPSEARCH_API_KEY` configuration check."""
        del settings.APPSEARCH_API_KEY
        with self.assertRaises(ImproperlyConfigured):
            config = DjangoAppSearchConfig(
                app_name=self.original_config.name,
                app_module=self.original_config.module
            )

    @override_settings(APPSEARCH_URL=None)
    def test_appsearch_url_is_none(self):
        """Test setting None for `APPSEARCH_URL` disables the app."""
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

    @override_settings(APPSEARCH_INDEXING_ENABLED=False)
    def test_appsearch_indexing_enabled_setting(self):
        """Test `APPSEARCH_INDEXING_ENABLED` setting."""
        config = DjangoAppSearchConfig(
            app_name=self.original_config.name,
            app_module=self.original_config.module
        )
        self.assertFalse(config.enabled)
