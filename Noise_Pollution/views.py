from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import Sensore, Dati, Stanza
from .form import NewSensor, MoveSensor, NewRoom, SetSensorTime, Filter
from .functions import random_password
from django.shortcuts import redirect
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from requests import get
import json

max_threshold = 70


def index(request):
    return render(request, 'Noise_Pollution/index.html', {})


def sensors(request):
    sensori_list = Sensore.objects.order_by('id')
    if request.method == "POST":
        form = Filter(request.POST)
        sens_type = request.POST['sensorType']
        sens_room = request.POST['room']
        if sens_type == '0' or sens_type == '1':
            t = sens_type == '1'
            if sens_room is not '':
                sensori_list = Sensore.objects.filter(type=t, room=sens_room)
            else:
                sensori_list = Sensore.objects.filter(type=t)
        else:
            if sens_room is not '':
                sensori_list = Sensore.objects.filter(room=sens_room)
    else:
        form = Filter()
    active = dict()
    for sens in list(sensori_list):
        try:
            data = Dati.objects.filter(sensore=sens.id).latest('date', 'time')
            if data.date == datetime.now().date() and datetime.now().time().hour == data.time.hour and datetime.now().time().minute == data.time.minute and datetime.now().time().second-10 <= data.time.second:
                active[sens.id] = 1
            else:
                active[sens.id] = 0
        except ObjectDoesNotExist:
            active[sens.id] = -1

    context = {
        'sensori_list': sensori_list,
        'current_time': datetime.now().time(),
        'current_data': datetime.now().date(),
        'active': active,
        'form': form
        }
    return render(request, 'Noise_Pollution/sensors.html', context)


def manage_sensors(request):
    form = SetSensorTime()
    sensori_list = Sensore.objects.order_by('id')
    context = {
        'sensori_list': sensori_list,
        'form': form
    }
    return render(request, 'Noise_Pollution/manage_sensors.html', context)


def rooms(request):
    sensori_list = Sensore.objects.order_by('id')
    stanza_list = list(Stanza.objects.order_by('id'))
    state = dict()
    for room in stanza_list:
        state[room.id] = 0
        try:
            sensor = Sensore.objects.get(room=room.id)
        except ObjectDoesNotExist:                                      # no sensors
            state[room.id] = -1
            continue

        except MultipleObjectsReturned:                                 # multiple sensors
            for obj in Sensore.objects.filter(room=room.id):
                latest_data = list(Dati.objects.filter(sensore=obj.id))[-20:]
                if state[room.id] == 0:
                    for data in latest_data:
                        if obj.type:   # analogical sensor
                            if data.analogic_value > max_threshold:
                                state[room.id] = 1
                        else:          # digital sensor
                            state[room.id] = 1 if data.digital_value else 0
            continue

        latest_data = list(Dati.objects.filter(sensore=sensor.id))[-20:]      # single sensor
        for data in latest_data:
            if sensor.type:
                if data.analogic_value > max_threshold:
                    state[room.id] = 1
                else:
                    state[room.id] = 1 if data.digital_value else 0
    return render(request, 'Noise_Pollution/rooms.html', {'stanza_list': stanza_list, 'sensori_list': sensori_list, 'room_state': state})


def room_sensors(request, id):
    sensors_list = Sensore.objects.filter(room=id)
    room = Stanza.objects.get(id=id)
    return render(request, 'Noise_Pollution/room_sensors.html', {'sensori_list': sensors_list, 'room': room})


def chart(request, id):
    dati_list = list(Dati.objects.filter(sensore=id))[-30:]
    return render(request, 'Noise_Pollution/chart.html', {'dati_list': dati_list, 'id': id})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        labels = []
        dati = []
        for obj in list(Dati.objects.filter(sensore=id))[-30:]:
            date = str(obj.time.hour)+':'+str(obj.time.minute)+':'+str(obj.time.second)
            labels.append(date)
            if obj.sensore.type:
                dati.append(obj.analogic_value)
            else:
                dati.append(obj.digital_value)
        data = {
            "labels": labels,
            "dati": dati
        }
        return Response(data)


@csrf_exempt
def send_data(request, id):
    try:
        sensor = Sensore.objects.get(id=id)
    except ObjectDoesNotExist:
        print("Sensor "+id+" doesn't exist")
        return HttpResponse("Sensor "+id+" doesn't exist")

    if request.method == "POST":
        threshold_exceeded = False
        json_data = json.loads(request.body.decode("utf-8"))
        if sensor.key != json_data['key']:
            print("ACCESS DENIED!")
            return HttpResponse("ACCESS DENIED!")
        if not sensor.authenticated:
            sensor.authenticated = 1
        value = int(float(json_data['value']))
        if sensor.is_analogic():
            if value > 1:
                Dati.objects.create(
                                        sensore=sensor,
                                        analogic_value=value
                                    )
                threshold_exceeded = value > max_threshold
            else:
                print("Wrong sensor type")
                HttpResponse("Wrong sensor type")

        else:
            if value == (1 or 0):
                Dati.objects.create(
                                        sensore=sensor,
                                        digital_value=json_data['value']
                                    )
                threshold_exceeded = value == 1
            else:
                print("Wrong sensor type")
                HttpResponse("Wrong sensor type")
        print("Data collected.")

        if threshold_exceeded:  # send an e-mail
            email = sensor.room.mail
            message = "The maximum threshold is exceeded in "+sensor.location+". Please, talk less loudly."
            get('http://ame97software.altervista.org/email/send.php?mittente=notify@noisepollution.com&destinatario='+email+'&oggetto=ATTENTION:%20maximum%20threshold%20exceeded!&body='+message)
        return HttpResponse()

    if request.method == "GET":
        return HttpResponse(sensor.time_collection)


