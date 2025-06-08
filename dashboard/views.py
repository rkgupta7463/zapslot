from django.shortcuts import render,get_object_or_404,redirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldDoesNotExist
from django.apps import apps
from django.http import HttpResponse
from ajax_datatable.views import AjaxDatatableView
import json
from .models import *
from core.forms import *
from core.models import *
from django.views.decorators.http import require_http_methods, require_POST
from django.http import HttpResponseRedirect
from django.contrib.auth import login,logout
from dashboard.forms import *
import socket
from django.views.decorators.csrf import csrf_exempt
from hospital_app.models import *


@csrf_exempt
def logout_view(request):
    try:
        logout(request)
        return redirect("/")
    
    except socket.gaierror:
        return HttpResponse(
                status=500,
                headers={
                    'HX-Trigger': json.dumps({
                        "changed": True,
                        "closeModal":True,
                        "showMessage": {"level": "success", "message": "Kindly check Internet connection!"}
                    })
                })
    
#     return response


def custom_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Redirect': "/zapslot/admin/"
                }
            )
        else:
            return HttpResponse("""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> Invalid username or password!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")

    return render(request, "dashboard/accounts/sign-in.html")


def base(request):
    context = {
    }
    return render(request, "base.html", context=context)


@login_required(login_url="login_admin")
def index(request):
    total_license=""
    request_license=""
    support_query=""

    context = {
        "total_license":total_license,
        "request_license":request_license,
        "support_query":support_query,
    }
    return render(request, "dashboard/dashboard.html", context=context)
    

@login_required(login_url="login_admin")
def users(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Users",
        # "description": "List of Users",
        "url": f"{reverse('users_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Users"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def users_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Users",
        "description": "List of Users",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_users_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        "hx_add_button": [
                {"url": reverse('add_user'),"icon": "","text": "Add User", "bs_toggle": "modal"},
                ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class UserProfileDatatableView(AjaxDatatableView):
    model = CustomUser
    title = "User"
    initial_order = [["full_name", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'full_name', 'title': 'Full Name', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'date_of_birth', 'title': 'DOB', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'phone', 'title': 'Mobile', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'email', 'title': 'E-Mail', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'gender', 'title': 'Gender', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'city', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'state', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'is_active', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
        if obj.is_active:
            row["is_active"] = f"""<span class="badge bg-label-success" text-capitalized="">Active</span>"""
        else:
            row["is_active"] = f"""<span class="badge bg-label-danger" text-capitalized="">Inactive</span>"""
        """<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-html="true" title="" data-original-title="<em>Tooltip</em> <u>with</u> <b>HTML</b>">Tooltip with HTML</button>"""
        
        row["first_name"] = obj.full_name
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                            </ul>
                        </div>
                        ''' %(
                            reverse('edit_user', args=(obj.id,)), "Edit",
                            reverse('set_password_user', args=(obj.id,)), "Set New Password",
                            reverse('change_password', args=(obj.id,)), "Change Password",
                            reverse('user_edit_active', args=(obj.id,)), "Deactivate" if obj.is_active else "Activate",
                            )

    def get_show_column_filters(self, request):
        return True

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "organization"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        queryset = CustomUser.objects.all()
        return queryset

from datetime import timedelta

def createUser(request, uid=None):
    instance = CustomUser.objects.get(id=uid) if uid else None
    form = CustomUserRegistrationForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("before form save:- ",form.cleaned_data['phone'])
            f = form.save(commit=False)
            print("after form save:- ",f.phone)
            f.save()
            toast = {"level": "success", "message": f"User: { f.full_name } saved"}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tableChanged": True,
                        "closeModal": True,
                        "showToast": toast
                    })
                }
            )
    return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": "Edit User" if instance else "Create User",'config':{'select2':True}})


def edit_user(request, uid=None):
    if uid:
        instance = CustomUser.objects.get(id=uid)
    else:
        instance = None
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": True,
                        "tableChanged": True,
                        "Changed": None,
                        "showMessage": {"level": "success", "message": "User updated." if instance else "User added."}
                    })
                }
            )
    else:
        form = CustomUserRegistrationForm(instance=instance)
    return render(request, "dashboard/partials/modal_add_form.html", {"form": form, "title": "Edit User" if instance else "Add User",'config':{'select2':True}})


def rest_password_view(request, uid=None):
    if uid:
        user_instance = get_object_or_404(UserProfile, id=uid)  # Ensure instance exists
    else:
        return HttpResponse(status=400)  # Bad Request if no UID
    
    form = YesConfirmForm(data=request.POST or None)

    if request.method == "POST":
        reg_link=PasswordGenLink(user=user_instance)
        reg_link.expiry_time=timezone.now() + timedelta(hours=1)
        reg_link.save()

        send_email_password_forgot.delay(to_mail=user_instance.email, hash_code=reg_link.hash)

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "closeModal": True,
                    "tableChanged": True,
                    "Changed": None,
                    "showMessage": {"level": "success", "message": "Email has sent for Rest Password!"}
                })
            }
        )
    else:
        form = YesConfirmForm()

    return render(request, "partials/modal_add_form.html", {"form": form, "title": "Change Password"})




from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def changepassword_view(request, uid=None):
    if uid:
        user_instance = get_object_or_404(CustomUser, id=uid)  # Ensure instance exists
    else:
        return HttpResponse(status=400)  # Bad Request if no UID

    if request.method == "POST":
        form = PasswordChangeForm(user=user_instance, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevent logout after password change
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": True,
                        "tableChanged": True,
                        "Changed": None,
                        "showMessage": {"level": "success", "message": "Password updated successfully."}
                    })
                }
            )
    else:
        form = PasswordChangeForm(user=user_instance)

    return render(request, "dashboard/partials/modal_add_form.html", {"form": form, "title": "Change Password"})


def userState(request, uid):
    user = CustomUser.objects.get(id=uid)
    form = YesConfirmForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user.is_active = True if not user.is_active else False
            user.save()
            toast = {"level": "success", "message": f"User: { user.get_full_name } updated"}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": True,
                        "showToast": toast,
                        "tableChanged": True
                    })
                }
            )
    return render(request, 'partials/modal_add_form.html', {"form": form, "title": f"{'Deactivate' if user.is_active else 'Activate'} User", })


def set_password_user(request, uid):
    user = CustomUser.objects.get(id=uid)
    if request.method == "POST":
        form = PasswordForm(data=request.POST or None)

        if form.is_valid():
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "closeModal": True,
                        "Changed": None,
                        "showMessage": {"level" : "success", "message" : "User updated."}
                    })
                }
            )
        else:
            print(form.errors)
    else:
        form = PasswordForm(data=request.POST or None)

    return render(request, 'dashboard/partials/modal_add_form.html', {"form": form, "title": "Set Password", })


## specialization view function
@login_required(login_url="login_admin")
def specialization(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Specialization",
        # "description": "List of Users",
        "url": f"{reverse('specializations_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Specialization"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def specializations_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Specialization",
        "description": "List of Specialization",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_specializations_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        "hx_add_button": [
                {"url": reverse('add_specialization'),"icon": "","text": "Add Specialization", "bs_toggle": "modal"},
                ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class SpecializationsDatatableView(AjaxDatatableView):
    model = Specialization
    title = "Specializations"
    initial_order = [["name", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'name', 'title': 'Name', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'created_by', 'title': 'Created By', 'visible': True, 'orderable': True, 'searchable': True},
            # {'name': 'is_active', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
        # if obj.is_active:
        #     row["is_active"] = f"""<span class="badge bg-label-success" text-capitalized="">Active</span>"""
        # else:
        #     row["is_active"] = f"""<span class="badge bg-label-danger" text-capitalized="">Inactive</span>"""
        # """<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-html="true" title="" data-original-title="<em>Tooltip</em> <u>with</u> <b>HTML</b>">Tooltip with HTML</button>"""
        
        # row["image_url"] = f"""<img src={obj.image_url.url} alt="{obj.image_url}" style="width:200px; height:100px">"""
        row["created_by"] = obj.created_by.email
            # Show the first price (or "N/A" if no prices exist)
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                            
                               </ul>
                        </div>
                        ''' %(
                            reverse('edit_specialization', args=(obj.id,)), "Edit",
                            )

    def get_show_column_filters(self, request):
        return False

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "created_by"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        if request.user.is_superuser:
            queryset = Specialization.objects.all()
        else:
            queryset = Specialization.objects.filter(created_by=request.user)

        return queryset



def add_specialization_edit(request, sid=None):
    instance = Specialization.objects.get(id=sid) if sid else None
    form = SpecializationForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by=request.user
            f.save()
            form.save_m2m()  # Explicitly save many-to-many relat

            toast = {"level": "success", "message": f"Specialization: { f.name } created!"}

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tableChanged": True,
                        "closeModal": True,
                        "showToast": toast
                    })
                }
            )
    return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": "Specialization has Edited!" if instance else "Specialization has Created!"})


## specialization view function
@login_required(login_url="login_admin")
def qualification(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Qualification",
        # "description": "List of Users",
        "url": f"{reverse('qualifications_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Qualification"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def qualifications_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Qualification",
        "description": "List of Qualification",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_qualifications_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        "hx_add_button": [
                {"url": reverse('add_qualification'),"icon": "","text": "Add Qualification", "bs_toggle": "modal"},
                ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class QualificationsDatatableView(AjaxDatatableView):
    model = Qualification
    title = "Qualification"
    initial_order = [["title", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'title', 'title': 'Title', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'issuing_authority', 'title': 'Issuing Authority', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'created_by', 'title': 'Created By', 'visible': True, 'orderable': True, 'searchable': True},
            # {'name': 'is_active', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
        # if obj.is_active:
        #     row["is_active"] = f"""<span class="badge bg-label-success" text-capitalized="">Active</span>"""
        # else:
        #     row["is_active"] = f"""<span class="badge bg-label-danger" text-capitalized="">Inactive</span>"""
        # """<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-html="true" title="" data-original-title="<em>Tooltip</em> <u>with</u> <b>HTML</b>">Tooltip with HTML</button>"""
        
        # row["image_url"] = f"""<img src={obj.image_url.url} alt="{obj.image_url}" style="width:200px; height:100px">"""
        row["created_by"] = obj.created_by.email
            # Show the first price (or "N/A" if no prices exist)
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                            
                               </ul>
                        </div>
                        ''' %(
                            reverse('edit_qualification', args=(obj.id,)), "Edit",
                            )

    def get_show_column_filters(self, request):
        return False

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "created_by"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        if request.user.is_superuser:
            queryset = Qualification.objects.all()
        else:
            queryset = Qualification.objects.filter(created_by=request.user)

        return queryset



def add_qualification_edit(request, qid=None):
    instance = Qualification.objects.get(id=qid) if qid else None
    form = QualificationForm(instance=instance, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by=request.user
            f.save()

            toast = {"level": "success", "message": f"Qualification: { f.title } created!"}

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tableChanged": True,
                        "closeModal": True,
                        "showToast": toast
                    })
                }
            )
    return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": "Qualification has Edited!" if instance else "Qualification has Created!"})


## hospital view function
@login_required(login_url="login_admin")
def hospital(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Hospital",
        # "description": "List of Users",
        "url": f"{reverse('hospitals_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Hospital"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def hospitals_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Hospitals",
        "description": "List of Hospitals",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_hospitals_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        "hx_add_button": [
                {"url": reverse('add_hospital'),"icon": "","text": "Add Hospital", "bs_toggle": "modal"},
                ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class HospitalsDatatableView(AjaxDatatableView):
    model = Hospital
    title = "Hospitals"
    initial_order = [["name", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'name', 'title': 'Name', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'email', 'title': 'Image', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'phone', 'title': 'Image', 'visible': True, 'orderable': True, 'searchable': True},
            # {'name': 'description', 'title': 'Image', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'address', 'title': 'Location', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'city', 'title': 'City', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'state', 'title': 'State', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'country', 'title': 'Country', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'pincode', 'title': 'Pincode', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'created_by', 'title': 'Created By', 'visible': True, 'orderable': True, 'searchable': True},
            # {'name': 'is_active', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
        # if obj.is_active:
        #     row["is_active"] = f"""<span class="badge bg-label-success" text-capitalized="">Active</span>"""
        # else:
        #     row["is_active"] = f"""<span class="badge bg-label-danger" text-capitalized="">Inactive</span>"""
        # """<button type="button" class="btn btn-secondary" data-toggle="tooltip" data-html="true" title="" data-original-title="<em>Tooltip</em> <u>with</u> <b>HTML</b>">Tooltip with HTML</button>"""
        
        # row["image_url"] = f"""<img src={obj.image_url.url} alt="{obj.image_url}" style="width:200px; height:100px">"""
        row["created_by"] = obj.created_by.email
            # Show the first price (or "N/A" if no prices exist)
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" href="%s">%s</a>
                            
                               </ul>
                        </div>
                        ''' %(
                            reverse('edit_hospital', args=(obj.id,)), "Edit",
                            # reverse('facility', args=(obj.id,)), "Facility",
                            # reverse('rules_view', args=(obj.id,)), "Rule",
                            reverse('add_hospital_img', args=(obj.id,)), "Add Picture",
                            reverse('hospital_detail', args=(obj.id,)), "View",
                            # reverse('add_ground_price', args=(obj.id,)), "Set Price",
                            )

    def get_show_column_filters(self, request):
        return True

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "created_by"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        if request.user.is_superuser:
            queryset = Hospital.objects.all()
        else:
            queryset = Hospital.objects.filter(created_by=request.user)

        return queryset



def add_hospital_edit(request, hid=None):
    instance = Hospital.objects.get(id=hid) if hid else None
    form = HospitalForm(instance=instance, data=request.POST or None, files=request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.created_by=request.user
            f.updated_by=request.user
            f.save()
            form.save_m2m()  # Explicitly save many-to-many relat

            toast = {"level": "success", "message": f"Hospital: { f.name } created!"}

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tableChanged": True,
                        "closeModal": True,
                        "showToast": toast
                    })
                }
            )
    return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": "Hospital has Edited!" if instance else "Hospital has Created!"})




def additional_hospital_img(request,hid, pid=None):
    hospital = Hospital.objects.get(id=hid) if hid else None
    
    instance = HospitalImage.objects.get(id=pid) if pid else None
    
    form = AdditionalHospitalImgForm(instance=instance, data=request.POST or None,files=request.FILES or None)
    
    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.hospital=hospital
            f.uploaded_by=request.user
            f.save()

            toast = {"level": "success", "message": f"IKmage Added for { f.hospital.name } Hospital!"}

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "tableChanged": True,
                        "closeModal": True,
                        "showToast": toast
                    })
                }
            )
    return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": f"Edited Hospital Image!" if instance else "Add Hospital Image!"})


def hospital_detail(request,hid):
    hospital = Hospital.objects.get(id=hid)
    hospital_images = HospitalImage.objects.filter(hospital=hospital).first()
    context={
        'hospital': hospital,
        "hospital_images":hospital_images
        }
    return render(request, 'dashboard/hospital_detail.html', context)


def hospital_services_list(request,hid):
    hospital = Hospital.objects.get(id=hid)
    services = HospitalServices.objects.filter(hospital=hospital)

    context={
        'hospital': hospital,
        'services': services
        }
    return render(request, 'dashboard/partials/services_lists.html', context)

### hospital_services
def hospital_services(request,hid,sid=None):
    hospital = Hospital.objects.get(id=hid) if hid else None
    instance = HospitalServices.objects.get(id=sid,hospital=hospital) if hospital and sid else None

    if request.method == "POST":
        form=HospitalServicesForm(data=request.POST,files=request.FILES or None,instance=instance)
        if form.is_valid():
            f=form.save(commit=False)
            f.hospital=hospital
            f.created_by=request.user
            f.updated_by=request.user
            f.save()
            print("Services before saving M2M:", form.cleaned_data['timslot'])  # Should not be None
            form.save_m2m()    # Then save the many-to-many relationships
            print("form.save_m2m():- ",form.save_m2m())

            toast = {"level": "success", "message": f"Service Added for { hospital.name}!"}
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "Changed": True,
                        "closeModal": True,
                        "showToast": toast,
                        "reloadServices": True
                        })})
    else:
        form=HospitalServicesForm(instance=instance)
        return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": f"Edited Hospital Service!" if instance else "Add Hospital's Services!"})




@login_required(login_url="login_admin")
def hospital_appoinment(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Hospital",
        # "description": "List of Users",
        "url": f"{reverse('hospitals_appoinment_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Hospital"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def hospitals_appoinment_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Hospitals",
        "description": "List of Hospitals",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_hospitals_appoinment_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        # "hx_add_button": [
        #         {"url": reverse('add_hospital'),"icon": "","text": "Add Hospital", "bs_toggle": "modal"},
        #         ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class HospitalsAppoinmentDatatableView(AjaxDatatableView):
    model = Appointment
    title = "Appointments"
    initial_order = [["name", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'booking_reference', 'title': 'Booking Reference No.', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'name', 'title': 'Name', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'email', 'title': 'Email', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'phone', 'title': 'Contact Number', 'visible': True, 'orderable': True, 'searchable': True},
            # {'name': 'description', 'title': 'Image', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'hospital', 'title': 'Hospital', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'services', 'title': 'Services', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'appointment_date', 'title': 'Appointment Date', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'timeslot', 'title': 'Time Slot', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'status', 'title': 'Status', 'visible': True, 'orderable': True, 'searchable': True,'choices':APPOINTMENT_STATUS_CHOICES},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
            # Show the first price (or "N/A" if no prices exist)
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                               </ul>
                        </div>
                        ''' %(
                            reverse('comfirm_appoinment', args=(obj.id,)), "Confirmed",
                            reverse('view_appoinment', args=(obj.id,)), "View",
                            )

    def get_show_column_filters(self, request):
        return True

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "hospital"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        if request.user.is_superuser:
            queryset = Appointment.objects.all()
        else:
            queryset = Appointment.objects.filter(created_by=request.user)
        return queryset



from hospital_app.forms import AppoinmentConfirmationForm

def comfirm_appoinment(request,ap_id):
    appointment = Appointment.objects.get(id=ap_id)
    if request.method == 'POST':
        form=AppoinmentConfirmationForm(data=request.POST,instance=appointment)
        if form.is_valid():
            form.save()

            toast = {"level": "success", "message": f"Status of Appoinment has {appointment.get_status_display()} changed!"}

            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger':json.dumps({
                            "tableChanged": True,
                            "closeModal": True,
                            "showMessage": toast,
                    })
                }
            )

    else:
        form = AppoinmentConfirmationForm(instance=appointment)
        return render(request, 'dashboard/partials/add_form.html', context={'form': form, "title": f"Update Confirmation!"})




def view_appoinmemt(request,ap_id):
    appoinment=Appointment.objects.get(id=ap_id)
    return render(request,'dashboard/partials/appoinment_view.html',context={'appoinment': appoinment, "title": f"View Appoinment!"})






@login_required(login_url="login_admin")
def enquiries(request):  
    query_string = request.GET.urlencode()
    context = {
        "title": "Enquires",
        # "description": "List of Users",
        "url": f"{reverse('enquiries_filtered')}{'?' + query_string if  query_string else ''}",
        "bread_crumbs":  [
                        {"name": "Home", "url": reverse("index")}, {"name": "Hospital"}, 
                    ]
        }
    return render(request, 'dashboard/filter-datatable-init.html', context)


def enquiries_filtered(request):
    query_string = request.GET.urlencode()
    
    filled_fields = 0
    for key, value in request.GET.items():
        if value:
            filled_fields += 1
            
    context = {
        "title": "Hospitals",
        "description": "List of Hospitals",
        # "filterForm": {"title": "Filter Users", "form": filter.form, "select2": True},
        
        "url": f"{reverse('ajax_datatable_enquiries_filter_list',)}?{query_string}",
        "params": query_string,
        "filled_fields": filled_fields,
        # "hx_add_button": [
        #         {"url": reverse('add_hospital'),"icon": "","text": "Add Hospital", "bs_toggle": "modal"},
        #         ],
        # "export_button": {"url": reverse('users_export'), "icon": '<i class="ti ti-table-export"></i>'},
        # "export_history": {"url": reverse('users_export_history'), "icon": '<i class="ti ti-clock"></i>'},
    }
    response = render(request, 'dashboard/partials/filter-datatable.html', context=context)
    if query_string:
        response['HX-Trigger'] = json.dumps({"closeModal": True})
    return response


class EnquiriesDatatableView(AjaxDatatableView):
    model = Enquiry
    title = "Appointments"
    initial_order = [["name", "dsc"], ]
    length_menu = [[10, 20, 30, 50], [10, 20, 30, 50]]
    search_values_separator = '+'
    column_defs = [
            {'name': 'SN', 'visible': True, 'placeholder': True, 'orderable': False, 'searchable': False, 'className': "sn-no" },
            {'name': 'name', 'title': 'Name', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'email', 'title': 'Email', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'phone', 'title': 'Contact Number', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'subject', 'title': 'Subject', 'visible': True, 'orderable': True, 'searchable': True},
            {'name': 'action', "title": "Action",  'visible': True,  'orderable': False,  'searchable': False, 'width': '2rem'},
    ]


    def customize_row(self, row, obj):
            # Show the first price (or "N/A" if no prices exist)
        row['action'] = '''
                        <div class="btn-group">
                            <button type="button" class="btn btn-primary btn-icon rounded-pill dropdown-toggle hide-arrow waves-effect waves-light" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="ti ti-dots-vertical"></i>
                            </button>
                            <ul class="dropdown-menu dropdown-menu-end" style="">
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                                <a class="dropdown-item waves-effect" hx-get="%s" hx-target="#modal-content" data-bs-toggle="modal" data-bs-target="#modal">%s</a>
                               </ul>
                        </div>
                        ''' %(
                            reverse('comfirm_appoinment', args=(obj.id,)), "Reply",
                            reverse('view_appoinment', args=(obj.id,)), "View",
                            )

    def get_show_column_filters(self, request):
        return True

    def get_column_defs(self, request):
        if request.user.is_superuser:
            return self.column_defs
        else:
            column_defs = [entry for entry in self.column_defs if entry['name'] not in "hospital"]
            return column_defs 
    
    def get_initial_queryset(self, request=None):
        if request.user.is_superuser:
            queryset = Enquiry.objects.all()
        return queryset




