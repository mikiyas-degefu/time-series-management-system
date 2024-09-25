from django.db import models
from Base.models import Indicator
from Base.models import DataPoint, Month, Quarter
# Create your models here.



colors = {
    ('blue' , 'blue'),
    ('red' , 'red'),
    ('green' , 'green'),
}


component_category = {
    ('card' , 'card'),
    ('graph' , 'graph'),
}


class Component(models.Model):
    data_type_options = (
        ('year','year'),
        ('month','month'),
        ('quarter','quarter'),
    )
    
    name = models.CharField(max_length=50)
    category = models.CharField(choices=component_category , max_length=50)
    is_multiple = models.BooleanField(default=False)
    is_range = models.BooleanField(default=False)
    data_type = models.CharField(choices=data_type_options, max_length=10,null=True, blank=True)
    #configuration = models.JSONField(default=dict,null=True , blank=True) 
    image = models.ImageField(upload_to='components/', null=True, blank=True)
    path = models.CharField(max_length=50 , null=True , blank=True)

    def __str__(self):
        return self.name
    

class Dashboard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(choices=colors , max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=30, null=True, blank=True)

    def row_list(self):
        return Row.objects.filter(for_dashboard=self)

    def __str__(self):
        return self.title

class Row(models.Model):
    rank = models.IntegerField()
    for_dashboard = models.ForeignKey(Dashboard , on_delete=models.CASCADE , related_name='dashBoard')

    def col_list(self):
        return DashboardIndicator.objects.filter(for_row=self)

    def __str__(self):
        return str(self.rank) + ' ' + self.for_dashboard.title


class DashboardIndicator(models.Model):
    for_row = models.ForeignKey(Row , on_delete=models.CASCADE)
    indicator = models.ManyToManyField(Indicator , related_name='indicator')  
    component = models.ForeignKey(Component ,  on_delete=models.SET_NULL , null = True , related_name='component')
    year = models.ForeignKey( DataPoint,on_delete=models.SET_NULL, null=True, blank=True)
    data_range_start = models.CharField(max_length=10,  null=True, blank=True)
    data_range_end = models.CharField(max_length=10,  null=True, blank=True)

    def __str__(self):
        return str(self.for_row.rank) 
