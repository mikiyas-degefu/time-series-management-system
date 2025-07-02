from django.db import models
from fontawesome_5.fields import IconField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import json

# Create your models here.

class Topic(models.Model):
    title_ENG = models.CharField(max_length=300, unique = True)
    title_AMH = models.CharField(max_length=300, null = True)
    is_dashboard = models.BooleanField(default = False)
    is_mobile_dashaboard_overview = models.BooleanField(default = False)
    rank = models.IntegerField(null=True, blank=True)
    icon = IconField()
    image = models.FileField(upload_to="media/topic-image" , null=True, blank=True)
    image_icons = models.FileField(upload_to="media/image_icons" , null=True, blank=True)
    background_image = models.FileField(upload_to="media/background_image" , null=True, blank=True)
    updated =  models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title_ENG
    
    def get_document_lists(self):
        return Document.objects.filter(topic = self)
    class Meta:
        ordering = ['rank'] #Oldest First    

class Document(models.Model):
    # Responsible to store file documents
    title_ENG = models.CharField(max_length=300, unique = True)
    title_AMH = models.CharField(max_length=300, null = True)
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL)
    file= models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title_ENG

class Category(models.Model):
    name_ENG = models.CharField(max_length=300, unique = True)
    name_AMH = models.CharField(max_length=300, unique = True)
    is_dashboard_visible = models.BooleanField(default = False)
    topic = models.ForeignKey(Topic, null=True, blank=True, on_delete=models.SET_NULL, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name_ENG

class Indicator(models.Model):
    KPI_CHARACTERISTIC_CHOICES = [
        ('inc', 'Increasing'),
        ('dec', 'Decreasing'),
        ('const', 'Constant'),
    ]

    title_ENG = models.CharField(max_length=300) 
    title_AMH = models.CharField(max_length=300 , null=True, blank=True)
    composite_key = models.CharField(max_length=300, unique = True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    for_category = models.ManyToManyField(Category, related_name='indicators')
    measurement_units = models.CharField(max_length=50, null=True, blank=True, default="")
    kpi_characteristics = models.CharField(
        max_length=10,
        choices=KPI_CHARACTERISTIC_CHOICES,
        default="inc"
    )
    is_dashboard_visible = models.BooleanField(default = False)
    is_public = models.BooleanField(default = True)
    is_deleted = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def create_composite_key(self, *args, **kwargs):
        self.composite_key = str(self.title_ENG.replace(" ","").replace("/","").replace("&","")) +  str(self.id)
        super(Indicator, self).save(*args, **kwargs)
    
    def create_data_value(self):
        #Annual Data
        obj = AnnualData()
        year = DataPoint.objects.order_by('-year_EC').first()
        obj.for_datapoint = year
        obj.performance = 0
        obj.indicator = self
        obj.save()

        #Quarterly Data
        obj = QuarterData()
        year = DataPoint.objects.order_by('-year_EC').first()
        quarter = Quarter.objects.order_by('-number').first()
        obj.for_quarter = quarter
        obj.for_datapoint = year
        obj.performance = 0
        obj.indicator = self
        obj.save()
    
    

    def get_previous_year_performance(self, year=None, quarter=None, month=None):
        if year:
            previous_year = str(int(year) - 1)
            try:
                current_year_plan = None
                previous_year_plan = None

                if month and year:
                    try:
                        current_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                        previous_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif quarter and year:
                    try:
                        current_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                        previous_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif year:
                    try:
                        current_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=year,
                            indicator=self
                        ).first()
                        previous_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                if (
                    previous_year_plan and current_year_plan and
                    previous_year_plan.performance is not None and
                    current_year_plan.performance is not None and
                    previous_year_plan.performance != 0
                ):
                    performance_change = current_year_plan.performance - previous_year_plan.performance
                    performance_change_percent = (performance_change / previous_year_plan.performance) * 100

                    if self.kpi_characteristics == 'inc':
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                    elif self.kpi_characteristics == 'dec':
                        return {
                            "change": round(-performance_change, 1),
                            "percent": round(-performance_change_percent, 1)
                        }
                    else:
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                else:
                    return None

            except Exception:
                return None

        return None
    
    def get_indicator_value_5_years_ago(self, year=None, quarter=None, month=None):
        if year:
            previous_year = str(int(year) - 5)
            try:
                current_year_plan = None
                previous_year_plan = None

                if month and year:
                    try:
                        current_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                        previous_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif quarter and year:
                    try:
                        current_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                        previous_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif year:
                    try:
                        current_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=year,
                            indicator=self
                        ).first()
                        previous_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                
                if (
                    previous_year_plan and current_year_plan and
                    previous_year_plan.performance is not None and
                    current_year_plan.performance is not None and
                    previous_year_plan.performance != 0
                ):
                    performance_change = current_year_plan.performance - previous_year_plan.performance
                    performance_change_percent = (performance_change / previous_year_plan.performance) * 100

                    if self.kpi_characteristics == 'inc':
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                    elif self.kpi_characteristics == 'dec':
                        return {
                            "change": round(-performance_change, 1),
                            "percent": round(-performance_change_percent, 1)
                        }
                    else:
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                else:
                    return None

            except Exception:
                return None

        return None
    
    def get_indicator_value_10_years_ago(self, year=None, quarter=None, month=None):
        if year:
            previous_year = str(int(year) - 10)
            try:
                current_year_plan = None
                previous_year_plan = None

                if month and year:
                    try:
                        current_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                        previous_year_plan = MonthData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_month__month_AMH=month,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif quarter and year:
                    try:
                        current_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                        previous_year_plan = QuarterData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            for_quarter__title_ENG=quarter,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                elif year:
                    try:
                        current_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=year,
                            indicator=self
                        ).first()
                        previous_year_plan = AnnualData.objects.filter(
                            for_datapoint__year_EC=previous_year,
                            indicator=self
                        ).first()
                    except (ObjectDoesNotExist, MultipleObjectsReturned, Exception):
                        return None

                
                if (
                    previous_year_plan and current_year_plan and
                    previous_year_plan.performance is not None and
                    current_year_plan.performance is not None and
                    previous_year_plan.performance != 0
                ):
                    performance_change = current_year_plan.performance - previous_year_plan.performance
                    performance_change_percent = (performance_change / previous_year_plan.performance) * 100

                    if self.kpi_characteristics == 'inc':
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                    elif self.kpi_characteristics == 'dec':
                        return {
                            "change": round(-performance_change, 1),
                            "percent": round(-performance_change_percent, 1)
                        }
                    else:
                        return {
                            "change": round(performance_change, 1),
                            "percent": round(performance_change_percent, 1)
                        }
                else:
                    return None

            except Exception:
                return None

        return None
   
  
   
    




    def __str__(self):
        return self.title_ENG 


