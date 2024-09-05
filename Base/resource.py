from import_export import resources
from .models import (
    Topic
)
class TopicResource(resources.ModelResource):

    class Meta:
        model = Topic