from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import EmployeeForm, ShiftForm, UserRegistrationForm
from core.models import Employee, Shift
from django.utils import timezone


def is_admin(user):
    """Check if user is admin (staff user)"""
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard view"""
    total_employees = Employee.objects.count()
    total_shifts = Shift.objects.count()
    active_shifts = Shift.objects.filter(
        start_time__lte=timezone.now(),
        end_time__gte=timezone.now()
    ).count()
    
    recent_employees = Employee.objects.order_by('-created_at')[:5]
    recent_shifts = Shift.objects.order_by('-created_at')[:5]
    
    context = {
        'total_employees': total_employees,
        'total_shifts': total_shifts,
        'active_shifts': active_shifts,
        'recent_employees': recent_employees,
        'recent_shifts': recent_shifts,
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Employee
    template_name = 'admin_dashboard/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_staff


class EmployeeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'admin_dashboard/employee_form.html'
    success_url = reverse_lazy('admin_dashboard:employee_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee created successfully!')
        return super().form_valid(form)


class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'admin_dashboard/employee_form.html'
    success_url = reverse_lazy('admin_dashboard:employee_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee updated successfully!')
        return super().form_valid(form)


class EmployeeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Employee
    template_name = 'admin_dashboard/employee_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:employee_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Employee deleted successfully!')
        return super().delete(request, *args, **kwargs)


class ShiftListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Shift
    template_name = 'admin_dashboard/shift_list.html'
    context_object_name = 'shifts'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_staff


class ShiftCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'admin_dashboard/shift_form.html'
    success_url = reverse_lazy('admin_dashboard:shift_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Shift created successfully!')
        return super().form_valid(form)


class ShiftUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'admin_dashboard/shift_form.html'
    success_url = reverse_lazy('admin_dashboard:shift_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Shift updated successfully!')
        return super().form_valid(form)


class ShiftDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Shift
    template_name = 'admin_dashboard/shift_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard:shift_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Shift deleted successfully!')
        return super().delete(request, *args, **kwargs)


@login_required
@user_passes_test(is_admin)
def create_employee_with_user(request):
    """Create both User and Employee in one form"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        
        if user_form.is_valid() and employee_form.is_valid():
            with transaction.atomic():
                user = user_form.save()
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
                
            messages.success(request, 'Employee and user account created successfully!')
            return redirect('admin_dashboard:employee_list')
    else:
        user_form = UserRegistrationForm()
        employee_form = EmployeeForm()
    
    context = {
        'user_form': user_form,
        'employee_form': employee_form,
    }
    return render(request, 'admin_dashboard/create_employee_with_user.html', context)
