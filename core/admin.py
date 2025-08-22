from django.contrib import admin
from django.utils.html import format_html
from .models import Employee, Shift


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'working_hours', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'email')
        }),
        ('Work Details', {
            'fields': ('working_hours',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'duration_display', 'employee_count', 'status']
    list_filter = ['start_time', 'end_time', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['employees']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'start_time', 'end_time')
        }),
        ('Employees', {
            'fields': ('employees',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_display(self, obj):
        hours = obj.duration_hours()
        return f"{hours:.2f} hours"
    duration_display.short_description = 'Duration'
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'
    
    def status(self, obj):
        if obj.is_active():
            return format_html('<span style="color: green;">Active</span>')
        elif obj.is_finished():
            return format_html('<span style="color: red;">Finished</span>')
        else:
            return format_html('<span style="color: blue;">Upcoming</span>')
    status.short_description = 'Status'
