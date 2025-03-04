from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _


class InsuranceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True) 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.name


class InsuranceSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(InsuranceCategory, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Insurance(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
    )

    policy_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    insurance_type = models.CharField(max_length=50)
    category = models.ForeignKey(InsuranceCategory, on_delete=models.SET_NULL, null=True, related_name="insurances")
    sub_category = models.ForeignKey(InsuranceSubCategory, on_delete=models.SET_NULL, null=True, related_name="insurances")
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Insurance Policy")
        verbose_name_plural = _("Insurance Policies")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.policy_number} - {self.customer_name}"
