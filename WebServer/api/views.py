from rest_framework import status, viewsets, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from web.models import *
from web import socket_connection


class TestView(APIView):
    def get(self, request, format=None):
        content = {'Test': 'response of test'}
        return Response(content, status=status.HTTP_200_OK)


class SwitchExtension(APIView):

    def get(self, request, extension_id):
        extension = Extension.objects.get(id=extension_id)
        content = {'Switched Extension': extension.extension_name}
        socket_connection.switch_ectension(extension)
        return Response(content, status=status.HTTP_200_OK)