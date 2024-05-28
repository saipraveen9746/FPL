

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from app1 import views
from .views import PlayerList,CreateTeamView,CreateYourTeam,position_select,GetPlayersView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.custom_logout, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    
    path('',views.Home,name='main'),
    path('players/', views.players_view, name='players_view'),
    path('playersave/',views.player_save,name='player_save'),
    path('playerlist/',PlayerList.as_view(),name='player-list'),
    path('highestview/',views.Topratedplayer,name='top-rated'),
    path('create-team/', CreateTeamView.as_view(), name='create_team'),
    path('create-your-team/',views.CreateYourTeam,name='createyourteam'),
    path('positioncategory/<str:position>/', views.position_select, name='position-select'),
    # path('add-players/<int:team_id>/',AddPlayersView.as_view(), name='add_players'),
    # path('team-detail/<int:team_id>/',TeamDetailView.as_view(), name='team_detail'),
    
    path('plsave/',views.Plsave,name='pl-save'),
    path('position/',views.Position,name='position'),
    # path('category/<str:category>/', CategoryView.as_view(), name='category_view'),
     path('get_players/<str:category>/', GetPlayersView.as_view(), name='get_players'),

 
        

    

    
]

