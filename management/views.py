from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property, Tenant, LeaseAgreement
from .forms import PropertyForm, TenantForm, LeaseAgreementForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


# Property Views
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


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save()
            messages.success(request, 'Property created successfully!')
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'property_management/property_form.html', 
                  {'form': form})


# Tenant Views
class TenantListView(LoginRequiredMixin, ListView):
    model = Tenant
    template_name = 'property_management/tenant_list.html'
    context_object_name = 'tenants'
    paginate_by = 10


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
    return render(request, 'property_management/tenant_form.html', 
                  {'form': form})


# Lease Agreement Views
class LeaseAgreementListView(LoginRequiredMixin, ListView):
    model = LeaseAgreement
    template_name = 'property_management/lease_list.html'
    context_object_name = 'leases'
    paginate_by = 10


@login_required
def lease_create(request):
    if request.method == 'POST':
        form = LeaseAgreementForm(request.POST)
        if form.is_valid():
            lease = form.save()
            messages.success(request, 'Lease agreement created successfully!')
            return redirect('lease_detail', pk=lease.pk)
    else:
        form = LeaseAgreementForm()
    return render(request, 'property_management/lease_form.html', 
                  {'form': form})
