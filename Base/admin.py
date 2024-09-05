from django.contrib import admin
from .models import *
from .resource import TopicResource
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class TopicAdmin(ImportExportModelAdmin):
    resource_class = [TopicResource]

admin.site.register(Topic, TopicAdmin)

admin.site.register(Document)
admin.site.register(Category)
admin.site.register(Indicator)

admin.site.register(DataPoint)
admin.site.register(Indicator_Point)
admin.site.register(Quarter)

admin.site.register(Month)
admin.site.register(QuarterData)
admin.site.register(MonthData)

admin.site.register(AnnualData)
admin.site.register(Source)