import constants
import glob, os

class User():
    username = None
    password = None
    team_name = None
    bot_mode = None
    user_to_challenge = None
    wins = 0
    losses = 0

    def __init__(self, username, team_name, bot_mode, user_to_challenge = None):

        self.username = username
        # with open("C:/Users/jonah/Desktop/Programs/FantasyPokemonWebApp/showdown/password.txt") as f:
        #     self.password = f.readlines()
        self.team_name = team_name
        self.bot_mode = bot_mode

        if self.bot_mode == constants.CHALLENGE_USER:
            self.user_to_challenge = user_to_challenge
        