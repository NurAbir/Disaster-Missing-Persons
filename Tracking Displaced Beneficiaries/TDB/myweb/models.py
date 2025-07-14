from django.db import models
from django.utils import timezone

class MissingPerson(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    current_location = models.CharField(max_length=200)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    address = models.TextField()
    comments = models.TextField(blank=True)
    date_reported = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='missing_photos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - Age {self.age}"
    
    class Meta:
        ordering = ['-date_reported']