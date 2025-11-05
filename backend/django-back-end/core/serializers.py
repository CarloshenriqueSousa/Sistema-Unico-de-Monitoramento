from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(max_length=20, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        identifier = attrs.get('identifier')
        password = attrs.get('password')

        if identifier and password:
            # Para o modelo User customizado, usamos identifier como username
            user = authenticate(
                request=self.context.get('request'),
                username=identifier,
                password=password
            )

            if not user:
                raise serializers.ValidationError('Não foi possível fazer o login com as credenciais fornecidas.', code='authorization')
            
            if not user.is_active:
                raise serializers.ValidationError('Usuário desativado.', code='authorization')
            
            attrs['user'] = user
            return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'identifier',
            'email',
            'nome',
            'user_type',
            'metadata'
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser']