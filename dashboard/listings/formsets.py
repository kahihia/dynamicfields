from django import forms
from django.core import exceptions
from django.forms.models import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from dashboard.utils.loading import get_classes, get_model

Listing = get_model('listings', 'Listing')
ListingClass = get_model('listings', 'ListingClass')
ListingAttribute = get_model('listings', 'ListingAttribute')
AttributeOptionGroup = get_model('listings', 'AttributeOptionGroup')
AttributeOption = get_model('listings', 'AttributeOption')

( ListingAttributesForm,
 AttributeOptionForm) = \
    get_classes('dashboard.listings.forms',
                 ('ListingAttributesForm',
                 'AttributeOptionForm'))


ListingAttributesFormSet = inlineformset_factory(ListingClass,
                                                 ListingAttribute,
                                                 form=ListingAttributesForm,
                                                 extra=3)


AttributeOptionFormSet = inlineformset_factory(AttributeOptionGroup,
                                               AttributeOption,
                                               form=AttributeOptionForm,
                                               extra=3)
