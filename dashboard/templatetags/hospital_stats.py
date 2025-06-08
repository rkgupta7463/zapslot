from django import template
from django.db.models import Count, Avg
from hospital_app.models import Hospital, HospitalReview

register = template.Library()

@register.simple_tag
def total_hospitals():
    return Hospital.objects.filter(is_active=True, is_deleted=False).count()

@register.simple_tag
def total_reviews():
    return HospitalReview.objects.count()

@register.simple_tag
def average_hospital_rating():
    avg = HospitalReview.objects.aggregate(avg_rating=Avg('rating'))['avg_rating']
    return round(avg, 1) if avg else 0

@register.simple_tag
def most_reviewed_hospital():
    hospital = Hospital.objects.annotate(review_count=Count('reviews')).order_by('-review_count').first()
    return hospital.name if hospital else "No reviews yet"
