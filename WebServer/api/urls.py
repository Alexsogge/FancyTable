from django.urls import path, include
from . import views
from rest_framework import routers
#from web.socket_connection import load_saved_config_file

router = routers.DefaultRouter()
#router.register(r'test', views.TestView, basename="test")



urlpatterns = [
    path('', include(router.urls)),
    path('test/', views.TestView.as_view(), name='test'),
    path('switch_extension/<int:extension_id>/', views.SwitchExtension.as_view(), name='switch_extension')
]
