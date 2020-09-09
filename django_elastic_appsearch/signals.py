"""Signals for Elastic App Search."""


def post_save_receiver(sender, instance, **kwargs):
    """Signal handler for when a sub-classed model has been saved."""
    instance.index_to_appsearch()


def post_delete_receiver(sender, instance, **kwargs):
    """Signal handler for when a sub-classed model has been deleted."""
    instance.delete_from_appsearch()
