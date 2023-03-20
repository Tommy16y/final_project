from rest_framework import serializers
from applications.post.models import Post,PostMedia,Repost
from applications.feedback.serializers import LikeSerializer
from applications.feedback.models import Like


class PostMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostMedia
        fields = '__all__'
        


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True,read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')
    likes = LikeSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ['likes']

    
    # def to_representation(self, instance):
        
        # representation = super().to_representation(instance)  
        # representation['like_count'] = instance.likes.filter(is_like=True).count()  
        
        # for like in representation['likes']:
        #     if not like['is_like']:
        #         representation['likes'].remove()
            
        # representation['name'] = 'John'
    def to_representation(self, instance):
        
        representation = super().to_representation(instance)  
        representation['like_count'] = instance.likes.filter(is_like=True).count()  
        
        # for like in representation['likes']:
        #     if not like['is_like']:
        #         representation['likes'].remove(like)
            
        # representation['name'] = 'John'
        # representation['likes'] = None

        # representation['owner'] = instance.owner.email
        # print(representation)       

        return representation      


    def create(self,validated_data):
        post = Post.objects.create(**validated_data)

        request = self.context.get('request')
        data = request.FILES
        media_objects = []
        for i in data.getlist('media'):
            media_objects.append(PostMedia(post=post,media=i))
        PostMedia.objects.bulk_create(media_objects)    
        return post
    


class RepostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    owner2 =  serializers.ReadOnlyField(source='owner2.email')
    
    class Meta:
       model = Repost
       fields = '__all__'


    def create(self, validated_data):
        # {owner: token, owner2: null, repost:1} # repost.owner

        validated_data['owner2'] = validated_data['repost']
        return super().create(validated_data)

    