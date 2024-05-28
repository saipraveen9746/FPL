from django.core.management.base import BaseCommand
from app1.models import Player  # Import your Player model


class Command(BaseCommand):
    help = 'Updates photo URLs for players'

    def handle(self, *args, **options):
        players = Player.objects.all()
        for player in players:
            # Check if player has a photo URL
            if player.photo:
                # Update photo URL
                player.photo = f"https://resources.premierleague.com/premierleague/photos/players/250x250/p{player.photo.replace('.jpg', '.png')}"
                player.save()

        self.stdout.write(self.style.SUCCESS('Photo URLs updated successfully'))
