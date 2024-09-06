from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from Base.models import (
    Category,
    Indicator
)
@api_view(['GET'])
def get_indicators(request,id):
   '''
   filter Indicator by category id with children
   '''
   indicators_list = []
   indicators = Indicator.objects.filter(for_category__id = id, is_deleted = False).select_related()
   for i in indicators:
      indicators_list.append({
         'id' : i.id,
         'title_ENG' : i.title_ENG,
         'title_AMH' : i.title_AMH,
         'composite_key' : i.composite_key,
         'parent_id' : i.parent.id if i.parent else None,
         'for_category' : list(i.for_category.filter().values_list('name_ENG', flat=True)),
         'measurement_units' : i.measurement_units,
         'kpi_characteristics' : i.kpi_characteristics,
         'is_dashboard_visible' : i.is_dashboard_visible,
         'is_public' : i.is_public,
      })
   context ={
      'indicators' : indicators_list
   }
   return Response(context)
