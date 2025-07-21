# type: ignore
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import MissingPerson
from .forms import MissingPersonForm

def home(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    # Start with all missing persons
    missing_persons = MissingPerson.objects.all()
    
    # Apply search filter
    if search_query:
        missing_persons = missing_persons.filter(
            Q(name__icontains=search_query) |
            Q(father_name__icontains=search_query) |
            Q(mother_name__icontains=search_query) |
            Q(case_number__icontains=search_query) |
            Q(current_location__icontains=search_query) |
            Q(family_contact__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        missing_persons = missing_persons.filter(status=status_filter)
    
    # Apply priority filter
    if priority_filter:
        missing_persons = missing_persons.filter(priority=priority_filter)
    
    # Get statistics
    total_cases = MissingPerson.objects.count()
    missing_cases = MissingPerson.objects.filter(status='missing').count()
    found_cases = MissingPerson.objects.filter(status='found').count()
    urgent_cases = MissingPerson.objects.filter(priority='urgent').count()
    
    context = {
        'missing_persons': missing_persons[:20],  # Show latest 20
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'total_cases': total_cases,
        'missing_cases': missing_cases,
        'found_cases': found_cases,
        'urgent_cases': urgent_cases,
    }
    return render(request, 'home.html', context)

def add_missing_person(request):
    if request.method == 'POST':
        form = MissingPersonForm(request.POST, request.FILES)
        if form.is_valid():
            missing_person = form.save(commit=False)
            if request.user.is_authenticated:
                missing_person.reported_by = request.user
            missing_person.save()
            messages.success(request, f'Missing person report has been submitted successfully. Case Number: {missing_person.case_number}')
            return redirect('home')
    else:
        form = MissingPersonForm()
    return render(request, 'missing_form.html', {'form': form})

def person_detail(request, pk):
    person = get_object_or_404(MissingPerson, pk=pk)
    return render(request, 'person_detail.html', {'person': person})

def update_status(request, pk):
    if request.method == 'POST':
        person = get_object_or_404(MissingPerson, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(MissingPerson.STATUS_CHOICES):
            person.status = new_status
            person.save()
            messages.success(request, f'Status updated to {new_status.title()}')
        return redirect('person_detail', pk=pk)
    return redirect('person_detail', pk=pk)