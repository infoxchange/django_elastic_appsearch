#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for save/delete signals."""

from django.test import TestCase, override_settings
from django.db.models.signals import post_save, post_delete

from django_elastic_appsearch.signals import post_save_receiver
from django_elastic_appsearch.signals import post_delete_receiver
from django_elastic_appsearch.decorators import disable_auto_indexing

from example.models import Car


class TestAutoIndexingSignals(TestCase):
    """Test auto-indexing signals."""

    def setUp(self):
        """Setup."""
        super().setUp()

        # Mock auto-index enabled
        # This needs to be done manually even with overriding the setting
        post_save.connect(post_save_receiver, sender=Car)
        post_delete.connect(post_delete_receiver, sender=Car)

    @override_settings(APPSEARCH_AUTOINDEXING_ENABLED=True)
    def test_auto_indexing_signals_enabled(self):
        """Test if the save/delete signals are connected/disconnected."""

        # disconnect() returns True if the signal is attached
        self.assertTrue(
            post_save.disconnect(post_save_receiver, sender=Car)
        )
        self.assertTrue(
            post_delete.disconnect(post_delete_receiver, sender=Car)
        )

        with disable_auto_indexing(Car):
            # disconnect() returns False if the signal is not attached
            self.assertFalse(
                post_save.disconnect(post_save_receiver, sender=Car)
            )
            self.assertFalse(
                post_delete.disconnect(post_delete_receiver, sender=Car)
            )

        # When context manager exists, signals should be re-attached
        self.assertTrue(
            post_save.disconnect(post_save_receiver, sender=Car)
        )
        self.assertTrue(
            post_delete.disconnect(post_delete_receiver, sender=Car)
        )

    def test_auto_indexing_signals_disabled(self):
        """Test if the save/delete signals remain disconnected."""

        with disable_auto_indexing(Car):
            pass

        # Tests that the decorator obeys default auto_indexing setting of False
        # Returns false because signal should not be re-attached by default
        # after context manager exits.
        self.assertFalse(
            post_save.disconnect(post_save_receiver, sender=Car)
        )
        self.assertFalse(
            post_delete.disconnect(post_delete_receiver, sender=Car)
        )
