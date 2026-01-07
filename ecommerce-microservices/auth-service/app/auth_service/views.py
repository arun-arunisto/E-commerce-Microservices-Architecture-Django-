from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class HealthCheck(APIView):
    authentication_classes = []

    def get(self, request):
        print("auth-service-up")
        return Response({"status": "auth-service-up"}, status=status.HTTP_200_OK)

class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)

