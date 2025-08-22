from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('profile/create/', views.create_employee_profile, name='create_employee_profile'),
    path('profile/update/', views.update_employee_profile, name='update_employee_profile'),
]
