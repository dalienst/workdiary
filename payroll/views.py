from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from company.permissions import IsFinanceOrIsCeo
from payroll.models import Payroll
from payroll.serializers import PayrollSerializer


class PayrollListCreateView(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [IsAuthenticated, IsFinanceOrIsCeo]

    def get_queryset(self):
        user = self.request.user
        if user.is_finance:
            return Payroll.objects.filter(employee=user)
        else:
            return Payroll.objects.filter(employee=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer
    permission_classes = [
        IsAuthenticated,
        IsFinanceOrIsCeo,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payroll.objects.all()
        return Payroll.objects.filter(employee=user)
