from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth import get_user_model


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,login, **extra_fields):
        email = self.normalize_email(email)
        
        user = self.model(email=email,login=login, **extra_fields)
        user.password = make_password(password)  # '1' -> sdjfhue8rb3457fgidysuif
        # user.password = password
        user.create_activation_code()
        user.save(using=self._db)
        Profile.objects.create(owner = user,profile_id = user.id)
        if user.login == None:
            user.is_active=True
            a='1234567'
            b=user.email
            user.password=make_password(a+b)    
        return user

    def create_user(self, email, password='1',login=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password,login, **extra_fields)

    def create_superuser(self, email, password,login,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password,login,**extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    login = models.CharField(max_length=20,unique=True,blank=True,null=True)
    username=None
    activation_code = models.CharField(max_length=50, blank=True)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)

    
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    def __str__(self):
        return f'{self.email}'

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

User = get_user_model()


class Profile(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_id = models.IntegerField(unique=True)
    first_name = models.CharField(null=True,blank=True,max_length=20)
    last_name = models.CharField(null=True,blank=True,max_length=20)
    followw = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followed_by')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    avatar=models.ImageField(upload_to='accounts/',blank=True,null=True)
    about_me = models.CharField(max_length=200,blank=True,null=True)
    date_of_birth = models.DateField(default=None,null=True,blank=True)



    def __str__(self):
        return f'profile -{self.owner}'




