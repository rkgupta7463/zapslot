import re
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from zapslot.bsclass import *
from core.models import *
from ckeditor.widgets import CKEditorWidget  # add this import
from django_select2 import forms as s2forms
from zapslot.widgets import *
from hospital_app.models import *

class CustomForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)

    def custom_field_class(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                if not field.widget.attrs.get("class", None):
                    field.widget.attrs['class'] = TEXTAREA_INPUT_CLASS
                else:
                    field.widget.attrs['class'] += TEXTAREA_INPUT_CLASS
            elif isinstance(field.widget, forms.DateInput):
                if not field.widget.attrs.get("class", None):
                    field.widget.attrs['class'] = DATE_INPUT_CLASS
                else:
                    field.widget.attrs['class'] += DATE_INPUT_CLASS
            else:
                input_type = field.widget.input_type
                if not field.widget.attrs.get("class", None):
                    # if field_name == "color":
                    #     field.widget.attrs['class'] = 'coloris ' + TEXT_INPUT_CLASS
                    #     field.widget.attrs['data-coloris'] = ''
                    if input_type == 'text':
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                    
                    elif input_type == 'password':
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                        
                    elif input_type == 'number':
                        field.widget.attrs['class'] = INT_INPUT_CLASS
                    elif input_type == 'select':
                        field.widget.attrs['class'] = SELECT_INPUT_CLASS
                    elif input_type == 'checkbox':
                        field.widget.attrs['class'] = CHECKBOX_INPUT_CLASS
                    elif input_type == 'radio':
                        field.widget.attrs['class'] = RADIO_INPUT_CLASS
                    # field.label.attrs['class'] = RADIO_INPUT_LABEL_CLASS
                else:
                    # if field_name == "color":
                    #     field.widget.attrs['class'] += 'coloris ' + TEXT_INPUT_CLASS
                    #     field.widget.attrs['data-coloris'] = ''
                    if input_type == 'text':
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS
                    
                    elif input_type == 'password':
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS
                    elif input_type == 'number':
                        field.widget.attrs['class'] += INT_INPUT_CLASS
                    elif input_type == 'select':
                        field.widget.attrs['class'] += SELECT_INPUT_CLASS
                    elif input_type == 'checkbox':
                        field.widget.attrs['class'] += CHECKBOX_INPUT_CLASS
                    elif input_type == 'radio':
                        field.widget.attrs['class'] += RADIO_INPUT_CLASS




class CustomModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomModelForm, self).__init__(*args, **kwargs)

    def custom_field_class(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                if not field.widget.attrs.get("class", None):
                    field.widget.attrs['class'] = TEXTAREA_INPUT_CLASS
                else:
                    field.widget.attrs['class'] += TEXTAREA_INPUT_CLASS
            elif isinstance(field.widget, forms.DateInput):
                if not field.widget.attrs.get("class", None):
                    field.widget.attrs['class'] = DATE_INPUT_CLASS
                else:
                    field.widget.attrs['class'] += DATE_INPUT_CLASS
            else:
                # Check if the widget has an input_type attribute
                input_type = getattr(field.widget, 'input_type', None)
                # input_type = field.widget.input_type
                if not field.widget.attrs.get("class", None):
                    # if field_name == "color":
                    #     field.widget.attrs['class'] = 'coloris ' + TEXT_INPUT_CLASS
                    #     field.widget.attrs['data-coloris'] = ''
                    if input_type == 'email':
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                    elif input_type == 'text':
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                    elif input_type == 'password':
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                    elif input_type == 'number':
                        field.widget.attrs['class'] = INT_INPUT_CLASS
                    elif input_type == 'select':
                        field.widget.attrs['class'] = SELECT_INPUT_CLASS
                    elif input_type == 'checkbox':
                        # field.widget = CustomCheckboxWidget()
                        field.widget.attrs['class'] = CHECKBOX_INPUT_CLASS
                    elif input_type == 'radio':
                        field.widget.attrs['class'] = RADIO_INPUT_CLASS
                    elif input_type == "url":
                        field.widget.attrs['class'] = TEXT_INPUT_CLASS
                    # field.label.attrs['class'] = RADIO_INPUT_LABEL_CLASS
                else:
                    # if field_name == "color":
                    #     field.widget.attrs['class'] += 'coloris ' + TEXT_INPUT_CLASS
                    #     field.widget.attrs['data-coloris'] = ''
                    if input_type == 'email':
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS
                    elif input_type == 'text':
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS
                    elif input_type == 'password':
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS
                    elif input_type == 'number':
                        field.widget.attrs['class'] += INT_INPUT_CLASS
                    elif input_type == 'select':
                        field.widget.attrs['class'] += SELECT_INPUT_CLASS
                    elif input_type == 'checkbox':
                        # field.widget = CustomCheckboxWidget()
                        field.widget.attrs['class'] += CHECKBOX_INPUT_CLASS
                    elif input_type == 'radio':
                        field.widget.attrs['class'] += RADIO_INPUT_CLASS
                    elif input_type == "url":
                        field.widget.attrs['class'] += TEXT_INPUT_CLASS




class YesConfirmForm(CustomForm):
    confirm = forms.CharField(max_length=150, help_text="Please enter 'YES' to confirm")

    def __init__(self, help_text="Please enter 'YES' to confirm", confirm_text="yes", *args, **kwargs):
        super(YesConfirmForm, self). __init__( *args, **kwargs)
        self.confirm_text = confirm_text
        self.help_text = help_text
        self.fields['confirm'].help_text = help_text
        self.custom_field_class()

    def clean_name(self):
        data = self.cleaned_data.get("confirm", "")
        if not data.lower() == self.confirm_text.lower():
            raise forms.ValidationError(self.help_text)


password_pattern =  '[A-Za-z0-9!@#$%^&*()_+=\-[\]{};:\'",.<>?/\\|]'


class PasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        }),
        label='Password'
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        }),
        label='Confirm Password'
    )

    def _init_(self, cus_fields=None, *args, **kwargs):
        super(PasswordForm, self)._init_(*args, **kwargs)

    # def clean_password(self):

    def clean(self):
        password = self.cleaned_data.get("password")
        print(password,'password')
        confirm_password = self.cleaned_data.get("confirm_password")
        print(confirm_password, 'confirm_password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be more than 8 characters.")

        if len(password) < 8:
            raise forms.ValidationError("Password must be more than 8 characters.")

        if not re.match(password_pattern, password):
            raise forms.ValidationError("Password must be a mix of letters, numbers & symbols (#?!@$%^&*-).")
    
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords doesn't match. Both passwords must be same.")
        return self.cleaned_data
    


class SpecializationForm(CustomModelForm):
    class Meta:
        model=Specialization
        fields=['name','description']
       
    def __init__(self, *args, **kwargs):
        super(SpecializationForm, self). __init__( *args, **kwargs)
        # Customize address field as textarea
        self.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter Description',
            'class': 'form-control w-100',  # Adjust width or other classes as needed
        })
        self.custom_field_class()

