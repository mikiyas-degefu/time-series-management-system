from rest_framework import serializers
from .models import (
  Topic,
  Category
)


class TopicSerializers(serializers.ModelSerializer):
  category_count = serializers.IntegerField(read_only=True)
  class Meta:
    model = Topic
    fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
  indicator_count = serializers.IntegerField(read_only=True)
  class Meta:
    model = Category
    fields = '__all__'

    