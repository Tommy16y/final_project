from applications.post.models import Post,PostMedia,Repost
from applications.post.serializers import PostSerializer,PostMediaSerializer,RepostSerializer,MyPostSerializer
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from applications.feedback.models import Like
from rest_framework.decorators import action
from rest_framework import generics, status
from django.contrib.auth import get_user_model  
from applications.account.models import Profile
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

User = get_user_model()


# class CustomPagination(PageNumberPagination):
#     page_size = 100
#     page_size_query_param = 'page_size'
#     max_page_size = 100

@method_decorator(cache_page(120),name='dispatch')
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination    
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(methods=['POST'],detail=True)  # lokalhost:8000/api/v1/post/15/like/
    def like(self,request,pk,*args,**kwargs):
        user = request.user
        # print(user), '!!!!!!!!!'
        like_obj,_ = Like.objects.get_or_create(owner=user,post_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'

        if not like_obj.is_like:
            status = 'unliked'
        

        return Response({'status': status})



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostMediaModelViewSet(viewsets.ModelViewSet):
    queryset = PostMedia.objects.all()
    serializer_class = PostMediaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)        

class RepostModelViewSet(viewsets.ModelViewSet):
    queryset = Repost.objects.all()
    serializer_class = RepostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)         


class MyPostView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyPostSerializer


    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(owner=user)



