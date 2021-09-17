from django.contrib import admin
from dashboard.utils.loading import get_model

AttributeOption = get_model('listings', 'AttributeOption')
AttributeOptionGroup = get_model('listings', 'AttributeOptionGroup')
Option = get_model('listings', 'Option')
Listing = get_model('listings', 'Listing')
ListingAttribute = get_model('listings', 'ListingAttribute')
ListingAttributeValue = get_model('listings', 'ListingAttributeValue')
ListingClass = get_model('listings', 'ListingClass')


class AttributeInline(admin.TabularInline):
    model = ListingAttributeValue

class ListingAttributeInline(admin.TabularInline):
    model = ListingAttribute
    extra = 2


class ListingClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ListingAttributeInline]


class ListingAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('get_title',  'get_product_class', 
                    'attribute_summary', 'date_created')
    list_filter = []
    prepopulated_fields = {"slug": ("title",)}
    search_fields = [ 'title']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (
            qs
            .select_related('product_class')
            .prefetch_related(
                'attribute_values',
                'attribute_values__attribute'))


class ListingAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'product_class', 'type')
    prepopulated_fields = {"code": ("name", )}


class OptionAdmin(admin.ModelAdmin):
    pass


class ListingAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption


class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]



admin.site.register(ListingClass, ListingClassAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(ListingAttribute, ListingAttributeAdmin)
admin.site.register(ListingAttributeValue, ListingAttributeValueAdmin)
admin.site.register(AttributeOptionGroup, AttributeOptionGroupAdmin)
admin.site.register(Option, OptionAdmin)
