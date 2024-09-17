from rest_framework import serializers
from Base.models import (
    Topic,
)

class TopicSerializers(serializers.ModelSerializer):
    category_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Topic
        exclude = ('updated', 'created')