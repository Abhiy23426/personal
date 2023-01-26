from django.shortcuts import render,get_object_or_404,redirect
from myApp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myApp.models import Comment,Like
from myApp.forms import CommentForm,SignUpForm,LikeForm,VerificationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your views here.

otp=0

def home_view(request):
	return render(request,'myApp/home.html')

@login_required
def post_list_view(request):
	post_list=Post.objects.all()
	paginator=Paginator(post_list,4)
	page_number=request.GET.get('page')
	try:
		post_list=paginator.page(page_number)
	except:
		post_list=paginator.page(1)
	d={'post_list':post_list}
	return render(request,'myApp/post_list.html',d)

@login_required
def post_detail_view(request,year,month,day,send_slug):
	post=get_object_or_404(Post,slug=send_slug,publish__year=year,publish__month=month,publish__day=day)
	user=request.user
	comments=post.comments.filter(active=True)
	form=CommentForm()

	likes=Like.objects.filter(post=post,liked=True)
	try:
		like=Like.objects.get(user=user,post=post)
	except:
		like=Like(user=user,post=post)
	like_f=LikeForm()
	if request.method=="POST":
		if 'comment_post' in request.POST:
			form=CommentForm(request.POST)
			if form.is_valid():
				newcomment=form.save(commit=False)
				newcomment.post=post
				newcomment.user=user
				newcomment.save()
				form=CommentForm()
		if 'liked' in request.POST:
			like_f=LikeForm(request.POST)
			if like_f.is_valid():
				if like.liked==True:
					like.delete()
					like=Like(user=user,post=post)
				else:
					like.liked=True
					like.save()
	d={'post':post,'form':form,'comments':comments,'like_f':like_f,'like':like,'likes':likes}
	return render(request,'myApp/post_detail.html',d)

def signup_view(request):
	global otp
	f=SignUpForm()
	if request.method=="POST":
		f=SignUpForm(request.POST)
		if f.is_valid():
			user=f.save(commit=False)
			# user.set_password(user.password)
			f_name=user.first_name
			l_name=user.last_name
			user_name=user.username
			password=user.password
			e_mail=user.email
			ran=''.join(random.choices(string.ascii_letters+string.digits,k=50))
			otp=random.randint(111111,999999)
			subject = "DevilQueen verification code: {}".format(otp)
			message = "Use this code to finish signing up for DevilQueen: \n{0}".format(otp)
			sender='Devil Queen'
			receiver=[user.email]
			send_mail(subject,message,sender,receiver)
			return HttpResponseRedirect(reverse('otp_verify',kwargs={'user':user,'f_name':f_name,'l_name':l_name,'user_name':user_name,'fake':ran,'password':password,'e_mail':e_mail}))
	d={"form":f}
	return render(request,'myApp/signup.html',d)


def logout_view(request):
	return render(request,'myApp/logout.html')

def verification_view(request,user,f_name,l_name,user_name,fake,password,e_mail):
	global otp
	print(otp)
	eror=False
	vform=VerificationForm()
	if request.method=='POST':
		vform=VerificationForm(request.POST)
		if vform.is_valid():
			ot=vform.cleaned_data['otp']
			print("entered otp is : ",ot)
			print("otp is : ",otp)
			if ot==otp:
				s_user=User(first_name=f_name,last_name=l_name,username=user_name,email=e_mail)
				s_user.set_password(password)
				s_user.save()
				return HttpResponseRedirect("/")
			else:
				eror=True
				return render(request,'myApp/verification.html',{'vform':vform,'eror':eror})
	else:
		vform=VerificationForm()
	return render(request,'myApp/verification.html',{'vform':vform,'eror':eror})

