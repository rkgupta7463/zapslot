from django.urls import path
from .views import *

urlpatterns = [
    path("logout/",logout_view,name="logout"),
    path("accounts/login/", custom_login_view, name="login_admin"),
    path("",index,name="index"),
    
    ############  USERS
    path('users/', users, name="users"),
    path('change/password/<int:uid>/', changepassword_view, name="change_password"),
    path('reset/password/<int:uid>/', rest_password_view, name="reset_password"),
    path('users/filtered/',  users_filtered, name="users_filtered"),
    path('ajax_datatable/projects/filter/', UserProfileDatatableView.as_view(), name="ajax_datatable_users_filter_list"),
    path('users/add/', createUser, name="add_user"),
    path('users/<int:uid>/edit/', createUser, name="edit_user"),
    path('users/<int:uid>/password/', set_password_user, name="set_password_user"),
    path('users/<int:uid>/edit/active/', userState, name="user_edit_active"),
    
    ####### Specialization's url 
    path('specialization/', specialization, name="specialization"),
    path('specialization/filtered/',  specializations_filtered, name="specializations_filtered"),
    path('ajax_datatable/specialization/filter/', SpecializationsDatatableView.as_view(), name="ajax_datatable_specializations_filter_list"),
    path('specialization/add/', add_specialization_edit, name="add_specialization"),
    path('specialization/<int:sid>/edit/', add_specialization_edit, name="edit_specialization"),
    
    ####### qualification's url 
    path('qualification/', qualification, name="qualification"),
    path('qualification/filtered/',  qualifications_filtered, name="qualifications_filtered"),
    path('ajax_datatable/qualification/filter/', QualificationsDatatableView.as_view(), name="ajax_datatable_qualifications_filter_list"),
    path('qualification/add/', add_qualification_edit, name="add_qualification"),
    path('qualification/<int:sid>/edit/', add_specialization_edit, name="edit_qualification"),
    
    ############  hospital's url 
    path('hospitals/', hospital, name="hospitals"),
    path('hospital/filtered/',  hospitals_filtered, name="hospitals_filtered"),
    path('ajax_datatable/hospital/filter/', HospitalsDatatableView.as_view(), name="ajax_datatable_hospitals_filter_list"),
    path('hospital/add/', add_hospital_edit, name="add_hospital"),
    path('hospital/<int:hid>/edit/', add_hospital_edit, name="edit_hospital"),
    path('hospital/<int:hid>/detail/', hospital_detail, name="hospital_detail"),
    path('add/hospital/<int:hid>/image/', additional_hospital_img, name="add_hospital_img"),
    path('edit/hospital/<int:hid>/image/<int:pid>/', additional_hospital_img, name="edit_hospital_img"),

    path('hospital/<int:hid>/services/', hospital_services, name="add_hospital_services"),
    path('hospital/<int:hid>/services/<int:sid>>/edit/', hospital_services, name="edit_hospital_services"),
    path('hospital/<int:hid>/services/list/', hospital_services_list, name="hospital_services_list"),

    ########## enuiried's url
    path('enquiry/', enquiries, name="enquiries"),
    path('enquiries/filtered/',  enquiries_filtered, name="enquiries_filtered"),
    path('ajax_datatable/enquiries/filter/', EnquiriesDatatableView.as_view(), name="ajax_datatable_enquiries_filter_list"),

    ########## services's url
    path('appoinments/', hospital_appoinment, name="appoinment"),
    path('hospital/appoinment/filtered/',  hospitals_appoinment_filtered, name="hospitals_appoinment_filtered"),
    path('ajax_datatable/hospital/appoinment/filter/', HospitalsAppoinmentDatatableView.as_view(), name="ajax_datatable_hospitals_appoinment_filter_list"),
    path('hospital/appoinment/<int:ap_id>/confirmation/',  comfirm_appoinment, name="comfirm_appoinment"),
    path('view/appoinment/<int:ap_id>/detail/',  view_appoinmemt, name="view_appoinment"),
]