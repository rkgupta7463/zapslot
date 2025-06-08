from django.db import migrations, models

def fix_duplicate_insurance_numbers(apps, schema_editor):
    CustomUser = apps.get_model('core', 'CustomUser')
    duplicates = CustomUser.objects.values('insurance_number').annotate(count=models.Count('id')).filter(count__gt=1)
    
    for duplicate in duplicates:
        users = CustomUser.objects.filter(insurance_number=duplicate['insurance_number'])
        for i, user in enumerate(users):
            user.insurance_number = f"{user.insurance_number}_{i+1}"  # Ensure uniqueness
            user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_qualification_created_by_specialization_created_by'),
    ]

    operations = [
        migrations.RunPython(fix_duplicate_insurance_numbers),
        migrations.AddField(
            model_name='customuser',
            name='registration_code',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='insurance_number',
            field=models.CharField(blank=True, max_length=50, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_number',
            field=models.CharField(blank=True, help_text='Official license number or registration number', max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='description',
            field=models.TextField(blank=True, help_text='Detailed description of the qualification (optional).', null=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='issuing_authority',
            field=models.CharField(blank=True, help_text='Name of the authority or institution that issues this qualification (optional).', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='title',
            field=models.CharField(help_text='Enter the name of the qualification (e.g., MBBS, MD, BDS). Must be unique.', max_length=100, unique=True),
        ),
    ]
