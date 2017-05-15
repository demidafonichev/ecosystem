import json
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status

from .models import Box, Plant, Watering, Illumination, CareMethod


def get_plants(request):
    plants = []
    for plant in Plant.objects.all():
        waterings = Watering.objects.filter(care_method=plant.care)
        w = []
        for watering in waterings:
            w.append({'start_time': watering.watering_start_time,
                      'volume': watering.watering_volume,
                      'frequency': watering.watering_frequency})
        illuminations = Illumination.objects.filter(care_method=plant.care)

        i = []
        for illumination in illuminations:
            i.append({'start_time': illumination.illumination_start_time,
                      'duration': illumination.illumination_duration_time,
                      'frequency': illumination.illumination_frequency})
        plants.append({'id': plant.id, 'name': plant.name, 'watering': w, 'illumination': i})

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({'plants': plants}),
                        content_type="application/json")


def check_key_and_name(request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.get(username=request.user.username)
    key = data['key']
    name = data['name']
    response_data = {}
    ok = True
    try:
        box = Box.objects.get(key=key)
        if box:
            response_data['key_status'] = 'OK'
            if not box.registered:
                response_data['box_status'] = 'OK'
            else:
                ok = False
                response_data['box_status'] = 'Registered'
            try:
                user_box_list = Box.objects.filter(owner=user)
                for box in user_box_list:
                    if box.name == name:
                        response_data['name'] = 'Registered</nav>'
                        ok = False
                else:
                    response_data['name'] = 'OK'
            except Box.DoesNotExist:
                pass
    except Box.DoesNotExist:
        ok = False
        response_data['key_status'] = 'Wrong key'

    if ok:
        response_status = status.HTTP_200_OK
    else:
        response_status = status.HTTP_400_BAD_REQUEST

    return HttpResponse(status=response_status,
                        content=json.dumps({'data': response_data}),
                        content_type="application/json")


def save_box(request):
    data = json.loads(request.body.decode('utf-8'))

    plant = data['plant']
    name = data['name']
    is_watering_default = data['is_watering_default']
    is_illumination_default = data['is_illumination_default']

    care_method = CareMethod(
        is_watering_default=is_watering_default,
        is_illumination_default=is_illumination_default
    )
    care_method.save()

    waterings = data['waterings']
    for watering in waterings:
        Watering.objects.create(
            watering_start_time=watering['start_time'],
            watering_volume=watering['volume'],
            watering_frequency=watering['frequency'],
            care_method=care_method
        )

    illuminations = data['illuminations']
    for illumination in illuminations:
        Illumination.objects.create(
            illumination_start_time=illumination['start_time'],
            illumination_duration_time=illumination['duration'],
            illumination_frequency=illumination['frequency'],
            care_method=care_method
        )

    box = Box.objects.get(key=data['key'])
    plant = Plant.objects.get(id=plant)
    user = User.objects.get(username=request.user.username)

    Box.objects.filter(pk=box.pk).update(plant=plant)
    Box.objects.filter(pk=box.pk).update(name=name)
    Box.objects.filter(pk=box.pk).update(registered=True)
    Box.objects.filter(pk=box.pk).update(care=care_method)
    Box.objects.filter(pk=box.pk).update(owner=user.id)

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({'id': box.pk}),
                        content_type="application/json")


def get_box_list(request):
    user = User.objects.get(username=request.user.username)
    box_list = Box.objects.filter(owner=user)

    response_data = []
    for box in box_list:
        waterings = []
        try:
            for watering in Watering.objects.filter(care_method=Box.objects.get(pk=box.id).care):
                waterings.append({
                    'start_time': watering.watering_start_time,
                    'volume': watering.watering_volume,
                    'frequency': watering.watering_frequency
                })
        except Watering.DoesNotExist:
            pass

        illuminations = []
        try:
            for illumination in Illumination.objects.filter(care_method=Box.objects.get(pk=box.id).care):
                illuminations.append({
                    'start_time': illumination.illumination_start_time,
                    'duration': illumination.illumination_duration_time,
                    'frequency': illumination.illumination_frequency
                })
        except Illumination.DoesNotExist:
            pass

        response_data.append({
            'id': box.id,
            'name': box.name,
            'plant': Plant.objects.get(name=box.plant).id,
            'temperature': box.temperature,
            'air_humidity': box.air_humidity,
            'soil_humidity': box.air_humidity,
            'status': box.status,
            'waterings': waterings,
            'illuminations': illuminations
        })

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({'box_list': response_data}),
                        content_type="application/json")


def change_box(request):
    data = json.loads(request.body.decode('utf-8'))

    box_id = data['id']
    name = data['name']
    plant = data['plant']
    waterings = data['waterings']
    illuminations = data['illuminations']

    care_method = CareMethod.objects.get(pk=Box.objects.get(pk=box_id).care.id)

    Watering.objects.filter(care_method=care_method).delete()
    for watering in waterings:
        Watering.objects.create(
            watering_start_time=watering['start_time'],
            watering_volume=watering['volume'],
            watering_frequency=watering['frequency'],
            care_method=care_method
        )

    Illumination.objects.filter(care_method=care_method).delete()
    for illumination in illuminations:
        Illumination.objects.create(
            illumination_start_time=illumination['start_time'],
            illumination_duration_time=illumination['duration'],
            illumination_frequency=illumination['frequency'],
            care_method=care_method
        )

    Box.objects.filter(pk=box_id).update(name=name)
    Box.objects.filter(pk=box_id).update(plant=plant)

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({}),
                        content_type="application/json")


def delete_box(request):
    data = json.loads(request.body.decode('utf-8'))

    box_id = data['id']

    if not Box.objects.get(pk=box_id).care.is_watering_default or \
       not Box.objects.get(pk=box_id).care.is_illumination_default:
        Watering.objects.filter(care_method=Box.objects.get(pk=box_id).care).delete()
        Illumination.objects.filter(care_method=Box.objects.get(pk=box_id).care).delete()
        CareMethod.objects.filter(pk=Box.objects.get(pk=box_id).care.id).delete()

    Box.objects.filter(pk=box_id).update(registered=False)
    Box.objects.filter(pk=box_id).update(owner=None)
    Box.objects.filter(pk=box_id).update(care=None)

    return HttpResponse(status=status.HTTP_200_OK,
                        content=json.dumps({}),
                        content_type="application/json")
