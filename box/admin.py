from django.contrib import admin
from .models import Box, Plant, CareMethod, Watering, Illumination

from django.contrib.auth.models import Group

admin.site.register(Box)
admin.site.register(Plant)
admin.site.register(CareMethod)
admin.site.register(Watering)
admin.site.register(Illumination)

admin.site.unregister(Group)
