from rest_framework import serializers
from Base.models import (
    Topic,
    Indicator,
    Category,
    AnnualData
)

class TopicSerializers(serializers.ModelSerializer):
    category_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Topic
        exclude = ('updated', 'created')

class AnnualDataSerializers(serializers.ModelSerializer):
    for_datapoint = serializers.SlugRelatedField(read_only=True, slug_field='year_GC')
    class Meta:
        model = AnnualData
        fields = '__all__'

class IndicatorSerializers(serializers.ModelSerializer):
    annual_data = serializers.SerializerMethodField()

    def get_annual_data(self, obj):
        annual = AnnualData.objects.filter(indicator = obj).order_by('for_datapoint__year_EC').reverse()[:10]
        serializer = AnnualDataSerializers(annual, many=True)
        return serializer.data
    
    class Meta:
        model = Indicator
        fields = ('id', 'title_ENG', 'title_AMH', 'for_category', 'measurement_units', 'parent', 'annual_data')


class CategorySerializers(serializers.ModelSerializer):
    indicators = IndicatorSerializers(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'