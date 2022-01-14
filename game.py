import sys
sys.path.append('/var/jail/home/team36/golfgame')
from database_manager import *
from website import getmaingame, gettitlescreen, getpairingscreen, getmenuscreen, getwinscreen
import math
import requests

def returnCurrentState():
    if get_state() == "START":
        return gettitlescreen()
    if get_state() == "PLAYING":
        return getmaingame()
    if get_state() == "MENU":
        return getmenuscreen()
    if get_state() == "PAIRING":
        return getpairingscreen()
    if get_state() == "END":
        return getwinscreen()


def request_handler(request):
    """
    this is where a bulk of the in game work will be done
    """

    if request['method'] == "POST":
        val_dict = request['form']
    else:
        val_dict = request['values']
        return returnCurrentState()


    ##either way use the information inside to knwo what to do to the state and website
    if get_state() == "START":
        ##if the website sent a get request saying that the action is start game then move to playing
        try:
            val_dict['action']
        except:
            return returnCurrentState()
        if val_dict['action'] == "start":
            ##move all players balls to the start location
            create_holes()
            set_up_hole(1)
            update_game(state="PLAYING")
            return getmaingame()
        elif val_dict['action'] == "update":
            ###there will be a form on the website that serves as the menu, this will send information in the request
            #that can be looked at here and used to update the setting of the game
            ###
            if 'weather' in val_dict:
                update_game(weather=int(val_dict["weather"]))
                #return "Weather Updated"
            if 'difficulty' in val_dict:
                update_game(difficulty=val_dict["difficulty"])
                #return "Reset Difficulty"
            if "clear" in val_dict:
                clear_users()
                #return "Users Cleared"
            #get the info from the websites initial page and update the settings accordingly
            ###
            return gettitlescreen()
        else:
            return returnCurrentState()
    if get_state() == "PLAYING":
        try:
            val_dict['action']
        except:
            return returnCurrentState()

        if val_dict['action'] == 'color':
            users_list = get_all_users()
            output = []
            for user in users_list:
                output.append(get_color(user))
            return output
        elif val_dict['action'] == 'get_pos':
            users_list = get_all_users()
            output = []
            for user in users_list:
                output.append(get_ball_location(user))
            return output
        elif val_dict['action'] == 'swing':
            user = val_dict['user']
            if not is_active(user):
                return "Player already made SUNK IT"
            game_difficulty = get_difficulty()
            ###
            #get swing info from the val_dict
            ###
            swing_power = float(val_dict["max"])
            add_angle = -float(val_dict["angle"])
            add_angle = add_angle*(math.pi/180)
            min_power = float(val_dict["a_low"])
            max_power = float(val_dict["a_high"])
            frac_of_max = (swing_power - min_power)/(max_power - min_power)
            ###
            #get angle to hole
            ###
            current_loc = get_ball_location(user)
            goal = get_hole_location(get_hole())
            d_x = goal[0]-current_loc[0]
            d_y = current_loc[1]-goal[1]
            ###find the total disstance, based on where we are, and divide to find the max distance
            current_info = get_affect(get_hole(), current_loc)
            ###travel distance
            t_d = current_info[0]*frac_of_max
            if game_difficulty == "HARD":
                swing_sensitivity = 3.5
            elif game_difficulty == "MEDIUM":
                swing_sensitivity = 2
            else:
                swing_sensitivity = 1
            t_d = t_d*(1-(0.1*(swing_sensitivity)))
            ##use angle to find x and y ####change to degrees later#####
            try:
                angle = math.atan(d_y/d_x)
            except:
                angle = math.pi
            angle = angle + add_angle + (current_info[1]*swing_sensitivity)*(math.pi/180)
            if d_x < 0: #in the bottom quadrants
                    angle = angle+math.pi
            d_x = int(math.cos(angle)*t_d)
            d_y = int(math.sin(angle)*t_d)
            ###
            #Now update with weather
            ###
            if get_weather():
                wind_speed = 0
                URL = "http://api.openweathermap.org/data/2.5/weather?q=Boston&appid=4511a3656229a5478afde63c8f5eba91"
                r = requests.get(url = URL)
                data = r.json()
                wind_speed = data["wind"]["speed"]
                wind_dir = data["wind"]["deg"]
                wind_speed = 15
                wind_dir = 180
                wind_dir_rad = wind_dir*math.pi/180
                ##wind should be scaled based on the distance the ball would go, like the t_d value
                wind_td = t_d*wind_speed/75
                wind_dx = math.sin(wind_dir_rad) * wind_td
                wind_dy = math.cos(wind_dir_rad) * wind_td
                d_x += wind_dx
                d_y += wind_dy
            #minus to flip the axis back
            move_ball(user, d_x, -d_y)
            ##
            #Check if the ball is out of bounds
            ##
            new_location = get_ball_location(user)
            new_info = get_affect(get_hole(), new_location)
            if new_location[0] < 0 or new_location[1] < 0 or new_location[0] > 1440 or new_location[1] > 700:
                new_info = "stroke_penalty"
            if new_info == "stroke_penalty":
                move_ball(user, -d_x, d_y)
                score = increase_score(user)
                return "Moved STROKE PENALTY"
            ###
            #someway of knowing if the ball hit the hole on this course and if so then set inactive and all that jazz, once all inactive then move to next hole
            ###
            nd_x = goal[0]-new_location[0]
            nd_y = goal[1]-new_location[1]
            ##find how far needed to make it into hole
            if game_difficulty == "HARD":
                dist_to_hole = 10
            elif game_difficulty == "MEDIUM":
                dist_to_hole = 20
            else:
                dist_to_hole = 30
            if math.sqrt(nd_x**2 + nd_y**2) < dist_to_hole:
                #made it into the hole
                set_active(user, active=False)
                score = increase_score(user)
                ##check if all the players made it
                active_list = get_active_users()
                if not active_list: #is empty
                    if get_hole() == 18:
                        #switch to the endgame
                        update_game(state="END")
                        return getwinscreen()
                    set_up_hole(get_hole()+1)
                    insertchange()
                    return getmaingame()
                return "Player Made It"
            ##check if all the players made it
            active_list = get_active_users()
            if not active_list: #is empty
                if get_hole() == 18:
                    #switch to the endgame
                    update_game(state="END")
                    return getwinscreen()
                set_up_hole(get_hole()+1)
                insertchange()
                return getmaingame()
            score = increase_score(user)
            return "Moved Ball to " + str(math.sqrt(nd_x**2 + nd_y**2)) + ". User's score is now " + str(score)
        elif val_dict['action'] == 'menu':
            update_game(state="MENU")
            return getmenuscreen()
        elif val_dict['action'] == 'reset': #complete reset of the game, as if it was just turned on
            reset_game()
            return "Reset Game"
        else:
            return returnCurrentState()
    if get_state() == "MENU": #a different state to prevent someone from hitting the ball while the menu is pulled up
        if 'weather' and 'difficulty' in val_dict:
            update_game(weather=int(val_dict["weather"]))
            update_game(difficulty=val_dict["difficulty"])
            return getmenuscreen()
        elif 'weather' in val_dict:
            update_game(weather=int(val_dict["weather"]))
            return getmenuscreen()
        elif 'restart' in val_dict:
            reset_game()
            return gettitlescreen()
        elif 'difficulty' in val_dict:
            update_game(difficulty=val_dict["difficulty"])
            return getmenuscreen()
        elif 'return' in val_dict:
            update_game(state="PLAYING")
            return getmaingame()
        elif 'skip' in val_dict:
            update_game(state="PLAYING")
            active_us = get_active_users()
            for user in active_us:
                for i in range(10):
                    increase_score(user)
            if get_hole() == 18:
                #switch to the endgame
                update_game(state="END")
                return getwinscreen()
            set_up_hole(get_hole()+1)
            insertchange()
            return getmaingame()
        else:
            return returnCurrentState()
    if get_state() == "END":
        if 'restart' in val_dict:
            reset_game()
            return gettitlescreen()
