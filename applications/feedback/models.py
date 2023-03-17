from django.db import models
from django.contrib.auth import get_user_model  

User = get_user_model()


# class Following(models.Model):
#     owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
#     owner2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
#     is_follow = models.BooleanField(default=False)
    

#     def __str__(self):
#         return f'{self.owner} liked - {self.owner2}'
    



