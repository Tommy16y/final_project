from django.contrib import admin
from .models import Post,PostMedia,Repost

class MediaAdmin(admin.TabularInline):
    model = PostMedia
    fields = ('media',)
    max_num = 4


class PostAdmin(admin.ModelAdmin):
    inlines = (MediaAdmin)
    list_display = ('title','owner','post_count','created_at')
    list_filter =('owner',)
    search_fields = ('title',)    

admin.site.register(Post)
admin.site.register(Repost)
admin.site.register(PostMedia)


