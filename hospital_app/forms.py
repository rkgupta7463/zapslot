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
from django_select2.forms import ModelSelect2MultipleWidget,ModelSelect2Widget

from core.forms import CustomForm,CustomModelForm

# class AppointmentForm(forms.ModelForm):
#     class Meta:
#         model = Appointment
#         fields = ['patient', 'doctor', 'date', 'time', 'status']
       



class AppointmentForm(CustomModelForm):
    class Meta:
        model = Appointment
        fields = [
            'name', 'email', 'phone',
            'hospital', 'services','doctor', 'timeslot',
            'appointment_date', 'symptoms',
        ]
        widgets = {
            'appointment_date': forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Select a date for appointment'
            }),
            'symptoms': forms.Textarea(attrs={'placeholder': 'Briefly describe your symptoms', 'rows': 2}),
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
            'doctor': PreOptionModelSelect2Widget(
                dependent_fields={'services': 'hospital_services'},
                search_fields=['username__icontains'],
                attrs={'data-placeholder': 'Select Doctor', 'class': "form-control"}
            ),
            'timeslot': PreOptionModelSelect2Widget(
                dependent_fields={'services': 'hospitalservices'},
                search_fields=['start_time__icontains'],
                attrs={'data-placeholder': 'Select a time slot'}
            )
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm,self).__init__(*args, **kwargs)
        self.custom_field_class()

        # Add placeholder text for input fields
        self.fields['name'].widget.attrs['placeholder'] = 'Enter your full name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email address'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['appointment_date'].widget.attrs['placeholder'] = 'Select a date for appointment'
        # self.fields['symptoms'].widget.attrs['placeholder'] = 'Briefly describe your symptoms'
        # self.fields['symptoms'].widget.attrs['row'] = '2'

        # For Select2 widgets, placeholders are already defined in Meta.widgets
        # But if you still want to ensure they're set, you can do:
        self.fields['hospital'].widget.attrs.setdefault('data-placeholder', 'Select a hospital')
        self.fields['services'].widget.attrs.setdefault('data-placeholder', 'Select a service')
        self.fields['timeslot'].widget.attrs.setdefault('data-placeholder', 'Select a time slot')



class AppoinmentConfirmationForm(CustomModelForm):
    class Meta:
        model=Appointment
        fields=['status','reason_rejection']

    def __init__(self,*args,**kwargs):
        super(AppoinmentConfirmationForm,self).__init__(*args,**kwargs)
        self.fields['reason_rejection'].widget.attrs.update({'rows': 3})
        self.custom_field_class()