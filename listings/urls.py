from django.urls import include, path, re_path
from dashboard.utils.loading import get_class

from listings.views import ListingView, ListingDetailView
app_name = 'listings'

urlpatterns = [
	path('', ListingView.as_view(), name='index'),
    re_path(r'^(?P<product_slug>[\w-]*)_(?P<pk>\d+)/$',  ListingDetailView.as_view(), name='detail'),
]
