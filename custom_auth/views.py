from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import UserProfile
from .serializers import UserProfileSerializer, UserDetailSerializer, EmailPhoneLoginSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .authentication import EmailPhoneUsernameAuthenticationBackend as EoP
from rest_framework_simplejwt.tokens import RefreshToken


# class RegisterUserView(APIView):
#     parser_classes = [JSONParser, MultiPartParser, FormParser]
#
#     def post(self, request):
#         if UserProfile.objects.filter(email=request.data['email']).exists():
#             return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             serializer = UserProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = EmailPhoneLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_or_phone = serializer.validated_data['email_or_phone']
        password = serializer.validated_data['password']
        user = EoP.authenticate(request, username=email_or_phone, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'refresh': str(refresh),
                'access': access_token
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        if UserProfile.objects.filter(email=request.data.get('email')).exists():
            return Response(
                {'error': 'Указанный адрес электронной почты уже зарегистрирован!'},
                     status=status.HTTP_400_BAD_REQUEST)
        elif UserProfile.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({'error': 'Этот номер телефона уже зарегестрирован!'},
                     status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        return {'Location': str(data['id'])}


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()


# class UserProfileAPIView(generics.RetrieveAPIView):
#     serializer_class = UserDetailSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         return self.request.user



