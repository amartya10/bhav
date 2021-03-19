from django.shortcuts import render
from . import bse_utils
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from rest_framework import serializers,pagination,generics
from rest_framework.views import APIView
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
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class EquitiesView(generics.ListAPIView):
    serializer_class = EquitySerializers
    pagination_class = LargeResultsSetPagination
    def get_queryset(self):
        date_str = self.request.query_params.get('date')
        try :
            if date_str:
                date = datetime.strptime(date_str,"%Y%m%d")
                return bse_utils.get(date)
        
        except Exception as e:
            print('date not format')
        return bse_utils.get()

