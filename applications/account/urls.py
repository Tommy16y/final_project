from django.urls import path
from applications.account.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationView.as_view()),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset_password/', ForgotPasswordAPIView.as_view()),
    path('reset_password_complete/', ForgotPasswordCompleteAPIView.as_view()),

    path('changepassword/', ChangePasswordView.as_view()),

    path('users/',ProfileView.as_view()),

    path('detail/<int:id>/',DetailUserView.as_view()),

    path('logout/',LogoutAPIView.as_view()),
    
    # path('follow',AccountModelViewSet.as_view()),


    path('customization/',ProfileUpdateAPIView.as_view()),
    
    # path('subscribe/<int:pk>/', subscribe),
    # path('unsubscribe/<int:pk>/', unsubscribe),
    path('profiles/<int:profile_id>/sub/',SubscribeView.as_view()),
    path('profiles/<int:profile_id>/unsub/',UnsubscribeView.as_view()),
    


]