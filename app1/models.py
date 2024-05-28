from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Player(models.Model):
    web_name = models.CharField(max_length=100,blank=True)
    first_name = models.CharField(max_length=100,blank=True)
    second_name = models.CharField(max_length=100,blank=True)
    team = models.IntegerField(default=0)
    element_type = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    assists= models.IntegerField(default=0)
    clean_sheets = models.IntegerField(default=0)
    saves = models.IntegerField(default=0)
    photo= models.URLField(blank=True,null=True)
    position= models.CharField(max_length=200,blank=True)
    team_name= models.CharField(max_length=200,blank=True)
    influence = models.DecimalField(decimal_places=3,max_digits=7,default=0.0)
    total_points = models.IntegerField(default=0)
    selected_by_percent = models.CharField(max_length=200,blank=True)
    value_form = models.CharField(max_length=200,blank=True)
    value_season = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.web_name




class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    budget = models.DecimalField(decimal_places=2, max_digits=10, default=100.00)
    total_points = models.IntegerField(default=0)

    players = models.ManyToManyField(Player, through='PlayerInTeam',related_name='teams')

    
    def add_player(self, player, is_captain=False, is_vice_captain=False):
        if self.is_position_limit_exceeded(player.position):
            raise ValueError(f"Position limit exceeded for position {player.position}")

        value_season_decimal = Decimal(player.value_season)

        if self.budget < value_season_decimal:
            raise ValueError("Not enough budget to add this player")

        if self.players.filter(id=player.id).exists():
            raise ValueError("Player is already in the team")

        

        # Create player_in_team without saving it
        player_in_team = PlayerInTeam.objects.create(
            team=self,
            player=player,
            is_captain=is_captain,
            is_vice_captain=is_vice_captain,
            
        )

        # Save player_in_team to calculate total_points
        

        self.budget -= value_season_decimal
        self.calculate_points()
        self.save()

        return player_in_team

    

    def is_budget_enough(self, player, is_captain=False, is_vice_captain=False):
  
        value_season_decimal = Decimal(player.value_season)

        if self.budget < value_season_decimal:
            raise ValueError("Not enough budget to add this player")


        player_in_team = PlayerInTeam.objects.create(
            player=player,
            team=self,
            is_captain=is_captain,
            is_vice_captain=is_vice_captain
            )


        self.budget -= value_season_decimal
        self.total_points+=player_in_team.calculate_points()
        self.save()

    def is_position_limit_exceeded(self, position):
            max_goalkeepers = 2
            max_defenders = 5
            max_midfielders = 5
            max_forwards = 3
            
            goalkeepers_count = self.players.filter(position='Goalkeeper').count()
            defenders_count = self.players.filter(position='Defender').count()
            midfielders_count = self.players.filter(position='Midfielder').count()
            forwards_count = self.players.filter(position='Forward').count()
            
            
            if position == 'Goalkeeper' and goalkeepers_count >= max_goalkeepers:
                return True
            elif position == 'Defender' and defenders_count >= max_defenders:
                return True
            elif position == 'Midfielder' and midfielders_count >= max_midfielders:
                return True
            elif position == 'Forward' and forwards_count >= max_forwards:
                return True

           
            return False

    # def calculate_points(self):
    
    #     players_in_team = PlayerInTeam.objects.filter(team=self)
    #     total_points = 0

    #     for player_in_team in players_in_team:
            
    #         player = player_in_team.player

            
    #         if player.total_points > player_in_team.total_points:
                
    #             increased_points = player.total_points - player_in_team.total_points

                
    #             if player_in_team.is_captain:
    #                 increased_points *= 2

                
    #             total_points += increased_points

        
        # self.total_points = total_points
        # self.save()
    
    def add_player(self, player, is_captain=False, is_vice_captain=False):
        if self.is_position_limit_exceeded(player.position):
            raise ValueError(f"Position limit exceeded for position {player.position}")

        # Check budget limit before adding a player
        if self.budget < Decimal(player.value_season):
            raise ValueError("Not enough budget to add this player")

        # Check if the player is already in the team
        if self.players.filter(id=player.id).exists():
            raise ValueError("Player is already in the team")

        # Add the player to the team
        player_in_team = PlayerInTeam.objects.create(
            team=self,
            player=player,
            is_captain=is_captain,
            is_vice_captain=is_vice_captain
        )

        # Update the budget
        self.budget -= Decimal(player.value_season)
        self.total_points 
        self.save()


class PlayerInTeam(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)
    is_vice_captain = models.BooleanField(default=False)
    total_points = models.IntegerField(default=0)  




@receiver(post_save, sender=Player)
def update_team_total_points(sender, instance, **kwargs):
  
    player_in_teams = PlayerInTeam.objects.filter(player=instance)
    for player_in_team in player_in_teams:
        increased_points = instance.total_points - player_in_team.total_points
        player_in_team.total_points = instance.total_points
        player_in_team.save()

        if increased_points > 0:
 
            team = player_in_team.team
            team.total_points += increased_points
            team.save()
