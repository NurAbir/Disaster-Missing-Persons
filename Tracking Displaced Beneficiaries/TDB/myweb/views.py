from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import MissingPerson
from .forms import MissingPersonForm

def home(request):
    missing_persons = MissingPerson.objects.all()[:10]  # Show latest 10
    return render(request, 'home.html', {'missing_persons': missing_persons})

def add_missing_person(request):
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Missing person report has been submitted successfully.')
            return redirect('home')
    else:
        form = MissingPersonForm()
    return render(request, 'missing_form.html', {'form': form})

def person_detail(request, pk):
    person = get_object_or_404(MissingPerson, pk=pk)
    return render(request, 'person_detail.html', {'person': person})