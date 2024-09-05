from django.contrib import admin
from .models import *
from .resource import(
    TopicResource,
)


from import_export.admin import ImportExportModelAdmin

class TopicAdmin(ImportExportModelAdmin):
    resource_classes = [TopicResource]

admin.site.register(Topic, TopicAdmin)

