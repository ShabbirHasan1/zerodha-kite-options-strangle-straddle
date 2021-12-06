from django.contrib import admin
from .models import KiteBroker


@admin.register(KiteBroker)
class KiteBrokerAdmin(admin.ModelAdmin):
    pass
