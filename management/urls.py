from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PropertyViewSet, TenantViewSet, LeaseAgreementViewSet  # This import should be fine now
from django.contrib import admin
from property_management import views 
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'leases', LeaseAgreementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('management/', include('management.urls')),  
 path('login/', auth_views.LoginView.as_view(), name='login'),
     path('property/create/', views.property_create, name='property_create'),
    path('tenant/create/', views.tenant_create, name='tenant_create'),
    path('maintenance/requests/', views.maintenance_request_list, name='maintenance_request_list'),
    path('payments/', views.payment_list, name='payment_list'),
]


