from django.contrib import admin

from cowapp.models import Cow, Record

admin.site.register([Cow, Record])
