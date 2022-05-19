from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from accounts.models import Accounts
from accounts.serializers import AccountsSerializer, LoginSerializer
from rest_framework.authtoken.models import Token

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate


class AccountsView(APIView):
    def post(self, request: Request):
        # request.data = body da request
        serializer = AccountsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_user = Accounts.objects.filter(
            email=serializer.validated_data["email"]
        ).exists()

        if found_user:
            return Response(
                {"message": "User already exists"}, status.HTTP_409_CONFLICT
            )

        user = Accounts.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data["password"])
        user.save()

        serializer = AccountsSerializer(user)

        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # user: Accounts = Accounts.objects.filter(
        #     email=serializer.validated_data["email"]
        # ).first()

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"message": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED
            )

        # if not check_password(serializer.validated_data["password"], user.password):
        #     return Response(
        #         {"message": "Invalid credentials"}, status.HTTP_401_UNAUTHORIZED
        #     )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
