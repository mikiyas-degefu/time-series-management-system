from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
from Base.models import (
    Topic
)

from DataPortal.serializers import (
    TopicSerializers,
)

@api_view(['GET'])
def topic_lists(request):
    if request.method == 'GET':
        topics = Topic.objects.filter(is_dashboard=True, is_deleted=False).annotate(category_count=Count('categories')).select_related()
        serializer = TopicSerializers(topics, many=True)
        return Response(serializer.data)