import sys
import logging
import constants
from environs import Env



battle_bot_module = None
websocket_uri = None
team_name = None
pokemon_mode = None
run_count = None
gambit_exe_path = ""
greeting_message = 'hf'
battle_ending_message = 'gg'
room_name = None
use_relative_weights = False
damage_calc_type = 'average'
search_depth = 2
dynamic_search_depth = False
save_replay = True

def parse_args():
    env = Env()
    env.read_env()
    
    global battle_bot_module
    global save_replay
    global use_relative_weights
    global gambit_exe_path
    global search_depth
    global dynamic_search_depth
    global greeting_message
    global battle_ending_message
    global websocket_uri
    global pokemon_mode
    global run_count
    global room_name

    battle_bot_module = env("BATTLE_BOT", 'safest')
    save_replay = env.bool("SAVE_REPLAY", save_replay)
    use_relative_weights = env.bool("USE_RELATIVE_WEIGHTS", use_relative_weights)
    gambit_exe_path = env("GAMBIT_PATH", gambit_exe_path)
    search_depth = int(env("MAX_SEARCH_DEPTH", search_depth))
    dynamic_search_depth = env.bool("DYNAMIC_SEARCH_DEPTH", dynamic_search_depth)
    greeting_message = env("GREETING_MESSAGE", greeting_message)
    battle_ending_message = env("BATTLE_OVER_MESSAGE", battle_ending_message)
    websocket_uri = env("WEBSOCKET_URI", "sim.smogon.com:8000")
    pokemon_mode = env("POKEMON_MODE", constants.DEFAULT_MODE)
    run_count = int(env("RUN_COUNT", 1))
    room_name = env("ROOM_NAME", room_name)

    init_logging(env("LOG_LEVEL", "DEBUG"))


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.module = "[{}]".format(record.module)
        record.levelname = "[{}]".format(record.levelname)
        return "{} {}".format(record.levelname.ljust(10), record.msg)


def init_logging(level):
    websockets_logger = logging.getLogger("websockets")
    websockets_logger.setLevel(logging.INFO)
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.INFO)

    logger = logging.getLogger()
    logger.setLevel(level)
    default_formatter = CustomFormatter()
    default_handler = logging.StreamHandler(sys.stdout)
    default_handler.setFormatter(default_formatter)
    logger.addHandler(default_handler)

