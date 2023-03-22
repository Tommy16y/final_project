from django.db import models
from django.contrib.auth import get_user_model
from applications.post.models import Post

User = get_user_model()

class Like(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} liked - {self.post.title}'

class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments',null=True,blank=True)
    body = models.TextField(null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    




class Favorite(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )



    def __str__(self):
        return f'{self.owner} favorite -{self.post}'