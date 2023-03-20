"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.account.views import VkAuthView


schema_view = get_schema_view(
    
    openapi.Info(
        title='Python 25 Hack',
        default_version='v1',
        description='Hack',
    ),
    public = True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger')),
    path('api/account/',include('applications.account.urls')),
    path('api/post/',include('applications.post.urls')),
    path('api/feedback/',include('applications.feedback.urls')),

    path('api/v1/auth/vk/', include('social_django.urls', namespace='social')),
    path('auth/token/', TokenObtainPairView.as_view, name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view, name='token_refresh'),

    path('api/v1/auth/vk/token/', VkAuthView.as_view()),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
