from rest_framework import serializers

from reviews.models import User  # noqa


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']
        extra_kwargs = {'email': {'required': True}}

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Invalid username.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with that email already exists.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField()

    class Meta:
        fields = ['username', 'confirmation_code']
