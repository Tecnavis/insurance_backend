from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

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
    
    @classmethod
    def get_soon_to_expire(cls, days=7):
        """Returns policies expiring within specified days"""
        today = timezone.now().date()
        threshold_date = today + timedelta(days=days)
        
        return cls.objects.filter(
            status="active",
            expiry_date__gte=today,
            expiry_date__lte=threshold_date
        ).order_by('expiry_date')
