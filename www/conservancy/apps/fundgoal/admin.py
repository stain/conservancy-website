from django.contrib import admin
from conservancy.apps.fundgoal.models import FundraisingGoal

class FundraisingGoalAdmin(admin.ModelAdmin):
    list_display = ('fundraiser_code_name', 'fundraiser_goal_amount')

admin.site.register(FundraisingGoal, FundraisingGoalAdmin)
