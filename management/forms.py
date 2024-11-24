from django import forms
from django.contrib.auth.models import User
from .models import Property, Tenant, LeaseAgreement, MaintenanceRequest


# ------------------- PROPERTY FORM -------------------
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'units', 'square_footage', 'property_type']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


# ------------------- TENANT FORM -------------------
class TenantForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Tenant
        fields = ['phone', 'emergency_contact', 'emergency_contact_phone']

    def save(self, commit=True):
        # Create a new user for the tenant
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Save the tenant instance and link it to the created user
        tenant = super().save(commit=False)
        tenant.user = user
        if commit:
            tenant.save()
        return tenant


# ------------------- LEASE AGREEMENT FORM -------------------
class LeaseAgreementForm(forms.ModelForm):
    class Meta:
        model = LeaseAgreement
        fields = [
            'property', 'tenant', 'unit_number', 'start_date', 'end_date',
            'monthly_rent', 'security_deposit', 'status'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pass the user if required for filtering
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'tenant_profile'):
            # Filter properties based on active lease agreements of the tenant
            self.fields['property'].queryset = Property.objects.filter(
                lease_agreements__tenant=user.tenant_profile,
                lease_agreements__status='active'
            )


# ------------------- MAINTENANCE REQUEST FORM -------------------
class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['property', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'property': forms.Select(attrs={'class': 'form-control'}),
        }

