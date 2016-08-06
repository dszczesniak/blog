from django.contrib import admin
from .models import Post, Profile, Comment, Membership, Favourite

admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Membership)
admin.site.register(Favourite)