import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from insurance.models import Insurance
from .serializers import InsurancePolicySerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status


# create insurance
@api_view(['POST'])
@permission_classes([AllowAny])
def create_insurance(request):
    serializer = InsurancePolicySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)      

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


