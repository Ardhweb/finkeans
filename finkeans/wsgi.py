import os
from django.core.wsgi import get_wsgi_application
import sys

# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/jusctod/finekeans'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finekeans.settings')
application = get_wsgi_application()
