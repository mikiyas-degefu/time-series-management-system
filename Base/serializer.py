from rest_framework import serializers
from .models import (
  Category
)

class CategorySerializers(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name_ENG', 'name_AMH', 'topic', 'is_dashboard_visible']
    