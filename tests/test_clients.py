#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Test cases for elastic app search client."""

from django.test import TestCase
from django_elastic_appsearch.clients import get_api_v1_client
from elastic_app_search import Client


class TestClients(TestCase):
    """Test clients."""

    def test_get_api_v1_client(self):
        """Test if the `get_api_v1_client` returns valid client."""

        client = get_api_v1_client()
        self.assertEqual(type(client), Client)
