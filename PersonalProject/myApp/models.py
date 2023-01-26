from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Post(models.Model):
	title=models.CharField(max_length=200)
	slug=models.SlugField(max_length=50,unique_for_date="publish")
	publish=models.DateTimeField(default=timezone.now)
	photo=models.ImageField(upload_to='static/postimg',default="")
	click_post=models.BooleanField(default=True)
	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("post_detail",args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])

class Like(models.Model):
	user=models.ForeignKey(User,related_name='like',on_delete=models.CASCADE)
	post=models.ForeignKey(Post,related_name='like',on_delete=models.CASCADE)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	liked=models.BooleanField(default=False)
	def __str__(self):
		return '{2} by {0} on {1}'.format(self.user.username,self.post,self.liked)

	class Meta:
		ordering = ('-updated',)

class Comment(models.Model):
	user=models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE,default="")
	post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	comment=models.CharField(max_length=200,default="")
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	active=models.BooleanField(default=True)
	comment_post=models.BooleanField(default=True)
	def __str__(self):
		return 'commented by {0} on {1}'.format(self.user.username,self.post)

	class Meta:
		ordering=('-created',)
