from django.contrib import admin
from .models import *
from .resource import(
    TopicResource,
    CategoryResource,
    IndicatorResource,
    AnnualDataResource,
    DataPointResource,
    QuarterDataResource,
    MonthDataResource
)


from import_export.admin import ImportExportModelAdmin


admin.site.register(Video)
class TopicAdmin(ImportExportModelAdmin):
    list_display = ('title_ENG', 'title_AMH', 'created', 'is_dashboard', 'is_deleted', 'rank')

admin.site.register(Topic, TopicAdmin)

admin.site.register(ProjectInitiatives)
admin.site.register(SubProject)


class DocumentAdmin(ImportExportModelAdmin):
    list_display = ('title_ENG', 'title_AMH', 'topic', 'file')

admin.site.register(Document, DocumentAdmin)


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name_ENG', 'name_AMH', 'topic', 'is_dashboard_visible', 'is_deleted')
    search_fields = ['name_ENG', 'name_AMH', 'topic__title_ENG']

admin.site.register(Category, CategoryAdmin)



class IndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [IndicatorResource]
    list_display = ('title_ENG', 'title_AMH', 'kpi_characteristics', 'is_dashboard_visible', 'is_public')
    filter_horizontal = ('for_category', )
    search_fields = ['title_ENG', 'title_AMH']

admin.site.register(Indicator, IndicatorAdmin)



class DataPointAdmin(ImportExportModelAdmin):
    resource_classes = [DataPointResource]
    list_display = ('year_EC', 'year_GC',)

admin.site.register(DataPoint,  DataPointAdmin)



class AnnualDataAdmin(ImportExportModelAdmin):
    resource_classes = [AnnualDataResource]
    list_display = ('for_datapoint' , 'performance','target' , )
    list_filter = ('indicator' , 'for_datapoint')
    search_fields = ('indicator' , 'for_datapoint')

    autocomplete_fields = ['indicator']

admin.site.register(AnnualData,  AnnualDataAdmin)





class QuarterDataAdmin(ImportExportModelAdmin):
    resource_classes = [QuarterDataResource]
    list_display = ('for_datapoint' , 'for_quarter' , 'performance','target' , )
    list_filter = ('indicator' , 'for_datapoint')
    search_fields = ('indicator' , 'for_datapoint')

    autocomplete_fields = ['indicator']

admin.site.register(QuarterData,  QuarterDataAdmin)


class MonthDataAdmin(ImportExportModelAdmin):
    resource_classes = [MonthDataResource]
    list_display = ('for_datapoint' , 'performance','target' , )
    list_filter = ('indicator' , 'for_datapoint')
    search_fields = ('indicator' , 'for_datapoint')

    autocomplete_fields = ['indicator']

admin.site.register(MonthData,  MonthDataAdmin)


admin.site.register(Quarter)
admin.site.register(Month)


