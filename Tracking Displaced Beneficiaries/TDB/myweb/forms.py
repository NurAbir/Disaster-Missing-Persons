# type: ignore
from django import forms
from .models import MissingPerson

class MissingPersonForm(forms.ModelForm):
    class Meta:
        model = MissingPerson
        fields = [
            'name', 'age', 'gender', 'current_location', 'last_seen_location',
            'father_name', 'mother_name', 'family_contact', 'family_phone',
            'status', 'priority', 'address', 'medical_info', 'identification_docs', 
            'comments', 'last_seen_date', 'photo'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last known location'}),
            'last_seen_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last seen location'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's Name"}),
            'family_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Family contact person'}),
            'family_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Family phone number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Home Address'}),
            'medical_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Medical conditions, medications, etc.'}),
            'identification_docs': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'ID documents, passport, etc.'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional information, circumstances of disappearance, etc.'}),
            'last_seen_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'})
        }