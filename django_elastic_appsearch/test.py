"""Django app search test utilites."""

# pylint:disable=invalid-name
# `setUp` and `addCleanup` derives from the unittests library.
# `assertAppSearchModelIndexCallCount`, `assertAppSearchModelDeleteCallCount`,
# `assertAppSearchQuerySetIndexCallCount` and
# `assertAppSearchQuerySetDeleteCallCount` follows the same camel case pattern
# from the python unittests library.

from unittest.mock import patch


class MockedAppSearchTestCase:
    """
    A test case which mocks the calls to the app search instance.

    You will have access to the following assert methods:
    * `self.assertAppSearchQuerySetIndexCallCount`
        - Lets you assert how many times `AppSearchQuerySet.index_to_appsearch`
          was called.
        - Usage: `self.assertAppSearchQuerySetIndexCallCount(2)`
    * `self.assertAppSearchQuerySetDeleteCallCount`
        - Lets you assert how many times
          `AppSearchQuerySet.delete_from_appsearch` was called.
        - Usage: `self.assertAppSearchQuerySetDeleteCallCount(2)`
    * `self.assertAppSearchModelIndexCallCount`
        - Lets you assert how many times
          `AppSearchModel.index_to_appsearch` was called.
        - Usage: `self.assertAppSearchModelIndexCallCount(2)`
    * `self.assertAppSearchModelDeleteCallCount`
        - Lets you assert how many times
          `AppSearchModel.delete_from_appsearch` was called.
        - Usage: `self.assertAppSearchModelDeleteCallCount(2)`
    Note that the call counts depend on your chunk size configuration.
    The default chunk size is 100.

    Example:
    If you call index_to_appsearch on a queryset of 250 objects, with
    the default chunk size of 100, you should see 3 calls.
    Example code below.

    ```
    queryset_with_250_objects = SomeAppSearchModel.objects.filter(some_filter)
    queryset_with_250_objects.index_to_appsearch()
    self.assertAppSearchQuerySetIndexCallCount(3)
    ```

    Important Note: The call counts will count up for all classes derived from
    `AppSearchModel`. You will not be able to get call counts for each of your
    app search models. The counts will reset for each test method.
    """

    def setUp(self, *args, **kwargs):
        """Initialise app search mocks."""
        queryset_class = kwargs.get('queryset_class', 'django_elastic_appsearch.orm.AppSearchQuerySet.')

        queryset_index_to_appsearch = patch(
            f'{queryset_class}index_to_appsearch'
        )
        queryset_delete_from_appsearch = patch(
            f'{queryset_class}delete_from_appsearch'
        )

        model_index_to_appsearch = patch(
            'django_elastic_appsearch.orm.BaseAppSearchModel._index_to_appsearch'
        )
        model_delete_from_appsearch = patch(
            'django_elastic_appsearch.orm.BaseAppSearchModel._delete_from_appsearch'
        )

        self.queryset_index_to_appsearch = queryset_index_to_appsearch.start()
        self.queryset_delete_from_appsearch = \
            queryset_delete_from_appsearch.start()
        self.model_index_to_appsearch = model_index_to_appsearch.start()
        self.model_delete_from_appsearch = model_delete_from_appsearch.start()

        self.addCleanup(queryset_index_to_appsearch.stop)
        self.addCleanup(queryset_delete_from_appsearch.stop)
        self.addCleanup(model_index_to_appsearch.stop)
        self.addCleanup(model_delete_from_appsearch.stop)

        super().setUp()

    def assertAppSearchModelIndexCallCount(self, call_count):
        """Check the call count on `BaseAppSearchModel._index_to_appsearch`."""
        self.assertEqual(self.model_index_to_appsearch.call_count, call_count)

    def assertAppSearchModelDeleteCallCount(self, call_count):
        """Check the call count on `BaseAppSearchModel._delete_from_appsearch`."""
        self.assertEqual(
            self.model_delete_from_appsearch.call_count,
            call_count
        )

    def assertAppSearchQuerySetIndexCallCount(self, call_count):
        """Check the call count on `AppSearchQueryset.index_to_appsearch`."""
        self.assertEqual(
            self.queryset_index_to_appsearch.call_count,
            call_count
        )

    def assertAppSearchQuerySetDeleteCallCount(self, call_count):
        """Check the call count on `AppSearchQueryset.delete_from_appsearch`."""
        self.assertEqual(
            self.queryset_delete_from_appsearch.call_count,
            call_count
        )

# pylint:enable=invalid-name