@receiver(post_save, sender=Indicator)
def call_my_function(sender, instance, created, **kwargs):
    if created: 
        instance.create_data_value()
        instance.create_composite_key()


    
   
class DataPoint(models.Model):
    year_EC = models.CharField(max_length=50, null=True, blank=True, unique=True)
    year_GC = models.CharField(max_length=50, null=True, blank=True, unique = True)
    is_interval = models.BooleanField(default=False)
    year_start_EC = models.CharField(max_length=50, null=True, blank=True)
    year_start_GC = models.CharField(max_length=50, null=True, blank=True)
    year_end_EC = models.CharField(max_length=50, null=True, blank=True)
    year_end_GC = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['year_EC'] #Oldest First
        

    def save(self, *args, **kwargs):
        self.year_GC = f'{str(int(self.year_EC )+ 7)}/{str(int(self.year_EC)+ 8)}'
        super(DataPoint, self).save(*args, **kwargs)


    def __str__(self):
        if self.is_interval:
            return self.year_start_EC + " - " + self.year_end_EC + "E.C"
        else:
            return self.year_EC+" "+"E.C"
        
class Indicator_Point(models.Model):
    is_actual = models.BooleanField()
    for_datapoint = models.ForeignKey("DataPoint",on_delete=models.SET_NULL, null = True)
    for_indicator = models.ForeignKey(Indicator,on_delete=models.SET_NULL, null = True)
   
    
class Quarter(models.Model):
    title_ENG = models.CharField(max_length=50)
    title_AMH = models.CharField(max_length=50)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return self.title_AMH + " " + self.title_AMH
    
class Month(models.Model):
    month_ENG = models.CharField(max_length=50)
    month_AMH = models.CharField(max_length=50)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.month_AMH + " : " + self.month_ENG + " ==> " + str(self.number)
    

