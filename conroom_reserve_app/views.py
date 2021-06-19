from django.shortcuts import render
import pandas as pd
import datetime
from conroom_reserve_app.models import Room


# Create your views here.
def main_conf_reserve(request):
    rooms = Room.objects.all()
    return render(request, 'conroom_reserve_app/main.html', context={'rooms': rooms})


def room_conf_reserve(request, room_id):
    room = Room.objects.get(pk=room_id)
    if room.projector_avaibility:
        projector = 'YES'
    else:
        projector = 'NO'
    return render(request, 'conroom_reserve_app/room.html', context={'room': room, 'projector': projector})


def date_reserve(request):
    L = []
    for time in pd.date_range(start=datetime.today(), periods=7):
        date_reserve = pd.date_range(time, periods=1, freq='D').strftime("%Y-%m-%d").tolist()

    return render(request, 'conroom_reserve_app/main.html', date_reserve='date_reserve')
