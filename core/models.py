from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from multiselectfield import MultiSelectField
import secrets
import string

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError("Email or phone must be provided.")

        email = self.normalize_email(email) if email else None
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email=email, password=password, **extra_fields)

# Role/Access Control
ROLE_CHOICES = [
    (0, "Select Role"),
    (1, "Patient"),
    (2, "Doctor"),
    (3, "Nurse"),
]

gender_choice=[(1, 'Male'), (2, 'Female'), (3, 'Other')]

SPECIALIZATION_CHOICES = [
    (1, "General Medicine"),
    (2, "Family Medicine"),
    (3, "Internal Medicine"),
    (4, "Pediatrics"),
    (5, "Obstetrics and Gynecology"),
    (6, "General Surgery"),
    (7, "Orthopedics"),
    (8, "Cardiology"),
    (9, "Neurology"),
    (10, "Neurosurgery"),
    (11, "Gastroenterology"),
    (12, "Hepatology"),
    (13, "Endocrinology"),
    (14, "Pulmonology (Chest Medicine)"),
    (15, "Nephrology"),
    (16, "Urology"),
    (17, "Dermatology"),
    (18, "Ophthalmology"),
    (19, "ENT (Otorhinolaryngology)"),
    (20, "Psychiatry"),
    (21, "Radiology"),
    (22, "Oncology"),
    (23, "Hematology"),
    (24, "Rheumatology"),
    (25, "Anesthesiology"),
    (26, "Emergency Medicine"),
    (27, "Critical Care Medicine"),
    (28, "Nuclear Medicine"),
    (29, "Geriatrics"),
    (30, "Allergy and Immunology"),
    (31, "Infectious Diseases"),
    (32, "Plastic Surgery"),
    (33, "Pediatric Surgery"),
    (34, "Thoracic Surgery"),
    (35, "Vascular Surgery"),
    (36, "Pain Management"),
    (37, "Sports Medicine"),
    (38, "Rehabilitation Medicine (PM&R)"),
    (39, "Occupational Medicine"),
    (40, "Transfusion Medicine"),
    (41, "Pathology"),
    (42, "Medical Genetics"),
    (43, "Forensic Medicine"),
    (44, "Sexual Health and Andrology"),
    (45, "Sleep Medicine"),
    (46, "Preventive and Social Medicine (PSM)"),
]

# Define the list of qualifications with integer keys
QUALIFICATION_CHOICES = [
    (1, "MBBS - Bachelor of Medicine, Bachelor of Surgery"),
    (2, "BDS - Bachelor of Dental Surgery"),
    (3, "BHMS - Bachelor of Homeopathic Medicine & Surgery"),
    (4, "BAMS - Bachelor of Ayurvedic Medicine & Surgery"),
    (5, "BUMS - Bachelor of Unani Medicine & Surgery"),
    (6, "BSMS - Bachelor of Siddha Medicine & Surgery"),
    (7, "BNYS - Bachelor of Naturopathy and Yogic Sciences"),
    (8, "B.Sc Nursing"),
    (9, "GNM - General Nursing and Midwifery"),
    (10, "BPT - Bachelor of Physiotherapy"),
    (11, "BOT - Bachelor of Occupational Therapy"),
    (12, "BMLT - Bachelor of Medical Laboratory Technology"),
    (13, "B.Pharm - Bachelor of Pharmacy"),
    (14, "MD - Doctor of Medicine"),
    (15, "MS - Master of Surgery"),
    (16, "MPT - Master of Physiotherapy"),
    (17, "MOT - Master of Occupational Therapy"),
    (18, "MMLT - Master of Medical Lab Technology"),
    (19, "MPH - Master of Public Health"),
    (20, "MPTh - Master of Physiotherapy"),
    (21, "MHA - Master of Hospital Administration"),
    (22, "M.Sc Nursing"),
    (23, "DM - Doctorate of Medicine (Super-specialty)"),
    (24, "MCh - Magister Chirurgiae / Master of Surgery (Super-specialty)"),
    (25, "M.Pharm - Master of Pharmacy"),
    (26, "Pharm.D - Doctor of Pharmacy"),
    (27, "PhD - Doctor of Philosophy"),
    (28, "M.Phil - Master of Philosophy"),
    (29, "DNB - Diplomate of National Board"),
    (30, "Postgraduate Diploma (Various Specializations)"),
    (31, "Diploma in Paramedical Sciences"),
    (32, "DMLT - Diploma in Medical Lab Technology"),
    (33, "MD (USA)"),
    (34, "DO - Doctor of Osteopathic Medicine (USA)"),
    (35, "MBChB - Bachelor of Medicine and Bachelor of Surgery (UK)"),
    (36, "MBBCh - Bachelor of Medicine and Bachelor of Surgery (Ireland/South Africa)"),
]

