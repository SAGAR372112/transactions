from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, CompanyUsersView

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth-api/', include('rest_framework.urls', namespace='rest_framework')),
    path('companies/<int:pk>/users/', CompanyUsersView.as_view({'get': 'list', 'post':'create'}), name='company-users'),
]
