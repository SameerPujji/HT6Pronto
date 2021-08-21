from django.db import models


class Available(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    stars = models.DecimalField(max_digits=1, decimal_places=1)
    price = models.DecimalField(max_digits=18, decimal_places=2)