DAYS_CHOICES = [
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
]

class CustomUser(AbstractBaseUser, PermissionsMixin):
    registration_code=models.CharField(max_length=16,unique=True)
    # Basic contact info
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    # Personal details
    full_name = models.CharField(max_length=100)
    gender = models.PositiveIntegerField(default=1, choices=gender_choice)
    date_of_birth = models.DateField(null=True, blank=True)

    # Address info
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='India')
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # Role
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        default=0
        )

    # Optional fields used based on role
    # Doctor-specific
    specialization = models.ForeignKey(
        'Specialization',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Choose your specialization by selecting"
    )
    qualification_level = models.ForeignKey(
        'Qualification',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Choose your qualification by selecting"
    )
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    registration_number = models.CharField(max_length=50, unique=True,help_text="Official license number or registration number",null=True,blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)
    available_days = MultiSelectField(
        choices=DAYS_CHOICES,
        max_length=100,  # To ensure the field can hold multiple choices
        blank=True,
        null=True,
        help_text="Select the days you are available."
    )

    hospitals=models.ForeignKey("hospital_app.Hospital",on_delete=models.CASCADE,null=True,blank=True)
    hospital_services=models.ForeignKey("hospital_app.HospitalServices",on_delete=models.CASCADE,null=True,blank=True)

    clinic_location = models.CharField(max_length=255, blank=True, null=True,help_text="If you have your own clinic, please enter the location here.")

    # Patient-specific
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    insurance_provider = models.CharField(max_length=100, blank=True, null=True)
    insurance_number = models.CharField(max_length=50, blank=True, null=True,unique=True)
    medical_history = models.TextField(blank=True, null=True)

    # Staff/General purpose
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_available = models.BooleanField(default=True)  # for doctors/staff availability
    is_verified = models.BooleanField(default=False)
    designation = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    # System fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def generate_registration_code(self):
        """Generates a random 16-character registration code."""
        characters = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(characters) for i in range(16))

    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = self.generate_registration_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.email or self.phone

    def is_doctor(self):
        return self.role == 2

    def is_patient(self):
        return self.role == 1
    
    def is_patient(self):
        return self.role == 3

    def is_admin(self):
        return self.role == 5
    
    def is_staff(self):
        return self.role == 4




class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='specialization_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Qualification(models.Model):
    title = models.CharField(max_length=100, unique=True,help_text="Enter the name of the qualification (e.g., MBBS, MD, BDS). Must be unique.")  # e.g. MBBS, MD, BDS
    issuing_authority = models.CharField(max_length=150, blank=True, null=True,help_text="Name of the authority or institution that issues this qualification (optional).")
    description = models.TextField(blank=True, null=True,help_text="Detailed description of the qualification (optional).")

    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='qualification_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




## email templates model
class EmailTemplate(models.Model):
    template_name = models.CharField(
        max_length=100, unique=True,
    )
    slug = models.SlugField(unique=True)
    subject = models.CharField(
        max_length=100,
    )
    html_header = models.TextField(blank=True, null=True, )
    html_footer =models.TextField(blank=True, null=True, )

    heading = models.CharField(
        max_length=100,
    )

    plain_text = models.TextField(
    )

    html = models.TextField(
    )

    locale = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    def _str_(self):
        return '%s' % self.template_name

    class Meta:
        ordering = ('template_name', 'locale')

        permissions = (
            ("mandate_add_emailtemplate", "Mandate Add EmailTemplate"),
            ("mandate_edit_emailtemplate", "Mandate Edit EmailTemplate"),
            ("mandate_delete_emailtemplate", "Mandate Delete EmailTemplate"),
        )
        
    def save(self):

        super(EmailTemplate,self).save()

    def __str__(self):
        return f"{self.template_name} - {self.subject}"




import datetime
import hashlib
from django.utils import timezone
import time, datetime

class RegistrationLink(models.Model):
    user =models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hash = models.CharField(max_length=64, unique=True, blank=True)
    expired =models.BooleanField(default=False)
    expiry_time = models.DateTimeField(null=True, blank=True)


    def save(self):
        if not self.id:
            self.expiry_time = timezone.now()+ datetime.timedelta(2,0,0)
        text= (str(self.user.phone) + str(time.time())).encode("utf-8")
        self.hash = hashlib.sha256(text).hexdigest()

        super(RegistrationLink, self).save()
    def __str__(self):
        return str(self.user)


class PasswordGenLink(models.Model):
    email = models.EmailField()
    hash = models.CharField(max_length=64)
    expired = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    expiry_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self):
        if not self.id:
            self.created =timezone.now()
        self.hash = hashlib.sha256(str(time.time()).encode("utf-8")+str(self.email).encode("utf-8")).hexdigest()
        super(PasswordGenLink,self ).save()





class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    subscribe_newsletter = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


