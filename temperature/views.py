from django.http import HttpResponse
from plotly import graph_objs
from plotly.offline import plot

from temperature.models import Temperature


def main(request):
    all_temps = Temperature.objects.all()
    actual_temps = all_temps.filter(type='actual').order_by('date')
    forecast_temps = all_temps.filter(type='forecast').order_by('date')
    trend_temps = all_temps.filter(type='trend').order_by('date')
    season_start_temperature = 5

    fig = graph_objs.Figure()
    actual_temp_line = graph_objs.Scatter(
        x=[t.date for t in actual_temps],
        y=[t.min for t in actual_temps],
        mode='lines',
        name='Actual',
        opacity=0.8,
    )
    forecast_temp_line = graph_objs.Scatter(
        x=[actual_temps.last().date] + [t.date for t in forecast_temps],
        y=[actual_temps.last().min] + [t.min for t in forecast_temps],
        mode='lines',
        name='Forecast',
        opacity=0.8,
    )
    trend_temp_line = graph_objs.Scatter(
        x=[forecast_temps.last().date] + [t.date for t in trend_temps],
        y=[forecast_temps.last().min] + [t.min for t in trend_temps],
        mode='lines',
        name='Trend',
        opacity=0.8,
    )

    season_start_temp_line = graph_objs.Scatter(
        x=[t.date for t in all_temps],
        y=[season_start_temperature for _ in range(len(all_temps))],
        mode='lines',
        name='Season start',
        opacity=0.6,
    )

    fig.add_trace(actual_temp_line)
    fig.add_trace(forecast_temp_line)
    fig.add_trace(trend_temp_line)
    fig.add_trace(season_start_temp_line)

    plt_div = plot(fig, output_type='div')

    return HttpResponse(plt_div)
