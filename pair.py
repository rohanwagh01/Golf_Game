#This is the script to handle incoming pair requests from clubs
import sys
sys.path.append('/var/jail/home/team36/golfgame')
from database_manager import *
from website import getpairingscreen, gettitlescreen
import sqlite3
golf_db = '/var/jail/home/team36/golfgame/golf.db'

def request_handler(request):
    """
    manages the pairing of the clubs
    """
    val_dict = request["form"]
    if "users" in val_dict and get_state() == "PAIRING": #if this is sending a list of users to add and the website is ready to pair club
        add_users(val_dict["users"])
        return "Added"
    elif "users" in val_dict and get_state() == "START":
        return "Not PAIRING Mode"
    else: #website saying to change to pairing mode
        if get_state() == "START":
            update_game(state="PAIRING")
            return getpairingscreen()
        elif get_state() == "PAIRING":
            update_game(state="START")
            return gettitlescreen()
            #change back to start, no longer trying to pair club
        return "Updated State to " + get_state()
