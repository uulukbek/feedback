from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from applications.account.tasks import send_confirmation_email, send_confirmation_code

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = [
            "last_login", "is_superuser", "date_joined",
            "first_name", "last_name", "is_staff",
            "activation_code", "confirm_code",
            "groups", "user_permissions",
        ]
        

class ChangeProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = [
            "last_login", "is_superuser", "date_joined",
            "first_name", "last_name", "is_staff",
            "activation_code", "confirm_code",
            "groups", "user_permissions", "is_active",
            "password"
        ]


class RegisterSerializer(serializers.ModelSerializer):
    contact = serializers.CharField(min_length=13)
    password = serializers.CharField(min_length=6)
    password_confirm = serializers.CharField(
        min_length=6,
        write_only=True,
        required=True,
    )
    
    
    class Meta:
        model = User
        fields = [
            "username", "email", 
            "password", "password_confirm", 
            "contact",
        ]
        
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        contact = attrs.get('contact')
        

        if password != password_confirm:
            raise serializers.ValidationError('Password dont match!')

        if not contact.startswith('+996'):
            raise serializers.ValidationError('Invalid contact, contact must start with +996!')
        
        if not contact[1:].isdigit():
            raise serializers.ValidationError('Invalid contact, phone number must not contain letters!')
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email.delay(user.email, code)
        return user
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        min_length=6
    )
    new_password_confirm = serializers.CharField(
        required=True,
        min_length=6
    )

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Password dont match!')
        return attrs

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Wrong password!')
        return old_password

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.password = make_password(password)
        user.save()
        
    
class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    
    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username doesn't exist")
        return username
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email doesn't exist.")
        return email
    
    def send_code(self):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        user.create_confirm_code()
        user.save()
        send_confirmation_code.delay(email, user.confirm_code)
        
        
class ForgotPasswordConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)
    
    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username doesn't exist.")
        return username
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email doesn't exist.")
        return email
    
    @staticmethod
    def validate_code(code):
        if not User.objects.filter(confirm_code=code).exists():
            raise serializers.ValidationError("Wrong code!")
        return code
    
    def validate(self, attrs):
        password = attrs.get("new_password")
        password_confirm = attrs.get("new_password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Password dont match!")
        return attrs
    
    def set_new_password(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")
        user = User.objects.get(email=email)
        user.password = make_password(password)
        user.confirm_code = ""
        user.save()
        