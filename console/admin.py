from django.contrib import admin
from .models import VMachine, VHost, OsType, Datastore, VType

# Register your models here.

admin.site.register(VHost)
admin.site.register(Datastore)
admin.site.register(VType)
