from django import forms
from .models import *
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from dashboard.forms import CustomModelForm,CustomForm
import re
from django.core.exceptions import ValidationError
from zapslot.widgets import *

password_pattern =  '[A-Za-z0-9!@#$%^&*()_+=\-[\]{};:\'",.<>?/\\|]'

class SetNewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(SetNewPasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label,
            })

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
    

from hospital_app.models import *

class CustomUserRegistrationForm(CustomModelForm):
    class Meta:
        model = CustomUser
        fields = [
            # Always visible
            'role','full_name', 'email', 'phone', 'gender', 'date_of_birth',
            'address', 'city', 'state', 'country', 'pincode','profile_picture',

            # Doctor-specific
            'specialization', 'qualification_level', 'experience_years',
            'registration_number', 'consultation_fee', 'available_from',
            'available_to', 'available_days', 'clinic_location',

            # Patient-specific
            'blood_group', 'emergency_contact', 'insurance_provider',
            'insurance_number',
        ]

        widgets = {
            'hospital': PreOptionModelSelect2Widget(
                model=Hospital,
                label="Select Hospital",
                queryset=Hospital.objects.all(),
                search_fields=['name__icontains'],
                attrs={'data-placeholder': 'Select a hospital'}
            ),
            'services': PreOptionModelSelect2Widget(
                dependent_fields={'hospital': 'hospital'},
                search_fields=['service_name__icontains'],
                attrs={'data-placeholder': 'Select a service','class':"form-control"}
            ),
            'specialization':PreOptionModelSelect2MultipleWidget(
                search_fields=['name__icontains'],
                attrs={'data-placeholder':'Select Specialization(s)'}
            ),
            'qualification_level':PreOptionModelSelect2MultipleWidget(
                search_fields=['name__icontains'],
                attrs={'data-placeholder':'Select Qualification Level(s)'}
            ),
            'role': s2forms.Select2Widget(attrs={'data-placeholder': 'Select Role'}),
            'available_days': s2forms.Select2MultipleWidget(attrs={'data-placeholder': 'Select Available Days'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'available_from': forms.TimeInput(attrs={'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': 3})
        # self.fields['medical_history'].widget.attrs.update({'rows': 3})
        # Add Bootstrap styling
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })
        self.fields['registration_number'].widget.attrs.update({
            "placeholder":"License Number or Registration Number"
        })

        self.custom_field_class()



class CustomUserRegistrationForm(CustomModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'email', 'phone', 'gender', 'date_of_birth',
            'address', 'city', 'state', 'country', 'pincode','profile_picture',

            'blood_group', 'emergency_contact', 'insurance_provider',
            'insurance_number',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomUserRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'rows': 3})
        # self.fields['medical_history'].widget.attrs.update({'rows': 3})
        # Add Bootstrap styling
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': field.label
                })

        self.custom_field_class()




class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
        return self.cleaned_data



##### forget password form
attrs_dict={}
from django.utils.translation import gettext_lazy as _


attrs_dict = {'class': 'form-control'}

class EPasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("New password")
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("New password (again)")
    )

    password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", _("Passwords do not match. Please enter the same password."))

            if not re.match(self.password_pattern, password1):
                self.add_error(
                    "password1",
                    _("Password must be at least 8 characters long and include an uppercase letter, "
                      "a lowercase letter, a number, and a special character (#?!@$%^&*-).")
                )

        return cleaned_data




class ForgotPasswordForm(CustomForm):
    email = forms.EmailField()

    def __init__(self,*args,**kwargs):
        super(ForgotPasswordForm,self).__init__(*args,**kwargs)
        return self.custom_field_class()


class EnquiryForm(CustomModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'subject', 'message', 'subscribe_newsletter']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 4}),
            'subscribe_newsletter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __inti__(self,*args,**kwargs):
        super(EnquiryForm,self).__init__(*args,**kwargs)
        self.custom_field_class()
