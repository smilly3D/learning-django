from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Accounts
from accounts.serializers import AccountsSerializer


class AccountsView(APIView):
    def post(self, request):
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

        serializer = AccountsSerializer(user)

        return Response(serializer.data, status.HTTP_201_CREATED)
