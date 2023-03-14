from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from applications.account.serializers import RegisterSerializer, ForgotPasswordSerializer,ForgotPasswordCompleteSerializer,ChangePasswordSerializer,UserProfileSerializer,UsersSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model  
from django.contrib.auth.hashers import check_password
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter ,SearchFilter

User = get_user_model()
class RegisterAPIView(APIView):
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Вы успешно зарегистрировались. Вам отправлено письмо с активацией', status=201)


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
            # проверяем старый пароль
            old_password = serializer.data.get("old_password")
            if check_password(old_password, self.object.password):
                # сохраняем новый пароль
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                # response = {
                #     'status': 'success',
                #     'message': 'Пароль успешно изменен'
                # }
                return Response('Пароль успешно изменен', status=status.HTTP_200_OK)

            else:
                # response = {
                #     'status': 'failed',
                #     'message': 'Старый пароль неверный'
                # }   
                return Response('Старый пароль неверный!', status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserUpdateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileSerializer(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = UsersSerializer
    queryset = User.objects.filter(is_superuser=False)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['login']
    # ordering_fields = ['login']
    # def get_queryset(self):
    #     queryset = User.objects.get(user=self.request.user)


# class DetailUserSerializer(generics.RetrieveAPIView):
#     pass