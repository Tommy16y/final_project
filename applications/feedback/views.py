from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework import viewsets
from applications.feedback.models import Comment,Like
from applications.feedback.serializers import CommentSerializer,LikeSerializer ,FavoriteSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import mixins
from rest_framework.response import Response
from applications.feedback.models import Favorite
from django.shortcuts import get_object_or_404
from applications.post.models import Post


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer      
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  


# class LikeModelViewSet(viewsets.ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer    
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user) 






class FavoriteViewSet(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin,   
               GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        
        return serializer.save(owner = self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner = self.request.user)
        print(queryset)
        return queryset
    

    # def post(self, request,id):
    #     post = get_object_or_404(Post, id=id)
        