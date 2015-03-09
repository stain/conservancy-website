from django.contrib import admin
from models import FundraisingGoal

class FundraisingGoalAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'display_until_date')

admin.site.register(FundraisingGoal, FundraisingGoalAdmin)