class MonthData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, blank=True ,null=True , related_name='month_data')
    for_month = models.ForeignKey(Month, on_delete=models.SET_NULL, blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG + " " + self.for_month.month_AMH
    
    class Meta:
        ordering = ['-for_datapoint__year_EC']
    
      
    def get_previous_year_performance(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 1
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = MonthData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_month = self.for_month,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except MonthData.DoesNotExist:
                return None
        return None
    

        
    def get_indicator_value_5_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 5
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = MonthData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_month = self.for_month,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except MonthData.DoesNotExist:
                return None
        return None
    

    def get_indicator_value_10_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 10
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = MonthData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_month = self.for_month,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except MonthData.DoesNotExist:
                return None
        return None
    

    


    


class QuarterData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, blank=True ,null=True , related_name='quarter_data')
    for_quarter = models.ForeignKey(Quarter, on_delete=models.SET_NULL, blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG + " " + self.for_quarter.title_AMH
        
    
    class Meta:
        ordering = ['-for_datapoint__year_EC']
    
    def get_previous_year_performance(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 1
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = QuarterData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_quarter = self.for_quarter,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except QuarterData.DoesNotExist:
                return None
        return None
    

    def get_performance_value_5_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 5
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = QuarterData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_quarter = self.for_quarter,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except QuarterData.DoesNotExist:
                return None
        return None
    
    def get_performance_value_10_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 10
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = QuarterData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    for_quarter = self.for_quarter,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except QuarterData.DoesNotExist:
                return None
        return None
    

    

    
    

    
    

class AnnualData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, related_name='annual_data' ,blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Round performance to two decimal places before saving
        if self.performance is not None:
            try:
                self.performance = round(self.performance, 2)
            except:
                pass    
        super().save(*args, **kwargs)


    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG
        else:
            return str(self.performance)
    
    class Meta:
        ordering = ['-for_datapoint__year_EC'] #Oldest First
    
    def get_previous_year_performance(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 1
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = AnnualData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except AnnualData.DoesNotExist:
                return None
        return None
    
    def get_performance_value_5_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 5
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = AnnualData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except AnnualData.DoesNotExist:
                return None
        return None
    
    def get_performance_value_10_years_ago(self):
        # Calculate and return the change in performance compared to the previous year
        if self.for_datapoint:
            previous_year = int (self.for_datapoint.year_EC) - 10
            previous_year = str(previous_year)
            try:
                
                previous_year_plan = AnnualData.objects.get(
                    for_datapoint__year_EC=previous_year,
                    indicator=self.indicator,
                )
                
                if previous_year_plan.performance is not None and self.performance is not None and previous_year_plan.performance != 0:
                    performance_change = self.performance - previous_year_plan.performance


                    performance_change_percent = (
                        (self.performance - previous_year_plan.performance)/previous_year_plan.performance) * 100

                    if self.indicator.kpi_characteristics == 'inc':
                        # For increasing KPIs, positive change is good, and negative change is bad
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" :round(performance_change_percent,1)
                            }
                    elif self.indicator.kpi_characteristics == 'dec':
                        # For decreasing KPIs, negative change is good, and positive change is bad
                        return {
                            "change" : round(-performance_change, 1), 
                            "percent" :round(-performance_change_percent,1)
                            }
                    else:
                        # For constant KPIs, return the change without modifying its sign
                        return {
                            "change" : round(performance_change, 1), 
                            "percent" : round(performance_change_percent,1)
                        }
                else:
                    return None
            except AnnualData.DoesNotExist:
                return None
        return None
    

    
class Source(models.Model):
    title_ENG = models.CharField(max_length=50)
    title_AMH = models.CharField(max_length=50)
    updated =  models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default = False)
    
    def __str__(self):
        return self.title_ENG


class ProjectInitiatives(models.Model):
    title_ENG = models.CharField(max_length=50)
    title_AMH = models.CharField(max_length=50)
    description = models.TextField()  
    image = models.FileField(upload_to="media/image" , null=True, blank=True)
    image_icons = models.FileField(upload_to="media/image_icons" , null=True, blank=True)
    content = models.JSONField(null=True , blank=True)  
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ENG


class SubProject(models.Model):
    title_ENG = models.CharField(max_length=50)
    title_AMH = models.CharField(max_length=50)
    project = models.ForeignKey(ProjectInitiatives, on_delete=models.SET_NULL, null=True, blank=True , related_name='sub_projects')
    description = models.TextField()
    image = models.FileField(upload_to="media/image" , null=True, blank=True)
    image_icons = models.FileField(upload_to="media/image_icons" , null=True, blank=True)  
    content = models.JSONField(null=True , blank=True) 
    data = models.JSONField(null=True , blank=True) 
    is_regional = models.BooleanField(default=False)
    is_stats = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.project.title_ENG})'  + ' - ' + self.title_ENG
    
    def save(self , *args , **kwargs ):
        if(self.content):
            data = json.loads(self.content)
            headers = data[0]
            rows = data[1:]  
            structured_data = []
            for row in rows:
                row_data = {headers[i]: row[i] for i in range(len(headers))}
                structured_data.append(row_data)
            
            self.data = json.dumps(structured_data)

        super(SubProject, self).save(*args, **kwargs)

    class Meta:
        ordering = ['project__title_ENG'] #Oldest First
         
            




















####################################### Test #################################
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    like = models.IntegerField(default=0)
    video = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def add_like(self):
        self.like += 1
        self.save()
    
    def remove_like(self):
        if self.like > 0:
            self.like -= 1
            self.save()