import asyncio
from concurrent.futures import ProcessPoolExecutor
import json
from copy import deepcopy

import constants
import config
from config import init_logging
import logging

import user

from teams import load_team
from showdown.run_battle import pokemon_battle
from showdown.websocket_client import PSWebsocketClient
from teams import team_generator

from data import all_move_json
from data import pokedex
from data.mods.apply_mods import apply_mods

import random

logger = logging.getLogger(__name__)


def check_dictionaries_are_unmodified(original_pokedex, original_move_json):
    # The bot should not modify the data dictionaries
    # This is a "just-in-case" check to make sure and will stop the bot if it mutates either of them
    if original_move_json != all_move_json:
        logger.critical("Move JSON changed!\nDumping modified version to `modified_moves.json`")
        with open("modified_moves.json", 'w') as f:
            json.dump(all_move_json, f, indent=4)
        exit(1)
    else:
        logger.debug("Move JSON unmodified!")

    if original_pokedex != pokedex:
        logger.critical("Pokedex JSON changed!\nDumping modified version to `modified_pokedex.json`")
        with open("modified_pokedex.json", 'w') as f:
            json.dump(pokedex, f, indent=4)
        exit(1)
    else:
        logger.debug("Pokedex JSON unmodified!")

async def showdown(user):

    original_pokedex = deepcopy(pokedex)
    original_move_json = deepcopy(all_move_json)

    ps_websocket_client = await PSWebsocketClient.create(user.username, user.password, config.websocket_uri)
    await ps_websocket_client.login()

    battles_run = 0
    wins = 0
    losses = 0
    while True:
        team = load_team(user.team_name)
        if user.bot_mode == constants.CHALLENGE_USER:
            await asyncio.sleep(3)
            await ps_websocket_client.challenge_user(user.user_to_challenge, config.pokemon_mode, team)
        elif user.bot_mode == constants.ACCEPT_CHALLENGE:
            await ps_websocket_client.accept_challenge(config.pokemon_mode, team, config.room_name)
        elif user.bot_mode == constants.SEARCH_LADDER:
            await ps_websocket_client.search_for_match(config.pokemon_mode, team)
        else:
            raise ValueError("Invalid Bot Mode")

        winner = await pokemon_battle(ps_websocket_client, config.pokemon_mode)

        if winner == user.username:
            wins += 1
        else:
            losses += 1

        logger.info("W: {}\tL: {}".format(wins, losses))

        check_dictionaries_are_unmodified(original_pokedex, original_move_json)

        battles_run += 1
        if battles_run >= config.run_count:
            break

if __name__ == "__main__":
    config.parse_args()
    apply_mods(config.pokemon_mode)

    types = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

    teamALoc = team_generator.generateTeam(random.choice(types))
    teamBLoc = team_generator.generateTeam(random.choice(types))

    user1 = user.User("epsilonbot",  teamALoc, "CHALLENGE_USER", "epsilonbot2")
    user2 = user.User("epsilonbot2", teamBLoc, "ACCEPT_CHALLENGE")

    loop = asyncio.get_event_loop()

    loop.run_until_complete(asyncio.gather(
        showdown(user1), showdown(user2)
    ))
