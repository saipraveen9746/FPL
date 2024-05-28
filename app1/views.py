from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect,get_object_or_404
import requests
from django.views.generic import ListView
from django.contrib import messages
from .forms import TeamCreationForm
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator


# Create your views here.
def login(request):
    return render(request, 'login.html')
# @login_required


# def home(request):
#     return render(request, 'home.html')
def Home(request):
    return render(request, 'Home1.html')


def custom_logout(request):
    
    logout(request)
    return redirect('main')





def players_view(request):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    

    if response.status_code == 200:
        data = response.json()

        elements = data.get('elements', [])
        element_types = data.get('element_types', [])
        teams = data.get('teams', [])

        combined_data = []
        for player in elements:
            player_id = player['element_type']
            for position in element_types:
                if position['id'] == player_id:
                    player['position'] = position['singular_name']
                    break

            team_id = player['team']
            for team in teams:
                if team['id'] == team_id:
                    player['team_name'] = team['name']
                    break

            combined_data.append(player)

        context = {'players': combined_data}
        return render(request, 'Playersview.html', context)
    else:
        return render(request, 'error.html', {'error_message': 'Failed to fetch data'})


from django.shortcuts import render
from .models import Player
import requests

def player_save(request):
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        players_data = data.get('elements', [])  

        for player_data in players_data:
            web_name = player_data.get('web_name')
            first_name = player_data.get('first_name')
            second_name = player_data.get('second_name')
            team = player_data.get('team')
            element_type = player_data.get('element_type')
            minutes = player_data.get('minutes')
            goals_scored = player_data.get('goals_scored')
            assists = player_data.get('assists')
            clean_sheets = player_data.get('clean_sheets')
            saves = player_data.get('saves')
            photo = player_data.get('photo')
            influence = player_data.get('influence')
            total_points = player_data.get('total_points')
            selected_by_percent = player_data.get('selected_by_percent')
            value_form = player_data.get('value_form')
            value_season = player_data.get('value_season')

     
            player, created = Player.objects.get_or_create(
                web_name=web_name,
                first_name=first_name,
                second_name=second_name,
                defaults={
                    'team': team,
                    'element_type': element_type,
                    'minutes': minutes,
                    'goals_scored': goals_scored,
                    'assists': assists,
                    'clean_sheets': clean_sheets,
                    'saves': saves,
                    'photo': photo,
                    'influence': influence,
                    'total_points': total_points,
                    'selected_by_percent': selected_by_percent,
                    'value_form': value_form,
                    'value_season': value_season
                }
            )

   
            player.save()

        return render(request, 'success_template.html', {'message': 'Data saved successfully'})
    else:
        return render(request, 'success_template.html', {'message': 'Failed to fetch data from the API'})

def Plsave(request):
    team_names = {
        1:'Arsenal',
        2:'Aston Villa',
        3:'Bournemouth',
        4:'Brentford',
        5:'Brighton',
        6:'Burnley',
        7:'Chelsea',
        8:'Crystal Palace',
        9:'Everton',
        10:'Fulham',
        11:'Liverpool',
        12:'Luton',
        13:'Man city',
        14:'Man United',
        15:'Newcastle United',
        16:'Nottingham Forest',
        17:'Sheffield Unied',
        18:'Spurs',
        19:'West Ham',
        20:'Wolves'


    }


    players = Player.objects.all()  # Retrieve all Player objects

    for player in players:
        team_number = player.team
        if team_number in team_names:
            player.team_name = team_names[team_number]
            player.save()

    return HttpResponse("Teams updated successfully")
    


def Position(request):
    team_elementsss = {
        1:"Goalkeeper",
        2:"Defender",
        3:"Midfielder",
        4:"Forward"
    }

    position = Player.objects.all()
    for i in position:
        position_num = i.element_type
        if position_num in team_elementsss:
            i.position = team_elementsss[position_num]
            i.save()
    return HttpResponse('position updated successfully')
    


class PlayerList(ListView):
    model = Player
    template_name = 'Playersview.html'

    
# from django.http import JsonResponse


# def get_product_list(request):
#     data = list(Player.objects.values('web_name', 'photo'))
#     return JsonResponse({'data': data})


# yourapp/management/commands/clear_data.py

def Topratedplayer(request):
    highest_player = Player.objects.order_by('-total_points')
    for rank, player in enumerate(highest_player, start=1):
        player.rank = rank
    return render(request, 'highestplayers.html',{'highest_points_players': highest_player})


from django.shortcuts import render, redirect
from django.views import View
from .models import Player, Team, PlayerInTeam
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import TeamCreationForm



