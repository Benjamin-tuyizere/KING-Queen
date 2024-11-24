from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from management import views
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),

    # Property URLs
    path(
        'properties/',
        views.PropertyListView.as_view(),
        name='property_list'
    ),
    path(
        'properties/<int:pk>/',
        views.PropertyDetailView.as_view(),
        name='property_detail'
    ),
    path(
        'properties/create/',
        views.property_create,
        name='property_create'
    ),

    # Tenant URLs
    path(
        'tenants/',
        views.TenantListView.as_view(),
        name='tenant_list'
    ),
    path(
        'tenants/create/',
        views.tenant_create,
        name='tenant_create'
    ),

    # Lease URLs
    path(
        'leases/',
        views.LeaseAgreementListView.as_view(),
        name='lease_list'
    ),
    path(
        'leases/create/',
        views.lease_create,
        name='lease_create'
    ),

    # Authentication URLs
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='login'),
        name='logout'
    ),

]
