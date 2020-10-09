import json

from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer
from django.forms import formset_factory
from django.forms.models import modelformset_factory

from asgiref.sync import async_to_sync
from .models import *
from .forms import *
from .socket_connection import update_config

# Create your views here.


def index(request):
    return render(request, 'frontend/index.html', {})

def control(request):
    return render(request, 'frontend/control.html', {})


def configs(request):
    extensions = Extension.objects.all()
    return render(request, 'frontend/configs.html', {'extensions': extensions})

def config(request, extension_id):
    # extension = Extension.objects.get(id=extension_id)
    # config_entrys = ConfigEntry.objects.filter(extension=extension)
    # print(config_entrys)
    # return render(request, 'frontend/config.html', {'config_entrys': config_entrys})
    if request.method == 'POST':
        print("Post")
        entry_formset = modelformset_factory(ConfigEntry, exclude=())
        formset = entry_formset(request.POST, request.FILES)
        if formset.is_valid():
            print("Valid form")
            forms = formset.save()
            print(forms, type(forms))
            for form in forms:
                update_config(form.extension.extension_name, form.config_key, form.config_value)


        else:
            print(formset.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        extension = Extension.objects.get(id=extension_id)
        print("Extension:", extension)
        entry_formset = modelformset_factory(ConfigEntry, exclude=(), extra=0)
        entry_forms = entry_formset(queryset=ConfigEntry.objects.filter(extension=extension))
        print("DISPLAY:", ConfigEntry.objects.filter(extension=extension))
        return render(request, 'frontend/config.html', {'config_entrys': entry_forms})

    extensions = Extension.objects.all()
    return render(request, 'frontend/configs.html', {'extensions': extensions})

def extension_select(request):
    return render(request, "frontend/extension_select.html", {'extensions': Extension.objects.filter(displayed=True)})


def highscore_page(request):
    extensions = list()
    for extension in Extension.objects.all():
        if extension.has_highscores:
            extensions.append(extension)
    return render(request, "frontend/highscore_select.html", {'extensions': extensions})


def highscores(request, extension_id):
    extension = Extension.objects.get(id=extension_id)
    score_data = SavedData.objects.filter(extension=extension, field_name='highscore')
    highscores = list()
    for score in score_data:
        content = json.loads(score.content)
        highscores.append({'score': content['score'], 'name': 'Test'})

    highscores = sorted(highscores, key=lambda k: k['score'], reverse=True)
    return render(request, "frontend/highscores.html", {'highscores': highscores})

