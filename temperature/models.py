from django.db import models


class Temperature(models.Model):
    min = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.min} ({self.date})'
