import imp
from models import *

# def my_scheduled_job():
#   pass

print(Listing.objects.filter(watch_model='5164r').order_by('-id')[:100].values('watch_price'))

l = list(Listing.objects.filter(watch_model='5164r').order_by('-id')[:100].values('watch_price'))

s = set([d['watch_price'] for d in l if 'watch_price' in d])