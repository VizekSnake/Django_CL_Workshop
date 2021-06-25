from django.shortcuts import render, redirect
import pandas as pd
from datetime import datetime
from conroom_reserve_app.models import Room, Reservation
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse



# Create your views here.
class RoomListView(View):
    def get(self, request):
        '''
            View returning names of conference room:
            + List of all Room names
            '''
        rooms = Room.objects.all()
        today = datetime.today()
        today = today.strftime("%A %d %B %Y")
        today = str(today)
        return render(request, "conroom_reserve_app/main.html",
                      context={"rooms": rooms, 'today': today ,})


def room_conf_detail(request, room_id):
    '''
    Function returning details of conference room:
    + Room name
    + Avaibility for 1 week in future
        - function getting list of reservations from room.reservation_set
        and compare with date range from pandas datetime
    + Projector avaibility
    + Max capacity of conference room
    '''
    reservations = Reservation.objects.filter(id=room_id)
    room = Room.objects.get(pk=room_id)
    days_calendar = list(pd.date_range(start=datetime.today(), periods=7).strftime("%Y-%m-%d"))
    reservation_dates = [r_day.reservation_date.strftime("%Y-%m-%d") for r_day in room.reservation_set.all()]
    occupied = []
    for day in days_calendar:
        if day in reservation_dates:
            occupied.append('OCCUPIED')
        else:
            day = (datetime.strptime(day, '%Y-%m-%d')).date()
            day = day.strftime("%Y-%m-%d")
            occupied.append(day)
    if room.projector_avaibility:
        projector = 'YES'
    else:
        projector = 'NO'

    return render(request, 'conroom_reserve_app/room.html',
                  context={'room': room, 'projector': projector, 'occupied': occupied,
                           'days_calendar': days_calendar, 'reservations':reservations})


def room_conf_edit(request, room_id):
    '''
        Function editing details of conference room:
        + Room name
        + Projector avaibility
        + Max capacity of conference room
    '''
    room = Room.objects.get(pk=room_id)
    projector = 'YES' if room.projector_avaibility else 'NO'
    if request.method == 'GET':
        if room.projector_avaibility:
            projector = 'YES'
        else:
            projector = 'NO'
        return render(request, 'conroom_reserve_app/room_edit.html', context={'room': room, 'projector': projector})
    elif request.method == 'POST':
        r_name = request.POST.get('r_name')
        max_capacity = request.POST.get('max_capacity')
        p_avaible = request.POST.get("projector") == "on"
        room.room_name = r_name
        max_capacity = int(max_capacity) if max_capacity else 0
        room.capacity = max_capacity
        room.projector_avaibility = p_avaible
        if Room.objects.filter(room_name=r_name).first():
            exist = 'Same conference room already exist'
            return render(request, "conroom_reserve_app/room_edit.html", context={'exist': exist})
        if r_name == "":
            return render(request, 'conroom_reserve_app/room_edit.html', context={'error': "Give me a name!"})
        room.save()
        return render(request, 'conroom_reserve_app/room_edit.html', context={'room': room, 'projector': projector})


def room_conf_add(request):
    '''
            Function adding new conference room:
            + Room name
            + Projector avaibility
            + Max capacity of conference room
        '''
    if request.method == 'GET':
        return render(request, 'conroom_reserve_app/room_add.html')
    elif request.method == 'POST':
        r_name = request.POST.get('r_name')
        try:
            max_capacity = int(request.POST.get('max_capacity'))
        except ValueError:
            return render(request, 'mconroom_reserve_app/room_add.html',
                          context={'error': "Fill capacity value!"})
        if r_name == "":
            return render(request, 'conroom_reserve_app/room_add.html', context={'error': "Give me a name!"})
        elif max_capacity < 0:
            return render(request, 'conroom_reserve_app/room_add.html',
                          context={'error': "Negative capacity? Not possible..."})
        p_avaible = request.POST.get("projector") == "on"
        max_capacity = int(max_capacity) if max_capacity else 0
        if Room.objects.filter(room_name=r_name).first():
            exist = 'Same conference room already exist'
            return render(request, "conroom_reserve_app/room_add.html", context={'exist': exist})
        Room.objects.create(room_name=r_name, capacity=max_capacity, projector_avaibility=p_avaible)
        return redirect('/crr')


def room_conf_delete(request, room_id):
    '''
        Function deleting conference room with specific id
    '''
    if request.method == 'GET':
        try:
            room = Room.objects.get(pk=room_id)
            room.delete()
            vanish = f"Room{room.room_name} has been deleted"
            return render(request, 'conroom_reserve_app/main.html', context={'vanish': vanish})
        except ObjectDoesNotExist:
            return HttpResponse("This room is not exists!")
    else:
        return redirect("/crr")


def room_reservation(request, room_id):
    '''
            Function adding reseravtion of conference room with specific date and comment
        '''
    if request.method == 'GET':
        room = Room.objects.get(pk=room_id)
        reservations = Reservation.objects.filter(id=room_id)
        if room.projector_avaibility:
            projector = 'YES'
        else:
            projector = 'NO'
        room = Room.objects.get(pk=room_id)
        today = datetime.today()
        today = today.strftime("%A %d %B %Y")
        return render(request, "conroom_reserve_app/room_reservation.html",
                      context={"room": room, 'today': today, 'projector': projector, 'reservations':reservations})
    if request.method == 'POST':
        room = Room.objects.get(pk=room_id)
        r_comment = request.POST.get('r_comment')
        occupied_day = request.POST.get('occupied_day')
        occupied_day = datetime.strptime(occupied_day, '%Y-%m-%d')
        new_reservation = Reservation.objects.create(reservation_date=occupied_day, comment=r_comment, room_id=room)
        return redirect('/crr')
