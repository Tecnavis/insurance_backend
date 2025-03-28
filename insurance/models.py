from django.db import models
from users.models import CustomUser
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
    description_subcategory = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class PolicyOwner(models.Model):
    GENDER_CHOICES = (
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Other", _("Other")),
    )

    MARITAL_STATUS_CHOICES = (
        ("Single", _("Single")),
        ("Married", _("Married")),
        ("Divorced", _("Divorced")),
        ("Widowed", _("Widowed")),
    )
    username = models.CharField(max_length=255)
    email=models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    marital_status = models.CharField(max_length=10,choices=MARITAL_STATUS_CHOICES,null=True,blank=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,null=True,blank=True)
    address = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    alternative_phone = models.CharField(max_length=15, null=True, blank=True)
    nominee_name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Policy Owner")
        verbose_name_plural = _("Policy Owners")

    def __str__(self):
        return f"Policy Owner: {self.user.email}"


class Insurance(models.Model):

    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending", "Pending"),
        ("cancelled", "Cancelled"),
    )

    policy_owner = models.ForeignKey(PolicyOwner,on_delete=models.CASCADE, related_name='insurance_policies',null=True,blank=True)
    policy_number = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(InsuranceCategory, on_delete=models.SET_NULL, null=True, related_name="insurances")
    sub_category = models.ForeignKey(InsuranceSubCategory, on_delete=models.SET_NULL, null=True, related_name="insurances")
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    document = models.ImageField(upload_to='insurance_documents/', null=True, blank=True)
    document_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Insurance Policy")
        verbose_name_plural = _("Insurance Policies")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.policy_number} - {self.policy_owner.user.email}"
    
  

   
 
    
