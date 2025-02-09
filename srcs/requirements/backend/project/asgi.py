"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from project.apps.pong.consumers import PongConsumer
# from project.apps.chat.consumers import ChatConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Import ChatConsumer lazily after Django is initialized
from project.apps.chat.consumers import ChatConsumer

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/pong/", PongConsumer.as_asgi()),
			path('ws/chat/', ChatConsumer.as_asgi()),
        ])
    ),
})
