from django.contrib import admin
from.models import *
# Register your models here.


admin.site.register(Topic)
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