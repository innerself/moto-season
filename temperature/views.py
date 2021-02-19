from django.http import HttpResponse
from plotly.offline import plot
from plotly import graph_objs

from temperature.models import Temperature


def main(request):
    temps = Temperature.objects.all()
    season_start_temperature = 5

    fig = graph_objs.Figure()
    actual_temp_line = graph_objs.Scatter(
        x=[t.date for t in temps],
        y=[t.min for t in temps],
        mode='lines',
        name='Current/Forecast',
        opacity=0.8,
    )
    season_start_temp_line = graph_objs.Scatter(
        x=[t.date for t in temps],
        y=[season_start_temperature for _ in range(len(temps))],
        mode='lines',
        name='Season start',
        opacity=0.2,
    )
    fig.add_trace(actual_temp_line)
    fig.add_trace(season_start_temp_line)
    plt_div = plot(fig, output_type='div')

    return HttpResponse(plt_div)
