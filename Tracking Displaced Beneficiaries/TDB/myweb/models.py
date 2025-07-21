# type: ignore
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class MissingPerson(models.Model):
    STATUS_CHOICES = [
        ('missing', 'Missing'),
        ('found', 'Found'),
        ('deceased', 'Deceased'),
        ('safe', 'Safe'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], blank=True)
    
    # Location Information
    current_location = models.CharField(max_length=200)
    last_seen_location = models.CharField(max_length=200, blank=True)
    
    # Family Information
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    family_contact = models.CharField(max_length=100, blank=True)
    family_phone = models.CharField(max_length=20, blank=True)
    
    # Case Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='missing')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    case_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    
    # Additional Information
    address = models.TextField()
    medical_info = models.TextField(blank=True)
    identification_docs = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    
    # Metadata
    date_reported = models.DateTimeField(default=timezone.now)
    last_seen_date = models.DateField(null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='missing_photos/', blank=True, null=True)
    
    # Tracking
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate case number: MP-YYYY-XXXX
            year = timezone.now().year
            last_case = MissingPerson.objects.filter(case_number__startswith=f'MP-{year}').order_by('-case_number').first()
            if last_case:
                try:
                    last_number = int(last_case.case_number.split('-')[-1])
                    new_number = last_number + 1
                except:
                    new_number = 1
            else:
                new_number = 1
            self.case_number = f'MP-{year}-{new_number:04d}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        case_num = self.case_number or "No Case Number"
        return f"{case_num} - {self.name} - Age {self.age}"
    
    class Meta:
        ordering = ['-date_reported']