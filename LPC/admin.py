from django.contrib import admin
from .models import Parent, Multi

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('punter','bet_date','bet_week','bet_number','bet_legs','bet_amount','bet_odds','bet_return')
    ordering = ['bet_date','punter','bet_number']
    
@admin.register(Multi)
class MultiAdmin(admin.ModelAdmin):
    list_display = ('parent','bet_leg','bet_type','bet_team','bet_opposition','bet_home','bet_odds','bet_win')
    ordering = ['parent','bet_leg']