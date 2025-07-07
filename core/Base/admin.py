from django.contrib import admin
from .models import *
from .resource import *
from import_export.admin import ImportExportModelAdmin



class TopicAdmin(ImportExportModelAdmin):
    list_display = ('title_ENG', 'title_AMH', 'created', 'is_dashboard', 'rank')
    resource_classes = [TopicResource]
admin.site.register(Topic,TopicAdmin)

class DocumentAdmin(ImportExportModelAdmin):
    list_display = ('title_ENG', 'title_AMH', 'topic', 'file')

admin.site.register(Document, DocumentAdmin)

class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('name_ENG', 'name_AMH', 'topic', 'is_dashboard_visible', 'is_deleted')
    search_fields = ['name_ENG', 'name_AMH', 'topic__title_ENG']

admin.site.register(Category, CategoryAdmin)


class TagAdmin(ImportExportModelAdmin):
    resource_classes = [TagResource]
    list_display = ('title',)
    search_fields = ('title',)

admin.site.register(Tag, TagAdmin)

class IndicatorAdmin(ImportExportModelAdmin):
    resource_classes = [IndicatorResource]
    list_display = ('code','title_ENG', 'title_AMH','measurement_units','kpi_characteristics','frequency', 'status' ,'is_dashboard_visible', 'is_public')
    filter_horizontal = ('for_category', )
    search_fields = ['code','title_ENG', 'title_AMH']

admin.site.register(Indicator, IndicatorAdmin)



class DataPointAdmin(ImportExportModelAdmin):
    resource_classes = [DataPointResource]
    list_display = ('year_EC', 'year_GC',)

admin.site.register(DataPoint,  DataPointAdmin)



class AnnualDataAdmin(ImportExportModelAdmin):
    resource_classes = [AnnualDataWideResource]
    list_display = ('indicator_title', 'for_datapoint', 'performance', 'target')
    list_filter = ('indicator' , 'for_datapoint')
    search_fields = ('indicator' , 'for_datapoint')

    autocomplete_fields = ['indicator']
    list_editable = ('performance','for_datapoint')

    def indicator_title(self, obj):
        return obj.indicator.title_ENG
    
    def year(self, obj):
        return obj.for_datapoint.year_EC

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
admin.site.register(Video)
admin.site.register(ProjectInitiatives)
admin.site.register(SubProject)

