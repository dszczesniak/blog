from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from datetime import datetime
from django.core.validators import RegexValidator



class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=75)
    image = models.ImageField(null=True, blank=True, width_field="width_field", height_field="height_field") #must be installed Pillow for ImageField
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(default=datetime.now())
    timestamp = models.DateTimeField(default=datetime.now())


    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Post)
def post_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    if instance.image:
        instance.image.delete(False)




class Profile(models.Model):
    onlyletters = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')

    author = models.ForeignKey('auth.User')
    name = models.CharField(max_length=20, null = True, validators=[onlyletters])
    surname = models.CharField(max_length=25, null = True, validators=[onlyletters])
    city = models.CharField(max_length=30, blank=True, validators=[onlyletters])
    birth_date = models.DateField(blank=True, null=True, help_text="Can not be more than 100 years - (Format yyyy-mm-dd)")

    topic = models.CharField(max_length = 50, null=True)


    def __str__(self):
        return self.topic


class Comment(models.Model):
    post = models.ForeignKey('blogapp.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

