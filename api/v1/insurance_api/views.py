import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from insurance.models import Insurance
from .serializers import InsurancePolicySerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from insurance.models import InsuranceSubCategory, InsuranceCategory,PolicyOwner
from .serializers import InsuranceCategorySerializer, InsuranceSubCategorySerializer,PolicyOwnerSerializer,InsuranceSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser


# CRUD INSURANCE CATEGORY

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    print(request.data)
    categories = InsuranceCategory.objects.all()
    serializer = InsuranceCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_category(request):
    print(request.data)
    serializer = InsuranceCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request, id):    
    category = InsuranceCategory.objects.get(id=id)
    serializer = InsuranceCategorySerializer(category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
    try:
        category = InsuranceCategory.objects.get(id=id)
    except InsuranceCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD INSURANCE SUB-CATEGORY

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_subcategories(request):
    subcategories = InsuranceSubCategory.objects.all()
    print(subcategories)
    serializer = InsuranceSubCategorySerializer(subcategories, many=True)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subcategory(request):
    print(request.data)
    serializer = InsuranceSubCategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_subcategory(request, subcategory_id):
    try:
        subcategory = InsuranceSubCategory.objects.get(id=subcategory_id)
    except InsuranceSubCategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InsuranceSubCategorySerializer(subcategory, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_subcategory(request, subcategory_id):
    try:
        subcategory = InsuranceSubCategory.objects.get(id=subcategory_id)
        subcategory.delete()
        return Response({'message': 'Subcategory deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except InsuranceSubCategory.DoesNotExist:
        return Response({'error': 'Subcategory not found'}, status=status.HTTP_404_NOT_FOUND)


# CRUD INSURANCE 
# create insurance
@api_view(['POST'])
@permission_classes([AllowAny])
def create(request):
    serializer = InsurancePolicySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)  



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_insurance(request):
    """
    Create an Insurance record for a policy owner.
    Only admins, super admins, or staff can perform this action.
    """
    serializer = InsuranceSerializer(data=request.data)
    
    if serializer.is_valid():
        policy_number = serializer.validated_data.get("policy_number")
        policy_owner = serializer.validated_data.get("policy_owner")
        category = serializer.validated_data.get("category")
        sub_category = serializer.validated_data.get("sub_category")
        premium_amount = serializer.validated_data.get("premium_amount")
        start_date = serializer.validated_data.get("start_date")
        expiry_date = serializer.validated_data.get("expiry_date")
        status_choice = serializer.validated_data.get("status")
        document = serializer.validated_data.get("document")
        document_url = serializer.validated_data.get("document_url")
        # Check if an insurance record already exists for this policy number
        if Insurance.objects.filter(policy_number=policy_number).exists():
            return Response(
                {"status": 400, "title": "Already Exists", "message": "Insurance record already exists for this policy number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create Insurance record
        insurance = Insurance.objects.create(
            policy_number=policy_number,
            policy_owner=policy_owner,
            category=category,
            sub_category=sub_category,
            premium_amount=premium_amount,
            start_date=start_date,
            expiry_date=expiry_date,
            status=status_choice,
            document=document,
            document_url=document_url,
        )
        
        response_data = {
            "status": 200,
            "title": "Successfully Created",
            "message": "Insurance policy created successfully.",
            "data": serializer.data,
            "redirect": "true",
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    else:
        response_data = {
            "status": 400,
            "title": "Validation Error",
            "message": "Form validation error.",
            "error": serializer.errors,
            "stable": "true",
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


#update insurance
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_insurance(request, pk):
    try:
        insurance = Insurance.objects.get(pk=pk)
    except Insurance.DoesNotExist:    
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = InsurancePolicySerializer(insurance, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete insurance
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_insurance(request, pk):
    try:
        insurance = Insurance.objects.get(pk=pk)
    except Insurance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    insurance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)  

# functionality for list all the users that are remaing 7 days to expire
@api_view(['GET'])
@permission_classes([AllowAny])
def list_expiring_insurance_policies(request):
    days = int(request.query_params.get('days', 7))
    today = datetime.date.today()
    threshold_date = today + datetime.timedelta(days=days)    
    policies = Insurance.objects.filter(
        status="active",
        expiry_date__gte=today,
        expiry_date__lte=threshold_date 
    ).order_by('expiry_date')
    serializer = InsurancePolicySerializer(policies, many=True)
    return Response(
        {
            'count': policies.count(),
            'days_threshold': days,
            'policies': serializer.data
        }
    )



# list all insurance data
@api_view(['GET'])
@permission_classes([AllowAny]) 
def insurance_list(request):
    policies = Insurance.objects.all()
    serializer = InsurancePolicySerializer(policies, many=True)
    return Response(serializer.data)    


# insurance_detail
@api_view(['GET'])  
@permission_classes([AllowAny])
def insurance_detail(request, pk):
    try:
        policy = Insurance.objects.get(pk=pk)
    except Insurance.DoesNotExist:        
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = InsurancePolicySerializer(policy)
    return Response(serializer.data)

# list all the insurance policies
@api_view(['GET'])
@permission_classes([AllowAny])
def list_insurance_policies(request):
    """Function to list all insurance policies with optional filtering"""
    queryset = Insurance.objects.all()
    
    # Apply filters if provided
    status = request.query_params.get('status')
    if status:
        queryset = queryset.filter(status=status)
        
    insurance_type = request.query_params.get('insurance_type')
    if insurance_type:
        queryset = queryset.filter(insurance_type=insurance_type)
    
    # Apply search if provided
    search = request.query_params.get('search')
    if search:
        queryset = queryset.filter(
            Insurance.Q(policy_number__icontains=search) |
            Insurance.Q(customer_name__icontains=search) |
            Insurance.Q(customer_email__icontains=search)
        )
    
    # Apply ordering if provided
    ordering = request.query_params.get('ordering', '-created_at')
    queryset = queryset.order_by(ordering)
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    
    serializer = InsurancePolicySerializer(queryset[start:end], many=True)
    
    return Response({
        'count': queryset.count(),
        'page': page,
        'page_size': page_size,
        'results': serializer.data
    })

# ------------------------------------------------------------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_policy_owner(request):
    """
    Create a Policy Owner record for a user (even if they don't have login access).
    Only admins, super admins, or staff can perform this action.
    """
    serializer = PolicyOwnerSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        contact_number = serializer.validated_data.get("contact_number")
        marital_status = serializer.validated_data.get("marital_status")
        gender = serializer.validated_data.get("gender")
        address = serializer.validated_data.get("address")
        alternative_phone = serializer.validated_data.get("alternative_phone")
        nominee_name = serializer.validated_data.get("nominee_name")
        date_of_birth = serializer.validated_data.get("date_of_birth")

        # Ensure required fields are provided
        if not username or not email or not contact_number:
            return Response(
                {"status": 400, "title": "Missing Data", "message": "Username, email, and contact number are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a PolicyOwner record already exists for this email
        if PolicyOwner.objects.filter(email=email).exists():
            return Response(
                {
                    "status": 400,
                    "title": "Already Exists",
                    "message": "Policy owner record already exists for this email."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create PolicyOwner record
        policy_owner = PolicyOwner.objects.create(
            username=username,
            email=email,
            contact_number=contact_number,
            marital_status=marital_status,
            gender=gender,
            address=address,
            alternative_phone=alternative_phone,
            nominee_name=nominee_name,
            date_of_birth=date_of_birth,
        )

        response_data = {
            "status": 200,
            "title": "Successfully Created",
            "message": "Policy owner created successfully.",
            "data": serializer.data,
            "redirect": "true",
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    else:
        response_data = {
            "status": 400,
            "title": "Validation Error",
            "message": "Form validation error.",
            "error": serializer.errors,
            "stable": "true",
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# list policy owners
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_policy_owners(request):
    policy_owners = PolicyOwner.objects.all()
    serializer = PolicyOwnerSerializer(policy_owners, many=True)
    return Response(serializer.data)

# update policy owner
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_policy_owner(request, id):
    try:
        policy_owner = PolicyOwner.objects.get(id=id)
    except PolicyOwner.DoesNotExist:
        return Response({"message": "Policy owner not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PolicyOwnerSerializer(policy_owner, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete policy owner
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_policy_owner(request, id):
    try:
        policy_owner = PolicyOwner.objects.get(id=id)
    except PolicyOwner.DoesNotExist:
        return Response({"message": "Policy owner not found"}, status=status.HTTP_404_NOT_FOUND)

    policy_owner.delete()
    return Response({"message": "Policy owner deleted successfully"}, status=status.HTTP_204_NO_CONTENT)