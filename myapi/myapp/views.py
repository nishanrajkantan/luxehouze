from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone
from django.utils.timezone import make_aware
from django.db.models import Avg
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

def get_all_watch_info(request):
    if request.method == 'GET':
        try:
            response = json.dumps(list(Watch.objects.values().order_by('-id')))
        except:
            response = json.dumps([{ 'Error': 'No all watch info'}])
    return HttpResponse(response, content_type='text/json')
    
def get_specific_watch_info(request, watch_model):
    if request.method == 'GET':
        try:
            watch = Watch.objects.get(model_name=watch_model)
            response = json.dumps([{'id': watch.pk, 'model_name': watch.model_name, 'brand' : watch.brand, 'avg_price' : watch.avg_price, 'total_listings' : watch.total_listings}])
        except:
            response = json.dumps([{ 'Error': 'No watch info'}])
    return HttpResponse(response, content_type='text/json')

def get_listing_info(request, l_id):
    if request.method == 'GET':
        try:
            listing = Listing.objects.get(pk=l_id)
            response = json.dumps([{'sender_number': listing.sender_number, 'listing_type' : listing.listing_type, 'datetime' : str(listing.datetime), 'watch_brand' : listing.watch_brand, 'watch_model' : listing.watch_model, 'watch_condition' : listing.watch_condition, 'watch_price' : listing.watch_price}])
        except:
            response = json.dumps([{ 'Error': 'No listing info'}])
    return HttpResponse(response, content_type='text/json')

