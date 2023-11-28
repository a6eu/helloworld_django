from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import UserProfile
from .serializers import UserProfileSerializer, UserDetailSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated


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


class RegisterUserView(generics.GenericAPIView, mixins.CreateModelMixin):
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        if UserProfile.objects.filter(email=request.data.get('email')).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
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


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

