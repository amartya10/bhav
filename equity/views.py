from django.shortcuts import render
from . import bse_utils
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers,pagination,generics
from rest_framework.views import APIView

from django.views.generic.list import ListView

from rest_framework.exceptions import APIException
from rest_framework import status
import csv

import logging
# Create your views here.
def equity_list(requests):
    equities_list = bse_utils.get()
    equities = {'equities':equities_list}
    return  JsonResponse(equities)

class EquitySerializers(serializers.Serializer):
    SC_NAME = serializers.CharField()
    SC_CODE = serializers.CharField()
    SC_GROUP = serializers.CharField()
    SC_TYPE = serializers.CharField()
    HIGH = serializers.FloatField()
    OPEN = serializers.FloatField()
    CLOSE = serializers.FloatField()
    LOW = serializers.FloatField()
    LAST = serializers.FloatField()
    PREVCLOSE = serializers.FloatField()
    NO_OF_SHRS = serializers.FloatField()
    NO_TRADES = serializers.FloatField()
    NET_TURNOV = serializers.FloatField()

class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'

class NotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = ('bad_request.')
    default_code = 'bad_request'


class EquitiesView(APIView):
    
    def get(self,request,*args,**kwargs):
        result = {}
        date = self.kwargs.get('date')
        query = self.request.query_params.get('q')
        page = self.request.query_params.get('page')
        limit = self.request.query_params.get('limit')
        if date != None:
            try :
               date =  datetime.strptime(date,"%d-%m-%Y")
            except Exception as e:
                data = { 'error' : 'URL date format incorrect dd-mm-yyyy'}
                raise NotFound(data)
        result = bse_utils.get(date,query,page,limit)
        return JsonResponse(result)
    

class  EquityExport(APIView):

    def post(self,request,*args,**kwargs):

        csv_headers = ['SC_CODE','SC_NAME',\
        'SC_GROUP','SC_TYPE','OPEN','HIGH',\
        'LOW','CLOSE','LAST','PREVCLOSE',\
        'NO_TRADES','NO_OF_SHRS','NET_TURNOV']

        response = HttpResponse(content_type='application/csv')
        headers={'Content-Disposition': 'attachment; filename=response.csv'},
        writer = csv.writer(response)

        writer.writerow(csv_headers)
        date = self.kwargs.get('date')
        if date != None:
            date =  datetime.strptime(date,"%d-%m-%Y")
        else:
            date = bse_utils.latest()

        dateFormated = date.strftime(bse_utils.DATE_FORMAT)
        print(dateFormated)

        scripts = request.data
        for script in scripts:
            script  = f'{bse_utils.SC_KEY_FORMAT}{script}'
            scData = bse_utils.getScript(script,dateFormated)
            listData = []
            for csv_header  in csv_headers:
                listData.append(scData[csv_header])
            writer.writerow(listData)
        return response
