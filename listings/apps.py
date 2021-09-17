from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _

class ListingsConfig(AppConfig):
    name = 'listings'
    label = 'listings'
    verbose_name = _('Listings')

    namespace = 'listings'
