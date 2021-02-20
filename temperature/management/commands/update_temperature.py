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

        Temperature.objects.update_or_create(
            date=self._format_date(daily_forecast[0].reference_time()),
            defaults={
                'min': daily_forecast[0].temperature('celsius')['min'],
                'type': 'actual',
            },
        )

        for day in daily_forecast[1:]:
            Temperature.objects.update_or_create(
                date=self._format_date(day.reference_time()),
                defaults={
                    'min': day.temperature('celsius')['min'],
                    'type': 'forecast',
                },
            )

        forecast_part = Temperature.objects.filter(type='forecast').order_by('date')

        temp_diff = forecast_part.last().min - forecast_part.first().min
        temp_trend = round(temp_diff / len(forecast_part), 2)

        for x in range(1, len(forecast_part) + 1):
            Temperature.objects.update_or_create(
                date=forecast_part.last().date + datetime.timedelta(days=x),
                defaults={
                    'min': forecast_part.last().min + (temp_trend * x),
                    'type': 'trend',
                },
            )

        return None

    @staticmethod
    def _format_date(raw_date):
        return datetime.datetime.utcfromtimestamp(raw_date).date()
