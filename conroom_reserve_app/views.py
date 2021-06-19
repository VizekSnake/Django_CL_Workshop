from django.shortcuts import render
import pandas as pd
from datetime import datetime
from conroom_reserve_app.models import Room


# Create your views here.
def main_conf_reserve(request):
    rooms = Room.objects.all()
    today = datetime.today()
    today = today.strftime("%A %d %B %Y")
    today = str(today)
    reserv_days = []
    days_calendar = pd.date_range(start=datetime.today(), periods=7).strftime("%A %Y-%m-%d")
    for day in days_calendar:
        reserv_days.append(day)
    return render(request, 'conroom_reserve_app/main.html',
                  context={'rooms': rooms, 'reserv_days': reserv_days, 'today': today})


def room_conf_detail(request, room_id):
    room = Room.objects.get(pk=room_id)
    if room.projector_avaibility:
        projector = 'YES'
    else:
        projector = 'NO'
    return render(request, 'conroom_reserve_app/room.html', context={'room': room, 'projector': projector})


def room_conf_edit(request, room_id):
    room = Room.objects.get(pk=room_id)
    if request.method == 'GET':
        if room.projector_avaibility:
            projector = 'YES'
        else:
            projector = 'NO'
        return render(request, 'conroom_reserve_app/room_edit.html', context={'room': room, 'projector': projector})
    elif request.method == 'POST':
        r_name = request.GET.get('r_name')
        max_capacity = request.GET.get('max_capacity')
        p_avaible = request.GET.get('p_avaible')
        Room.objects.update_or_create(room_id=request.POST['room_id'])


#
# L = []
# for time in pd.date_range(start=datetime.today(), periods=7).strftime("%A %Y-%m-%d"):
#     L.append(pd.date_range(start=datetime.today(), periods=7).strftime("%A %Y-%m-%d").tolist())
#
# print(L)
