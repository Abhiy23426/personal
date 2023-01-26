from django.contrib import admin
from myApp.models import Post,Comment,Like
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	l=['title','slug','publish','photo']
	prepopulated_fields={'slug':('title',)}
	list_filter=['publish',]
	search_fields=['title',]
	ordering=['publish',]

class CommentAdmin(admin.ModelAdmin):
	l=['post','user','comment','created','updated','active']
	list_filter=['active','created','updated']

class LikeAdmin(admin.ModelAdmin):
	l=['post','user','liked','created','updated']
	list_filter=['post','user','liked']

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Like,LikeAdmin)