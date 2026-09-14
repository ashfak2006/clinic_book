from rest_framework import serializers
from .models import user, City, DoctorProfile, ReceptionistProfile, PatientProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'email', 'phone_number', 'user_role', 'password', 'is_active', 'is_phone_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.username = validated_data.get('email').split('@')[0]
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
class get_otp_serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class username_login_serializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()