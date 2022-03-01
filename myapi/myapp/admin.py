from django.contrib import admin
from .models import Message

admin.site.register(Message)
class CustomMessageAdmin(admin.ModelAdmin):
    model        = Message
    list_display = ('group_id','sender_id','sender_name','message_id','message')