def add_sensor(request):
    if request.method == "POST":
        form = NewSensor(request.POST)

        if form.is_valid():
            stanza = form.cleaned_data['room']
            if form.cleaned_data['type'] == 'analogical':
                t = True
            else:
                t = False
            key = random_password()

            Sensore.objects.create(room=stanza, type=t, key=key)
            sensor = Sensore.objects.get(key=key)
            print("Sensor "+str(sensor.id)+" create.\n The secure key is "+key+"\nA mail with the infos is coming.")

            if form.cleaned_data['email'] == '':
                email = stanza.mail
            else:
                email = form.cleaned_data['email']
            message = "New sensor with id: "+str(sensor.id)+", has the following security key:\n"+key
            get('http://ame97software.altervista.org/email/send.php?mittente=notify@noisepollution.com&destinatario='+email+'&oggetto=New%20sensor%20added!&body='+message)

            HttpResponse("Sensor "+str(sensor.id)+" create.\n The secure key is "+key+"\nA mail with the infos is coming.")
            return redirect('../manage_sensors/')

    else:
        form = NewSensor()
    return render(request, 'Noise_Pollution/add_sensor.html', {'form': form})


def move_sensor(request, id):
    nome = ''
    if request.method == "POST":
        form = MoveSensor(request.POST)

        if form.is_valid():
            nuova_stanza = form.cleaned_data['room']
            sensor = Sensore.objects.get(id=id)
            sensor.room = nuova_stanza
            nome = nuova_stanza.name
            sensor.save()
            return redirect('../../manage_sensors/')
    else:
        form = MoveSensor()
    return render(request, 'Noise_Pollution/move_sensor.html', {'form': form, 'stanza': nome, 'id': id})


@require_POST
def change_time_collection(request, id):
    try:
        sensor = Sensore.objects.get(id=id)
    except ObjectDoesNotExist:
        print("Sensor "+str(id)+" doesn't exist")
        return HttpResponse("Sensor "+str(id)+" doesn't exist")
    sensor.time_collection = request.POST['time']
    sensor.save()
    HttpResponse("Sensor " + str(id)+" collection time modified")
    return redirect('../../manage_sensors/')

@require_POST
def delete_sensor(request, id):
    try:
        sensor = Sensore.objects.get(id=id)
    except ObjectDoesNotExist:
        print("Sensor "+str(id)+" doesn't exist")
        return HttpResponse("Sensor "+str(id)+" doesn't exist")

    sensor.delete()
    HttpResponse("Sensor "+str(id)+" successfully deleted!")
    return redirect('../../manage_sensors/')


@require_POST
def delete_room(request, id):
    try:
        room = Stanza.objects.get(id=id)
    except ObjectDoesNotExist:
        print("Room "+str(id)+" doesn't exist")
        return HttpResponse("Room "+str(id)+" doesn't exist")

    room.delete()
    HttpResponse(room.name+" successfully deleted!")
    return redirect('../../room_list/')


def add_room(request):
    if request.method == "POST":
        form = NewRoom(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            rep = form.cleaned_data['rep']
            email = form.cleaned_data['email']
            Stanza.objects.create(name=name, rep=rep, mail=email)
            room = Stanza.objects.latest('id')
            message = "New room "+room.name+" created!\nRepresentative: "+room.rep
            get('http://ame97software.altervista.org/email/send.php?mittente=notify@noisepollution.com&destinatario='+email+'&oggetto=New%20sensor%20added!&body='+message)
            return redirect('../room_list/')
    else:
        form = NewRoom()
    return render(request, 'Noise_Pollution/add_room.html', {'form': form})


def history_chart(request, id, data):
    dati = []
    labels = []
    div = ","
    for object in list(Dati.objects.filter(sensore=id, date=data)):
        time = str(object.time.hour) + str(object.time.minute) + str(object.time.second)
        labels.append(time)
        if object.sensore.type:
            dati.append(object.analogic_value)
        else:
            dati.append(object.digital_value)
    return render(request, 'Noise_Pollution/history_one_day_chart.html', {'dati_list': dati, 'label_list': labels, 'data':data, 'id': id})


def history_chart2(request, id, datastart, dataend):
    dati = []
    labels = []
    div = ","
    for object in list(Dati.objects.filter(sensore=id)):
        if object.date.year >= int(datastart[0:4]) and object.date.month >= int(datastart[5:7]) and object.date.day >= int(datastart[8:10]) and object.date.year <= int(dataend[0:4]) and object.date.month <= int(dataend[5:7]) and object.date.day <= int(dataend[8:10]):
            time = str(object.time.hour) + str(object.time.minute) + str(object.time.second)
            labels.append(time)
            if object.sensore.type:
                dati.append(object.analogic_value)
            else:
                dati.append(object.digital_value)
    title = "from " + datastart + " to " + dataend
    context = {'dati_list': dati, 'label_list': labels, 'dataTitle':  title, 'id': id}
    return render(request, 'Noise_Pollution/history_more_days_chart.html', context)
