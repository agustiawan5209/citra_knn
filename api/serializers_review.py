from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        # Pastikan akun aktif
        user = self.user
        if not user.is_active:
            raise serializers.ValidationError("Akun tidak aktif. Hubungi admin.")

        # Tambahkan informasi tambahan dalam token
        data.update({'username': user.username, 'email': user.email})
        return data
    
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token