from import_export import resources
from .models import (
    Topic,
)

class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
        exclude = ('created', 'icon', 'rank', 'updated', 'is_deleted')
        import_order = ('id', 'title_ENG', 'title_AMH', 'is_dashboard', )
