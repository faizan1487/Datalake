from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import AlNafi_User
from .models import IslamicAcademy_User, User, NavbarLink, AlNafi_User,Main_User
from .utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import Group

# from django.contrib.auth.models import User

# For Main Site Al-Nafi User Table:
class AlnafiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlNafi_User
        fields = ('username','first_name','last_name','email','phone','isAffiliate','isMentor','country','created_at',)
    def create(self,validated_data):
      email = validated_data.get("email")
      
      if email:
        try:
          obj = AlNafi_User.objects.get(email=email)
        except AlNafi_User.DoesNotExist:
              obj = None
      else:
          obj = None
      
      # If the object exists, update its fields with the validated data
      if obj:
          for key, value in validated_data.items():
              setattr(obj, key, value)
          obj.save()
      else:
          obj = AlNafi_User.objects.create(**validated_data)
      
      return obj
# For Islamic Academy Users:
class IslamicAcademyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = IslamicAcademy_User
        fields = ('username','first_name','last_name','email','phone','is_paying_customer','created_at',)
        
        
class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main_User
        fields = ("id","username","email", "first_name", "last_name","source","phone","address","country","created_at")
    
class MainUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main_User
        fields = '__all__'
            
        
#For albaseer users        
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'phone', 'department', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)
  
class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']
    
    
class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'name']
    
    
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
      fields = ['password', 'password2']

    def validate(self, attrs):
      password = attrs.get('password')
      password2 = attrs.get('password2')
      user = self.context.get('user')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      user.set_password(password)
      user.save()
      return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
      fields = ['email']

    def validate(self, attrs):
      email = attrs.get('email')
      if User.objects.filter(email=email).exists():
        user = User.objects.get(email = email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        # print('Encoded UID', uid)
        token = PasswordResetTokenGenerator().make_token(user)
        # print('Password Reset Token', token)
        link = 'http://localhost:3000/user/reset/'+uid+'/'+token
        # print('Password Reset Link', link)
        # Send EMail
        body = 'Click Following Link to Reset Your Password '+link
        data = {
          'subject':'Reset Your Password',
          'body':body,
          'to_email':user.email
        }
        Util.send_email(data)
        return attrs
      else:
        raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    
    
class NavbarSerializer(ModelSerializer):
    class Meta:
        model = NavbarLink
        fields = '__all__'
        
        
class GroupsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        
        
class UsersCombinedSerializer(serializers.Serializer):
    data1 = AlnafiUserSerializer(many=True)
    data2 = IslamicAcademyUserSerializer(many=True)