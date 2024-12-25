import os

from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()
from config.env import env  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", env("DJANGO_SETTINGS_MODULE"))


from channels.routing import ProtocolTypeRouter  # noqa
from channels.routing import URLRouter  # noqa

from core.apps.chat.middlewares import JWTAuthMiddlewareStack  # noqa
from core.apps.chat.ws_urls import websocket_urlpatterns  # noqa

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
