from django.contrib import admin
from .models import Order, Strategy, StrategyOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    pass

@admin.register(StrategyOrder)
class StrategyOrderAdmin(admin.ModelAdmin):
    pass