def get_all_deals_info(request):
    if request.method == 'GET':
        try:
            response = json.dumps(list(Deal.objects.values().order_by('-id')), default=str)
        except:
            response = json.dumps([{ 'Error': 'No all deals info'}])
    return HttpResponse(response, content_type='text/json', )
    
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

        message = message.replace('.','')
        message = message.replace(r',','')
        message = message.replace(r'(',' ')
        message = message.replace(r'\n', ' ') 
        message = message.lower()

        #convert unix time to str
        # message_converted_timestamp = datetime.fromtimestamp(message_timestamp, timezone.utc).astimezone().strftime("%d/%M/%Y %H:%M:%S %p")

        # convert unix time to django datetime format
        message_converted_timestamp = make_aware(datetime.fromtimestamp(message_timestamp))

        contact = find_contact_no(sender_id)
        price  = find_price(message)
        message_type = find_listing_type(message)
        state = find_state_name(contact)
        model, brand = find_model_brand(message)
        year = find_year(message)
        condition = find_condition(message)

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

        if price == 0:
            pass

        else:

            listing_obj = Listing(
                sender_number = contact,
                group_id = group_id,
                message_id = message_id,
                listing_type = message_type,
                state_name = state,
                watch_brand = brand,
                watch_model = model,
                watch_year = year,
                watch_price = price,
                datetime = message_converted_timestamp,
                watch_condition = condition,
                )
            listing_obj.save()            

            avg_price = round(Listing.objects.values('watch_model').annotate(avg_price=Avg('watch_price')).last()['avg_price'], 0)
            # avg_price = Listing.groupby('watch_brand', as_index=False)['watch_price'].mean()
            print(avg_price)

            margin = -10
            margin_diff = ((price/avg_price)-1)*100

            if (margin_diff < margin) & (model != ''):

                deals_obj = Deal(
                    model_name = model,
                    brand = brand,
                    avg_price = avg_price,
                    watch_price = price,
                    margin_difference = margin_diff,
                    group_id = group_id,
                    sender_id = sender_id,
                    sender_name = sender_name,
                    message = message,
                    replied = is_reply,
                    datetime = message_converted_timestamp
                    )
                deals_obj.save()

            else:
                pass
            

        try:
            message_obj.save()
            response = json.dumps([{ 'Success':'Message sent successfully!'}]
            )
        except:
            response = json.dumps([{ 'Error': 'Message could not be added!'}]
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
    end_contact   = sender_id.find('@')
    contact       = sender_id[start_contact:end_contact]
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


pp_models    = {'5164a': ['5164a'],
                '5164r': ['5164r'], 
                '5711/1a' : ['5711/1a'],
                '5711/1r' : ['5711/1r', '5711r', '5711 / 1r'], 
                '6102r': ['6102r', '6102 r'],  
                '6102p': ['6102p'], 
                '5110g': ['5110g'], 
                '5110p': ['5110p'],
                '5968g': ['5968g'], 
                '5968a': ['5968a'], 
                '5968/1a': ['5968/1a'],
                '5980r': ['5980r'], 
                '5980/1a': ['5980/1a'], 
                '5990/1a': ['5990/1a', '5990 1a'], 
                '5712r': ['5712r'], 
                '5712/1a': ['5712/1a'],
                '5930p': ['5930p'], 
                '5930g': ['5930g'], 
                '5905/1a': ['5905/1a', '5905 '], 
                '5905r': ['5905r'], 
                '5905p': ['5905p'],
                '7118/1200a': ['7118/1200a'], 
                '7118/1200r': ['7118/1200r'], 
                '7118/1a': ['7118/1a', '7118-1a'], 
                '7118/1r': ['7118/1r'], 
                '5269/200r': ['5269/200r'],
                '5961p':['5961p'],
                '5072r':['5072r'],
                '5711j':['5711j'],
                '5270p':['5270p'],
                '7010r':['7010r'],
                '5168g':['5168g'],
                '7011/1r':['7011/1r'],
                '5130r/1r':['5130r/1r'],
                '5724r':['5724r'],
                '5270g':['5270g'],
                '5147g':['5147g'],
                '126334g':['126334g'],
                '5980/1r':['5980/1r', '5980-1r'],
                '5212a':['5212a'],
                '18238':['18238'],
                '3710/1a':['3710/1a'],
                '4948r':['4948r'],
                '5167':['5167']}

rolex_models = {'126710blro jub': ['126710blro jub'],
                '126710blro oys': ['126710blro oys'], 
                '126710blnr jub': ['126710blnr jub','126710blnr,jub'], 
                '126710blnr oys': ['126710blnr oys', '126710 blnr oys'], 
                '116619lb': ['116619lb', '116619 '], 
                '268622': ['268622'], 
                '279171g choc jub': ['279171g choc jub', '279171g choco jubilee'], 
                '279171g green jub': ['279171g green jub'], 
                '279171g purple jub': ['279171g purple jub'], 
                '116508 green': ['116508 green', '116508green', '116508gr', '116508g'], 
                '116508 black': ['116508 black', '116508 blk'],
                '279174g':['279174g'],
                '126613lb':['126613lb'],
                '16700':['16700'],
                '126200':['126200'],
                '114270':['114270'],
                '16013':['16013'],
                '116689':['116689'],
                '16233':['16233'],
                '16523':['16523'],
                '18038':['18038'],
                '126231':['126231'],
                '16523':['16523'],
                '126619lb':['126619lb'],
                '126613lb':['126613lb'],
                '279174g':['279174g'],
                '116519':['116519'],
                '116500ln':['116500ln', '116500 ln'],
                '228283':['228283'],
                '126610lv':['126610lv'],
                '326934':['326934'],
                '116331g':['116331g'],
                '126233':['126233'],
                '116509':['116509'],
                '162334':['162334'],
                '116508':['116508'],
                '116518':['116518'],
                '116505a':['116505a'],
                '124300':['124300'],
                '116520':['116520'],
                '278384rbr':['278384rbr'],
                '126900':['126900'],
                '16528':['16528'],
                '226658':['226658'],
                '126333':['126333'],
                '126331':['126331'],
                '116710ln':['116710ln'],
                '116610lv':['116610lv'],
                '116713ln':['116713ln'],
                '116589rbr':['116589rbr'],
                '1600':['1600'],
                '126622':['126622'],
                '278273':['278273'],
                '116589rbr':['116589rbr'],
                '279381rbr':['279381rbr'],
                '326933':['326933'],
                '114300':['114300'],
                '68278':['68278'],
                '228239':['228239'],
                '126300 ':['126300'],
                '126000':['126000'],
                '326934':['skydweller', 'sky-dweller', '326934'],
                '16520':['16520', 'daytona zenith'],
                '126715':['126715']}

rm_models    = {'rm055': ['rm055'],
                'rm030': ['rm030'],
                'rm023': ['rm023'],
                'rm011': ['rm11', 'rm011', '011 wg'],
                'rm010': ['rm010'],
                'rm029': ['rm029'],
                'rm07' : ['rm07']}

ap_models    = {'26240st': ['26240st'],
                '26402cb': ['26402cb'],
                '26170st': ['26170st'],
                '15202bc': ['15202bc'],
                '25808ba': ['25808ba'],
                '26609ti': ['26609ti'],
                '26510st': ['26510st'],
                '15206pt': ['15206pt'],
                '15305or': ['15305or'],
                '26405ce': ['26405ceooa056ca01'],
                '26022or': ['26022or', '26022'],
                '15202st': ['15202st'],
                '26231st':['26231st'],
                '15500st':['15500st'],
                '15202st':['15202st', '15202']}

casio_models = {'3284':['3284']}

cartier_models = {'wssa0030':['wssa0030']}


def find_pp_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in pp_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
                brand = 'Patek Philippe'
            else:
                pass
    if model=='':
        if re.findall('[0-9][0-9][0-9][0-9][a-z] ', text) != []:
            model = re.findall('[0-9][0-9][0-9][0-9][a-z] ', text)[0]
            brand = 'Patek Philippe'
        
        elif re.findall('[0-9][0-9][0-9][0-9][/][0-9]+[a-z] ', text) != []:
            model = re.findall('[0-9][0-9][0-9][0-9][/][0-9]+[a-z] ', text)[0]
            brand = 'Patek Philippe'
        
        elif re.findall('[0-9][0-9][0-9][0-9][-][0-9]+[a-z] ', text) != []:
            model = re.findall('[0-9][0-9][0-9][0-9][-][0-9]+[a-z] ', text)[0]
            brand = 'Patek Philippe'

        elif re.findall('[0-9][0-9][0-9][0-9][a-z][-]', text) != []:
            model = re.findall('[0-9][0-9][0-9][0-9][a-z]', text)[0]
            brand = 'Patek Philippe'
    
    return model, brand

def find_rolex_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in rolex_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
                brand = 'Rolex'
            else:
                pass

    if model=='':
        if re.findall('[0-9][0-9][0-9][0-9][0-9][0-9][a-z][a-z] ', text) != []:
            model = re.findall('[0-9][0-9][0-9][0-9][0-9][0-9][a-z][a-z] ', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+rbr', text) != []:
            model = re.findall('[0-9]+rbr', text)[0]
            brand = 'Rolex'
        
        elif re.findall('[0-9]+ln', text) != []:
            model = re.findall('[0-9]+ln', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+lb', text) != []:
            model = re.findall('[0-9]+lb', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+lv', text) != []:
            model = re.findall('[0-9]+lv', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+ oys', text) != []:
            model = re.findall('[0-9]+ oys', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+[a-z]+ oys', text) != []:
            model = re.findall('[0-9]+[a-z]+ oys', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+ sabr', text) != []:
            model = re.findall('[0-9]+ sabr', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+blnr', text) != []:
            model = re.findall('[0-9]+blnr', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+blro', text) != []:
            model = re.findall('[0-9]+blro', text)[0]
            brand = 'Rolex'

        elif re.findall('[0-9]+tbr', text) != []:
            model = re.findall('[0-9]+tbr', text)[0]
            brand = 'Rolex'
        

    return model, brand


def find_rm_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in rm_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
                brand = 'Richard Mille'
            else:
                pass
    if model=='':
        if re.findall('rm[0-9]+', text) != []:
            model = re.findall('rm[0-9]+', text)[0]
            brand = 'Richard Mille'

        elif re.findall('rm [0-9]+', text) != []:
            model = re.findall('rm [0-9]+', text)[0]
            brand = 'Richard Mille'
            
    return model, brand


def find_ap_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in ap_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
            else:
                pass
    if model=='':
        if re.findall('[0-9]+[a-z][a-z] ', text) != []:
            model = re.findall('[0-9]+[a-z][a-z] ', text)[0]
            brand = 'Audemars Piquet'

        elif re.findall('[0-9]+or', text) != []:
            model = re.findall('[0-9]+or', text)[0]
            brand = 'Audemars Piquet'

        elif re.findall('[0-9]+st', text) != []:
            model = re.findall('[0-9]+st', text)[0]
            brand = 'Audemars Piquet'

        elif re.findall('[0-9]+oo', text) != []:
            model = re.findall('[0-9]+oo', text)[0]
            brand = 'Audemars Piquet'

        elif re.findall('[0-9]+so', text) != []:
            model = re.findall('[0-9]+so', text)[0]
            brand = 'Audemars Piquet'
    
    return model, brand

def find_casio_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in casio_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
                brand = 'Casio'
            else:
                pass
    return model, brand

def find_cartier_model(text):
    model = ''
    brand = ''
    for model_name, name_variations in cartier_models.items():
        for index in name_variations:
            if re.findall(index, text) != []:
                model = model_name
                brand = 'Cartier Santos'
            else:
                pass

    if model=='':
        if re.findall('wssa[0-9]+', text) != []:
            model = re.findall('wssa[0-9]+', text)[0]
            brand = 'Cartier Santos'
    
    return model, brand


def find_model_brand(message):
    model1, brand1 = find_rolex_model(message)
    model2, brand2 = find_pp_model(message)
    model3, brand3 = find_rm_model(message)
    model4, brand4 = find_ap_model(message)
    model5, brand5 = find_casio_model(message)
    model6, brand6 = find_cartier_model(message)

    model_list = [model1, model2, model3, model4, model5, model6]
    brand_list = [brand1, brand2, brand3, brand4, brand5, brand6]
    model = [model_name for model_name in model_list if(model_name != '')]
    brand = [brand_name for brand_name in brand_list if(brand_name != '')]

    if model != []:
        model = model[0]
        brand = brand[0]

    else:
        model = ''
        brand = ''
        
    return model, brand


years = {'2022':['2022', '/2022', '-2022'],
         '2021':['2021', '/2021', '-2021'],
         '2020':['2020', '/2020', '-2020'],
         '2019':['2019', '/2019', '-2019'],
         '2018':['2018', '/2018', '-2018'],
         '2017':['2017', '/2017', '-2017'],
         '2016':['2016', '/2016', '-2016'],
         '2015':['2015', '/2015', '-2015'],
         '2014':['2014', '/2014', '-2014'],
         '2013':['2013', '/2013', '-2013'],
         '2012':['2012', '/2012', '-2012'],
         '2011':['2011', '/2011', '-2011'],
         '2010':['2010', '/2010', '-2010'],
         '2009':['2009', '/2009', '-2009'],
         '2008':['2008', '/2008', '-2008'],
         '2007':['2007', '/2007', '-2007'],
         '2006':['2006', '/2006', '-2006'],
         '2005':['2005', '/2005', '-2005'],
         '2004':['2004', '/2004', '-2004'],
         '2003':['2003', '/2003', '-2003'],
         '2002':['2002', '/2002', '-2002'],
         '2001':['2001', '/2001', '-2001'],
         '2000':['2000', '/2000', '-2000']}

def find_year(text):
    year = ''
    for year_index, year_variations in years.items():
        for index in year_variations:
            if text.find(index) != -1:
                year = year_index
                
    if year == '':
        year = NULL
    return year


conditions = {'new':['new', 'brandnew'],
              'unworn':['unworn'],
              'no adjustment':['no adjustment', 'no adj'],
              'pre-owned':['pre-owned', 'pre owned'],
              'mint':['mint'],
              'used':['used'],
              'without box':['without box', 'w/o box'],
              'with card':['with card'],
              'with paper':['with paper']}

def find_condition(text):
    condition = ''
    for condition_index, condition_variations in conditions.items():
        for index in condition_variations:
            if re.findall(index, text) != []:
                condition = condition_index
            else:
                pass
    return condition


def find_price(message):
    price = ''
    
    if re.findall('[$][0-9]+k', message):
            price = re.findall('[$][0-9]+k', message)[0]
            price = price.replace('$', '')
            price = price.replace('k', '000')

    elif re.findall('[$][0-9]+m', message):
            price = re.findall('[$][0-9]+m', message)[0]
            price = price.replace('$', '')
            price = price.replace('m', '000000')

    elif re.findall(' [$] [0-9]+', message):
            price = re.findall(' [$] [0-9]+', message)[0]
            price = price.replace('$ ', '')
            price = price.replace(' ', '')

    elif re.findall('[0-9]+k[-][$]', message):
            price = re.findall('[0-9]+k[-][$]', message)[0]
            price = price.replace('$', '')
            price = price.replace('-', '')
            price = price.replace('k', '000')
            price = price.replace('m', '000000')

    elif re.findall('[$][0-9]+k usd', message):
            price = re.findall('[$][0-9]+k usd', message)[0]
            price = price.replace('$', '')
            price = price.replace(' usd', '')
            price = price.replace('k', '000')
            price = price.replace('m', '000000')

    elif re.findall(' [0-9]+ usd', message):
            price = re.findall(' [0-9]+ usd', message)[0]
            price = price.replace(' usd', '')
            price = price.replace(' ', '')
            price = price.replace('k', '000')
            price = price.replace('m', '000000')

    elif re.findall(':[0-9]+usd', message):
            price = re.findall(':[0-9]+usd', message)[0]
            price = price.replace('usd', '')
            price = price.replace(':', '')
            price = price.replace('k', '000')
            price = price.replace('m', '000000')

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
            price = price.replace('m', '000000')

    elif re.findall(' [0-9]+ aed', message):
            price = re.findall(' [0-9]+ aed', message)[0]
            price = price.replace(' aed', '')
            price = price.replace(' ', '')
            price = str(int(price)*0.27)
    
    elif re.findall(' [0-9]+[$]', message):        
            price = re.findall(' [0-9]+[$]', message)[0]
            price = price.replace('$', '')
            price = price.replace(' ', '')

    elif re.findall('[0-9]+hkd', message):
            price = re.findall('[0-9]+hkd', message)[0]
            price = price.replace('hkd', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)
        
    elif re.findall('hkd [0-9]+', message):
            price = re.findall('hkd [0-9]+', message)[0]
            price = price.replace('hkd ', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[$][0-9]+', message):
            price = re.findall('hkd[$][0-9]+', message)[0]
            price = price.replace('hkd$', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[:][0-9]+', message):
            price = re.findall('hkd[:][0-9]+', message)[0]
            price = price.replace('hkd:', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[:] [0-9]+', message):
            price = re.findall('hkd[:] [0-9]+', message)[0]
            price = price.replace('hkd: ', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[$][0-9]+', message):
            price = re.findall('hkd[$][0-9]+', message)[0]
            price = price.replace('hkd$', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd [$][0-9]+', message):
            price = re.findall('hkd [$][0-9]+', message)[0]
            price = price.replace('hkd $', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[0-9]+', message):
            price = re.findall('hkd[0-9]+', message)[0]
            price = price.replace('hkd', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+ hkd', message):        
            price = re.findall('[0-9]+ hkd', message)[0]
            price = price.replace(' hkd', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+hkd', message):        
            price = re.findall('[0-9]+hkd', message)[0]
            price = price.replace('hkd', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('hkd[0-9]+ [0-9]+', message):        
            price = re.findall('hkd[0-9]+ [0-9]+', message)[0]
            price = price.replace('hkd', '')
            price = price.replace(' ', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+k hkd', message):        
            price = re.findall('[0-9]+k hkd', message)[0]
            price = price.replace(' hkd', '')
            price = price.replace('k', '000')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+m hkd', message):        
            price = re.findall('[0-9]+m hkd', message)[0]
            price = price.replace(' hkd', '')
            price = price.replace('m', '000000')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[$][0-9]+m hkd', message):        
            price = re.findall('[$][0-9]+m hkd', message)[0]
            price = price.replace(' hkd', '')
            price = price.replace('$', '')
            price = price.replace('m', '000000')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[$][0-9]+hkd', message):        
            price = re.findall('[$][0-9]+hkd', message)[0]
            price = price.replace('hkd', '')
            price = price.replace('$', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[$][0-9]+k hkd', message):        
            price = re.findall('[$][0-9]+k hkd', message)[0]
            price = price.replace(' hkd', '')
            price = price.replace('$', '')
            price = price.replace('k', '0000')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+[$] hkd', message):        
            price = re.findall('[0-9]+[$] hkd', message)[0]
            price = price.replace(' hkd', '')
            price = price.replace('$', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.13)

    elif re.findall('[0-9]+ aed', message):        
            price = re.findall('[0-9]+ aed', message)[0]
            price = price.replace(' aed', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.27)

    elif re.findall('[0-9]+k aed', message):        
            price = re.findall('[0-9]+k aed', message)[0]
            price = price.replace(' aed', '')
            price = price.replace('k', '000')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.27)

    elif re.findall('[0-9]+[€] eur', message):        
            price = re.findall('[0-9]+[€] eur', message)[0]
            price = price.replace('€ eur', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*1.04)

    elif re.findall('[0-9]+ eur', message):        
            price = re.findall('[0-9]+ eur', message)[0]
            price = price.replace(' eur', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*1.04)

    elif re.findall('[0-9]+[€]', message):        
            price = re.findall('[0-9]+[€]', message)[0]
            price = price.replace('€', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*1.04)

    elif re.findall('[0-9]+eur', message):        
            price = re.findall('[0-9]+eur', message)[0]
            price = price.replace('eur', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*1.04)

    elif re.findall('[0-9]+k eur', message):        
            price = re.findall('[0-9]+k eur', message)[0]
            price = price.replace(' eur', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = price.replace('k', '000')
            price = str(int(price)*1.04)
        
    elif re.findall('[€] [0-9]+', message):        
            price = re.findall('[€] [0-9]+', message)[0]
            price = price.replace('€ ', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*1.04)

    elif re.findall('[0-9]+cny', message):        
            price = re.findall('[0-9]+cny', message)[0]
            price = price.replace('cny', '')
            # price = json.loads(requests.request("GET", "https://api.apilayer.com/fixer/convert?to=HKD&from=USD&amount=" + price, headers = {"apikey": "bY7HCCHbIrP37ukL0gBgNEjkKbN0UVKr"}, data = {}).text)['result']
            price = str(int(price)*0.15)

    elif re.findall('[$][0-9]+', message):
            price = re.findall('[$][0-9]+', message)[0]
            price = price.replace('$', '')

    else:
            pass

    if price == '':
            price = NULL

    else:
            price = int(round(float(price), 0))
            
    return price