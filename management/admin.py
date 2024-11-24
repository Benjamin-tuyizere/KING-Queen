from django.contrib import admin
from .models import Property, Tenant, LeaseAgreement, Role, UserRole, MaintenanceRequest, Payment


# ------------------- ROLE & USER ROLE -------------------
admin.site.register(Role)
admin.site.register(UserRole)


# ------------------- PROPERTY ADMIN -------------------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'units', 'property_type', 'created_at', 'updated_at')
    search_fields = ('name', 'address', 'property_type')
    list_filter = ('property_type',)
    ordering = ('name',)


# ------------------- TENANT ADMIN -------------------
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'phone', 'emergency_contact', 'created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'phone', 'emergency_contact')
    ordering = ('user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    get_full_name.short_description = 'Tenant Name'


# ------------------- LEASE AGREEMENT ADMIN -------------------
@admin.register(LeaseAgreement)
class LeaseAgreementAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant_name', 'unit_number', 'start_date', 'end_date', 'status', 'created_at', 'updated_at')
    search_fields = ('property__name', 'tenant__user__first_name', 'tenant__user__last_name', 'unit_number')
    list_filter = ('status', 'property')
    ordering = ('property__name', 'unit_number')

    def tenant_name(self, obj):
        return f"{obj.tenant.user.first_name} {obj.tenant.user.last_name}"

    tenant_name.short_description = 'Tenant Name'


# ------------------- MAINTENANCE REQUEST ADMIN -------------------
@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'requested_by', 'status', 'created_at', 'updated_at')
    search_fields = ('property__name', 'requested_by__username', 'description')
    list_filter = ('status', 'property')
    ordering = ('created_at',)


# ------------------- PAYMENT ADMIN -------------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'amount', 'payment_type', 'status', 'payment_date')
    search_fields = ('property__name', 'tenant__username', 'payment_type', 'status')
    list_filter = ('status', 'payment_type', 'property')
    ordering = ('payment_date',)



