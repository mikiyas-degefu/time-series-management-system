from import_export import resources, fields
from import_export.formats.base_formats import XLS
import tablib
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.results import RowResult, Result
from .models import *
#############Import export Model Resources################


class TopicResource(resources.ModelResource):
    class Meta:
        model = Topic
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
        exclude = ( 'id', 'created_at', 'is_deleted','is_dashboard_visible',)
        import_id_fields = ('name_ENG', 'name_AMH')

class TagResource(resources.ModelResource):
    class Meta:
        model = Tag

class IndicatorResource(resources.ModelResource):
    for_category = fields.Field(
        column_name='for_category',
        attribute='for_category',
        widget=ManyToManyWidget(Category, field='name_ENG', separator=','),
        saves_null_values=True,
    )
    
    parent = fields.Field(
        column_name='parent',
        attribute='parent',
        widget=ForeignKeyWidget(Indicator, field='id'),
        saves_null_values=True,
    )

    tags = fields.Field(
        column_name='tags',
        attribute='tags',
        widget=ManyToManyWidget(Tag, field='title',separator=','),
        saves_null_values=True,
    )

    class Meta:
        model = Indicator
        import_id_fields = ('id',)             
        skip_unchanged = False                 
        report_skipped = True  
        use_bulk = False               
    
    def after_import_row(self, row, row_result, **kwargs):
        instance = row_result.instance
        if instance:
            instance.generate_code()
            instance.save(update_fields=['code'])

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
        widget=ForeignKeyWidget(Indicator, field='code'),
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
        import_id_fields = ('indicator', 'for_datapoint')

class AnnualDataWideResource(resources.ModelResource):
    indicator = fields.Field(
        column_name='indicator',
        attribute='indicator',
        widget=ForeignKeyWidget(Indicator, 'code')  # Use the 'code' field instead of ID
    )
    for_datapoint = fields.Field(
        column_name='for_datapoint',
        attribute='for_datapoint',
        widget=ForeignKeyWidget(DataPoint, 'year_EC')  # Adjust if needed
    )
    performance = fields.Field(
        column_name='performance',
        attribute='performance'
    )

    class Meta:
        model = AnnualData
        skip_unchanged = True
        report_skipped = True
        use_bulk = True
        import_id_fields = ('indicator', 'for_datapoint',)
        fields = ('indicator', 'for_datapoint', 'performance')

    def get_instance(self, instance_loader, row):
        indicator_code = row.get('indicator')
        year_ec = row.get('for_datapoint')
        if not indicator_code or not year_ec:
            return None

        try:
            indicator = Indicator.objects.get(code=indicator_code)
            datapoint = DataPoint.objects.get(year_EC=year_ec)
            return AnnualData.objects.get(indicator=indicator, for_datapoint=datapoint)
        except (Indicator.DoesNotExist, DataPoint.DoesNotExist, AnnualData.DoesNotExist):
            return None
        
    def before_import_row(self, row, **kwargs):
        if row.get('for_datapoint') is None:
               pass
        year = row.get("for_datapoint")
        if year:
            datapoint, created = DataPoint.objects.get_or_create(year_EC=year)
            row["for_datapoint"] = datapoint.year_EC

    def import_data(self, dataset, dry_run=False, raise_errors=False, use_transactions=None, **kwargs):
        from tablib import Dataset
        result_dataset = Dataset(headers=['indicator', 'for_datapoint', 'performance'])

        new_count = 0
        updated_count = 0

        for row_number, row in enumerate(dataset.dict, start=1):
            indicator_key = row.get('indicator')
            if not indicator_key:
                continue

            try:
                indicator = Indicator.objects.get(code=indicator_key)
            except Indicator.DoesNotExist:
                continue

            for year, value in row.items():
                if year == 'indicator' or value in [None, '']:
                    continue

                try:
                    datapoint, created = DataPoint.objects.get_or_create(year_EC=year)
                except DataPoint.DoesNotExist:
                    continue

                try:
                    performance = float(value)
                except ValueError:
                    continue

                result_dataset.append([indicator_key, year, performance])

                if not dry_run:
                    obj, created = AnnualData.objects.update_or_create(
                        indicator=indicator,
                        for_datapoint=datapoint,
                        defaults={'performance': performance}
                    )
                    if created:
                        new_count += 1
                    else:
                        updated_count += 1

        if dry_run:
            return super().import_data(result_dataset, dry_run=True, raise_errors=raise_errors, **kwargs)

        result = Result()
        result.rows = []
        result.totals = {
            'new': new_count,
            'update': updated_count,
            'skip': 0,
            'failed': 0,
            'delete': 0,
        }
        result.diff_headers = ['indicator', 'for_datapoint', 'performance']

        return result

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
        import_id_fields = ('indicator', 'for_datapoint', 'for_quarter' )

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
        widget=ForeignKeyWidget(Month, field='number'),
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
        import_id_fields = ('indicator', 'for_datapoint', 'for_month' )


#############Handle uploaded excel files################

def handle_uploaded_Topic_file(file):
    try:
        resource = TopicResource()
        dataset = tablib.Dataset()

        imported_data = dataset.load(file.read())
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows=True)
        
        if not result.has_errors():
            return True, imported_data, result
        else:
            return False, imported_data, result
    except Exception as e:
        # Ensure variables are initialized in case of an exception
        imported_data = None
        result = None
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
        imported_data = None
        result = None
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
    
def handle_uploaded_Quarter_file(file):
    try:
        resource  = QuarterDataResource()
        dataset = tablib.Dataset()
        imported_data = dataset.load(file.read())

        data_set = []
        
        for item in imported_data.dict:
            for i,key in enumerate(item):
                   if item['year'] != None and key != "year" and key != "quarter":
                       data_set.append((
                          key.strip() , #indicator 
                           item['quarter'], #Quarter number
                           item['year'], #Year
                           item[key], #Performance
                           None, #Target
                           ))

        data_set_table = tablib.Dataset(*data_set, headers=['indicator', 'for_quarter', 'for_datapoint', 'performance', 'target'])
        result = resource.import_data(data_set_table, dry_run=True)
        return True, data_set_table, result
    except Exception as e:
        return False, '', ''
    
def handle_uploaded_Month_file(file):
    try:
        resource  = MonthDataResource()
        dataset = tablib.Dataset()
        imported_data = dataset.load(file.read())

        data_set = []
        
        for item in imported_data.dict:
            for i,key in enumerate(item):
                   if item['year'] != None and key != "year" and key != "month":
                       data_set.append((
                           key.strip() , #indicator 
                           item['month'], #Month number
                           item['year'], #Year
                           item[key], #Performance
                           None, #Target
                           ))

        data_set_table = tablib.Dataset(*data_set, headers=['indicator', 'for_month', 'for_datapoint', 'performance', 'target'])
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
        elif type == 'yearly':
            resource = AnnualDataResource()
        elif type == 'quarterly':
            resource = QuarterDataResource()
        elif type == 'monthly':
            resource = MonthDataResource()
        result = resource.import_data(imported_data, dry_run=True, collect_failed_rows = True)
        
        if not result.has_errors():
            resource.import_data(imported_data, dry_run=False)  # Actually import now
            return True, f"Data imported successfully: {len(imported_data)} records imported."
        else:
            return False, f"Error importing data: Please review your Document."
    except Exception as e:
         return False, f"Error importing data: Please review your Document."