"""Elastic App Search Client base test cases."""

from unittest.mock import patch

from django.test import TestCase


class BaseElasticAppSearchClientTestCase(TestCase):
    """Base Elastic App Search Client Test case."""

    def setUp(self):
        """Initialise the patches."""
        super().setUp()
        client_index = patch('elastic_enterprise_search.AppSearch.index_documents')
        client_update = patch('elastic_enterprise_search.AppSearch.put_documents')
        client_destroy = patch('elastic_enterprise_search.AppSearch.delete_documents')

        self.client_index = client_index.start()
        self.client_update = client_update.start()
        self.client_destroy = client_destroy.start()

        self.addCleanup(client_index.stop)
        self.addCleanup(client_update.stop)
        self.addCleanup(client_destroy.stop)
