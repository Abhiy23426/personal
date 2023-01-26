from django import forms
from myApp.models import Comment,Like,Post
from django.contrib.auth.models import User
class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=('comment','comment_post')
		widgets={'comment_post':forms.HiddenInput}

class SignUpForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['first_name','last_name','username','password','email']
		help_texts={'username':None}

class LikeForm(forms.ModelForm):
	class Meta:
		model=Like
		fields=('liked',)
		widgets={'liked':forms.HiddenInput}

class VerificationForm(forms.Form):
	otp=forms.IntegerField()