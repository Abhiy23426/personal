"""PersonalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from myApp.views import *
from django.conf.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path("^$",post_list_view),
    re_path('(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<send_slug>[-\w]+)/',post_detail_view,name='post_detail'),
    re_path('verification/(?P<user>[\w]+)/(?P<f_name>[\w]+)/(?P<l_name>[\w]+)/(?P<user_name>[_@.\w]+)/(?P<fake>[\w]+)/(?P<password>[ _@.$%#\w]+)/(?P<e_mail>[@.\w]+)/',verification_view,name='otp_verify'),
    path('signup/',signup_view),
    path('logout_page/',logout_view),
    path('accounts/',include('django.contrib.auth.urls'))

]
