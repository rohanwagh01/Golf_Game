import sys
import sqlite3
import datetime
import math
import json

sys.path.append("/var/jail/home/team36/golfgame")
from database_manager import *

def request_handler(request):
    users = get_all_users()
    output = []
    for user in users:
        output.append((user + ": ", str(get_score(user))))
    output.sort(key=lambda pair: pair[1])
    #make string representation of table
    output_str = ""
    for val in output:
        output_str = output_str + val[0] + val[1] + "\n"
    return output_str

