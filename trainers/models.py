from django.db import models
from products.models import *
# Create your models here.


class Trainer(models.Model):
    trainer_name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Main_Product')

    def __str__(self):
        return self.trainer_name

    class Meta:
        managed = True
        verbose_name = "Trainer"
