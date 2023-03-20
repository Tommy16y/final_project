from rest_framework import serializers
from django.contrib.auth import get_user_model
from applications.account.send_email import  send_reset_password_code
from applications.account.task import send_activation_code as celery_register
# from applications.feedback.models import Following
from applications.account.models import Profile

import datetime
User = get_user_model()  # CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        required=True,
        min_length=6,
        write_only=True 
    )

    class Meta:
        # model = CustomUser
        model = User
        fields = ('email','login','password', 'password2')
    

    def validate_email(self, email):
        print('Okay')
        return email
    

    
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password2')

        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают!')

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        celery_register.delay(user.email, user.activation_code)
        # send_activation_code(user.email, user.activation_code)
        # Profile.objects.create(owner = user,profile_id = user.id)
        
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists(): # not False = True
            raise serializers.ValidationError('Пользователь с такой почтой не существует!')

        return email

    def send_reset_password_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_reset_password_code(email=email, code=user.activation_code)
        


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)
    code = serializers.CharField(required=True)

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('пароли не совпадают')
        return attrs

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Неверный код!')
        return code
    
    def set_new_password(self):
        user = User.objects.get(activation_code=self.validated_data.get('code'))
        password = self.validated_data.get('password')
        user.password = password # john123 -> fjdshfksffkjnefjhfjk
        user.set_password(password)
        user.activation_code = ''
        user.save(update_fields=['password', 'activation_code'])




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Пароль должен быть от 6 и выше символов ")

        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверный")

        return value

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login',)


class UserrSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('login','created_at',)

   



class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False)
    about_me = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)

    class Meta:
        model = Profile
        fields = ('avatar', 'about_me', 'first_name', 'last_name', 'date_of_birth')

    
        
    def validate_date_of_birth(self,date_of_birth):
        self.dayss(date_of_birth)
        
        if date_of_birth ==datetime.date.today():
            raise serializers.ValidationError('Дата рождения не может быть сегодня!')
        
        elif date_of_birth>datetime.date.today():
            raise serializers.ValidationError('Дата рождения не может быть в будущем!')
        
        elif self.dayss(date_of_birth)>36500:
            raise serializers.ValidationError('вам не может быть 100 лет')
        
        return date_of_birth

    def dayss(self,date_of_birth):
        d2 = str(datetime.date.today()).split('-')
        d1 = str(date_of_birth).split('-')
        aa = datetime.date(int(d2[0]),int(d2[1]),int(d2[2]))
        bb = datetime.date(int(d1[0]),int(d1[1]),int(d1[2]))
        cc = aa-bb
        dd = str(cc)
        dd = (dd.split()[0])
        return int(dd)



    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance




# class SubSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['profile_id', 'owner', 'followers', 'following']
#         read_only_fields = ['profile_id','owner'm']



class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'login', 'followers', 'following']
        read_only_fields = ['id', 'login']