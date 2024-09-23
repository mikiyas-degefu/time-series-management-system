from rest_framework import serializers
from .models import Component, DashboardIndicator
from Base.models import Indicator, AnnualData


class IndicatorSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Indicator
        fields = ('id', 'title_ENG', 'title_AMH',)


class AnnualDataSerializers(serializers.ModelSerializer):
    for_datapoint = serializers.SlugRelatedField(read_only=True, slug_field='year_GC')
    class Meta:
        model = AnnualData
        fields = '__all__'



class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = '__all__'


class DashboardIndicatorSerializer(serializers.ModelSerializer):
    component = ComponentSerializer()
    indicator = IndicatorSerializers(many=True, read_only=True)

    class Meta:
        model = DashboardIndicator
        fields = '__all__'
