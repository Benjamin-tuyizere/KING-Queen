from django import forms
from .models import Property, Tenant, LeaseAgreement
from django.contrib.auth.models import User


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
          'name', 'address', 'units', 'square_footage', 'property_type'
          ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class TenantForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Tenant
        fields = ['phone', 'emergency_contact', 'emergency_contact_phone']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        tenant = super().save(commit=False)
        tenant.user = user
        if commit:
            tenant.save()
        return tenant


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
