from django.db import models

class Message(models.Model):

    group_id = models.TextField(null = True, blank = True)
    sender_id = models.TextField(null = True, blank = True)
    sender_name = models.TextField(null = True, blank = True)

    is_reply = models.BooleanField(null = True, blank = True)
    user_id = models.TextField(null = True, blank = True)

    message_id = models.TextField(null = True, blank = True)
    message_timestamp = models.IntegerField(null = True, blank = True)
    message = models.TextField(null = True, blank = True)
    message_type = models.TextField(null = True, blank = True)

    image_url = models.TextField(null = True, blank = True)
    image_mimetype = models.TextField( null = True, blank = True)
    image_height = models.IntegerField(null = True, blank = True)
    image_width = models.IntegerField(null = True, blank = True)
    jpeg_thumbnail  = models.TextField(null = True, blank = True)

    reply_message_id = models.TextField(null = True, blank = True)
    reply_message_sender_id = models.TextField(null = True, blank = True)
    reply_message_quote = models.TextField(null = True, blank = True)

class Listing(models.Model):

    sender_number = models.TextField(null = True, blank = True)
    group_id = models.TextField(null = True, blank = True)
    message_id = models.TextField(null = True, blank = True)
    listing_type = models.TextField(null = True, blank = True)
    watch_price = models.IntegerField(null = True, blank = True)
    watch_condition = models.TextField(null = True, blank = True)
    watch_year = models.IntegerField(null = True, blank = True)
    datetime = models.DateTimeField(null = True, blank = True)
    state_name = models.TextField(null = True, blank = True)
    watch_brand = models.TextField(null = True, blank = True)
    watch_model = models.TextField(null = True, blank = True)


class Watch(models.Model):

    model_name = models.TextField(null = True, blank = True)
    brand = models.TextField(null = True, blank = True)
    avg_price = models.IntegerField(null = True, blank = True)
    total_listings = models.IntegerField(null = True, blank = True)
    name_variations = models.TextField(null = True, blank = True)

class Deal(models.Model):

    model_name = models.TextField(null = True, blank = True)
    brand = models.TextField(null = True, blank = True)
    avg_price = models.IntegerField(null = True, blank = True)
    watch_price = models.IntegerField(null = True, blank = True)
    margin_difference = models.IntegerField(null = True, blank = True)
    group_id = models.TextField(null = True, blank = True)
    sender_id = models.TextField(null = True, blank = True)
    sender_name = models.TextField(null = True, blank = True)
    message = models.TextField(null = True, blank = True)
    replied = models.BooleanField(default=False)
    datetime = models.DateTimeField(null = True, blank = True)