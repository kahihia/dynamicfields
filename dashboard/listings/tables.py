from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django_tables2 import A, Column, LinkColumn, TemplateColumn

from dashboard.utils.loading import get_class, get_model

DashboardTable = get_class('dashboard.tables', 'DashboardTable')
Listing = get_model('listings', 'Listing')
AttributeOptionGroup = get_model('listings', 'AttributeOptionGroup')
Option = get_model('listings', 'Option')


class ListingTable(DashboardTable):
    title = TemplateColumn(
        verbose_name=_('Title'),
        template_name='oscar/dashboard/listings/product_row_title.html',
        order_by='title', accessor=A('title'))
    product_class = Column(
        verbose_name=_('Listing type'),
        accessor=A('product_class'),
        order_by='product_class__name')
       
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/listings/product_row_actions.html',
        orderable=False)

    icon = 'fas fa-sitemap'

    class Meta(DashboardTable.Meta):
        model = Listing
        fields = ('is_public', 'date_updated')
        sequence = ('title',  'product_class',  '...', 'is_public', 'date_updated', 'actions')
        order_by = '-date_updated'


class AttributeOptionGroupTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='oscar/dashboard/listings/attribute_option_group_row_name.html',
        order_by='name')
    option_summary = TemplateColumn(
        verbose_name=_('Option summary'),
        template_name='oscar/dashboard/listings/attribute_option_group_row_option_summary.html',
        orderable=False)
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/listings/attribute_option_group_row_actions.html',
        orderable=False)

    icon = "sitemap"
    caption = ngettext_lazy("%s Attribute Option Group", "%s Attribute Option Groups")

    class Meta(DashboardTable.Meta):
        model = AttributeOptionGroup
        fields = ('name',)
        sequence = ('name', 'option_summary', 'actions')
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE


class OptionTable(DashboardTable):
    name = TemplateColumn(
        verbose_name=_('Name'),
        template_name='oscar/dashboard/listings/option_row_name.html',
        order_by='name')
    actions = TemplateColumn(
        verbose_name=_('Actions'),
        template_name='oscar/dashboard/listings/option_row_actions.html',
        orderable=False)

    icon = "reorder"
    caption = ngettext_lazy("%s Option", "%s Options")

    class Meta(DashboardTable.Meta):
        model = Option
        fields = ('name', 'type', 'required')
        sequence = ('name', 'type', 'required', 'actions')
        per_page = settings.OSCAR_DASHBOARD_ITEMS_PER_PAGE
