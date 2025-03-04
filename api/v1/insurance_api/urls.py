from django.urls import path
from . import views

app_name = 'insurance_api'

urlpatterns = [
    
    path('insurances/', views.insurance_list, name='insurance_list'),
    path('insurances/<int:id>/', views.insurance_detail, name='insurance_detail'),
    path('insurances/create/', views.create_insurance, name='create_insurance'),
    path('insurances/<int:id>/', views.update_insurance, name='update_insurance'),
    path('insurances/<int:id>/', views.delete_insurance, name='delete_insurance'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:id>/', views.update_category, name='update_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='delete_category'),
   
]