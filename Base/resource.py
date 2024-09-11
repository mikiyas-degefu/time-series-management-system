from import_export import resources, fields
import datetime
from import_export.formats.base_formats import XLS
import tablib
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import (
    Topic,
    Category,
    Indicator,
    AnnualData,
    DataPoint,
    QuarterData,
    MonthData,
    Month,
    Quarter,
)

#############Import export Model Resources################


class TopicResource(resources.ModelResource):

    class Meta:
        model = Topic
        skip_unchanged = True
        report_skipped = True
        exclude = ( 'id', 'updated', 'created', 'is_deleted', 'rank', 'icon', 'is_dashboard')
        import_id_fields = ('title_ENG', 'title_AMH')


class CategoryResource(resources.ModelResource):
    topic = fields.Field(
        column_name='topic',
        attribute='topic',
        widget=ForeignKeyWidget(Topic, field='title_ENG'),
        saves_null_values = True,
        )


    def before_import_row(self, row, **kwargs):
            if row.get('topic') is None:
               pass
            else :
               topic_name = row["topic"]
               Topic.objects.get_or_create(title_ENG=topic_name, defaults={"title_ENG": topic_name, "title_AMH":topic_name})
    
    class Meta:
        model = Category
        report_skipped = True
        skip_unchanged = True
        exclude = ( 'id', 'created_at', 'is_deleted','is_dashboard_visible', )
        import_id_fields = ('name_ENG', 'name_AMH','topic')


class IndicatorResource(resources.ModelResource):    
    for_category = fields.Field(
        column_name='for_category',
        attribute='for_category',
        widget=ManyToManyWidget(Category, field='name_ENG', separator='|'),
        saves_null_values = True,
    )

    
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Indicator, field='id'),
        saves_null_values = True,
    )


    class Meta:
        model = Indicator
        report_skipped = True
        skip_unchanged = True
        exclude = ( 'created_at', 'is_deleted', 'composite_key','op_type')



class DataPointResource(resources.ModelResource):

    class Meta:
        model = DataPoint
        skip_unchanged = True
        report_skipped = True
        exclude = ( 'id','created_at', 'updated_at')
        import_id_fields = ('year_EC', 'year_GC')



class AnnualDataResource(resources.ModelResource):    
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field='composite_key'),
        saves_null_values = True,
    ) 
    

    for_datapoint = fields.Field(
        column_name='for_datapoint',
        attribute='for_datapoint',
        widget=ForeignKeyWidget(DataPoint, field='year_EC'),
        saves_null_values = True,
    )


    class Meta:
        model = AnnualData
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        exclude = ( 'id', 'created_at')
        import_id_fields = ('indicator', 'for_datapoint', 'performance', 'target')


class QuarterDataResource(resources.ModelResource):    
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field='composite_key'),
        saves_null_values = True,
    ) 


    for_quarter = fields.Field(
        column_name='for_quarter',
        attribute='for_quarter',
        widget=ForeignKeyWidget(Quarter, field='number'),
        saves_null_values = True,
    )
    

    for_datapoint = fields.Field(
        column_name='for_datapoint',
        attribute='for_datapoint',
        widget=ForeignKeyWidget(DataPoint, field='year_EC'),
        saves_null_values = True,
    )


    class Meta:
        model = QuarterData
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        exclude = ( 'id', 'created_at')
        import_id_fields = ('indicator', 'for_datapoint', 'for_quarter' ,'performance', 'target')



class MonthDataResource(resources.ModelResource):    
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, field='composite_key'),
        saves_null_values = True,
    ) 


    for_month = fields.Field(
        column_name='for_month',
        attribute='for_month',
        widget=ForeignKeyWidget(Quarter, field='number'),
        saves_null_values = True,
    )
    

    for_datapoint = fields.Field(
        column_name='for_datapoint',
        attribute='for_datapoint',
        widget=ForeignKeyWidget(DataPoint, field='year_EC'),
        saves_null_values = True,
    )


    class Meta:
        model = MonthData
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        exclude = ( 'id', 'created_at')
        import_id_fields = ('indicator', 'for_datapoint', 'for_month' ,'performance', 'target')


#############Handle uploaded excel files################

def handle_uploaded_Topic_file(file):
    try:
        resource  = TopicResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    

def handle_uploaded_Indicator_file(file):
    try:
        resource  = IndicatorResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result
    

def handle_uploaded_Category_file(file):
    try:
        resource  = CategoryResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
         return False, imported_data, result

    
def handle_uploaded_Annual_file(file):
    try:
        resource  = AnnualDataResource()
        dataset = tablib.Dataset()
        imported_data = dataset.load(file.read())

        data_set = []
        
        for item in imported_data.dict:
            for i,key in enumerate(item):
                if i != 0 and item['indicator'] != None:
                    data_set.append((
                        item['indicator'].strip(), #indicator key
                        key,  #year lists
                        item[key],  #performance
                        None, #target
                    ))
          

        data_set_table = tablib.Dataset(*data_set, headers=['indicator', 'for_datapoint', 'performance', 'target'])
        result = resource.import_data(data_set_table, dry_run=True)
        return True, data_set_table, result
    except Exception as e:
        return False, '', ''
    



############# Handle uploaded excel files and take action ################
def confirm_file(imported_data, type):
    try:
        if type == 'topic':
            resource  = TopicResource()
        elif type == 'category':
            resource = CategoryResource()
        elif type == 'indicator':
            resource = IndicatorResource()
        elif type == 'annual_data':
            resource = AnnualDataResource()
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            resource.import_data(imported_data, dry_run=False)  # Actually import now
            return True, f"Data imported successfully: {len(imported_data)} records imported."
        else:
            return False, f"Error importing data: Please review your Document."
    except Exception as e:
         return False, f"Error importing data: Please review your Document."