from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import (
    CeoSerializer,
    EmployeeSerializer,
    UserLoginSerializer,
    UserSerializer,
)

User = get_user_model()


class TokenView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(email=email, password=password)

            if user:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    user_details = {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_superuser": user.is_superuser,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "is_verified": user.is_verified,
                        "is_client": user.is_client,
                        "is_employee": user.is_employee,
                        "is_ceo": user.is_ceo,
                        "is_manager": user.is_manager,
                        "is_personal": user.is_personal,
                        "token": token.key,
                    }
                    return Response(user_details, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"detail": ("User account is disabled.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": ("Unable to log in with provided credentials.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )


"""
Different user registration views
"""


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CeoRegistrationView(APIView):
    serializer_class = CeoSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeCreateView(APIView):
    serializer_class = EmployeeSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "id"

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)
