from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
from django.utils.timezone import make_aware
from django.db.models import Count
import numpy as np
import re
import json
import requests
from sqlalchemy import null
from myapp.models import *

def index(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

def get_message(request, m_id):
    if request.method == 'GET':
        try:
            message = Message.objects.get(pk=m_id)
            message = message.replace('\n', ' ')
            response = json.dumps([{'message': message.message, 'timestamp': message.message_timestamp,
                                  'group_id': message.group_id, 'sender_id': message.sender_id, 'sender_name': message.sender_name}])
        except:
            response = json.dumps([{'Error': 'No message with that id'}])
    return HttpResponse(response, content_type='text/json')

def get_latest_message(request):
    if request.method == 'GET':
        try:
            sorted_messages = Message.objects.all().order_by('-message_timestamp')
            distinct_messages = Message.objects.filter(id__in=sorted_messages).distinct('message')
            latest_messages = Message.objects.filter(id__in=distinct_messages).order_by('-message_timestamp')[:100].values('message_id', 'message', 'message_timestamp',
                                  'group_id', 'sender_id', 'sender_name', 'image_url')
            response = json.dumps(list(latest_messages))

            # response = json.dumps([{ 'message_id': message.id, 'message': message.message, 'timestamp' : message.message_timestamp, 'group_id' : message.group_id, 'sender_id' : message.sender_id, 'sender_name' : message.sender_name, 'image_url': message.image_url}])

        except:
            response = json.dumps([{'Error': 'No latest message'}])
    return HttpResponse(response, content_type='text/json')

def get_all_watch_info(request):
    if request.method == 'GET':
        try:
            response = json.dumps(list(Watch.objects.values('id', 'model_name', 'model_number', 'series',
                                  'sex', 'brand', 'avg_price', 'median_price', 'total_listings', 'year', 'name_variations')))

        except:
            response = json.dumps([{'Error': 'No all watch info'}])
    return HttpResponse(response, content_type='text/json')

def get_watch_brands(request):
    if request.method == 'GET':
        try:
            brand = Watch.objects.values('brand').distinct('brand')
            response = json.dumps(list(brand))
        except:
            response = json.dumps([{'Error': 'No watch brand info'}])
    return HttpResponse(response, content_type='text/json')

def get_watch_brands_series(request, brand_name):
    if request.method == 'GET':
        try:
            brand_series = Watch.objects.filter(
                brand=brand_name).values('series').distinct()
            response = json.dumps(list(brand_series))
        except:
            response = json.dumps([{'Error': 'No watch brand series info'}])
    return HttpResponse(response, content_type='text/json')

def get_watch_brands_series_models(request, brand_name, series):
    if request.method == 'GET':
        try:
            query = Watch.objects.filter(
                brand=brand_name, series=series).values('id', 'model_number')
            response = json.dumps(list(query))
        except:
            response = json.dumps(
                [{'Error': 'No watch brand series model info'}])
    return HttpResponse(response, content_type='text/json')

def get_watch_brands_series_models_variation(request, watch_id):
    if request.method == 'GET':
        try:
            query = Watch.objects.filter(id=watch_id).values('name_variations')
            response = json.dumps(list(query))

        except:
            response = json.dumps(
                [{'Error': 'No watch brand series model info'}])
    return HttpResponse(response, content_type='text/json')

def get_specific_watch_info(request, w_id):
    if request.method == 'GET':
        try:
            watch = Watch.objects.get(id=w_id)
            response = json.dumps([{'id': watch.pk, 'model_name': watch.model_name, 'brand': watch.brand,
                                  'avg_price': watch.avg_price, 'total_listings': watch.total_listings}])
        except:
            response = json.dumps([{'Error': 'No watch info'}])
    return HttpResponse(response, content_type='text/json')

def get_listing_info(request, l_id):
    if request.method == 'GET':
        try:
            listing = Listing.objects.get(pk=l_id)
            response = json.dumps([{'sender_number': listing.sender_number, 'listing_type': listing.listing_type, 'datetime': str(
                listing.datetime), 'watch_brand': listing.watch_brand, 'watch_model': listing.watch_model, 'watch_condition': listing.watch_condition, 'watch_price': listing.watch_price}])

        except:
            response = json.dumps([{'Error': 'No listing info'}])
    return HttpResponse(response, content_type='text/json')

def get_all_listing_info(request):
    if request.method == 'GET':
        try:
            sorted_listings = Listing.objects.all().order_by('-datetime')
            distinct_listings = Listing.objects.filter(id__in=sorted_listings).exclude(watch_price__exact=0).distinct('message')
            latest_listings = Listing.objects.filter(id__in=distinct_listings).order_by('-datetime')[:500].values('message', 'sender_number', 'group_id', 'message_id', 'listing_type', 'watch_price', 'watch_condition', 'watch_year', 'datetime', 'state_name', 'watch_brand', 'watch_model')

            response = json.dumps(list(latest_listings), default=str)

        except:
            response = json.dumps([{'Error': 'No listing info'}])
    return HttpResponse(response, content_type='text/json')

def get_all_deals_info(request):
    if request.method == 'GET':
        try:
            # response = json.dumps(list(Deal.objects.values().order_by('-id')), default=str)
            response = json.dumps(list(Deal.objects.values('model_name', 'brand', 'avg_price', 'watch_price', 'margin_difference',
                                  'group_id', 'sender_name', 'message', 'replied', 'datetime').order_by('-datetime').distinct('datetime'))[:100], default=str)

        except:
            response = json.dumps([{'Error': 'No all deals info'}])
    return HttpResponse(response, content_type='text/json')

def get_all_variations_for_watches(request):
    if request.method == 'GET':
        try:
            response = json.dumps([{'all_variations': list(
                Watch.objects.values_list('name_variations', flat=True))}])
        except:
            response = json.dumps([{'Error': 'No all variations info'}])
    return HttpResponse(response, content_type='text/json')

# def get_all_undetected_watches_info(request):
#     if request.method == 'GET':
#         try:
#             response = json.dumps(list(Undetected.objects.values('datetime', 'message', 'model_name','brand','name_variations', 'watch_price').order_by('-datetime').distinct('datetime'))[:100], default=str)
#         except:
#             response = json.dumps([{ 'Error': 'No undetected watches info'}])
#     return HttpResponse(response, content_type='text/json', )

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

        message = message.replace('.', '')
        message = message.replace(r',', '')
        message = message.replace(r'(', ' ')
        message = message.replace(r'\n', ' ')
        message = message.lower()

        # convert unix time to str
        # message_converted_timestamp = datetime.fromtimestamp(message_timestamp, timezone.utc).astimezone().strftime("%d/%M/%Y %H:%M:%S %p")

        # convert unix time to django datetime format
        message_converted_timestamp = make_aware(
            datetime.fromtimestamp(message_timestamp))

        message_obj = Message(
            group_id=group_id,
            sender_id=sender_id,
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
            reply_message_quote=reply_message_quote
        )

        try:
            message_obj.save()
            response = json.dumps([{'Success': 'Message sent successfully!'}]
                                  )
            contact = find_contact_no(sender_id)
            message_type = find_listing_type(message)
            state = find_state_name(contact)
            model, brand = find_model_brand(message)
            price = find_price(message, model)
            year = find_year(message)
            condition = find_condition(message)
            # price = check_price(price)

            ################################################################

            print('\nDebug results here:\n')
            print(message)
            print(year)
            print(model)
            print(brand)
            print(condition)
            print(state)
            print(price)
            print(image_url)

            ################################################################

            if price == None:
                pass

            else:

                listing_obj = Listing(
                    sender_number=contact,
                    group_id=group_id,
                    message_id=message_id,
                    listing_type=message_type,
                    state_name=state,
                    watch_brand=brand,
                    watch_model=model,
                    watch_year=year,
                    watch_price=price,
                    datetime=message_converted_timestamp,
                    watch_condition=condition,
                    message = message
                )
                listing_obj.save()

                if model != '':
                    avg_price = Watch.objects.get(model_number=model).avg_price

                    margin = -10
                    margin_diff = ((price/avg_price)-1)*10
                    if (margin_diff < margin) & (model != ''):
                        deals_obj = Deal(
                            model_name=model,
                            brand=brand,
                            avg_price=avg_price,
                            watch_price=price,
                            margin_difference=margin_diff,
                            group_id=group_id,
                            sender_id=sender_id,
                            sender_name=sender_name,
                            message=message,
                            replied=is_reply,
                            datetime=message_converted_timestamp
                        )
                        deals_obj.save()
                    else:
                        pass
        except:
            response = json.dumps([{'Error': 'Message could not be added!'}]
                                  )
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def add_watch(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        model_name = payload['model_name']
        model_number = payload['model_number']
        series = payload['series']
        sex = payload['sex']
        brand = payload['brand']
        avg_price = payload['avg_price']
        median_price = payload['median_price']
        total_listings = payload['total_listings']
        name_variations = payload['name_variations']

        watch_obj = Watch(
            model_name=model_name,
            model_number=model_number,
            series=series,
            sex=sex,
            brand=brand,
            avg_price=avg_price,
            median_price=median_price,
            total_listings=total_listings,
            name_variations=name_variations)

        try:
            watch_obj.save()
            response = json.dumps([{'Success': 'Watch added successfully!'}]
                                  )
        except:
            response = json.dumps([{'Error': 'Watch not added!'}]
                                  )
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def add_watch_variation(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        watch_id = payload['watch_id']
        variation = payload['variation']

        watch_obj = Watch.objects.get(id=watch_id)

        old_variation = watch_obj.name_variations

        watch_obj.name_variations = old_variation + ',' + variation

        try:
            watch_obj.save()
            response = json.dumps([{'Success': 'Variation updated successfully!'}]
                                  )
        except:
            response = json.dumps([{'Error': 'Variation not updated!'}]
                                  )
    return HttpResponse(response, content_type='text/json')

def find_listing_type(message):
    if (message.find('look') != -1) or (message.find('need') != -1) or (message.find('wtb') != -1):
        listing_type = 'Buy'
    else:
        listing_type = 'Sell'
    return listing_type

def find_contact_no(sender_id):
    start_contact = 0
    end_contact = sender_id.find('@')
    contact = sender_id[start_contact:end_contact]
    return contact

def find_datetime(message_timestamp):
    dt = make_aware(datetime.fromtimestamp(message_timestamp))
    return dt

def find_state_name(contact):
    if contact[:2] == '97':
        state = 'Indonesia'
    elif contact[:3] == '852':
        state = 'Hong Kong'
    elif contact[:1] == '1':
        state = 'America'
    elif contact[:2] == '84':
        state = 'Vietnam'
    elif contact[:2] == '44':
        state = 'United Kingdom'
    elif contact[:2] == '91':
        state = 'India'
    elif contact[:2] == '61':
        state = 'Australia'
    elif contact[:2] == '66':
        state = 'Thailand'
    elif contact[:3] == '961':
        state = 'Lebanon'
    elif contact[:2] == '39':
        state = 'Italy'
    elif contact[:2] == '60':
        state = 'Malaysia'
    elif contact[:2] == '86':
        state = 'China'
    elif contact[:3] == '971':
        state = 'United Arab Emirates'
    elif contact[:2] == '33':
        state = 'France'
    elif contact[:2] == '65':
        state = 'Singapore'
    elif contact[:2] == '31':
        state = 'Netherlands'
    elif contact[:2] == '32':
        state = 'Belgium'
    elif contact[:2] == '34':
        state = 'Spain'
    elif contact[:3] == '389':
        state = 'Macedonia'
    elif contact[:2] == '41':
        state = 'Switzerland'
    elif contact[:2] == '81':
        state = 'Japan'
    elif contact[:2] == '82':
        state = 'South Korea'
    elif contact[:3] == '853':
        state = 'Macau'
    elif contact[:2] == '90':
        state = 'Turkey'
    elif contact[:2] == '92':
        state = 'Pakistan'
    elif contact[:3] == '966':
        state = 'Saudi Arabia'
    else:
        state = ''
    return state

#TODO
# values = list(Watch.objects.filter(brand='Rolex').values_list('name_variations',flat=True))
# keys = list(Watch.objects.filter(brand='Rolex').values_list('model_number',flat=True))
# watch_dict = dict(zip(keys, values))
# watch_dict.update((k, v.split(', ')) for k,v in watch_dict.items())

values = list(Watch.objects.all().values_list('name_variations',flat=True))
keys = list(Watch.objects.all().values_list('model_number',flat=True))
watch_models = dict(zip(keys, values))
watch_models.update((k, v.split(', ')) for k,v in watch_models.items())

# watch_models = {
#     "12300A": ["12300A", "12300-A", "123 000A"],
#     "116505": ["116505"],
#     "116508": ["116508"],
#     "126710BLNR Jubilee": [
#         "126710BLNR Jubilee",
#         "126710BLNR Jub",
#         "126710BLNR Batgirl",
#         "126710 Batgirl",
#         "Batgirl",
#     ],
#     "126710BLNR Oyster": [
#         "126710BLNR Oyster",
#         "126710BLNR Oys",
#         "126710BLNR Batman",
#         "126710 Batman",
#         "Batman",
#     ],
#     "126710BLRO Jubilee": [
#         "126710BLRO Jubilee",
#         "126710BLRO Jub",
#         "126710 Pepsi Jubilee",
#         "126710 Pepsi Jub",
#         "Pepsi Jubilee",
#         "Pepsi Jub",
#     ],
#     "126710BLRO Oyster": [
#         "126710BLRO Oyster",
#         "126710BLRO Oys",
#         "126710 Pepsi Oyster",
#         "126710 Pepsi Oys",
#         "Pepsi Oyster",
#         "Pepsi Oys",
#     ],
#     "126711CHNR": [
#         "126711",
#         "126711CHNR",
#         "126711 CHNR",
#         "126711 Rootbeer",
#         "126711CHNR Rootbeer",
#         "Rootbeer",
#     ],
#     "126715CHNR": [
#         "126715",
#         "126715CHNR",
#         "126715 CHNR",
#         "126715 Rootbeer",
#         "126715CHNR Rootbeer",
#     ],
#     "126719BLRO": ["126719", "126719 Blue", "126719BLRO", "126719BLRO Blue"],
#     "126719BLRO Meteorite": [
#         "126719 Mete",
#         "126719 Met",
#         "126719 Meteorite",
#         "126719BLRO Mete",
#         "126719BLRO Meteorite",
#     ],
#     "126720VTNR Oyster": [
#         "126720 Oys",
#         "126720 Oyster",
#         "126720VTNR Oys",
#         "126720 VTNR Oys",
#         "126720 VTNR Oyster",
#         "126720VTNR Oyster",
#     ],
#     "126720VTNR Jubilee": [
#         "126720 Jub",
#         "126720 Jubilee",
#         "126720VTNR Jub",
#         "126720VTNR Jubilee",
#         "126720 VTNR Jub",
#         "126720 VTNR Jubilee",
#     ],
#     "116500LN": [
#         "116500LN White",
#         "116500 White",
#         "16500LN White Panda",
#         "116500 Pana",
#         "Daytona Panda",
#     ],
#     "124060": ["124060"],
#     "126610LV": ["126110LV", "126610LV Starbucks", "126610 Starbucks", "Starbucks"],
#     "126610LN": ["126610LN"],
#     "126613LB": ["126613LB", "126613 Dual Tone Blue Dial", "126613 Blue Dial"],
#     "126613LN": ["126613LN", "126613 Black"],
#     "126618LB": ["126618LB", "126618 Blue"],
#     "126618LN": ["126618LN", "126618 Black"],
#     "126619LB": ["126619LB", "126619 Smurf", "126619LB Smurf", "Smurf"],
#     "278271 Chocolate DIamonds": ["278271G Choco", "278271 Choco Diamonds"],
#     "278271VI Chocolate": ["278271VI Choco", "278271 Choco VI"],
#     "278271 Pink Diamonds": ["278271G Pink", "278271 Pink Diamonds"],
#     "278274 Blue Roman Jubilee": [
#         "278274 Blue Roman Jub",
#         "278274 Blue Roman Jubilee",
#         "278274 Blue Rom Jubilee",
#     ],
#     "278274 Blue Roman Oyster": ["278274 Blue Roman Oys", "278274 Blue Roman Oyster"],
#     "278274 Black Roman Jubilee": [
#         "278274 Black Roman Jub",
#         "278274 Black Roman Jubilee",
#         "278274 Blk Roman Jub",
#         "278274 Blk Rom Jub",
#         "278274 Blk Roman Jubilee",
#     ],
#     "278274 Green Jubilee": [
#         "278274 Green Jub",
#         "278274 Green Index Jub",
#         "278274 Green Jubilee",
#     ],
#     "278274 Pink Index Jubilee": [
#         "278274 Pink Jub",
#         "278274 Pink Index Jub",
#         "278274 Pink Jubilee",
#     ],
#     "278274 Pink Roman Jubilee": [
#         "278274 Pink Roman",
#         "278274 Pink Roman Jub",
#         "278274 Pink Roman Jubilee",
#         "278274 Pink Rom Jub",
#     ],
#     "278274VI Grey Jubilee": [
#         "278274VI Grey Jub",
#         "278274VI Grey Jubilee",
#         "278274 Grey VI Jubilee",
#     ],
#     "278274VI Pink Jubilee": [
#         "278274VI Pink Jub",
#         "278274VI Pink Jubilee",
#         "278274 Pink VI Jubilee",
#     ],
#     "278274VI Purple Jubilee": [
#         "278274VI Purple Jub",
#         "278274VI Purple Jubilee",
#         "278274 Purple VI Jubilee",
#     ],
#     "278274 Pink Diamonds Jubilee": [
#         "278274G Pink Jubilee",
#         "278274G Pink Jub",
#         "278274 Pink Diamonds Jubilee",
#         "278274 Pink Diamonds Jub",
#     ],
#     "278274 Grey Diamonds Jubilee": [
#         "278274G Grey Jubilee",
#         "278274G Grey Jub",
#         "278274 Grey Diamonds Jubilee",
#         "278274 Grey Diamonds Jub",
#     ],
#     "278271 Pink Index Jubilee": ["278271 Pink Index Jub", "278271 Pink Index Jubilee"],
#     "278271 Pink Roman Jubilee": [
#         "278271 Pink Roman Jub",
#         "278271 Pink Roman Jubilee",
#         "278271 Pink Rom Jub",
#     ],
#     "278271VI Grey Jubilee": [
#         "278271VI Grey Jubilee",
#         "278271VI Grey Jub",
#         "278271 Grey VI Jub",
#     ],
#     "278271VI Purple Jubilee": [
#         "278271VI Purple Jubilee",
#         "278271VI Purple Jub",
#         "278271 Purple VI Jub",
#     ],
#     "278271 Silver Diamonds Jubilee": [
#         "278271G Silver Jubilee",
#         "278271G Silver Jub",
#         "278271 Silver Diamonds Jub",
#     ],
#     "278271 White MOP Jubilee": [
#         "278271NG Jubilee",
#         "278271NG Jub",
#         "278271G White MOP Jubilee",
#         "278271G White MOP Jub",
#     ],
#     "278273 Champagne Index Jubilee": [
#         "278273 Champ Index Jub",
#         "278273 Champ Index Jubilee",
#         "278273 Champagne Index Jub",
#     ],
#     "278273VI Green Jubilee": [
#         "278273VI Green Jub",
#         "278271VI Green Jubilee",
#         "278271 Green VI Jubilee",
#     ],
#     "278273 Champagne Diamonds Jubilee": [
#         "278273 Champagne Diamonds Jubilee",
#         "278273G Champ Jubilee",
#         "278273G Champ Jub",
#     ],
#     "278273 Green Diamonds Jubilee": [
#         "278273 Green Diamonds Jubilee",
#         "278273G Green Jub",
#         "278273G Green Jubilee",
#     ],
#     "279174 Pink Roman Jubilee": ["279174 Pink Roman Jub", "279174 Pink Roman Jubilee"],
#     "279174 Silver Roman Jubilee": [
#         "279174 Silver Roman Jub",
#         "279174 Silver Roman Jub",
#     ],
#     "279174 White MOP Jubilee": [
#         "279174NG Jubilee",
#         "270174NG Jub",
#         "279174G MOP Jubilee",
#         "279174G MOP Jub",
#         "279174 White MOP Jubilee",
#     ],
#     "279173 Champagne Diamonds Jubilee": [
#         "279173G Champ Jub",
#         "279173G Champ Jubilee",
#         "279173G Champagne Jub",
#         "279173 Champage Diamonds Jubilee",
#     ],
#     "126234 Black Index Jubilee": [
#         "126234 Black Index Jubilee",
#         "126234 Black Index Jub",
#         "126234 Blk Index Jub",
#     ],
#     "126234 Blue Fluted Jubilee": [
#         "126234 Blue Fluted Jub",
#         "126234 Blue Fluted Jubilee",
#         "126234 Blue Index Motif Jub",
#         "126234 Blue Index Motif Jubilee",
#     ],
#     "126234 Green Palm Jubilee": [
#         "126234 Green Palm Jub",
#         "126234 Green Palm Jubilee",
#         "126234 Palm Olive Jub",
#     ],
#     "126234 Wimbledon Jubilee": ["126234 Wimbledon Jub", "126234 Wimbledon Jubilee"],
#     "126234 Blue Diamonds Jubilee": [
#         "126234G Blue Jub",
#         "126234G Blue Jubilee",
#         "126234 Blue Diamonds Jubilee",
#     ],
#     "126234 Black Diamonds Jubilee": [
#         "126234G Black Jub",
#         "126234G Black Jubilee",
#         "126234G Blk Jub",
#         "126234G Blk Jubilee",
#         "126234 Blk Diamonds Jub",
#     ],
#     "126331 Wimbledon Jubilee": [
#         "126331 Wimbledon Jub",
#         "126331 Wimbledon Jubilee",
#         "126331 Wimb Jub",
#     ],
#     "126331 Wimbledon Oyster": [
#         "126331 Wimbledon Oys",
#         "126331 Wimbledon Oyster,1 26331 Wimb Oys",
#         "126331 Wim Oys",
#     ],
#     "126334 Black Index Jubilee": [
#         "126334 Black Index Jubilee",
#         "126334 Balck Index Jub",
#         "126334 Blk Jub",
#     ],
#     "126334 Blue Index Jubilee": [
#         "126334 Blue Index Jubilee",
#         "126334 Blue Index Jub",
#         "126334 Blue Jub",
#     ],
#     "126334 Blue Index Oyster": [
#         "126334 Blue Index Oyster",
#         "126334 Blue Index Oys",
#         "126334 Blue Oys",
#     ],
#     "126334 Green Index Jubilee": [
#         "126334 Green Index Jubilee",
#         "126334 Green Index Jub",
#         "126334 Green Jub",
#     ],
#     "126334 Grey Index Jubilee": [
#         "126334 Grey Index Jubilee",
#         "126334 Grey Index Jub",
#         "126334 Grey Jub",
#     ],
#     "126334 Wimbledon Jubilee": [
#         "126334 Wimbledon Jubilee",
#         "126334 Wimbledon Jub",
#         "126334 Wimb Jub",
#     ],
#     "277200 Candy Pink": ["277200 Candy Pink"],
#     "277200 Green": ["277200 Green"],
#     "277200 Red": ["277200 Red"],
#     "277200 Yellow": ["277200 Yellow"],
#     "277200 Blue": ["277200 Blue"],
#     "277200 Tiffany Blue": ["277200 Tiffany Blue"],
#     "126000 Blue": ["126000 Blue"],
#     "126000 Green": ["126000 Green"],
#     "126000 Candy Pink": ["126000 Candy Pink"],
#     "126000 Tiffany Blue": ["126000 Tiffany Blue"],
#     "124300 Green": ["124300 Green"],
#     "124300 Red": ["124300 Red"],
#     "124300 Tiffany Blue": ["124300 Tiffany Blue"],
#     "124300 Black": ["124300 Black"],
#     "126600": ["126600"],
#     "126603": ["126603"],
#     "126660 Black": ["126660 Black", "126660 Blk"],
#     "126660 Deepsea Blue": [
#         "126660 Deepsea Blye",
#         "126660 Blue",
#         "126660Dblue",
#         "126660DB",
#     ],
#     "326235 Chocolate": ["3262365 Choco", "326235 Chocolate"],
#     "326934 Black Jubilee": [
#         "326934 Black Jubilee",
#         "326934 Black Jub",
#         "326934 Blk Jub",
#     ],
#     "326934 Black Oyster": [
#         "326934 Black Oyster",
#         "326934 Black Oys",
#         "326934 Blk Oys",
#     ],
#     "326934 Blue Jubilee": ["326934 Blue Jubilee", "326934 Blue Jub"],
#     "326934 Blue Oyster": ["326934 Blue Oyster", "326934 Blue Oys"],
#     "116509 Grey": ["116509 Grey"],
#     "116509 Black Diamonds": ["116509 Black Diamonds", "116509G Black"],
#     "116509 Blue": ["116509 Blue", "116509 WG Blue"],
#     "116515LN Black": ["116515LN Black", "116515LN BLK"],
#     "116515LN Black Diamonds": [
#         "116515LN Black Diamonds",
#         "116515G Black",
#         "116515G Blk",
#     ],
#     "116515LN Chocolate": ["116515LN Choco", "116515LN Chocolate", "116515 Choco"],
#     "116519LN Black Dimaonds": [
#         "116519LN Black Diamonds",
#         "116519G Black",
#         "116519G Blk",
#         "116519LN G Blk",
#     ],
#     "116519LN Grey": ["116519LN Grey", "116519 Grey"],
#     "116518LN Paul Newman": ["116518 Paul Newman", "116518PN", "116518LN Paul Newman"],
#     "116518LN YML": ["116518YML", "116518LN YML"],
#     "128345RBR Eisenkiesel": ["128345 Eisenkiesel", "128345RBR Eisenkiesel"],
#     "228235 Olive Green": ["228235 Green", "228235 Olive Green", "228235 Olive"],
#     "228230 Olive Green": ["228239 Green", "228239 Olive Greenm 228239 WG Green"],
#     "226570 White": ["226570 White"],
#     "226570 Black": ["226570 Black"],
#     "226658": ["226658"],
#     "226659": ["226659"],
#     "268622": ["268622", "268622 grey"],
#     "268621": ["268621", "268621 Black", "268621 Blk"],
#     "126622": ["126622", "126622 grey"],
#     "126621": ["126621", "126621 Choco"],
#     "26420SO.OO.A600CA.01": ["26420SO.OO.A600CA.01", "26420SO Smoked Grey"],
#     "26420SO.OO.A002CA.01": ["26420SO.OO.A002CA.01", "26420SO Black"],
#     "26420IO.OO.A009CA.01": ["26420IO.OO.A009CA.01", "26420IO", "26420IO Grey"],
#     "26420TI.OO.A027CA.01": ["26420TI.OO.A027CA.01", "26420TI", "26420TI Blue"],
#     "26315ST.OO.1256ST.02": ["26315ST.OO.1256ST.02", "26315ST Grey", "26315 Grey"],
#     "26315ST.OO.1256ST.01": [
#         "26315ST.OO.1256ST.01",
#         "26315ST White",
#         "26315 White",
#         "26315ST White Panda",
#         "26315ST White Blue",
#     ],
#     "15500ST.OO.1220ST.01": ["15500ST.OO.1220ST.01", "15500 Blue", "15500ST Blue"],
#     "15500ST.OO.1220ST.02": ["15500ST.OO.1220ST.02", "15500 Grey", "15500ST Grey"],
#     "15500ST.OO.1220ST.03": ["15500ST.OO.1220ST.03", "15500 Black", "15500ST Black"],
#     "15500ST.OO.1220ST.04": ["15500ST.OO.1220ST.04", "15500 White", "15500ST White"],
#     "26331ST.OO.1220ST.03": [
#         "26331ST.OO.1220ST.03",
#         "26331 White",
#         "26331ST White",
#         "26331ST Panda",
#     ],
#     "26331ST.OO.1220ST.02": ["26331ST.OO.1220ST.02", "26331 Black", "26331ST Black"],
#     "26331ST.OO.1220ST.01": ["26331ST.OO.1220ST.01", "26331 Blue", "26331ST Blue"],
#     "67651SR.ZZ.1261SR.01": ["67651SR.ZZ.1261SR.01", "67651SR"],
#     "67651ST.ZZ.1261ST.01": ["67651ST.ZZ.1261ST.01", "67651ST", "67651ST (lady 33mm)"],
#     "77350SR.OO.1261SR.01": ["77350SR.OO.1261SR.01", "77350SR"],
#     "77350ST.OO.1261ST.01": [
#         "77350ST.OO.1261ST.01",
#         "77350STOO1261ST01",
#         "77350ST",
#         "77350ST White",
#     ],
#     "77351OR.ZZ.1261OR.01": ["77351OR.ZZ.1261OR.01", "77351OR", "77351OR White"],
#     "77351ST.ZZ.1261ST.01": [
#         "77351ST.ZZ.1261ST.01",
#         "77351ST",
#         "77351ST Blue Dial",
#         "77351ST Blue",
#     ],
#     "15720ST.OO.A009CA.01": ["15720ST.OO.A009CA.01", "15720ST Gray", "15720ST Grey"],
#     "15720ST.OO.A027CA.01": ["15720ST.OO.A027CA.01 15720ST Blue"],
#     "15720ST.OO.A052CA.01": ["15720ST.OO.A052CA.01", "15720ST Green"],
#     "26470SO.OO.A002CA.01": ["26470SO.OO.A002CA.01", "26470SO Vampire"],
#     "26420RO.OO.A002CA.01": ["26420RO.OO.A002CA.01", "26420RO"],
#     "15600CE.OO.A002CA.01": ["15600CE.OO.A002CA.01", "156000CE"],
#     "15600TI.OO.A343CA.01": ["15600TI.OO.A343CA.01", "15600TI"],
#     "5267/200A-011": ["5267/200A-011", "5267/200A Green"],
#     "5267/200A-001": ["5267/200A-001", "5267/200A Black", "5267/200A Blk"],
#     "5267/200-010": ["5267/200-010", "5267/200 White", "5267 white"],
#     "5269/200R-001": ["5268/200R-001", "5268/200R"],
#     "5164A-001": ["5164A-001", "5164A", "PP 5164A"],
#     "5164R-001": ["5164R-001", "5164R", "PP 5164R"],
#     "5168G-001": ["5168G-001", "5168G Blue", "5168 Blue"],
#     "5168G-010": ["5168G-010", "5168G Green", "5168 Green"],
#     "5968A-001": ["5968A-001", "5968A"],
#     "5968G-001": ["5968G-001", "5968G Blue"],
#     "5968G-010": ["5968G-010", "5968G Green"],
#     "5167R-001": ["5167R-001", "5167R"],
#     "5167A-001": ["5167A-001", "5167A"],
#     "7010R-011": ["7010R-011", "7010R White"],
#     "7010R-012": ["7010R-012", "7010R Champ"],
#     "5711/1A": [
#         "5711/1A",
#         "5711/1A Blue",
#         "5711 Blue",
#         "5711/1A Blue Dial",
#         "5711/1A Blue Dial Discontinued",
#     ],
#     "5711/1R": ["5711/1R"],
#     "5712/1A-001": ["5712/1A-001", "5712/1A Blue", "5712/1A Blue Dial", "5712 Blue"],
#     "5712R-001": ["5712R-001", "5712R"],
#     "5712G-001": ["5712G-001", "5712G"],
#     "5726/1A-014": [
#         "5726/1A-014",
#         "5726/1A",
#         "5726/1A Blue",
#         "5726 Blue",
#         "5726/1A Blue Dial",
#     ],
#     "5726A-001": ["5726A-001", "5726A", "5726A Grey", "5726A Grey Leather"],
#     "5980/1R-001": ["5980/1R-001", "5980/1R", "5980 1R"],
#     "5980/1AR-001": ["5980/1AR-001", "5980/1AR"],
#     "5980R-001": ["5980R-001", "5980R"],
#     "5990/1A": ["5990/1A", "5990 1A", "5990/1A Old Buckle"],
#     "5990/1R-001": ["5990/1R-001", "5990/1R"],
#     "7010/1R-011": ["7010/1R-011", "7010/1R White"],
#     "7010/1R-012": ["7010/1R-012", "7010/1R Champ", "7010/1R Champagne Dial"],
#     "7118/1R-001": ["7118/1R-001", "7118/1R White"],
#     "7118/1R-010": ["7118/1R-010", "7118/1R Champ", "7118 1R Champagne "],
#     "7118/1A-001": ["7118/1A-001", "7118/1A Blue"],
#     "7118/1A-010": ["7118/1A-010", "7118/1A White"],
#     "7118/1A-011": ["7118/1A-011", "7118/1A Grey"],
#     "7118/1200R-001": ["7118/1200R-001", "7118/1200R White"],
#     "7118/1200R-010": ["7118/1200R-010", "7118/1200R Champ", "7118/1200R Champagne"],
#     "7118/1200A-001": ["7118/1200A-001", "7118/1200A Blue"],
#     "7118/1200A-010": ["7118/1200A-010", "7118/1200A White"],
#     "7118/1200A-011": ["7118/1200A-011", "7118/1200A Grey", "7118 1200A Grey"],
#     "RM011-03 Rosegold": [
#         "RM011-03 RG",
#         "RM11-03 RG",
#         "RM011-03 Rosegold",
#         "RM 11-03 Rosegold",
#         "RM 11-03 Full RG",
#     ],
#     "RM011-03 RG/TI": [
#         "RM011-03 RG/TI",
#         "RM11-03 RG/TI",
#         "RM 11-03 RG/TI",
#         "RM 11-03 RGTI",
#     ],
#     "RM011-03 Titanium": [
#         "RM011-03 TI",
#         "RM11-03 TI",
#         "RM011-03 Titanium",
#         "RM11-03 Tinanium",
#         "RM 11-03 Titanium",
#         "RM 11-03 Titan",
#     ],
#     "RM011-03 NTPT": ["RM011-03 NTPT", "RM 11-03 NTPT", "RM 1103 NTPT"],
#     "RM011-03 Utimate": ["RM011-03 Utimate", "RM 11-03 Ultimate"],
#     "RM65-01 NTPT": ["RM65-01 NTPT", "RM 65-01 NTPT", "RM 6501 NTPT"],
#     "RM65-01 Rosegold": [
#         "RM65-01 RG",
#         "RM65-01 Rosegold",
#         "RM65-01 RG/Carbon",
#         "RM 65-01 RG",
#         "RM 65-01 Rosegold",
#         "RM 65-01 RG/Carbon",
#     ],
#     "RM65-01 Titanium": [
#         "RM65-01 TI",
#         " RM65-01 Titanium",
#         "RM 65-01 Tinanium",
#         "RM 65-01 Titan",
#         "RM 65-01 TI",
#     ],
#     "RM030 Rosegold": [
#         "RM030 RG",
#         "RM30 RG",
#         "RM 030 RG",
#         "RM 30 RG",
#         "RM030 Rosegold",
#         "RM 030 Rosegold RM 30 Rosegold",
#     ],
#     "RM030 NTPT": ["RM030 NTPT", "RM30 NTPT", "RM 030 NTPT", "RM 30 NTPT"],
#     "RM67-02 Mutaz Essa Barshim": [
#         "RM67-02 Mutaz Essa Barshim",
#         "RM 67-02 Mutaz Essa Barshim",
#         "RM67-02 Purple",
#         "RM 67-02 Purple",
#     ],
#     "RM67-02 Alexis Pinturault": [
#         "RM67-02 Alexis Pinturault",
#         "RM 67-02 Alexis Pinturault",
#         "RM67-02 White",
#         "RM 67-02 White",
#     ],
#     "RM67-02 Sprint Wayde Van Niekerk": [
#         "RM67-02 Sprint Wayde Van Niekerk",
#         "RM 7-02 Sprint Wayde Van Niekerk",
#         "RM67-02 Green",
#         "RM 67-02 Green",
#     ],
#     "RM67-02 Alexander Zherev": [
#         "RM67-02 Alexander Zherev",
#         "RM 67-02 Alexander Zherev",
#         "RM67-02 Red",
#         "RM 67-02 Red",
#     ],
#     "RM35-01 Black": ["RM35-01 Black", "RM 35-01 Black"],
#     "RM35-02 Red": ["RM35-02 Red", "RM 35-02 Red"],
#     "RM07-01 Plain WG Red Lips": [
#         "RM07-01 Plain WG Red Lips",
#         "RM 07-01 Plain WG Red Lips",
#     ],
#     "RM07-01 WG Snow Red Lips": [
#         "RM07-01 WG Snow Red Lips",
#         "RM 07-01 WG Snow Red Lips",
#         "RM07-01 WG Snow diamonds Red Lips",
#     ],
#     "RM07-01 WG Medium Set Red Dial": [
#         "RM07-01 WG Medium Set Red Dial",
#         "RM 07-01 WG Medium Set Red Dial",
#         "RM07-01 WG MedSet Red Dial",
#     ],
#     "RM029-01 Lemans": [
#         "RRM029-01 Lemans",
#         "RM29-01 Lemans",
#         "M029 Lemans",
#         "RM 29 Lemans",
#         "RM029 Leman",
#     ],
# }

def find_model(text):
    text = re.sub(' +', ' ', text.lower())
    model = ''
    for model_name, name_variations in watch_models.items():
        for index in name_variations:
            index = index.lower()
            if re.findall(index, text) != []:
                model = model_name.upper()
                variation = index
            else:
                pass

    return model

def find_brand(model):
    if model != '':
        brand = Watch.objects.filter(
            model_name=model).values('brand')[0]['brand']
    else:
        brand = ''
    return brand

def find_model_brand(message):

    model = find_model(message)
    brand = find_brand(model)

    return model, brand

years = {'2022': [' 2022', '/2022', '-2022'],
         '2021': [' 2021', '/2021', '-2021'],
         '2020': [' 2020', '/2020', '-2020'],
         '2019': [' 2019', '/2019', '-2019'],
         '2018': [' 2018', '/2018', '-2018'],
         '2017': [' 2017', '/2017', '-2017'],
         '2016': [' 2016', '/2016', '-2016'],
         '2015': [' 2015', '/2015', '-2015'],
         '2014': [' 2014', '/2014', '-2014'],
         '2013': [' 2013', '/2013', '-2013'],
         '2012': [' 2012', '/2012', '-2012'],
         '2011': [' 2011', '/2011', '-2011'],
         '2010': [' 2010', '/2010', '-2010'],
         '2009': [' 2009', '/2009', '-2009'],
         '2008': [' 2008', '/2008', '-2008'],
         '2007': [' 2007', '/2007', '-2007'],
         '2006': [' 2006', '/2006', '-2006'],
         '2005': [' 2005', '/2005', '-2005'],
         '2004': [' 2004', '/2004', '-2004'],
         '2003': [' 2003', '/2003', '-2003'],
         '2002': [' 2002', '/2002', '-2002'],
         '2001': [' 2001', '/2001', '-2001'],
         '2000': [' 2000', '/2000', '-2000']}

def find_year(text):
    year = ''
    for year_index, year_variations in years.items():
        for index in year_variations:
            if text.find(index) != -1:
                year = year_index

    if year == '':
        year = None
    return year

conditions = {'new': ['new', 'brandnew'],
              'unworn': ['unworn'],
              'no adjustment': ['no adjustment', 'no adj'],
              'pre-owned': ['pre-owned', 'pre owned'],
              'mint': ['mint'],
              'used': ['used'],
              'without box': ['without box', 'w/o box'],
              'with card': ['with card', 'w/card'],
              'with paper': ['with paper', 'w/paper']}

def find_condition(text):
    condition = ''
    for condition_index, condition_variations in conditions.items():
        for index in condition_variations:
            if re.findall(index, text) != []:
                condition = condition_index
            else:
                pass
    return condition

def find_price(message, model):
    price = ''

    # if model != '':
    if re.findall(' [0-9]+ aed', message):
        price = re.findall(' [0-9]+ aed', message)[0]
        price = price.replace(' aed', '')
        price = price.replace(' ', '')
        price = int(price)/3.6725

    elif re.findall('[0-9]+hkd', message):
        price = re.findall('[0-9]+hkd', message)[0]
        price = price.replace('hkd', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd [0-9]+', message):
        price = re.findall('hkd [0-9]+', message)[0]
        price = price.replace('hkd ', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[$][0-9]+', message):
        price = re.findall('hkd[$][0-9]+', message)[0]
        price = price.replace('hkd$', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[:][0-9]+', message):
        price = re.findall('hkd[:][0-9]+', message)[0]
        price = price.replace('hkd:', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[:] [0-9]+', message):
        price = re.findall('hkd[:] [0-9]+', message)[0]
        price = price.replace('hkd: ', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[$][0-9]+', message):
        price = re.findall('hkd[$][0-9]+', message)[0]
        price = price.replace('hkd$', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd [$][0-9]+', message):
        price = re.findall('hkd [$][0-9]+', message)[0]
        price = price.replace('hkd $', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[0-9]+', message):
        price = re.findall('hkd[0-9]+', message)[0]
        price = price.replace('hkd', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[0-9]+ hkd', message):
        price = re.findall('[0-9]+ hkd', message)[0]
        price = price.replace(' hkd', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[0-9]+hkd', message):
        price = re.findall('[0-9]+hkd', message)[0]
        price = price.replace('hkd', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hkd[0-9]+ [0-9]+', message):
        price = re.findall('hkd[0-9]+ [0-9]+', message)[0]
        price = price.replace('hkd', '')
        price = price.replace(' ', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[0-9]+k hkd', message):
        price = re.findall('[0-9]+k hkd', message)[0]
        price = price.replace(' hkd', '')
        price = price.replace('k', '000')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hk[$][0-9]+', message):
        price = re.findall('hk[$][0-9]+', message)[0]
        price = price.replace('hk$', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[0-9]+m hkd', message):
        price = re.findall('[0-9]+m hkd', message)[0]
        price = price.replace(' hkd', '')
        price = price.replace('m', '0000')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[$][0-9]+m hkd', message):
        price = re.findall('[$][0-9]+m hkd', message)[0]
        price = price.replace(' hkd', '')
        price = price.replace('$', '')
        price = price.replace('m', '0000')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[$][0-9]+hkd', message):
        price = re.findall('[$][0-9]+hkd', message)[0]
        price = price.replace('hkd', '')
        price = price.replace('$', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[$][0-9]+k hkd', message):
        price = re.findall('[$][0-9]+k hkd', message)[0]
        price = price.replace(' hkd', '')
        price = price.replace('$', '')
        price = price.replace('k', '000')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('[0-9]+[$] hkd', message):
        price = re.findall('[0-9]+[$] hkd', message)[0]
        price = price.replace(' hkd', '')
        price = price.replace('$', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/7.8

    elif re.findall('hk[$][0-9]+m', message):
        price = re.findall('hk[$][0-9]+m', message)[0]
        price = price.replace('hk$', '')
        price = price.replace('m', '0000')
        price = int(price)/7.8

    elif re.findall('[0-9]+ aed', message):
        price = re.findall('[0-9]+ aed', message)[0]
        price = price.replace(' aed', '')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/3.6725

    elif re.findall('[0-9]+k aed', message):
        price = re.findall('[0-9]+k aed', message)[0]
        price = price.replace(' aed', '')
        price = price.replace('k', '000')
        # price = json.loads(requests.request("GET", "https:/api.apilayer.com/fixer/convert?to=HKD&from=USD&amount="+ price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text['result']
        price = int(price)/3.6725

    elif re.findall('[0-9]+[€] eur', message):
        price = re.findall('[0-9]+[€] eur', message)[0]
        price = price.replace('€ eur', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/1.10

    elif re.findall('[0-9]+ eur', message):
        price = re.findall('[0-9]+ eur', message)[0]
        price = price.replace(' eur', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/1.10

    elif re.findall('[0-9]+[€]', message):
        price = re.findall('[0-9]+[€]', message)[0]
        price = price.replace('€', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/1.10

    elif re.findall('[0-9]+eur', message):
        price = re.findall('[0-9]+eur', message)[0]
        price = price.replace('eur', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/1.10

    elif re.findall('[0-9]+k eur', message):
        price = re.findall('[0-9]+k eur', message)[0]
        price = price.replace(' eur', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = price.replace('k', '000')
        price = int(price)/1.10

    elif re.findall('[€] [0-9]+', message):
        price = re.findall('[€] [0-9]+', message)[0]
        price = price.replace('€ ', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/1.10

    elif re.findall('[0-9]+cny', message):
        price = re.findall('[0-9]+cny', message)[0]
        price = price.replace('cny', '')
        # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixerconvert?to=HKD&from=USD&amount=" + price, headers = {"apikey":    "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
        price = int(price)/6.75

    elif re.findall('[$][0-9]+', message):
        price = re.findall('[$][0-9]+', message)[0]
        price = price.replace('$', '')

    elif re.findall('[$][0-9]+k', message):
        price = re.findall('[$][0-9]+k', message)[0]
        price = price.replace('$', '')
        price = price.replace('k', '000')

    elif re.findall('[$][0-9]+m', message):
        price = re.findall('[$][0-9]+m', message)[0]
        price = price.replace('$', '')
        price = price.replace('m', '0000')

    elif re.findall(' [$] [0-9]+', message):
        price = re.findall(' [$] [0-9]+', message)[0]
        price = price.replace('$ ', '')
        price = price.replace(' ', '')

    elif re.findall('[0-9]+k[-][$]', message):
        price = re.findall('[0-9]+k[-][$]', message)[0]
        price = price.replace('$', '')
        price = price.replace('-', '')
        price = price.replace('k', '000')

    elif re.findall('[$][0-9]+k usd', message):
        price = re.findall('[$][0-9]+k usd', message)[0]
        price = price.replace('$', '')
        price = price.replace(' usd', '')
        price = price.replace('k', '000')

    elif re.findall(' [0-9]+ usd', message):
        price = re.findall(' [0-9]+ usd', message)[0]
        price = price.replace(' usd', '')
        price = price.replace(' ', '')

    elif re.findall(':[0-9]+usd', message):
        price = re.findall(':[0-9]+usd', message)[0]
        price = price.replace('usd', '')
        price = price.replace(':', '')

    elif re.findall('[0-9]+ us[$]', message):
        price = re.findall('[0-9]+ us[$]', message)[0]
        price = price.replace(' us$', '')
        price = price.replace('k', '000')
        price = price.replace('m', '000000')
    elif re.findall(' [0-9]+k usd', message):
        price = re.findall(' [0-9]+k usd', message)[0]
        price = price.replace('k', '000')
        price = price.replace(' usd', '')
        price = price.replace(' ', '')

    elif re.findall(' [0-9]+k usd', message):
        price = re.findall(' [0-9]+k usd', message)[0]
        price = price.replace('k', '000')
        price = price.replace(' usd', '')
        price = price.replace(' ', '')

    elif re.findall('usd [0-9]+', message):
        price = re.findall('usd [0-9]+', message)[0]
        price = price.replace('usd ', '')

    elif re.findall('us[$][0-9]+', message):
        price = re.findall('us[$][0-9]+', message)[0]
        price = price.replace('us$', '')

    elif re.findall(' [0-9]+[$]', message):
        price = re.findall(' [0-9]+[$]', message)[0]
        price = price.replace('$', '')
        price = price.replace(' ', '')

    elif re.findall('[0-9]+k', message):
        if model != '':
            price = re.findall('[0-9]+k', message)[0]
            price = price.replace('k', '000')
            model_avg = Watch.objects.get(model_number=model).avg_price
            hi = model_avg * 1.1
            low = model_avg * 0.9
            price = int(price)
            price_hkd = price/7.8
            price_aed = price/3.65

            # if low < price_hkd < hi:
            #     price = price_hkd

            # elif low < price_aed < hi:
            #     price = price_aed

            # else:
            #     price = price

            if (price_hkd > low) and (price_hkd < hi):
                price = price_hkd

            elif (price_aed > low) and (price_aed < hi):
                price = price_aed

            elif (price_eur > low) and (price_eur < hi):
                price = price_eur

            else:
                price = price

    elif re.findall('[0-9]+m', message):
        if model != '':
            price = re.findall('[0-9]+m', message)[0]
            price = price.replace('m', '0000')
            model_avg = Watch.objects.get(model_number=model).avg_price
            hi = model_avg * 1.1
            low = model_avg * 0.9
            price = int(price)
            price_hkd = price/7.8
            price_aed = price/3.6725
            price_eur = price/1.10

            # if low < price_hkd < hi:
            #     price = price_hkd

            # elif low < price_aed < hi:
            #     price = price_aed

            # elif low < price_eur < hi:
            #     price = price_eur

            if (price_hkd > low) and (price_hkd < hi):
                price = price_hkd

            elif (price_aed > low) and (price_aed < hi):
                price = price_aed

            elif (price_eur > low) and (price_eur < hi):
                price = price_eur

            else:
                price = price

    elif re.findall('[0-9]+', message):
        if model != '':
            price = re.findall('[0-9]+', message)[0]
            model_avg = Watch.objects.get(model_number=model).avg_price
            hi = model_avg * 1.1
            low = model_avg * 0.9
            price = int(price)
            price_hkd = price/7.8
            price_aed = price/3.6725
            price_eur = price/1.10

            # if low < price_hkd < hi:
            #     price = price_hkd

            # elif low < price_aed < hi:
            #     price = price_aed

            # elif low < price_eur < hi:
            #     price = price_eur

            if (price_hkd > low) and (price_hkd < hi):
                price = price_hkd

            elif (price_aed > low) and (price_aed < hi):
                price = price_aed

            elif (price_eur > low) and (price_eur < hi):
                price = price_eur

            else:
                price = price

    else:
        price = 0

    if model != '':
        model_avg = Watch.objects.get(model_number=model).avg_price
        price = int(round(float(price), 0))

        hi = model_avg * 1.1
        low = model_avg * 0.9

        price_hkd = price/7.8
        price_aed = price/3.6725
        price_eur = price/1.10

        # if low < price_hkd < hi:
        #     price = price_hkd

        # elif low < price_aed < hi:
        #     price = price_aed

        # elif low < price_eur < hi:
        #     price = price_eur

        if (price_hkd > low) and (price_hkd < hi):
            price = price_hkd

        elif (price_aed > low) and (price_aed < hi):
            price = price_aed

        elif (price_eur > low) and (price_eur < hi):
            price = price_eur

    else:
        price = price

    if price == '':
        price = 0

    else:
        price = int(round(float(price), 0))

    return price

# def get_average(query):
#     df =  pd.DataFrame.from_records(query)
#     df_agg_avg = df.groupby('watch_model').agg({'watch_price':'mean'}).to_dict('records')
#     return df_agg_avg

# def get_median(query):
#     df =  pd.DataFrame.from_records(query)
#     df_agg_med = df.groupby('watch_model').agg({'watch_price':'median'}).to_dict('records')
#     return df_agg_med

def check_price(price, model):
    model_avg = Watch.objects.get(model_number=model).avg_price

    hi = model_avg * 1.1
    low = model_avg * 0.9

    if low < price < hi:
        price = price

    else:
        price = None

    return price
