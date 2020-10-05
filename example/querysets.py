from django_elastic_appsearch.orm import AppSearchQuerySet


class CustomQuerySet(AppSearchQuerySet):
    def index_to_appsearch(self):
        pass
