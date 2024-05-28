from django import forms
from .models import Player

class TeamCreationForm(forms.Form):
    team_name = forms.CharField(max_length=100, label='Team Name')
    