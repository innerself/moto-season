import datetime
import random

from django.core.management import call_command
from django.test import TestCase

from temperature.models import Temperature


class UpdateTemperatureTest(TestCase):
    today = datetime.datetime.today()
    random_temp = random.randint(-99, 99)

    @classmethod
    def setUpTestData(cls):
        Temperature.objects.create(
            min=cls.random_temp,
            date=cls.today,
        )

    def test_command(self):
        self.assertEquals(
            Temperature.objects.get(date=self.today).min,
            self.random_temp,
        )

        call_command('update_temperature')

        self.assertEquals(len(Temperature.objects.all()), 8)
        self.assertNotEquals(
            Temperature.objects.get(date=self.today).min,
            self.random_temp,
        )
