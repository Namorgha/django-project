from django.contrib import admin
from .models import GameModel

class GameModelAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'get_players']  # Display room name and players in the list view
    readonly_fields = ['get_players']  # Make players read-only in the admin form
    exclude = ['players']  # Hide the default multi-select box for players

    # A simple method to display players in the current game room
    def get_players(self, obj):
        return ", ".join([player.username for player in obj.players.all()])  # Display usernames of players
    
    get_players.short_description = 'Players in this Room'  # Set a label for the column

# Register the GameModel with the custom admin
admin.site.register(GameModel, GameModelAdmin)

