from django.urls import path,include
from applications.feedback.views import *
from rest_framework.routers import DefaultRouter
from rest_framework import routers

# class FavoriteRouter(routers.DefaultRouter):
#     lookup_url_kwarg = 'post'


router = DefaultRouter()
# router.register('likes',LikeModelViewSet)
router.register('favorites', FavoriteViewSet)

router.register('comments',CommentModelViewSet)

urlpatterns = [
    # path('favorite',FavoriteViewSet.as_view()),
    path('',include(router.urls)),
]
