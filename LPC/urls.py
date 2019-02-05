from django.urls import path
#from . import views
from .views import ParentListView, MultiListView, LeaderboardView

app_name = 'LPC'
urlpatterns = [
        # /LPC/
        path('', ParentListView.as_view(), name='parent_list'),
        # /LPC/detail/
        path('<int:pk>/', MultiListView.as_view(), name='multi_list'),
        # /LPC/leaderboard/
        path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
        ]