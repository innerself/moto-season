import datetime

from decouple import config
from django.core.management.base import BaseCommand
from pyowm import OWM

from temperature.models import Temperature


class Command(BaseCommand):
    def handle(self, *args, **options):
        owm = OWM(config('OPENWEATHERMAP_API_KEY'))
        city_id_registry = owm.city_id_registry()
        moscow = city_id_registry.locations_for('Moscow', country='RU')[0]
        mgr = owm.weather_manager()
        one_call = mgr.one_call(lat=moscow.lat, lon=moscow.lon)
        daily_forecast = one_call.forecast_daily

        for day in daily_forecast:
            dt = datetime.datetime.utcfromtimestamp(day.reference_time()).date()
            obj, created = Temperature.objects.update_or_create(
                date=dt,
                defaults={'min': day.temperature('celsius')['min']},
            )

        return None
