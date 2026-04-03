# main.py
from poker.events import *   # noqa: F401,F403 — registers all socket.io event handlers
from poker.server import socket_app as app
