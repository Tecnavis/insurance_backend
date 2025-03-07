from datetime import date, timezone
from rest_framework import serializers
from datetime import datetime  
from insurance.models import InsuranceCategory, InsuranceSubCategory ,PolicyOwner,Insurance

    
class InsuranceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceCategory
        fields = ['id', 'name', 'description', 'is_active']

class InsuranceSubCategorySerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceCategory.objects.all(),
        source='category', 
        write_only=True
    )

    category = InsuranceCategorySerializer(read_only=True) 

    class Meta:
        model = InsuranceSubCategory
        fields = ['id', 'name','description_subcategory', 'category', 'category_id',]


class PolicyOwnerSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.CharField()

    class Meta:
        model = PolicyOwner
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate_date_of_birth(self, value):
        """Convert dd-MM-yyyy to YYYY-MM-DD"""
        try:
            return datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format. Use dd-MM-yyyy.")



class InsurancePolicySerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    insurance_category = InsuranceCategorySerializer(read_only=True)
    insurance_sub_category = InsuranceSubCategorySerializer(read_only=True)
    policy_owner = PolicyOwnerSerializer(read_only=True)

    class Meta:
        model = Insurance
        fields = [
            'id', 'policy_number', 'customer_name', 'customer_email', 
            'customer_phone', 'insurance_type', 'premium_amount',
            'start_date', 'expiry_date', 'status', 'status_display',
            'days_remaining', 'insurance_category', 'insurance_sub_category', 'policy_owner',
            'created_at', 'updated_at'
        ]

    def get_days_remaining(self, obj):
        if obj.expiry_date:
            remaining = (obj.expiry_date - date.today()).days
            return max(remaining, 0)  
        return None
