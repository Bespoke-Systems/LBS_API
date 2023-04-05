from django.db import models


class CountyModel(models.Model):
    Name = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Counties'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.Name


class TownsModel(models.Model):
    Name = models.CharField(max_length=50)
    County = models.ForeignKey(CountyModel, on_delete=models.CASCADE, related_name="counties")

    class Meta:
        verbose_name = "Towns"
        verbose_name_plural = "Towns"

    def __str__(self):
        return self.Name
