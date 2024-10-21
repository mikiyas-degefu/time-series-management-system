from DashBoard.serializer import( 
    ComponentSerializer, 
    DashboardIndicatorSerializer,
    AnnualDataSerializers
    )

from django.http import HttpResponse     

from Base.models import (
    AnnualData , Indicator
)
from DashBoard.models import Component, DashboardIndicator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response

@api_view(['GET'])
def components(request):
    if request.method == 'GET':
        dashboard_indicators = DashboardIndicator.objects.all().first()
        indicator_list = dashboard_indicators.indicator.all()
        if(not dashboard_indicators.component.is_range):
            annual_data = AnnualData.objects.filter(indicator__in = indicator_list, for_datapoint__year_EC = 2017)
            annual_data_serializer = AnnualDataSerializers(annual_data, many=True)
        dashboard_indicators_serializer = DashboardIndicatorSerializer(dashboard_indicators)

        context = {
            'col' : dashboard_indicators_serializer.data,
            'annual_data' : annual_data_serializer.data
        }
        return Response(context)





@api_view(['GET'])
def single_indicator_data(request, id, year):
    if request.method == 'GET':
        try:
            indicator = Indicator.objects.get(id=id)
            annual_data = AnnualData.objects.get(indicator=indicator, for_datapoint__year_EC=year)

            serializer = AnnualDataSerializer(annual_data)  # Serialize the annual_data object

            return Response(serializer.data)
        except Indicator.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except AnnualData.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)