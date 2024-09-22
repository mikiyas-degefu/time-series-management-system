from DashBoard.serializer import ComponentSerializer
from DashBoard.models import Component
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def components(request):
    if request.method == 'GET':
        components = Component.objects.all()
        serializer = ComponentSerializer(components, many=True)
        return Response(serializer.data)

