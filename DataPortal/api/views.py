from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Count
from Base.models import (
    Topic,
    Category
)

from DataPortal.serializers import (
    TopicSerializers,
    CategorySerializers,
)

@api_view(['GET'])
def topic_lists(request):
    if request.method == 'GET':
        topics = Topic.objects.filter(is_dashboard=True, is_deleted=False).annotate(category_count=Count('categories')).select_related()
        serializer = TopicSerializers(topics, many=True)
        import time
        time.sleep(1)
        return Response(serializer.data)
    

@api_view(['GET'])
def category_with_indicator(request, id):
    try:
        topic = Topic.objects.get(pk = id)
    except Topic.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        categories = Category.objects.filter(topic =  topic).select_related()
        serializer = CategorySerializers(categories, many=True)
        import time
        time.sleep(1)
        return Response(serializer.data)