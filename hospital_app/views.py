from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from core.tasks import appointment_confirmation,secure_account_set_password


def appoinment_view(request):
    return render(request,'appointment.html')


def book_appoinment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            f=form.save(commit=False)
            f.save()
            print("form has submitted!!")
            appointment_confirmation.delay(to_mail=f.email,appoinment_id=f.id)
            return HttpResponse("""<div class="alert alert-success mt-2" role="alert">Appoinment Booking Confirmed!</div>""")
        else:
            print("fo9orm error:- ",form.errors)
    else:
        form = AppointmentForm()
    
    return render(request, 'partials/appointment_form.html', {'form': form})






