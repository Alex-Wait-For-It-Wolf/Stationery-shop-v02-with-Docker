from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Order
from .serializers import OrderSerializer


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(payer=user)
