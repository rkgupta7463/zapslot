from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate
import socket
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout
from core.forms import *
from core.models import *
from django.shortcuts import redirect
from core.tasks import *
from django.utils.timezone import timedelta

# Create your views here.


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(
                status=204,
                headers={
                    'HX-Redirect': "/"
                }
            )
        else:
            return HttpResponse("""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> Invalid username or password!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")

    return render(request, 'login.html')

def load_role_specific_fields(request):
    role = request.GET.get('role')
    print("Raw role:", role)

    form = CustomUserRegistrationForm()
    fields = []

    try:
        role = int(role)  # Convert from string to integer
        if role in [2, 3]:  # Doctor or Nurse
            fields = [form[f] for f in [
                'full_name', 'email', 'phone', 'gender',
                'specialization', 'qualification_level', 'experience_years',
                'registration_number', 'consultation_fee', 'available_from',
                'available_to', 'available_days', 'clinic_location'
            ]]
        elif role == 1:  # Patient
            fields = [form[f] for f in [
                'full_name', 'email', 'phone', 'gender', 'date_of_birth',
                'address', 'city', 'state', 'country', 'pincode',
                'blood_group', 'emergency_contact', 'insurance_provider',
                'insurance_number'
            ]]
    except (ValueError, TypeError):
        print("Invalid role received:", role)

    return render(request, "main/plugins/role_specific_fields.html", {'fields': fields})



@csrf_exempt
def register_user_view(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
                # Generate registration link
            if user:
                reg_link = RegistrationLink(user=user)
                reg_link.expiry_time = timezone.now() + timedelta(hours=24, minutes=59, microseconds=59)
                reg_link.save()
                try:
                    send_email_password_set_new.delay(to_mail=user.email, hash_code=reg_link.hash)
                    print("Email sent!")
                except Exception as e:
                    print("Email sending error: ", e)

            return HttpResponse("""<div class="alert alert-success alert-dismissible fade show mt-2" role="alert">
                        <strong>Success!</strong> A link to set your password has been sent to your email. Please check your inbox (or spam folder) and follow the instructions to set your new password.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    """)
            # login(request, user)
            # return HttpResponse(status=204, headers={'HX-Redirect': '/'})
        else:
            return HttpResponse(f"""<div class="alert alert-warning alert-dismissible fade show mt-2" role="alert">
                        <strong>Warning!</strong> {form.errors}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>
                    """)
        

    form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})





#### forgot_password_reg_email

def forgot_password_form(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user=CustomUser.objects.get(email=email)
            except:
                return HttpResponse("""<div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Warning!</strong> This email is not registered in our Portal.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")
            if user:
                expiry_time = timezone.now() + timezone.timedelta(hours=1)  # 1 hour expiry
                reset_link = PasswordGenLink(user=user,email=email, expiry_time=expiry_time)
                reset_link.save()

                send_email_password_forgot.delay(to_mail=email, hash_code=reset_link.hash)
                print("mail sent!")
                return HttpResponse("""<div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Email Sent!</strong> A password reset link has been sent to your registered email address. 
                    Please check your inbox and follow the instructions to reset your password.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")
    else:
        form = ForgotPasswordForm()

    return render(request, "dashboard/accounts/auth-forgot-password-basic.html", {"form": form})



def forgot_password_reg_email(request, hash):
    pass_forgot=None
    error_messages=None
    try:
        pass_forgot = get_object_or_404(PasswordGenLink, hash=hash)
    except Exception as e:
        return HttpResponse("The Link is Invalid or Expired!")

    if pass_forgot.expired or timezone.now() > pass_forgot.expiry_time:
        pass_forgot.expired = True
        pass_forgot.save()
        return HttpResponse("The Link is Invalid or Expired!")

    if request.method == "POST":
        form = EPasswordChangeForm(request.POST)
        if form.is_valid():
            user = pass_forgot.user  
            user.set_password(form.cleaned_data["password1"])
            user.save()

            pass_forgot.expired = True
            pass_forgot.save()

            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Redirect': "/accounts/login/"
                    }
                )
        else:
            # Collect form errors and return as an alert
            for field, error_list in form.errors.items():
                for error in error_list:
                    # messages.error(request, f"{field.capitalize()}: {error}")
                    return HttpResponse(f"""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> {field.capitalize()}: {error}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")
        
    else:
        form = EPasswordChangeForm()

    return render(request, "dashboard/accounts/auth-reset-password-basic.html", {"form": form,"message":error_messages,"hash":hash})


### new set password
def new_set_password_reg_email(request, hash):
    error_messages=None
    try:
        reg_link = RegistrationLink.objects.get(hash=hash)
    except:
        print("exception block of coding is getting runs.....")
        return HttpResponse("The Link is Invalid or Expired!")
    
    if timezone.now() > reg_link.expiry_time:
        reg_link.expired=True
        print("if block of coding is getting runs.....")
        return HttpResponse("The Link is Invalid or Expired!")

    if request.method == "POST":
        form = EPasswordChangeForm(request.POST)
        if form.is_valid():
            u = reg_link.user
            u.set_password(form.cleaned_data["password1"])
            u.is_verified=True
            u.save()
            reg_link.expired = True
            reg_link.save()
            return HttpResponse(
                    status=204,
                    headers={
                        'HX-Redirect': "/main/login/"
                    }
                )
        else:
            # Collect form errors and return as an alert
            for field, error_list in form.errors.items():
                for error in error_list:
                    return HttpResponse(f"""<div class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    <strong>Warning!</strong> {field.capitalize()}: {error}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>""")
    else:
        form = EPasswordChangeForm()

    return render(request, "dashboard/accounts/auth-set_new-password-basic.html", {"form": form,"message":error_messages,"hash":hash}, )


def logout_view(request):
    logout(request)
    return redirect('/')

def index(request):
    return render(request, 'index.html')

def about_us(request):
    return render(request, 'main/about.html')


def contact_us(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            user_enquiry_tasks.delay(enqiuey_id=f.id,to_mail=f.email)
            admin_enquiry_tasks.delay(enqiuey_id=f.id)
            return HttpResponse("""<div class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>Message Sent!</strong> Thank you for reaching out. We have received your enquiry and will get back to you shortly.
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>""")
    else:
        form = EnquiryForm()

    return render(request, 'contact.html', {'form': form})


def doctor_list(request):
    return render(request, 'main/doctor.html')

def department_list(request):
    return render(request, 'main/dep.html')

def services(request):
    return render(request, 'service.html')

def time_table(request):
    return render(request, 'time-table.html')

def doctors_list(request):
    return render(request, 'doctors.html')

def aboutus(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')

def hospital_details(request,title):
    return render(request, 'portfolio-details.html')
