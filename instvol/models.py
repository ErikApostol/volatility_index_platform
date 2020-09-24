from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=False)
    def __str__(self):
        return self.ticker

class StockPrice(models.Model):
    ts = models.DateTimeField(db_index=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=6, null=True)
    def __str__(self):
        return str((self.ts, self.price))
        # return str((self.ts, self.close_price))
