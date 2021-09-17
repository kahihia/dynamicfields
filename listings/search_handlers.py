from django.conf import settings
from django.utils.module_loading import import_string
from django.views.generic.list import MultipleObjectMixin

from dashboard.utils.loading import get_class, get_model
SearchHandler = get_class('search.search_handlers', 'SearchHandler')
is_solr_supported = get_class('search.features', 'is_solr_supported')
is_elasticsearch_supported = get_class('search.features', 'is_elasticsearch_supported')
Listing = get_model('listings', 'Listing')





class SolrProductSearchHandler(SearchHandler):
    """
    Search handler specialised for searching products.  Comes with optional
    category filtering. To be used with a Solr search backend.
    """
    model_whitelist = [Listing]
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path):
        super().__init__(request_data, full_path)

    def get_search_queryset(self):
        print(sqs)
        sqs = super().get_search_queryset()
       
        return sqs


class ESProductSearchHandler(SearchHandler):
    """
    Search handler specialised for searching products.  Comes with optional
    category filtering. To be used with an ElasticSearch search backend.
    """
    model_whitelist = [Listing]
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path):
        super().__init__(request_data, full_path)

    def get_search_queryset(self):
        sqs = super().get_search_queryset()
        print(sqs)		
        return sqs


class SimpleProductSearchHandler(MultipleObjectMixin):
    """
    A basic implementation of the full-featured SearchHandler that has no
    faceting support, but doesn't require a Haystack backend. It only
    supports category browsing.

    Note that is meant as a replacement search handler and not as a view
    mixin; the mixin just does most of what we need it to do.
    """
    paginate_by = settings.OSCAR_PRODUCTS_PER_PAGE

    def __init__(self, request_data, full_path):
        self.kwargs = {'page': request_data.get('page') or 1}
        self.object_list = self.get_queryset()

    def get_queryset(self):
        qs = Listing.objects.browsable().base_queryset()
        return qs

    def get_search_context_data(self, context_object_name):
        # Set the context_object_name instance property as it's needed
        # internally by MultipleObjectMixin
        self.context_object_name = context_object_name
        context = self.get_context_data(object_list=self.object_list)
        context[context_object_name] = context['page_obj'].object_list
        return context

def get_product_search_handler_class():
    """
    Determine the search handler to use.

    Currently only Solr is supported as a search backend, so it falls
    back to rudimentary category browsing if that isn't enabled.
    """
    # Use get_class to ensure overridability
    if settings.OSCAR_PRODUCT_SEARCH_HANDLER is not None:
        return import_string(settings.OSCAR_PRODUCT_SEARCH_HANDLER)
    if is_solr_supported():
        return SolrProductSearchHandler
    elif is_elasticsearch_supported():
        return ESProductSearchHandler
    else:
        return SimpleProductSearchHandler