from .models import Users
from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now, timedelta

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if validate_password(validated_data["password"]) == None:
            password = make_password(validated_data["password"])
            user = Users.objects.create(
                email=validated_data["email"], password=password
            )
            return user




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        # fields = ["id", "email", "is_staff", "is_superuser"]
        # fields = ["id", "email"]
        fields = "__all__"


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



# reset password by otp
class RequestOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not registered.")
        return value
    

class VerifyOTPAndChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')
        user = Users.objects.filter(email=email).first()
        if not user or user.otp_code != otp_code or user.otp_expiry < now():
            raise serializers.ValidationError("Invalid or expired OTP.")
        return attrs

    def save(self):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        user = Users.objects.get(email=email)
        user.set_password(new_password)
        user.otp_code = None  # Clear OTP after successful reset
        user.otp_expiry = None
        user.save()
        return user