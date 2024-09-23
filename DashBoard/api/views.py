from DashBoard.serializer import( 
    ComponentSerializer, 
    DashboardIndicatorSerializer,
    AnnualDataSerializers
    
    )

from Base.models import (
    AnnualData
)
from DashBoard.models import Component, DashboardIndicator
from rest_framework.decorators import api_view
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

