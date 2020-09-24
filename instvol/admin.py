from django.contrib import admin

# Register your models here.
from .models import Stock, StockPrice

admin.site.register(Stock)
admin.site.register(StockPrice)
