from django.contrib import admin
from .models import Cook, DishType, Dish, Ingredient

admin.site.register(Cook)
admin.site.register(DishType)
admin.site.register(Dish)
admin.site.register(Ingredient)
