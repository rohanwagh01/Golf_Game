import sys
sys.path.append('/var/jail/home/team36/golfgame')
from database_manager import *

cols_to_vals = {"antiquewhite": "250,235,215", "aquamarine": "127,255,212", "lightpink": "255,182,193", "lightseagreen": "32,178,170", "sandybrown": "244,164,96", "tomato": "255,99,71", "royalblue": "65,105,225", "peru": "205,133,63", "plum": "221,160,221", "powderblue": "176,224,230", "mediumslateblue": "123,104,238", "mediumpurple": "147,112,219", "lightsteelblue": "176,196,222", "lightskyblue": "135,206,250", "lightcoral": "240,128,128"}
def request_handler(request):
    """
    this is where a bulk of the in game work will be done
    """

    if request['method'] == "POST":
        val_dict = request['form']
    else:
        val_dict = request['values']
    
    ##get the user
    username = val_dict["user"]
    return cols_to_vals[get_color(username)]