from django.urls import path,include
from applications.feedback.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('likes',LikeModelViewSet)
router.register('comments',CommentModelViewSet)

urlpatterns = [
    path('',include(router.urls))
]
