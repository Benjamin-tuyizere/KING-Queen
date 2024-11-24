from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Property, Tenant, LeaseAgreement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TenantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    active_leases = serializers.SerializerMethodField()

    class Meta:
        model = Tenant
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_active_leases(self, obj):
        active_leases = LeaseAgreement.objects.filter(tenant=obj, status='ACTIVE')
        return LeaseAgreementSerializer(active_leases, many=True).data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        tenant = Tenant.objects.create(user=user, **validated_data)
        return tenant

class LeaseAgreementSerializer(serializers.ModelSerializer):
    property_details = PropertySerializer(source='property', read_only=True)
    tenant_details = TenantSerializer(source='tenant', read_only=True)

    class Meta:
        model = LeaseAgreement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data