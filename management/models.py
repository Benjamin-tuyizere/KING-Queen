from django.db import models
from django.contrib.auth.models import User


# ------------------- ROLE MANAGEMENT -------------------
class Role(models.Model):
    ADMIN = 'admin'
    PROPERTY_MANAGER = 'property_manager'
    TENANT = 'tenant'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PROPERTY_MANAGER, 'Property Manager'),
        (TENANT, 'Tenant'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


# ------------------- PROPERTY MANAGEMENT -------------------
class Property(models.Model):
    RESIDENTIAL = 'Residential'
    COMMERCIAL = 'Commercial'
    INDUSTRIAL = 'Industrial'
    APARTMENT = 'Apartment'
    HOUSE = 'House'

    PROPERTY_TYPE_CHOICES = [
        (RESIDENTIAL, 'Residential'),
        (COMMERCIAL, 'Commercial'),
        (INDUSTRIAL, 'Industrial'),
        (APARTMENT, 'Apartment'),
        (HOUSE, 'House'),
    ]

    name = models.CharField(max_length=200)
    address = models.TextField()
    description = models.TextField(blank=True)
    units = models.IntegerField()
    square_footage = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Properties"


# ------------------- TENANT MANAGEMENT -------------------
class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ------------------- LEASE AGREEMENT -------------------
class LeaseAgreement(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_PENDING = 'pending'
    STATUS_EXPIRED = 'expired'
    STATUS_TERMINATED = 'terminated'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PENDING, 'Pending'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_TERMINATED, 'Terminated'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease for {self.property.name} - Unit {self.unit_number}"


# ------------------- MAINTENANCE REQUESTS -------------------
class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    description = models.TextField()
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Maintenance Request for {self.property} by {self.requested_by.username}"


# ------------------- PAYMENT MANAGEMENT -------------------
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)  # e.g., 'rent', 'deposit', 'maintenance'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of ${self.amount} by {self.tenant.user.username} for {self.property.name}"
