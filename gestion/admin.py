from django.contrib import admin
from .models import Message, Coment, Follow, UserProfile
# Register your models here.

admin.site.register(Message)
admin.site.register(Coment)
admin.site.register(Follow)
admin.site.register(UserProfile)
