from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EnvironmentalData(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    date = models.DateField()
    air_quality_index = models.IntegerField()
    temperature = models.FloatField()
    rainfall = models.FloatField(null=True, blank=True)
    waste_collected_kg = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.district.name} - {self.date}"
