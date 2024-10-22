from rest_framework import serializers
from expenses.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            email=validated_data['email'],  
            password=validated_data['password'],
            name=validated_data['name'],  
            mobile=validated_data['mobile']
        )
        return user
