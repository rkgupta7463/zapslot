from django.urls import path
from .views import *

urlpatterns = [
    path('book/appoinment/',appoinment_view,name="book_appoinment"),
    path('book/appoinment/form/',book_appoinment,name="book_appoinment_form")
]

