from django.forms.widgets import CheckboxInput
from django.utils.safestring import mark_safe
from django_select2 import forms as s2forms


class CustomCheckboxWidget(CheckboxInput):
    template_name = 'widgets/checkbox.html'

    def __init__(self, attrs=None, check_test=None):
        super().__init__(attrs)
        # check_test is a callable that takes a value and returns True
        # if the checkbox should be checked for that value.
        

class PreOptionModelSelect2Widget(s2forms.ModelSelect2Widget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Set select2's AJAX attributes."""
        default_attrs = {
            "data-ajax--url": self.get_url(),
            "data-ajax--cache": "true",
            "data-ajax--type": "GET",
            "data-minimum-input-length": 0,
        }

        default_attrs.update(base_attrs)

        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)

        attrs["data-field_id"] = self.field_id

        attrs["class"] += " select2-primary django-select2-heavy"
        return attrs
    

class PreOptionModelSelect2MultipleWidget(s2forms.ModelSelect2MultipleWidget):
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Set select2's AJAX attributes."""
        default_attrs = {
            "data-ajax--url": self.get_url(),
            "data-ajax--cache": "true",
            "data-ajax--type": "GET",
            "data-minimum-input-length": 0,
        }

        default_attrs.update(base_attrs)

        attrs = super().build_attrs(default_attrs, extra_attrs=extra_attrs)

        attrs["data-field_id"] = self.field_id

        attrs["class"] += " select2-primary django-select2-heavy"
        return attrs
    


