## dadjokes/admin.py
## Author: Author: William Fugate wfugate@bu.edu
## description: admin model registrations for dadjokes app
from django.contrib import admin


from .models import Picture, Joke

admin.site.register(Picture)
admin.site.register(Joke)

