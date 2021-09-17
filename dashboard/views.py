import json
from datetime import timedelta
from decimal import ROUND_UP
from decimal import Decimal as D

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg, Count, Sum
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import TemplateView

from dashboard.utils.loading import get_class, get_model

RelatedFieldWidgetWrapper = get_class('dashboard.widgets', 'RelatedFieldWidgetWrapper')

class IndexView(TemplateView):
    """
    An overview view which displays several reports about the shop.

    Supports the permission-based dashboard. It is recommended to add a
    :file:`oscar/dashboard/index_nonstaff.html` template because Oscar's
    default template will display potentially sensitive store information.
    """

    def get_template_names(self):
        return ['oscar/dashboard/index.html', ]
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

  

class PopUpWindowMixin:

    @property
    def is_popup(self):
        return self.request.GET.get(
            RelatedFieldWidgetWrapper.IS_POPUP_VAR,
            self.request.POST.get(RelatedFieldWidgetWrapper.IS_POPUP_VAR))

    @property
    def is_popup_var(self):
        return RelatedFieldWidgetWrapper.IS_POPUP_VAR

    def add_success_message(self, message):
        if not self.is_popup:
            messages.info(self.request, message)


class PopUpWindowCreateUpdateMixin(PopUpWindowMixin):

    @property
    def to_field(self):
        return self.request.GET.get(
            RelatedFieldWidgetWrapper.TO_FIELD_VAR,
            self.request.POST.get(RelatedFieldWidgetWrapper.TO_FIELD_VAR))

    @property
    def to_field_var(self):
        return RelatedFieldWidgetWrapper.TO_FIELD_VAR

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.is_popup:
            ctx['to_field'] = self.to_field
            ctx['to_field_var'] = self.to_field_var
            ctx['is_popup'] = self.is_popup
            ctx['is_popup_var'] = self.is_popup_var

        return ctx


class PopUpWindowCreateMixin(PopUpWindowCreateUpdateMixin):

    def popup_response(self, obj):
        if self.to_field:
            attr = str(self.to_field)
        else:
            attr = obj._meta.pk.attname
        value = obj.serializable_value(attr)
        popup_response_data = json.dumps({
            'value': str(value),
            'obj': str(obj),
        })
        return TemplateResponse(
            self.request,
            'oscar/dashboard/widgets/popup_response.html',
            {'popup_response_data': popup_response_data, }
        )


class PopUpWindowUpdateMixin(PopUpWindowCreateUpdateMixin):

    def popup_response(self, obj):
        opts = obj._meta
        if self.to_field:
            attr = str(self.to_field)
        else:
            attr = opts.pk.attname
        # Retrieve the `object_id` from the resolved pattern arguments.
        value = self.request.resolver_match.kwargs['pk']
        new_value = obj.serializable_value(attr)
        popup_response_data = json.dumps({
            'action': 'change',
            'value': str(value),
            'obj': str(obj),
            'new_value': str(new_value),
        })
        return TemplateResponse(
            self.request,
            'oscar/dashboard/widgets/popup_response.html',
            {'popup_response_data': popup_response_data, }
        )


class PopUpWindowDeleteMixin(PopUpWindowMixin):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        if self.is_popup:
            ctx['is_popup'] = self.is_popup
            ctx['is_popup_var'] = self.is_popup_var

        return ctx

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL, or closes the popup, it it is one.
        """
        obj = self.get_object()

        response = super().delete(request, *args, **kwargs)

        if self.is_popup:
            obj_id = obj.pk
            popup_response_data = json.dumps({
                'action': 'delete',
                'value': str(obj_id),
            })
            return TemplateResponse(
                request,
                'oscar/dashboard/widgets/popup_response.html',
                {'popup_response_data': popup_response_data, }
            )
        else:
            return response

