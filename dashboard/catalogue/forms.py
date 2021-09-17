from django import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from treebeard.forms import movenodeform_factory

from dashboard.utils.loading import get_class, get_classes, get_model
from dashboard.utils.utils import slugify
from dashboard.utils.forms.widgets import DateTimePickerInput

Product = get_model('catalogue', 'Product')
ProductClass = get_model('catalogue', 'ProductClass')
ProductAttribute = get_model('catalogue', 'ProductAttribute')
AttributeOptionGroup = get_model('catalogue', 'AttributeOptionGroup')
AttributeOption = get_model('catalogue', 'AttributeOption')
Option = get_model('catalogue', 'Option')
ProductSelect = get_class('dashboard.catalogue.widgets', 'ProductSelect')
(RelatedFieldWidgetWrapper,
 RelatedMultipleFieldWidgetWrapper) = get_classes('dashboard.widgets',
                                                  ('RelatedFieldWidgetWrapper',
                                                   'RelatedMultipleFieldWidgetWrapper'))



class SEOFormMixin:
    seo_fields = ['meta_title', 'meta_description', 'slug']

    def primary_form_fields(self):
        return [field for field in self if not field.is_hidden and not self.is_seo_field(field)]

    def seo_form_fields(self):
        return [field for field in self if self.is_seo_field(field)]

    def is_seo_field(self, field):
        return field.name in self.seo_fields

class ProductClassSelectForm(forms.Form):
    """
    Form which is used before creating a product to select it's product class
    """

    product_class = forms.ModelChoiceField(
        label=_("Create a new product of type"),
        empty_label=_("-- Choose type --"),
        queryset=ProductClass.objects.all())

    def __init__(self, *args, **kwargs):
        """
        If there's only one product class, pre-select it
        """
        super().__init__(*args, **kwargs)
        qs = self.fields['product_class'].queryset
        if not kwargs.get('initial') and len(qs) == 1:
            self.fields['product_class'].initial = qs[0]


class ProductSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255, required=False, label=_('Product title'))

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['title'] = cleaned_data['title'].strip()
        return cleaned_data



def _attr_text_field(attribute):
    return forms.CharField(label=attribute.name,
                           required=attribute.required)


def _attr_textarea_field(attribute):
    return forms.CharField(label=attribute.name,
                           widget=forms.Textarea(),
                           required=attribute.required)


def _attr_integer_field(attribute):
    return forms.IntegerField(label=attribute.name,
                              required=attribute.required)


def _attr_boolean_field(attribute):
    return forms.BooleanField(label=attribute.name,
                              required=attribute.required)


def _attr_float_field(attribute):
    return forms.FloatField(label=attribute.name,
                            required=attribute.required)


def _attr_date_field(attribute):
    return forms.DateField(label=attribute.name,
                           required=attribute.required,
                           widget=forms.widgets.DateInput)


def _attr_datetime_field(attribute):
    return forms.DateTimeField(label=attribute.name,
                               required=attribute.required,
                               widget=DateTimePickerInput())


def _attr_option_field(attribute):
    return forms.ModelChoiceField(
        label=attribute.name,
        required=attribute.required,
        queryset=attribute.option_group.options.all())


def _attr_multi_option_field(attribute):
    return forms.ModelMultipleChoiceField(
        label=attribute.name,
        required=attribute.required,
        queryset=attribute.option_group.options.all())


def _attr_entity_field(attribute):
    # Product entities don't have out-of-the-box supported in the ProductForm.
    # There is no ModelChoiceField for generic foreign keys, and there's no
    # good default behaviour anyway; offering a choice of *all* model instances
    # is hardly useful.
    return None


def _attr_numeric_field(attribute):
    return forms.FloatField(label=attribute.name,
                            required=attribute.required)


def _attr_file_field(attribute):
    return forms.FileField(
        label=attribute.name, required=attribute.required)


def _attr_image_field(attribute):
    return forms.ImageField(
        label=attribute.name, required=attribute.required)


