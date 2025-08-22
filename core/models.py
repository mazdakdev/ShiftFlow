from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    working_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0.00)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_current_shift(self):
        """Get the current active shift for this employee"""
        now = timezone.now()
        return self.shifts.filter(
            start_time__lte=now,
            end_time__gte=now
        ).first()

    def get_next_shift(self):
        """Get the next upcoming shift for this employee"""
        now = timezone.now()
        return self.shifts.filter(
            start_time__gt=now
        ).order_by('start_time').first()

    def is_on_leave_today(self):
        """Check if employee is on leave today"""
        today = timezone.now().date()
        return self.leaves.filter(
            date=today,
            status='approved'
        ).exists()

    def get_today_leave(self):
        """Get today's leave if exists"""
        today = timezone.now().date()
        return self.leaves.filter(
            date=today,
            status='approved'
        ).first()


class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    employees = models.ManyToManyField(Employee, related_name='shifts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"

    def is_active(self):
        """Check if the shift is currently active"""
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    def is_finished(self):
        """Check if the shift has finished"""
        now = timezone.now()
        return now > self.end_time

    def is_upcoming(self):
        """Check if the shift is upcoming"""
        now = timezone.now()
        return now < self.start_time

    def duration_hours(self):
        """Calculate shift duration in hours"""
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 3600


class Leave(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]
    
    LEAVE_TYPE_CHOICES = [
        ('annual', 'مرخصی سالانه'),
        ('sick', 'مرخصی استعلاجی'),
        ('personal', 'مرخصی شخصی'),
        ('other', 'سایر'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='annual')
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['employee', 'date']

    def __str__(self):
        return f"{self.employee.name} - {self.date} ({self.get_leave_type_display()})"

    def approve(self, user):
        """Approve the leave"""
        self.status = 'approved'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()

    def reject(self, user):
        """Reject the leave"""
        self.status = 'rejected'
        self.approved_by = user
        self.approved_at = timezone.now()
        self.save()
