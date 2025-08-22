from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Employee
from django.contrib.auth import logout
from admin_dashboard.forms import UserRegistrationForm
from admin_dashboard.forms import EmployeeForm


@login_required
def employee_dashboard(request):
    """Employee dashboard view"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        # If user doesn't have employee profile, redirect to create one
        messages.warning(request, 'Please complete your employee profile.')
        return redirect('core:create_employee_profile')
    
    current_shift = employee.get_current_shift()
    next_shift = employee.get_next_shift()
    
    context = {
        'employee': employee,
        'current_shift': current_shift,
        'next_shift': next_shift,
        'now': timezone.now(),
    }
    return render(request, 'core/employee_dashboard.html', context)


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully! Please complete your employee profile.')
            return redirect('core:create_employee_profile')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'core/register.html', context)


@login_required
def create_employee_profile(request):
    """Create employee profile for existing user"""
    try:
        # Check if user already has an employee profile
        existing_profile = request.user.employee_profile
        messages.info(request, 'You already have an employee profile.')
        return redirect('core:employee_dashboard')
    except Employee.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            messages.success(request, 'Employee profile created successfully!')
            return redirect('core:employee_dashboard')
    else:
        form = EmployeeForm()
    
    context = {'form': form}
    return render(request, 'core/create_employee_profile.html', context)


@login_required
def update_employee_profile(request):
    """Update employee profile"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'Employee profile not found.')
        return redirect('core:create_employee_profile')
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:employee_dashboard')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {'form': form, 'employee': employee}
    return render(request, 'core/update_employee_profile.html', context)

@login_required
def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard:dashboard')
        else:
            return redirect('core:employee_dashboard')
    
    return render(request, 'core/home.html')
