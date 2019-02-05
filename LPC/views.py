from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.db.models import Avg, Count, Sum
from .models import Parent, Multi


class ParentListView(ListView):
    model = Parent
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bet_count'] = Parent.objects.count()
        context['bet_count_wins'] = Parent.objects.filter(bet_win__exact=True).count()
        context['bet_win_ratio'] = round((context['bet_count_wins'] / context['bet_count'])*100,2)
        context['bet_count_multi'] =  Multi.objects.count()
        context['bet_count_multi_wins'] = Multi.objects.filter(bet_win__exact=True).count()
        context['bet_win_ratio_multi'] = round((context['bet_count_multi_wins'] / context['bet_count_multi'])*100,2)
        context['bet_return_total'] = Parent.objects.aggregate(bet_return_sum=Sum('bet_return'))['bet_return_sum']
        context['bet_amount_total'] = Parent.objects.aggregate(bet_amount_sum=Sum('bet_amount'))['bet_amount_sum']
        context['bet_cum_pnl'] = context['bet_return_total'] - context['bet_amount_total']
        context['bet_return_average'] = Parent.objects.aggregate(bet_return_average=Avg('bet_return'))['bet_return_average']

        punts = Parent.objects.all()
        punters = []
        for punt in punts:
            if punt.punter not in punters:
                punters.append(punt.punter)

        punting_data = []
        for punter in punters:
            spent = Parent.objects.filter(punter__exact=punter).aggregate(bet_amount_sum=Sum('bet_amount'))['bet_amount_sum']
            returned = Parent.objects.filter(punter__exact=punter).aggregate(bet_return_sum=Sum('bet_return'))['bet_return_sum']
            profit = round(returned - spent,2)
            punting_data.append({'name':punter,'spent':spent,'returned':returned,'profit':profit})
        
        sorted_punting_data = sorted(punting_data, key=lambda k: k['profit'], reverse=True) 
        context['profit_ladder'] = sorted_punting_data[0]
            
        odds_data = {}
        for punter in punters:
            total_spent = Parent.objects.filter(punter__exact=punter).aggregate(bet_amount_sum=Sum('bet_amount'))['bet_amount_sum']
            bet_count = Parent.objects.filter(punter__exact=punter).annotate(bet_amount_count=Count('bet_amount'))
            sum_product = sum([bet.bet_amount * bet.bet_odds for bet in bet_count])
            weighted_ave = sum_product / total_spent
            odds_data[punter] = weighted_ave
        
        sorted_odds = sorted(odds_data.items(), key=lambda x: x[1])
        
        x,y = sorted_odds[0] 
        if x == "Unsanctioned":
            context['odds_ladder'] = sorted_odds[1]
        else:
            context['odds_ladder'] = sorted_odds[0]
            
        return context 

class MultiListView(ListView):
    
    def get_queryset(self):
        self.parent = get_object_or_404(Parent, id=self.kwargs['pk'])
        return Multi.objects.filter(parent=self.parent)
    
    
class LeaderboardView(ListView):
    model = Parent
    context_object_name = 'bets'
    template_name = 'LPC/leaderboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        punts = Parent.objects.all()
        punters = []
        for punt in punts:
            if punt.punter not in punters:
                punters.append(punt.punter)

        punting_data = []
        for punter in punters:
            spent = Parent.objects.filter(punter__exact=punter).aggregate(bet_amount_sum=Sum('bet_amount'))['bet_amount_sum']
            returned = Parent.objects.filter(punter__exact=punter).aggregate(bet_return_sum=Sum('bet_return'))['bet_return_sum']
            profit = round(returned - spent,2)
            punting_data.append({'name':punter,'spent':spent,'returned':returned,'profit':profit})
        
        sorted_punting_data = sorted(punting_data, key=lambda k: k['profit'], reverse=True) 
        context['profit_ladder'] = sorted_punting_data
            
        odds_data = {}
        for punter in punters:
            total_spent = Parent.objects.filter(punter__exact=punter).aggregate(bet_amount_sum=Sum('bet_amount'))['bet_amount_sum']
            bet_count = Parent.objects.filter(punter__exact=punter).annotate(bet_amount_count=Count('bet_amount'))
            sum_product = sum([bet.bet_amount * bet.bet_odds for bet in bet_count])
            weighted_ave = sum_product / total_spent
            odds_data[punter] = weighted_ave
        
        sorted_odds = sorted(odds_data.items(), key=lambda x: x[1])
        context['odds_ladder'] = sorted_odds
        
        return context
