from rest_framework import serializers
from applications.feedback.models import Like,Comment
from applications.feedback.models import Favorite

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

  

class CommentSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source='owner.email') 

    class Meta:
        model = Comment
        fields = '__all__'        



class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Favorite
        fields = '__all__'

