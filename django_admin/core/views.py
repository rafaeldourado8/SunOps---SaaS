from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'detail': 'Dados inválidos'}, status=status.HTTP_400_BAD_REQUEST)
    
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']
    
    try:
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
    except User.DoesNotExist:
        user = None
    
    if user is None:
        return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'token_type': 'bearer'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
