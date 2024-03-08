from rest_framework import generics, permissions
from django.http.response import JsonResponse


class GetBalanceAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        return JsonResponse({"balance": user.balance})


class UpdateBalanceAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user.balance += int(request.data.get("amount"))
        user.save()
        return JsonResponse({"balance": user.balance})
