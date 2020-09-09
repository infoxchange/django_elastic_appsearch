#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for save/delete signals."""

from django.test import TestCase
from django.db.models.signals import post_save, post_delete

from django_elastic_appsearch.signals import post_save_receiver
from django_elastic_appsearch.signals import post_delete_receiver

from django_elastic_appsearch.decorators import disable_auto_indexing

from example.models import Car


class TestSignals(TestCase):
    """Test signals."""

    def test_auto_indexing_signals(self):
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
