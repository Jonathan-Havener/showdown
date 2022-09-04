import constants

class User():
    username = None
    password = None
    bot_mode = None
    user_to_challenge = None


    def __init__(self, username, password, bot_mode, user_to_challenge = None):
        self.username = username
        self.password = password
        self.bot_mode = bot_mode

        if self.bot_mode == constants.CHALLENGE_USER:
            self.user_to_challenge = user_to_challenge
        