from django.contrib import admin
from .models import Listing, Message

admin.site.register(Message)
class CustomMessageAdmin(admin.ModelAdmin):
    model        = Message
    list_display = ('group_id','sender_id','sender_name','message_id','message')

admin.site.register(Listing)
class CustomListingAdmin(admin.ModelAdmin):
    model        = Listing
    list_display = ('group_id','sender_number','message_id','message_id','listing_type','watch_price','watch_condition','watch_year','datetime','state_name','watch_brand','watch_model')