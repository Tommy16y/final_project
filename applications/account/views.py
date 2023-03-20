from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from applications.account.serializers import RegisterSerializer, ForgotPasswordSerializer,ForgotPasswordCompleteSerializer,ChangePasswordSerializer,UsersSerializer,UserrSerializer,ProfileSerializer,SubSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model  
from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter ,SearchFilter
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from applications.feedback.models import Following
from applications.account.models import Profile
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view




User = get_user_model()
class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        

        return Response('Вы успешно зарегистрировались. Вам отправлено письмо с активацией', status=201)
    

class LogoutAPIView(APIView):
    permission_classes =[IsAuthenticated]
    def post(self,request):
        try:
            user = request.user
            Token.objects.get(user=user).delete()
            return Response('Вы успешно разлогинились',status=200)
        except:
            return Response(status=403)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Успешно', status=200)
        except User.DoesNotExist:
            return Response('Link expired', status=400)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_password_code()
        return Response('вам отправлено письмо для восстановления пароля')


class ForgotPasswordCompleteAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно изменен')



class ChangePasswordView(generics.UpdateAPIView):
  
    model = User
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            
            old_password = serializer.data.get("old_password")
            if check_password(old_password, self.object.password):
               
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
            
                return Response('Пароль успешно изменен', status=status.HTTP_200_OK)

            else:
                
                return Response('Старый пароль неверный!', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UsersSerializer
    queryset = User.objects.filter(is_superuser=False)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['login']


    

class DetailUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UserrSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)





class VkAuthSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token

class VkAuthView(TokenObtainPairView):
    serializer_class = VkAuthSerializer



class ProfileUpdateAPIView(generics.GenericAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_field = ['profile_id','login',]
    search_fields = ['login',] 

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        profile_instance = self.get_object()
        profile_serializer = self.get_serializer(
            profile_instance, data=request.data, partial=True
        )
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscribeView(APIView):
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, profile_id=profile_id)
        user_profile = request.user.profile
        if not user_profile.followw.filter(profile_id=profile_id).exists():
            user_profile.followw.add(profile)
            user_profile.following += 1
            user_profile.save()
            profile.followers += 1
            profile.save()
            return Response({'success': 'Вы подписались на аккаунт.'})
        else:
            return Response({'error': 'Вы уже подписаны.'})


class UnsubscribeView(APIView):
    def post(self, request, profile_id):
        profile = get_object_or_404(Profile, profile_id=profile_id)
        user_profile = request.user.profile
        if user_profile.followw.filter(profile_id=profile_id).exists():
            user_profile.followw.remove(profile)
            user_profile.following -= 1
            user_profile.save()
            profile.followers -= 1
            profile.save()
            return Response({'success': 'Вы отписались от аккаунта.'})
        else:
            return Response({'error': 'Вы не подписаны.'})