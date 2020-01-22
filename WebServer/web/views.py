from django.shortcuts import render
from django.http import HttpResponse
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

# Create your views here.


def index(request):
    return render(request, 'frontend/index.html', {})

def control(request):
    return render(request, 'frontend/control.html', {})

def test(request):
    print('test')
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('table', {
        'type': 'message',
        'content': {'message': "view test"}
    })
    return render(request, 'frontend/control.html', {})