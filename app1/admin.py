from django.contrib import admin
from .models import Player,PlayerInTeam,Team


# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(PlayerInTeam)