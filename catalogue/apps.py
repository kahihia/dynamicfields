from django.apps import apps
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _

from dashboard.application import OscarConfig
from dashboard.utils.loading import get_class


class CatalogueOnlyConfig(OscarConfig):
    label = 'catalogue'
    name = 'catalogue'
    verbose_name = _('Catalogue')

    namespace = 'catalogue'

    def ready(self):

        super().ready()

        self.detail_view = get_class('catalogue.views', 'ProductDetailView')
        self.catalogue_view = get_class('catalogue.views', 'CatalogueView')
       
    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('', self.catalogue_view.as_view(), name='index'),
            re_path(
                r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',
                self.detail_view.as_view(), name='detail'),
           
        ]
        return self.post_process_urls(urls)


class CatalogueConfig(CatalogueOnlyConfig):
    """
    Composite class combining Products with Reviews
    """
