from django.urls import path
from .views import *


urlpatterns = [
    path('main/login/',login_view,name="main_login"),
    path('main/register/',register_user_view,name="main_register"),
    path('ajax/role-fields/', load_role_specific_fields, name='load_role_specific_fields'),

    path('main/logout/',logout_view,name="main_logout"),

    path('',index,name="home"),
    path('about-us/',about_us,name="about_us"),
    path('contact/',contact_us,name="contact_us"),
    path('services/',services,name="services"),
    path('doctor/',doctor_list,name="doctor"),
    path('department/',department_list,name="departments"),
    path('time/table/',time_table,name="time_table"),
    path('doctors/',doctors_list,name="doctors_list"),
    path('info/',aboutus,name="about"),
    path('faq/',faq,name="faq"),
    path('<slug:title>/hospital/',hospital_details,name="hospital_portfolio"),
    
    ## url's for `reset password`
    path('reset_password/<str:hash>/', forgot_password_reg_email,name="forgot_password_reg_email"),

    path('forgot/password/', forgot_password_form,name="forgot_password"),
    path('set_new_password/<str:hash>/', new_set_password_reg_email,name="set_new_pass_reg")
]

