
from celery import shared_task

from zapslot.celery import *
from core.models import *
import json
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Context, Template
from django.utils.timezone import now
from django.contrib.sites.models import Site
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from hospital_app.models import Appointment




def send_email(subject, to_mail, html, plain_text=None, cc_mails=None):
    # Gmail SMTP Configuration
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USERNAME = "rishukumargupta.offical@gmail.com"         # Replace with your Gmail address
    SMTP_PASSWORD = "lchdbgwtsregomin"            # Use App Password if 2FA is enabled
    SMTP_TLS = True

    # Email Details
    sender_email = SMTP_USERNAME
    recipients = to_mail if isinstance(to_mail, list) else [to_mail]
    
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    # Optional CC
    if cc_mails:
        cc_recipients = cc_mails if isinstance(cc_mails, list) else [cc_mails]
        msg["Cc"] = ", ".join(cc_recipients)
        recipients += cc_recipients

    # Attach plain text and HTML content
    if plain_text:
        msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        if SMTP_TLS:
            server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")



@shared_task
def send_email_password_set_new(hash_code,to_mail=None,cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="set_password")
    
    rest_url=f"http://{Site.objects.get_current().domain}/set_new_password/{hash_code}"

    start_date = now()
    subject = Template(t.subject).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    plain_text = Template(t.plain_text).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({ "data": rest_url}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")



@shared_task
def send_email_password_forgot(hash_code,to_mail=None,cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="reset_password")
    
    rest_url=f"http://{Site.objects.get_current().domain}/reset_password/{hash_code}"

    start_date = now()
    subject = Template(t.subject).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    plain_text = Template(t.plain_text).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({ "data": rest_url}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")

@shared_task
def secure_account_set_password(hash_code,to_mail=None,cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="secure-your-account-set-password")
    
    rest_url=f"http://{Site.objects.get_current().domain}/reset_password/{hash_code}"

    start_date = now()
    subject = Template(t.subject).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    plain_text = Template(t.plain_text).render(Context({"start_date": start_date.strftime("%d-%m-%Y")}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({ "data": rest_url}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")


@shared_task
def appointment_confirmation(appoinment_id,to_mail=None,cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="appointment-confirmation")
    
    appointment = get_object_or_404(Appointment, id=appoinment_id)
    
    current_site=Site.objects.get_current().domain

    start_date = now()
    subject = Template(t.subject).render(Context({}))
    plain_text = Template(t.plain_text).render(Context({}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({"appoinment":appointment,'current_site':current_site}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")

@shared_task
def user_enquiry_tasks(enqiuey_id,to_mail=None,cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="user-enquiry-received")
    
    enquiry = get_object_or_404(Enquiry, id=enqiuey_id)
    
    subject = Template(t.subject).render(Context({}))
    plain_text = Template(t.plain_text).render(Context({}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({"enquiry":enquiry}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")

@shared_task
def admin_enquiry_tasks(enqiuey_id,to_mail="rishukumargupta8409@gmail.com",cc_mails=None):
    t = get_object_or_404(EmailTemplate, slug="admin-enquiry-received")
    
    enquiry = get_object_or_404(Enquiry, id=enqiuey_id)
    
    subject = Template(t.subject).render(Context({}))
    plain_text = Template(t.plain_text).render(Context({}))
    header = Template(t.html_header).render(Context({}))
    footer = Template(t.html_footer).render(Context({}))
    html = Template(t.html).render(Context({"enquiry":enquiry}))
    
    html = header + html + footer

    send_email(subject,to_mail,html,plain_text,cc_mails)

    print("email has sent!")




