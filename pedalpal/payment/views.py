from rest_framework import generics, permissions
from django.http.response import JsonResponse
from .models import Payment


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

        if request.data.get("amount") < 0:
            payment = Payment(
                user=user, amount=request.data.get("amount"), status="DEBIT"
            )
        else:
            payment = Payment(
                user=user, amount=request.data.get("amount"), status="CREDIT"
            )
        payment.save()

        return JsonResponse({"balance": user.balance})
