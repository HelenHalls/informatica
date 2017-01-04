from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    author = models.ForeignKey(User)
    text = models.CharField(max_length=140, default='')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.pk)

class Coment(models.Model):
	date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User)
	text = models.CharField(max_length=140, default='')
	id_message = models.ForeignKey(Message)

	def __str__ (self):
			return "%s" % (self.id_message)

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="who_follows")
    followed = models.ForeignKey(User, related_name="who_is_followed")
    follow_time = models.DateTimeField(auto_now=True)

    def __str__(self):
      return "%s is following %s" % (self.follower, self.followed)

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_count = models.IntegerField(default=0)
    followed_count = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % (self.user)