@method_decorator(login_required, name='dispatch')
class CreateTeamView(View):
    template_name = 'create_team.html'

    def get(self, request):
       
        form = TeamCreationForm()

        context = {
            'form': form,
        }
        return render(request, self.template_name,context)
    
    def post(self, request):
        form = TeamCreationForm(request.POST)

        if form.is_valid():
           
            team_name = form.cleaned_data['team_name']
            user = request.user

          
            team = Team.objects.create(name=team_name, user=user)

            return redirect('add_players', team_id=team.id)


        context = {
            'form': form,
        }

        return render(request, self.template_name, context)




# @method_decorator(login_required, name='dispatch')
# class AddPlayersView(View):
#     template_name = 'add_players.html'

#     def get(self, request, team_id):
#         team = Team.objects.get(id=team_id)
#         players = Player.objects.all()

#         context = {
#             'team': team,
#             'players': players,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, team_id):
#         team = Team.objects.get(id=team_id)
#         player_ids = request.POST.getlist('player_ids')
        
#         for player_id in player_ids:
#             player = Player.objects.get(id=player_id)
#             try:
#                 team.add_player(player)
#             except ValueError as e:
#                 error_message = str(e)
#                 context = {
#                  'team': team,
#                  'players': Player.objects.all(),
#                  'error_message': error_message,
#                 }
#                 return render(request, self.template_name, context)
#         return redirect('team_detail', team_id=team_id)

        
    




def calculate_points(self):
    playerpoint = Player.objects.filter(total_points)

    players_in_team = PlayerInTeam.objects.filter(team=self)
    total_points = 0
    for player_in_team in players_in_team:
        player = player_in_team.player
        previous_points = player.total_points
        if player.total_points > previous_points:
            increased_points = player.total_points - previous_points
            total_points += increased_points
                

        
    self.total_points = total_points
    self.save()



# @method_decorator(login_required, name='dispatch')
# class AddPlayersView(View):
#     template_name = 'add_players.html'

#     def get(self, request, team_id):
#         team = Team.objects.get(id=team_id)
#         available_players = Player.objects.exclude(id__in=team.players.values_list('id', flat=True))
#         form = TeamCreationForm()

#         context = {
#             'team': team,
#             'available_players': available_players,
#             'form': form,
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, team_id):
#         team = get_object_or_404(Team, id=team_id)
#         available_players = Player.objects.exclude(id__in=team.players.values_list('id', flat=True))
#         form = TeamCreationForm(request.POST)

#         if form.is_valid():
#             player_ids = form.cleaned_data['player_ids']  # Ensure that the form has a 'player_ids' field

#             for player_id in player_ids:
                
#                 try:
#                     player = Player.objects.get(id=player_id)
#                     team.add_player(player)
#                 except ValueError as e:
#                     form.add_error(None, str(e))
#                     return render(request, self.template_name, {'team': team, 'available_players': available_players, 'form': form})

#             return redirect('team_detail', team_id=team_id)

#         context = {
#             'team': team,
#             'available_players': available_players,
#             'form': form,
#         }

#         return render(request, self.template_name, context)


def CreateYourTeam(request):
    return render(request, 'addplayers.html')


# def position_select(request, position):
#     homes = Player.objects.filter(Position=position)  # Assuming Category is a field in your Home model
#     return render(request, 'template_name.html', {'homes': homes})


def position_select(request):
    if request.method == 'GET' and request.is_ajax():
        position = request.GET.get('position')
        players = Player.objects.filter(Position=position)
        player_list = [{'name': player.name, 'id': player.id} for player in players]
        return JsonResponse({'players': player_list})
    else:
        return JsonResponse({'error': 'Invalid request'})
    



# class CategoryView(ListView):
#     model = Player
#     template_name = 'addplayers.html'

#     def get_queryset(self):
#         category = self.kwargs.get('category')
#         queryset = Player.objects.filter(position=category)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = self.kwargs.get('category')
#         context['category_players'] = Player.objects.filter(position=category)
#         return context

# class GetPlayersView(View):
#     def get(self, request, category):
#         players = Player.objects.filter(position=category)
#         players1 = players.order_by('-total_points')
#         data = [{'web_name': player.web_name} for player in players1]
#         return JsonResponse(data, safe=False)
    



class GetPlayersView(View):
    def get(self, request, category):
        # Fetch players based on the category
        players = Player.objects.filter(position=category)

        # Order players by total_points
        players = players.order_by('-total_points')
        paginator = Paginator(players,15)
        page_number=request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Construct data dictionary with desired fields
        data = []
        for player in players:
            player_data = {
                'web_name': player.web_name,
                'team_name': player.team_name,
                'total_points': player.total_points,
                'value_season': player.value_season,
                'photo': player.photo # Assuming photo is a FileField or ImageField
            }
            data.append(player_data)

        return JsonResponse(data, safe=False)
