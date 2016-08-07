"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from blogapp.views import *
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', home, name='home'),
    #logging
    url(r'^login/$',  login_view, name='login'),
    url(r'^register/$',  register_view, name='register'),
    url(r'^logout/$',  logout_view, name='logout'),
    url(r'^captcha/', include('captcha.urls')),
    #creating
    url(r'^new_prof/$',  new_prof_view, name='new_prof'),
    url(r'^blog/(?P<pk>[0-9]+)/$', blog_detail_view, name='blog_detail'),
    url(r'^my_blog/$',  my_blog_view, name='my_blog'),
    url(r'^post/(?P<pk>[0-9]+)/$',  post_view, name='post_view'),
    url(r'^post/(?P<pk>\d+)/comment/$', post_view, name='add_comment_to_post'),
    #favs
    url(r'^favs/$', favourites_view, name='favourites'),
    #ajax
    url(r'^search/$', search_blog_view),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)