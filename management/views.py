from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from datetime import datetime, timedelta


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Property, Tenant, LeaseAgreement, MaintenanceRequest, Payment
)
from .forms import PropertyForm, TenantForm, LeaseAgreementForm
from .serializers import (
    PropertySerializer, TenantSerializer, LeaseAgreementSerializer
)
from .permissions import role_required


# ------------------- REST FRAMEWORK VIEWSETS -------------------

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available_units(self, request):
        """List properties with available units."""
        properties = self.get_queryset().filter(
            Q(leaseagreement__isnull=True) | ~Q(leaseagreement__status='ACTIVE')
        ).distinct()
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Filter properties by type."""
        property_type = request.query_params.get('type', '')
        properties = self.get_queryset().filter(property_type=property_type)
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def lease_history(self, request, pk=None):
        """Get tenant's lease history."""
        tenant = self.get_object()
        leases = LeaseAgreement.objects.filter(tenant=tenant)
        serializer = LeaseAgreementSerializer(leases, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def active_leases(self, request, pk=None):
        """Get tenant's active leases."""
        tenant = self.get_object()
        leases = LeaseAgreement.objects.filter(tenant=tenant, status='ACTIVE')
        serializer = LeaseAgreementSerializer(leases, many=True)
        return Response(serializer.data)


class LeaseAgreementViewSet(viewsets.ModelViewSet):
    queryset = LeaseAgreement.objects.all()
    serializer_class = LeaseAgreementSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Terminate a lease agreement."""
        lease = self.get_object()
        lease.status = 'TERMINATED'
        lease.end_date = datetime.now().date()
        lease.save()
        serializer = self.get_serializer(lease)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get lease agreements expiring within 30 days."""
        leases = self.get_queryset().filter(
            status='ACTIVE',
            end_date__lte=(datetime.now().date() + timedelta(days=30))
        )
        serializer = self.get_serializer(leases, many=True)
        return Response(serializer.data)


# ------------------- CLASS-BASED VIEWS -------------------

class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'property_management/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'property_management/property_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leases'] = LeaseAgreement.objects.filter(property=self.object)
        return context


class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'property_management/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10


class LeaseAgreementListView(LoginRequiredMixin, ListView):
    model = LeaseAgreement
    template_name = 'property_management/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 10


# ------------------- FUNCTION-BASED VIEWS -------------------

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save()
            messages.success(request, 'Property created successfully!')
            return redirect('property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
    return render(request, 'property_management/property_form.html', {'form': form})


@login_required
def tenant_create(request):
    if request.method == 'POST':
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save()
            messages.success(request, 'Tenant created successfully!')
            return redirect('tenant_detail', pk=tenant.pk)
    else:
        form = TenantForm()
    return render(request, 'property_management/tenant_form.html', {'form': form})


@login_required
@role_required(['tenant', 'property_manager', 'admin'])
def maintenance_request_list(request):
    if hasattr(request.user, 'userrole') and request.user.userrole.role.name == 'tenant':
        maintenance_requests = MaintenanceRequest.objects.filter(requested_by=request.user)
    else:
        maintenance_requests = MaintenanceRequest.objects.all()
    return render(request, 'management/maintenance_list.html', {
        'maintenance_requests': maintenance_requests
    })


@login_required
@role_required(['tenant', 'admin'])
def create_maintenance_request(request):
    if request.method == 'POST':
        # Handle form submission logic here
        pass
    return render(request, 'management/maintenance_form.html')


@login_required
@role_required(['tenant', 'property_manager', 'admin'])
def payment_list(request):
    if hasattr(request.user, 'userrole') and request.user.userrole.role.name == 'tenant':
        payments = Payment.objects.filter(tenant=request.user)
    else:
        payments = Payment.objects.all()
    return render(request, 'management/payment_list.html', {'payments': payments})


@login_required
def lease_create(request):
    if request.method == 'POST':
        form = LeaseAgreementForm(request.POST)
        if form.is_valid():
            lease = form.save()
            messages.success(request, 'Lease agreement created successfully!')
            return redirect('lease_detail', pk=lease.pk)  # Adjust 'lease_detail' as per your URL configuration
    else:
        form = LeaseAgreementForm()
    return render(request, 'property_management/lease_form.html', {'form': form})

@login_required
def some_view(request):
    return render(request, 'some_template.html')