"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from project.apps.pong.consumers import PongConsumer
from project.apps.chat import consumers


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/pong/", PongConsumer.as_asgi()),
			path('ws/chat/', consumers.ChatConsumer.as_asgi()),
        ])
    ),
})
