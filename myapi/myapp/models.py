from django.db import models

class Message(models.Model):
    # sender = models.IntegerField()
    # text = models.CharField(max_length=200)
    # group = models.CharField(max_length=200)

    group_id = models.TextField(null = True, blank = True)
    sender_id = models.TextField(null = True, blank = True)
    sender_name = models.TextField(null = True, blank = True)

    is_reply = models.BooleanField(null = True, blank = True)
    user_id = models.TextField(null = True, blank = True)

    message_id = models.TextField(null = True, blank = True)
    message_timestamp = models.IntegerField(null = True, blank = True)
    message = models.TextField(null = True, blank = True)

    image_url = models.TextField(null = True, blank = True)
    image_mimetype = models.TextField( null = True, blank = True)
    image_height = models.IntegerField(null = True, blank = True)
    image_width = models.IntegerField(null = True, blank = True)
    jpeg_thumbnail  = models.TextField(null = True, blank = True)

    reply_message_id = models.TextField(null = True, blank = True)
    reply_message_sender_id = models.TextField(null = True, blank = True)
    reply_message_quote = models.TextField(null = True, blank = True)