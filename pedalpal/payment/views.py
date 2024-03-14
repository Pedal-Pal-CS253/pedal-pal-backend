from rest_framework import generics, permissions
from django.http.response import JsonResponse
from .models import Payment
from .serializers import PaymentSerializer


class AddPaymentAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        payment = Payment(user=user, amount=request.data.get("amount"))
        payment.save()
        return JsonResponse({"id": payment.id})


class GetBalanceAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        return JsonResponse({"balance": user.balance})


class UpdateBalanceAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
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


class GetTransactionsAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        transactions = Payment.objects.filter(user=user)
        serializer = self.serializer_class(transactions, many=True)

        return JsonResponse(serializer.data, safe=False)
