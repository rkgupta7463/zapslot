from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Specialization)
admin.site.register(Qualification)
admin.site.register(EmailTemplate)
admin.site.register(Enquiry)
