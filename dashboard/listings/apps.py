from django.urls import path
from django.utils.translation import gettext_lazy as _

from dashboard.application import OscarDashboardConfig
from dashboard.utils.loading import get_class


class ListingDashboardConfig(OscarDashboardConfig):
    label = 'listings_dashboard'
    name = 'dashboard.listings'
    verbose_name = _('Listing')


    def ready(self):
        app_name = 'listings'
        self.product_list_view = get_class('dashboard.listings.views',
                                           'ListingListView')
        self.product_lookup_view = get_class('dashboard.listings.views',
                                             'ListingLookupView')
        self.product_create_redirect_view = get_class('dashboard.listings.views',
                                                      'ListingCreateRedirectView')
        self.product_createupdate_view = get_class('dashboard.listings.views',
                                                   'ListingCreateUpdateView')
        self.product_delete_view = get_class('dashboard.listings.views',
                                             'ListingDeleteView')

        self.product_class_create_view = get_class('dashboard.listings.views',
                                                   'ListingClassCreateView')
        self.product_class_update_view = get_class('dashboard.listings.views',
                                                   'ListingClassUpdateView')
        self.product_class_list_view = get_class('dashboard.listings.views',
                                                 'ListingClassListView')
        self.product_class_delete_view = get_class('dashboard.listings.views',
                                                   'ListingClassDeleteView')
        self.attribute_option_group_create_view = get_class('dashboard.listings.views',
                                                            'AttributeOptionGroupCreateView')
        self.attribute_option_group_list_view = get_class('dashboard.listings.views',
                                                          'AttributeOptionGroupListView')
        self.attribute_option_group_update_view = get_class('dashboard.listings.views',
                                                            'AttributeOptionGroupUpdateView')
        self.attribute_option_group_delete_view = get_class('dashboard.listings.views',
                                                            'AttributeOptionGroupDeleteView')

        self.option_list_view = get_class('dashboard.listings.views', 'OptionListView')
        self.option_create_view = get_class('dashboard.listings.views', 'OptionCreateView')
        self.option_update_view = get_class('dashboard.listings.views', 'OptionUpdateView')
        self.option_delete_view = get_class('dashboard.listings.views', 'OptionDeleteView')

    def get_urls(self):
        urls = [
		    path('index', self.product_list_view.as_view(), name='index'),
            path('listings/<int:pk>/', self.product_createupdate_view.as_view(), name='listings-product'),
            path('listings/create/', self.product_create_redirect_view.as_view(), name='listings-product-create'),
            path(
                'listings/create/<slug:product_class_slug>/',
                self.product_createupdate_view.as_view(),
                name='listings-product-create'),
            path(
                'listings/<int:parent_pk>/create-variant/',
                self.product_createupdate_view.as_view(),
                name='listings-product-create-child'),
            path('listings/<int:pk>/delete/', self.product_delete_view.as_view(), name='listings-product-delete'),
            path('', self.product_list_view.as_view(), name='listings-product-list'),
            path('product-lookup/', self.product_lookup_view.as_view(), name='listings-product-lookup'),
            path(
                'product-type/create/',
                self.product_class_create_view.as_view(),
                name='listings-class-create'),
            path(
                'product-types/',
                self.product_class_list_view.as_view(),
                name='listings-class-list'),
            path(
                'product-type/<int:pk>/update/',
                self.product_class_update_view.as_view(),
                name='listings-class-update'),
            path(
                'product-type/<int:pk>/delete/',
                self.product_class_delete_view.as_view(),
                name='listings-class-delete'),
            path(
                'attribute-option-group/create/',
                self.attribute_option_group_create_view.as_view(),
                name='listings-attribute-option-group-create'),
            path(
                'attribute-option-group/',
                self.attribute_option_group_list_view.as_view(),
                name='listings-attribute-option-group-list'),
            # The RelatedFieldWidgetWrapper code does something funny with
            # placeholder urls, so it does need to match more than just a pk
            path(
                'attribute-option-group/<str:pk>/update/',
                self.attribute_option_group_update_view.as_view(),
                name='listings-attribute-option-group-update'),
            # The RelatedFieldWidgetWrapper code does something funny with
            # placeholder urls, so it does need to match more than just a pk
            path(
                'attribute-option-group/<str:pk>/delete/',
                self.attribute_option_group_delete_view.as_view(),
                name='listings-attribute-option-group-delete'),
            path('option/', self.option_list_view.as_view(), name='listings-option-list'),
            path('option/create/', self.option_create_view.as_view(), name='listings-option-create'),
            path('option/<str:pk>/update/', self.option_update_view.as_view(), name='listings-option-update'),
            path('option/<str:pk>/delete/', self.option_delete_view.as_view(), name='listings-option-delete'),
        ]
        return self.post_process_urls(urls)
