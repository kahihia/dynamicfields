from django.apps import apps
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from dashboard.application import OscarDashboardConfig
from dashboard.utils.loading import get_class


class DashboardConfig(OscarDashboardConfig):
    label = 'dashboard'
    name = 'dashboard'
    verbose_name = _('Dashboard')

    namespace = 'dashboard'

    def ready(self):
        self.index_view = get_class('dashboard.views', 'IndexView')

        self.catalogue_app = apps.get_app_config('catalogue_dashboard')
        self.listings_app = apps.get_app_config('listings_dashboard')
        
    def get_urls(self):
        from django.contrib.auth import views as auth_views

        urls = [
            path('', self.index_view.as_view(), name='index'),
            path('catalogue/', include(self.catalogue_app.urls[0])),
            path('listings/', include(self.listings_app.urls[0])),
        ]
        return self.post_process_urls(urls)
