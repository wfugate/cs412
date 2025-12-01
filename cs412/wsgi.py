"""
WSGI config for cs412 project.
"""

import os
import sys
import site

# Add user site-packages to path (for server deployment)
user_site = os.path.expanduser('~/.local/lib/python3.12/site-packages')
if os.path.exists(user_site):
    site.addsitedir(user_site)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs412.settings')

application = get_wsgi_application()