class QualificationForm(CustomModelForm):
    class Meta:
        model=Qualification
        fields=['title','issuing_authority','description']
       
    def __init__(self, *args, **kwargs):
        super(QualificationForm, self). __init__( *args, **kwargs)
        # Customize address field as textarea
        self.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter Description',
            'class': 'form-control w-100',  # Adjust width or other classes as needed
        })
        self.custom_field_class()



class HospitalForm(CustomModelForm):
    class Meta:
        model=Hospital
        fields=['name','email','phone','description','address','city','state','country','pincode','opened_on','latitude','longitude']
        widgets={
            'opened_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(HospitalForm, self). __init__( *args, **kwargs)
        # Customize address field as textarea
        self.fields['address'].widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Enter full address',
            'class': 'form-control w-100',  # Adjust width or other classes as needed
        })
        self.custom_field_class()



class AdditionalHospitalImgForm(CustomModelForm):

    class Meta:
        model = HospitalImage
        fields = ['image','caption','sequence']

    def __init__(self,*args,**kwargs):
        super(AdditionalHospitalImgForm, self).__init__(*args,**kwargs)
        self.custom_field_class()



class HospitalServicesForm(CustomModelForm):
    class Meta:
        model = HospitalServices
        fields = ['service_name','service_description','service_price','timslot']

    def __init__(self, *args, **kwargs):
        super(HospitalServicesForm, self).__init__(*args, **kwargs)
        self.fields['service_description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control w-100',  # Adjust width or other classes as needed
        })
        self.custom_field_class()
        