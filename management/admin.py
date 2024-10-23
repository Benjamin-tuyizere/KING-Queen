from django.contrib import admin
from .models import Property, Tenant, LeaseAgreement


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'units',
        'property_type',
    )
    search_fields = ('name', 'address')
    list_filter = ('property_type',)


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'phone',
        'emergency_contact',
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'phone',
    )

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_full_name.short_description = 'Tenant Name'


@admin.register(LeaseAgreement)
class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = (
        'property',
        'tenant',
        'unit_number',
        'start_date',
        'end_date',
        'status',
    )
    search_fields = (
        'property__name',
        'tenant__user__first_name',
        'tenant__user__last_name',
        'unit_number',
    )
    list_filter = ('status', 'property')


