from django.conf import settings

PUBLIC_PIPE = settings.NODESHOT['WEBSOCKETS']['PUBLIC_PIPE']
PRIVATE_PIPE = settings.NODESHOT['WEBSOCKETS']['PRIVATE_PIPE']
ADDRESS = settings.NODESHOT['WEBSOCKETS'].get('LISTENING_ADDRESS', 8080)
PORT = settings.NODESHOT['WEBSOCKETS'].get('LISTENING_PORT', 8080)
PATH = settings.NODESHOT['WEBSOCKETS'].get('PATH', '')
DOMAIN = settings.NODESHOT['WEBSOCKETS']['DOMAIN']
