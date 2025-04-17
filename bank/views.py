from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, render, redirect
from .models import Company, BalanceHistory, User
from .serializers import (
     CompanySerializer, BalanceHistorySerializer, UserSerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['put', 'patch'])
    def update_company(self, request, pk=None):
        partial = request.method == 'PATCH'
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def balance_history(self, request, pk=None):
        company = self.get_object()
        history = BalanceHistory.objects.filter(company=company).order_by('-timestamp')
        serializer = BalanceHistorySerializer(history, many=True)
        return Response({
            'company_name': company.name,
            'current_balance': company.total_balance,
            'history': serializer.data
        })

class CompanyUsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        company_id = self.kwargs['pk']
        return User.objects.filter(company_id=company_id)
    
    def perform_create(self, serializer):
        company_id = self.kwargs['pk']
        company = get_object_or_404(Company, pk=company_id)
        serializer.save(company=company)