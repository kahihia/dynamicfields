from django.db import models
from datetime import datetime
"""
Vanilla product models
"""
from dashboard.listings.abstract_models import *  # noqa
from dashboard.utils.loading import is_model_registered

__all__ = ['ListingAttributesContainer']


if not is_model_registered('listings', 'ListingClass'):
    class ListingClass(AbstractListingClass):
        pass

    __all__.append('ListingClass')


if not is_model_registered('listings', 'Listing'):
    class Listing(AbstractListing):
        address = models.CharField(max_length=200)
        town = models.CharField(max_length=100)
        country = models.CharField(max_length=100)
        def __str__(self):
            return self.title

    __all__.append('Listing')


if not is_model_registered('listings', 'ListingAttribute'):
    class ListingAttribute(AbstractListingAttribute):
        pass

    __all__.append('ListingAttribute')


if not is_model_registered('listings', 'ListingAttributeValue'):
    class ListingAttributeValue(AbstractListingAttributeValue):
        pass

    __all__.append('ListingAttributeValue')


if not is_model_registered('listings', 'AttributeOptionGroup'):
    class AttributeOptionGroup(AbstractAttributeOptionGroup):
        pass

    __all__.append('AttributeOptionGroup')


if not is_model_registered('listings', 'AttributeOption'):
    class AttributeOption(AbstractAttributeOption):
        pass

    __all__.append('AttributeOption')


if not is_model_registered('listings', 'Option'):
    class Option(AbstractOption):
        pass

    __all__.append('Option')



