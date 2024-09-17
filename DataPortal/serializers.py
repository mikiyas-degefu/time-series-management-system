from rest_framework import serializers
from Base.models import (
    Topic,
    Indicator,
    Category,
)

class TopicSerializers(serializers.ModelSerializer):
    category_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Topic
        exclude = ('updated', 'created')


class IndicatorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ('id', 'title_ENG', 'title_AMH', 'for_category', 'measurement_units', 'parent')


class CategorySerializers(serializers.ModelSerializer):
    indicators = IndicatorSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'