from django.urls import re_path

from .consumers import SosConsumer

websocket_urlpatterns = [
    re_path(r"^ws/sos/(?P<room_name>\w+)/$", SosConsumer.as_asgi()),
]