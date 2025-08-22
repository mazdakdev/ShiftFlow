from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Employee management
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee_update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    path('employees/create-with-user/', views.create_employee_with_user, name='create_employee_with_user'),
    
    # Shift management
    path('shifts/', views.ShiftListView.as_view(), name='shift_list'),
    path('shifts/create/', views.ShiftCreateView.as_view(), name='shift_create'),
    path('shifts/<int:pk>/update/', views.ShiftUpdateView.as_view(), name='shift_update'),
    path('shifts/<int:pk>/delete/', views.ShiftDeleteView.as_view(), name='shift_delete'),
    
    # Leave management
    path('leaves/', views.LeaveListView.as_view(), name='leave_list'),
    path('leaves/create/', views.LeaveCreateView.as_view(), name='leave_create'),
    path('leaves/<int:pk>/update/', views.LeaveUpdateView.as_view(), name='leave_update'),
    path('leaves/<int:pk>/delete/', views.LeaveDeleteView.as_view(), name='leave_delete'),
    path('leaves/<int:pk>/approve/', views.leave_approve, name='leave_approve'),
    path('leaves/<int:pk>/reject/', views.leave_reject, name='leave_reject'),
]