class ProductForm(SEOFormMixin, forms.ModelForm):
    FIELD_FACTORIES = {
        "text": _attr_text_field,
        "richtext": _attr_textarea_field,
        "integer": _attr_integer_field,
        "boolean": _attr_boolean_field,
        "float": _attr_float_field,
        "date": _attr_date_field,
        "datetime": _attr_datetime_field,
        "option": _attr_option_field,
        "multi_option": _attr_multi_option_field,
        "entity": _attr_entity_field,
        "numeric": _attr_numeric_field
    }

    class Meta:
        model = Product
        fields = [
            'title',  'description', 'is_public',  'slug', 'meta_title',
            'meta_description']
        widgets = {
            'meta_description': forms.Textarea(attrs={'class': 'no-widget-init'})
        }

    def __init__(self, product_class, data=None, *args, **kwargs):
        self.set_initial(product_class, kwargs)
        super().__init__(data, *args, **kwargs)
        self.instance.product_class = product_class
        self.add_attribute_fields(product_class)

        if 'slug' in self.fields:
            self.fields['slug'].required = False
            self.fields['slug'].help_text = _('Leave blank to generate from product title')
        if 'title' in self.fields:
            self.fields['title'].widget = forms.TextInput(
                attrs={'autocomplete': 'off'})

    def set_initial(self, product_class, kwargs):
        """
        Set initial data for the form. Sets the correct product structure
        and fetches initial values for the dynamically constructed attribute
        fields.
        """
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(product_class, kwargs)
 

    def set_initial_attribute_values(self, product_class, kwargs):
        """
        Update the kwargs['initial'] value to have the initial values based on
        the product instance's attributes
        """
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in product_class.attributes.all():
            try:
                value = instance.attribute_values.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attr_%s' % attribute.code] = value

    def add_attribute_fields(self, product_class):
        """
        For each attribute specified by the product class, this method
        dynamically adds form fields to the product form.
        """
        for attribute in product_class.attributes.all():
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attr_%s' % attribute.code] = field

    def get_attribute_field(self, attribute):
        """
        Gets the correct form field for a given attribute type.
        """
        return self.FIELD_FACTORIES[attribute.type](attribute)

    def delete_non_child_fields(self):
        """
        Deletes any fields not needed for child products. Override this if
        you want to e.g. keep the description field.
        """
        for field_name in ['description']:
            if field_name in self.fields:
                del self.fields[field_name]

    def _post_clean(self):
        """
        Set attributes before ModelForm calls the product's clean method
        (which it does in _post_clean), which in turn validates attributes.
        """
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attr_%s' % attribute.code
            # An empty text field won't show up in cleaned_data.
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.code, value)
        super()._post_clean()




class ProductClassForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        remote_field = self._meta.model._meta.get_field('options').remote_field
        self.fields["options"].widget = RelatedMultipleFieldWidgetWrapper(
            self.fields["options"].widget, remote_field)

    class Meta:
        model = ProductClass
        fields = ['name', 'options']


class ProductAttributesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # because we'll allow submission of the form with blank
        # codes so that we can generate them.
        self.fields["code"].required = False

        self.fields["option_group"].help_text = _("Select an option group")

        remote_field = self._meta.model._meta.get_field('option_group').remote_field
        self.fields["option_group"].widget = RelatedFieldWidgetWrapper(
            self.fields["option_group"].widget, remote_field)

    def clean_code(self):
        code = self.cleaned_data.get("code")
        title = self.cleaned_data.get("name")

        if not code and title:
            code = slugify(title)

        return code

    def clean(self):
        attr_type = self.cleaned_data.get('type')
        option_group = self.cleaned_data.get('option_group')
        if attr_type in [ProductAttribute.OPTION, ProductAttribute.MULTI_OPTION] and not option_group:
            self.add_error('option_group', _('An option group is required'))

    class Meta:
        model = ProductAttribute
        fields = ["name", "code", "type", "option_group", "required"]


class AttributeOptionGroupForm(forms.ModelForm):

    class Meta:
        model = AttributeOptionGroup
        fields = ['name']


class AttributeOptionForm(forms.ModelForm):

    class Meta:
        model = AttributeOption
        fields = ['option']


class OptionForm(forms.ModelForm):

    class Meta:
        model = Option
        fields = ['name', 'type', 'required']
