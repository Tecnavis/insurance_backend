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

    path('subcategories/', views.list_subcategories, name='list_subcategories'),
    path('subcategories/create/', views.create_subcategory, name='create_subcategory'),
    path('subcategories/<int:subcategory_id>/', views.update_subcategory, name='update_subcategory'),
    path('subcategories/<int:subcategory_id>/delete/', views.delete_subcategory, name='delete_subcategory'),

    path("policy-owners/", views.list_policy_owners, name="list-policy-owners"),
    path("policy-owner/create/", views.create_policy_owner, name="create-policy-owner"),
    path("policy-owner/<int:id>/", views.update_policy_owner, name="update-policy-owner"),
    path("policy-owner/<int:id>/delete/", views.delete_policy_owner, name="delete-policy-owner"),
   
]