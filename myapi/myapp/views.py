from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
from django.utils.timezone import make_aware
import re
import json

from myapp.models import *

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

def get_message(request, m_id):
    if request.method == 'GET':
        try:
            message = Message.objects.get(pk=m_id)          
            response = json.dumps([{ 'message': message.message, 'timestamp' : message.message_timestamp, 'group_id' : message.group_id, 'sender_id' : message.sender_id, 'sender_name' : message.sender_name}])
        except:
            response = json.dumps([{ 'Error': 'No message with that id'}])
    return HttpResponse(response, content_type='text/json')

def get_latest_message(request):
    if request.method == 'GET':
        try:
            message = Message.objects.last()
            utc_time = datetime.fromtimestamp(message.message_timestamp, timezone.utc)
            message.message_timestamp = utc_time.astimezone().strftime("%H:%M:%S %p")
            
            response = json.dumps([{ 'message_id': message.id, 'message': message.message, 'timestamp' : message.message_timestamp, 'group_id' : message.group_id, 'sender_id' : message.sender_id, 'sender_name' : message.sender_name, 'image_url': message.image_url}])

        except:
            response = json.dumps([{ 'Error': 'No latest message'}])
    return HttpResponse(response, content_type='text/json')

def get_top10_message(request):
    if request.method == 'GET':
        try:
            message = Message.objects.last()
            utc_time = datetime.fromtimestamp(message.message_timestamp, timezone.utc)
            message.message_timestamp = utc_time.astimezone().strftime("%H:%M:%S %p")
            
            response = json.dumps([{ 'message_id': message.id, 'message': message.message, 'timestamp' : message.message_timestamp, 'group_id' : message.group_id, 'sender_id' : message.sender_id, 'sender_name' : message.sender_name, 'image_url': message.image_url}])

        except:
            response = json.dumps([{ 'Error': 'No latest message'}])
    return HttpResponse(response, content_type='text/json')

def get_watch_info(request, watch_model):
    if request.method == 'GET':
        try:
            listing = Listing.objects.filter(watch_model=watch_model).latest('watch_model')
            response = json.dumps([{'sender_number': listing.sender_number, 'listing_type' : listing.listing_type, 'datetime' : str(listing.datetime), 'watch_brand' : listing.watch_brand, 'watch_model' : listing.watch_model, 'watch_condition' : listing.watch_condition, 'watch_price' : listing.watch_price}])
        except:
            response = json.dumps([{ 'Error': 'No watch info'}])
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
        
        ################################################################

        pp_models    = ['5164r', '5711/1a blue'] 
        rolex_models = ['126710blro jub', '126710blro oys', '126710blro oys', '126710blnr bub', '126710blnr oys']
        conditions   = ['pre-owned', 'pre owned', 'mint', 'unworn', 'new', 'used', 'without box']

        message = message.replace('.','')
        message = message.replace(r'(',' ')
        message = message.lower()

        #convert unix time to str
        # message_converted_timestamp = datetime.fromtimestamp(message_timestamp, timezone.utc).astimezone().strftime("%d/%M/%Y %H:%M:%S %p")

        # convert unix time to django datetime format
        message_converted_timestamp = make_aware(datetime.fromtimestamp(message_timestamp))

        if (message.find('look') != -1) or (message.find('need') != -1) or (message.find('wtb') != -1):
            message_type = 'Buy'
        else:
            message_type = 'Sell'

        start_contact = 0
        end_contact   = sender_id.find('@')
        contact = sender_id[start_contact:end_contact]

        if contact[:2] == '97':
            state = 'Indonesia'
        elif contact[:3] == '852':
            state = 'Hong Kong'  
        elif contact[:4] == '1347':
            state = 'America'
        elif contact[:2] == '84':
            state = 'America'
        elif contact[:2] == '91':
            state = 'India'
        elif contact[:2] == '66':
            state = 'Thailand'
        elif contact[:3] == '961':
            state = 'Lebanon'
        elif contact[:2] == '60':
            state = 'Malaysia'
        else:
            state = ''
        
        model = ''
        brand = ''
        condition = ''
        price = ''

        model1 = [ele for ele in rolex_models if(ele in message)]

        if model1 != []:
            model = model1[0]
            start_model = message.find(model)
            end_model = start_model + len(model)

            if model in rolex_models:
                brand = 'Rolex'

        model2 = [ele for ele in pp_models if(ele in message)]

        if model2 != []:
            model = model2[0]
            start_model = message.find(model)
            end_model = start_model + len(model)

            if model in pp_models:
                brand = 'Patek'

        condition = [ele for ele in conditions if(ele in message)]

        if condition != []:
            condition = condition[0]
        
        else:
            condition = ' '.join([str(elem) for elem in condition])

        if re.findall('$[0-9]+', message):
            if message.find('$') != -1:
                start_price = message.find('$', end_model)
                end_price = message.find(' ',start_price)
                price = message[start_price:end_price]

        elif re.findall('[0-9]+ usd', message):
            start_price = message.find('[0-9]+', end_model)
            end_price = message.find('usd',start_price)
            price = message[start_price:end_price]

        elif re.findall('[0-9]+hkd', message):
            start_price = message.find('[0-9]+', end_model)
            end_price = message.find('hkd',start_price)
            price = message[start_price:end_price]

        else:
            if re.findall('[0-9]+[$]', message) != []:
                price = '$' + re.findall('[0-9]+[$]', message)[0][:-1]

        ################################################################

        print('\nDebug results here:\n')
        print(message + '\n')
        print(model+ '\n')
        print(brand+ '\n')
        print(condition)
        print('\n' + contact+ '\n')
        print(state+ '\n')
        print(price+ '\n')
        print(image_url)
        
        ################################################################

        message_obj = Message(
            group_id = group_id, 
            sender_id = sender_id,
            sender_name = sender_name,
            is_reply = is_reply,
            user_id = user_id,
            message_id = message_id,
            message_timestamp = message_timestamp,
            message = message,
            image_url = image_url,
            image_mimetype = image_mimetype,
            image_height = image_height,
            image_width = image_width,
            jpeg_thumbnail = jpeg_thumbnail,
            reply_message_id = reply_message_id,
            reply_message_sender_id = reply_message_sender_id,
            reply_message_quote = reply_message_quote
            )

        listing_obj = Listing(
            sender_number = contact,
            group_id = group_id,
            message_id = message_id,
            listing_type = message_type,
            state_name = state,
            watch_brand = brand,
            watch_model = model,
            watch_price = price,
            datetime = message_converted_timestamp,
            watch_condition = ' '.join([str(elem) for elem in condition])
            )
        listing_obj.save()

        try:
            message_obj.save()
            response = json.dumps([{ 'Success':'Message sent successfully!'}]
            )
        except:
            response = json.dumps([{ 'Error': 'Message could not be added!'}]
            )
    return HttpResponse(response, content_type='text/json')