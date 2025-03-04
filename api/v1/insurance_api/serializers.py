from datetime import timezone
from rest_framework import serializers
from insurance.models import Insurance
from insurance.models import InsuranceCategory, InsuranceSubCategory  

class InsurancePolicySerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Insurance
        fields = [
            'id', 'policy_number', 'customer_name', 'customer_email', 
            'customer_phone', 'insurance_type', 'premium_amount',
            'start_date', 'expiry_date', 'status', 'status_display',
            'days_remaining', 'created_at', 'updated_at'
        ]
    
    def get_days_remaining(self, obj):
        if obj.status == 'active':
            today = timezone.now().date()
            remaining = (obj.expiry_date - today).days
            return max(0, remaining)
        return 0
    
class InsuranceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCategory
        fields = ['id', 'name', 'description', 'is_active']
       

class InsuranceSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceSubCategory
        fields = ['id', 'name', 'category'] 