from django.db import models
from django.contrib.auth import get_user_model
from applications.account.models import Profile

User = get_user_model()

class Post(models.Model):
    title = models.CharField('Название поста',max_length=50,null=True,blank=True)
    descriptions = models.TextField('Описание поста')
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts',verbose_name='Владелец поста')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Дата создание')
    # repost = models.ManyToManyField(User,related_name='reposts',blank=True)
    # updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.title} '

class PostMedia(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='media')
    media = models.FileField(upload_to='post_media') 



class Repost(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='repostsss')
    repost = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='repostsss')
    created_at = models.DateTimeField(auto_now_add=True)
    # avatar = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='avatar')
    
    # owner2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reposts2',verbose_name='владелец репоста')


    def __str__(self):
        return f'{self.owner} -repost {self.repost}'



