#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django_elastic_appsearch
------------

Tests for `django_elastic_appsearch` models module.
"""

from django.test import TestCase

from django_elastic_appsearch.test import MockedAppSearchTestCase


class TestDjango_elastic_appsearch(MockedAppSearchTestCase, TestCase):

    def test_something(self):
        pass

    def tearDown(self):
        pass
