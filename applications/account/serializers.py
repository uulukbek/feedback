from rest_framework import serializers
from django.contrib.auth import get_user_model

from applications.account.models import Profile
from applications.account.tasks import send_act_code_celery, send_confirmation_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
         
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        code = user.activation_code
        send_act_code_celery.delay(user.email, code)
        user.save()
        return user
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password2 = serializers.CharField(required=True, min_length=8)
    
    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('new_password2')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
        
    def validate_old_password(self, password):
        user = self.context.get('request').user
        if not user.check_password(password):
            raise serializers.ValidationError('Введенный пароль не верный')
        return password
        
    def set_new_password(self):
        user = self.context.get('request').user    
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()
        
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=20)
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с такой почтой не существует')
        return email
    
    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_act_code()
        user.save()
        send_confirmation_code.delay(user.email, user.activation_code)
      
        
class ForgotPasswordFinishSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    password2 = serializers.CharField(required=True, min_length=8)
    
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователя с такой почтой не сушествует')
        return email
    
    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Не правильный код')
        return code
    
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password2')
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
    
    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()    
        
        
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Profile
        fields = '__all__'
        
        
    
    
    