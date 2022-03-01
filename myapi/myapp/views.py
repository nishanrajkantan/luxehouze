from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

from myapp.models import Message

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

def get_message(request, message_text):
    if request.method == 'GET':
        try:
            message = Message.objects.get(name=message_text)
            response = json.dumps([{ 'Message': message.text}])
        except:
            response = json.dumps([{ 'Error': 'No message with that text'}])
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        group_id = payload['group_id']
        sender_id = payload['sender_id']
        sender_name = payload['sender_name']
        is_reply = payload['is_reply']
        user_id = payload['user_id']
        message_id = payload['message_id']
        message_timestamp = payload['message_timestamp']
        message = payload['message']
        image_url = payload['image_url']
        image_mimetype = payload['image_mimetype']
        image_height = payload['image_height']
        image_width = payload['image_width']
        jpeg_thumbnail = payload['jpeg_thumbnail']
        reply_message_id = payload['reply_message_id']
        reply_message_sender_id = payload['reply_message_sender_id']
        reply_message_quote = payload['reply_message_quote']

        message_obj = Message(group_id=group_id, sender_id=sender_id,
        sender_name=sender_name,
        is_reply=is_reply,
        user_id=user_id,
        message_id=message_id,
        message_timestamp=message_timestamp,
        message=message,
        image_url=image_url,
        image_mimetype=image_mimetype,
        image_height=image_height,
        image_width=image_width,
        jpeg_thumbnail=jpeg_thumbnail,
        reply_message_id=reply_message_id,
        reply_message_sender_id=reply_message_sender_id,
        reply_message_quote=reply_message_quote)

        try:
            message_obj.save()
            response = json.dumps([{ 'Success': 'Message added successfully!'}])
        except:
            response = json.dumps([{ 'Error': 'Message could not be added!'}])
    return HttpResponse(response, content_type='text/json')
