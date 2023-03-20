from django.urls import path,include
from applications.post.views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post_media',PostMediaModelViewSet)
router.register('repost',RepostModelViewSet)
router.register('',PostModelViewSet)


urlpatterns = [
    # path('likeon',like),
    path('',include(router.urls)),
    # path('repost/',RepostAPIView.as_view())
    

]
