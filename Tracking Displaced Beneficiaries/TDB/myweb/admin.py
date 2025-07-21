# type: ignore
from django.contrib import admin
from .models import MissingPerson

@admin.register(MissingPerson)
class MissingPersonAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'name', 'age', 'gender', 'status', 'priority', 'current_location', 'date_reported']
    list_filter = ['status', 'priority', 'date_reported', 'age', 'gender']
    search_fields = ['name', 'father_name', 'mother_name', 'case_number', 'family_contact']
    readonly_fields = ['case_number', 'date_reported', 'created_at', 'updated_at']
    list_editable = ['status', 'priority']
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_number', 'status', 'priority', 'date_reported')
        }),
        ('Personal Information', {
            'fields': ('name', 'age', 'gender', 'photo')
        }),
        ('Location Information', {
            'fields': ('current_location', 'last_seen_location', 'last_seen_date')
        }),
        ('Family Information', {
            'fields': ('father_name', 'mother_name', 'family_contact', 'family_phone')
        }),
        ('Additional Information', {
            'fields': ('address', 'medical_info', 'identification_docs', 'comments')
        }),
        ('System Information', {
            'fields': ('reported_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )