from django.db import models

class Dates(models.Model):
    start_sell = models.DateTimeField()
    end_sell = models.DateTimeField()
    start_purchase = models.DateTimeField()
    end_purchase = models.DateTimeField()