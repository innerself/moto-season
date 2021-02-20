from django.db import models


class Temperature(models.Model):
    TYPES = [
        ('actual', 'actual'),
        ('forecast', 'forecast'),
        ('trend', 'trend'),
    ]

    min = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return f'{self.min} ({self.date})'
