from django.contrib import admin
from .models import MissingPerson

@admin.register(MissingPerson)
class MissingPersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'current_location', 'date_reported']
    list_filter = ['date_reported', 'age']
    search_fields = ['name', 'father_name', 'mother_name']
    readonly_fields = ['date_reported']