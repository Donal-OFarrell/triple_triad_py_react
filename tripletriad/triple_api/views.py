import pprint 
from django.shortcuts import render
from .tt_for_api import Card # import tt game objects 
from .models import TripleTriadUpdated

from django.http import HttpResponse, JsonResponse
from django.core import serializers

import json
import random 


def onLoadCpuCardData(request):
    ''' retrieves 5 random cards of powers 5 to 9 for the CPU to use as it's deck'''
    # retrieve cards of powers 5 to 9 
    five_nine_cards = list(TripleTriadUpdated.objects.filter(card_type__gte=5, card_type__lte=9).values_list('id','card_name','north_pole', 'west_pole', 'east_pole', 'south_pole', 'card_type'))
    random.shuffle(five_nine_cards) # shuffle the result 
    five_cards = five_nine_cards[:5] # take 5 from the shuffled result 
    # -> and return 
    return HttpResponse(five_cards) 



