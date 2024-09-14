from rest_framework import serializers
from .models import (
  Topic,
  Category,
  Indicator,
  AnnualData,
  DataPoint,
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


class IndicatorSerializers(serializers.ModelSerializer):
  class Meta:
    model = Indicator
    fields = '__all__'


class AnnualDataSerializers(serializers.ModelSerializer):
  class Meta:
    model = AnnualData
    fields = '__all__'


class DataPointSerializers(serializers.ModelSerializer):
  class Meta:
    model = DataPoint
    fields = ['id','year_EC','year_GC']

    