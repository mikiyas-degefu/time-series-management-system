from django.db import models
from fontawesome_5.fields import IconField
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.

class Topic(models.Model):
    title_ENG = models.CharField(max_length=300, unique = True)
    title_AMH = models.CharField(max_length=300, null = True)
    is_dashboard = models.BooleanField(default = False)
    rank = models.IntegerField(null=True, blank=True)
    icon = IconField()
    updated =  models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title_ENG
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
        null=True,
        blank=True,
        default=""
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
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, blank=True ,null=True)
    for_month = models.ForeignKey(Month, on_delete=models.SET_NULL, blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG + " " + self.for_month.month_AMH

class QuarterData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, blank=True ,null=True)
    for_quarter = models.ForeignKey(Quarter, on_delete=models.SET_NULL, blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG + " " + self.for_quarter.title_AMH

class AnnualData(models.Model):
    indicator = models.ForeignKey(Indicator, on_delete=models.SET_NULL, related_name='annual_data' ,blank=True ,null=True)
    for_datapoint = models.ForeignKey(DataPoint, on_delete=models.SET_NULL, blank=True, null=True)
    performance = models.FloatField(blank=True ,null=True)
    target = models.FloatField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.indicator:
            return self.indicator.title_ENG
        else:
            return str(self.performance)
    
class Source(models.Model):
    title_ENG = models.CharField(max_length=50)
    title_AMH = models.CharField(max_length=50)
    updated =  models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default = False)
    
    def __str__(self):
        return self.title_ENG


