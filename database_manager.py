###
#Used to update and manage the database, can be imported into any of the other scripts to helkp with database stuff
###

import sqlite3
import random
from PIL import Image
import datetime
golf_db = '/var/jail/home/team36/golf.db'

###database has three tables
##user_table
#stores the format "user1,user2,user3,user4....."
##game_state
#stores the format (settings)**Will be added later**, game_state text
##player_info
#stores the format "user, ball lat int, ball lon int, active boolean"
##Hole Information
#stores the info about each hole as a number and hole location

############### Managing user information ######################
colors = ["antiquewhite", "aquamarine", "lightpink", "lightseagreen", "sandybrown", "tomato", "royalblue", "peru", "plum", "powderblue", "mediumslateblue", "mediumpurple", "lightsteelblue", "lightskyblue", "lightcoral"]


def add_users(user_list_or_str):
    """
    gets a list of users updates the table with the users, alslo updates the player_info with default information
    returns none
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_table (users text);''')
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    current_list = []
    db_info = c.execute('''SELECT * FROM user_table''').fetchall()
    for row in db_info:
        existing = row[0]
    try:
        existing = existing.split(",")
        current_list = existing
    except:
        pass
    #now I have a list of the existing users, in order
    if isinstance(user_list_or_str, str):
        current_list.extend(user_list_or_str.split(","))
    else:
        current_list.extend(user_list_or_str)
    current_list = set(current_list) #remove repeated users adn empty user from splitting
    try:
        current_list.remove("")
    except:
        pass
    ##now find the new users and add them to player_info_table
    for user in current_list:
        color_ind = random.randint(0,14)
        color = colors[color_ind]
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (user,0,0,1,0,color))
    current_list = list(current_list)
    #now add this list to the database
    db_input = current_list[0]
    for user in current_list[1:]:
        db_input += "," + user
    c.execute('''INSERT into user_table VALUES (?);''', (db_input,))
    conn.commit()
    conn.close()
    return current_list

def get_all_users(returnlist=True):
    """
    returns all the users in the game, doesn't matter if active or not
    toggle returnlist to return the list of the string format
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_table (users text);''')
    db_info = c.execute('''SELECT * FROM user_table''').fetchall()
    current = ""
    for row in db_info:
        current = row[0]
    #now have hte most recent one
    conn.commit()
    conn.close()
    if returnlist:
        #turn into list and return the list
        return current.split(',')
    else:
        return current

def clear_users():
    """
    clears the users db by adding an empty string
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_table (users text);''')
    c.execute('''INSERT into user_table VALUES (?);''', ("",))
    conn.commit()
    conn.close()

def get_active_users():
    """
    Gets and returns all the active users in the game
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_list = get_all_users()
    output_list = []
    for user in user_list:
        user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
        for info in user_info:
            state = info
        try:
            if state[3] == 1:
                output_list.append(user)
        except:
            pass
    conn.commit()
    conn.close()
    return output_list

def is_active(user):
    """
    returns whether a user is active or not
    """
    active_users = get_active_users()
    if user in active_users:
        return True
    return False

def set_active(user, active=True):
    """
    Sets a user to be active of unactive
    """
    if active:
        inp = 1
    else:
        inp = 0
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    for info in user_info:
        recent = info
    try:
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (user,recent[1],recent[2],inp,recent[4],recent[5]))
    except:
        conn.commit()
        conn.close()
        return "FAILED"
    conn.commit()
    conn.close()

def increase_score(user):
    """
    Increments user score
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    #recent = [user, 0, 0, 1, 0, get_color(user)]
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    for info in user_info:
        recent = info
    try:
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (user,recent[1],recent[2],recent[3],recent[4]+1,recent[5]))
    except:
        conn.commit()
        conn.close()
        return "FAILED"
    conn.commit()
    conn.close()
    return recent[4]+1

def get_score(user):
    """
    Increments user score
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    for info in user_info:
        recent = info
    return recent[4]

def get_color(user):
    """
    Increments user score
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    #recent = [user, 0, 0, 1, 0, "here"]
    for info in user_info:
        recent = info
    conn.commit()
    conn.close()
    return recent[5]

############### Managing Game information ######################
def reset_game():
    """
    start or reset the game
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    c.execute('''INSERT into game_state_table VALUES (?,?,?,?);''', (1,"MEDIUM",0,"START"))
    ###clear playerinfo
    user_list = get_all_users()
    for user in user_list:
        conn.commit()
        conn.close()
        color = get_color(user)
        conn = sqlite3.connect(golf_db)
        c = conn.cursor()
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (user,0,0,1,0,color))
    conn.commit()
    conn.close()
    create_holes()
    #clear_users()

def get_hole():
    """
    returns the hole that the game is in
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    user_info = c.execute('''SELECT hole FROM game_state_table''').fetchall()
    for info in user_info:
        recent = info
    conn.commit()
    conn.close()
    return recent[0]

def get_difficulty():
    """
    returns the difficulty that the game is in
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    user_info = c.execute('''SELECT difficulty FROM game_state_table''').fetchall()
    for info in user_info:
        recent = info
    conn.commit()
    conn.close()
    try:
        return recent[0]
    except:
        return "MEDIUM"

def get_weather():
    """
    returns the weather that the game is in
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    user_info = c.execute('''SELECT weather FROM game_state_table''').fetchall()
    for info in user_info:
        recent = info
    conn.commit()
    conn.close()
    try:
        if recent[0] == 1:
            return True
        else:
            return False
    except:
        return False

def get_state():
    """
    returns the state that the game is in
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    user_info = c.execute('''SELECT state FROM game_state_table''').fetchall()
    for info in user_info:
        recent = info
    conn.commit()
    conn.close()
    try:
        return recent[0]
    except:
        return "START"

def update_game(hole="Current",difficulty="Current",weather="Current",state="Current"):
    """
    changess the hole the game is in
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game_state_table (hole int, difficulty text, weather int, state text);''')
    user_info = c.execute('''SELECT * FROM game_state_table''').fetchall()
    #recent = [1,"MEDIUM",0,"START"]
    for info in user_info:
        recent = info
    if hole == "Current":
        hole = recent[0]
    if difficulty == "Current":
        difficulty = recent[1]
    if weather == "Current":
        weather = recent[2]
    if state == "Current":
        state = recent[3]
    c.execute('''INSERT into game_state_table VALUES (?,?,?,?);''', (hole,difficulty,weather,state))
    conn.commit()
    conn.close()

############### Managing Ball information ######################

def move_ball(user, d_lat, d_lon):
    """
    Moves the ball according to the change in lat and lon
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    #recent = [user, d_lat, d_lon, 1, 1, get_color(user)]
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    for info in user_info:
        recent = info
    try:
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (recent[0],recent[1]+d_lat,recent[2]+d_lon,recent[3],recent[4],recent[5]))
    except:
        pass
    conn.commit()
    conn.close()

def place_ball(user, lat, lon):
    """
    Moves the ball according to the change in lat and lon
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    #recent = [user, lat, lon, 1, 1, get_color(user)]
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    for info in user_info:
        recent = info
    try:
        c.execute('''INSERT into player_table VALUES (?,?,?,?,?,?);''', (recent[0],lat,lon,recent[3],recent[4],recent[5]))
    except:
        pass
    conn.commit()
    conn.close()

def get_ball_location(user):
    """
    getss the ball location for a specific user
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    #recent = [user, 0, 0, 1, 0, get_color(user)]
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    for info in user_info:
        recent = info
    try:
        conn.commit()
        conn.close()
        return (recent[1],recent[2])
    except:
        pass

def get_ball_loccol(user):
    """
    getss the ball location for a specific user
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player_table (user text, lat int, lon int, active int, score int, color text);''')
    user_info = c.execute('''SELECT * FROM player_table WHERE user=?''', (user,)).fetchall()
    conn.commit()
    conn.close()
    #recent = [user, 0, 0, 1, 0, get_color(user)]
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    for info in user_info:
        recent = info
    try:
        conn.commit()
        conn.close()
        return (recent[1],recent[2],recent[5])
    except:
        pass

############### Managing Hole information ######################

def create_holes():
    """
    Resets the hole to hole number one
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hole_table (hole int, lat int, lon int, start_lat int, start_lon int);''')
    holes_locations = {1:(1052,280, 148, 221), 2:(1116,149,100,135), 3:(1122,129,100,185), 4:(1058,220,175,150), 5:(1098,197,105,302), 6:(950,220,125,595), 7:(150,203,1091,182), 8:(978,300,214,147), 9:(960,327,95,425), 10:(1080,330,92,309), 11:(1113,251,85,146), 12:(163,227,1064,320), 13:(868,359,102,113), 14:(884,159,92,451), 15:(864,297,130,285), 16:(901,261,94,375), 17:(105,89,684,403), 18:(774,73,73,423)}
    for hole in holes_locations:
        c.execute('''INSERT into hole_table VALUES (?,?,?,?,?);''', (hole, holes_locations[hole][0], holes_locations[hole][1], holes_locations[hole][2], holes_locations[hole][3]))
    conn.commit()
    conn.close()

def get_hole_location(hole):
    """
    returns the location of the hole in question
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hole_table (hole int, lat int, lon int, start_lat int, start_lon int);''')
    user_info = c.execute('''SELECT * FROM hole_table WHERE hole=?''', (hole,)).fetchall()
    #recent = [1,530,90,100, 390]
    for info in user_info:
        recent = info
    return (recent[1],recent[2])

def get_start_location(hole):
    """
    returns the location of the hole in question
    """
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hole_table (hole int, lat int, lon int, start_lat int, start_lon int);''')
    user_info = c.execute('''SELECT * FROM hole_table WHERE hole=?''', (hole,)).fetchall()
    #recent = [1,530,90,100, 390]
    for info in user_info:
        recent = info
    return (recent[3], recent[4])

def set_up_hole(h):
    """
    Set up the hole number and set all users balls to the start.
    """
    update_game(hole=h)
    users_list = get_all_users()
    loc = get_start_location(h)
    for user in users_list:
        set_active(user, active=True)
        place_ball(user, loc[0], loc[1])

###
#Update to pull the current hole from the website
###
def locationchooser(holenum):
    return "http://608dev-2.net/sandbox/sc/team36/golfgame/Images/hole{}.jpg".format(holenum)\

def image_chooser(holenum):
    return "/var/jail/home/team36/golfgame/Images/hole{}.jpg".format(holenum)

def niceuserlist():
    allelements = get_all_users()
    nicestring = ""
    for element in allelements:
        nicestring += element
        nicestring += ", "
    return nicestring

def get_winner():
    users = get_all_users()
    output = ""
    lowest = float("inf")
    for user in users:
        if get_score(user) < lowest:
            output = user
            lowest = get_score(user)
    return output

def get_score_table():
    users = get_all_users()
    output = []
    for user in users:
        output.append((user + ": ", get_score(user)))
    output.sort(key=lambda pair: pair[1])
    #make string representation of table
    output_str = ""
    for val in output:
        output_str = output_str + val[0] + str(val[1]) + "<br>"
    return output_str

def insertchange():
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS holechangetimes (timing timestamp);''')
    c.execute('''INSERT into holechangetimes VALUES (?);''',(datetime.datetime.now(),))
    conn.commit()
    conn.close()

def lastchange():
    two_seconds_ago = datetime.datetime.now()- datetime.timedelta(seconds = 2)
    conn = sqlite3.connect(golf_db)
    c = conn.cursor()
    data = c.execute('''SELECT * FROM holechangetimes WHERE timing > ?;''',(two_seconds_ago,)).fetchone()
    conn.commit()
    conn.close()

    if data == None:
        return "0"
    else:
        return "1"

def get_affect(holenum,location):
    """
    return hole number and location
    """
    start = get_start_location(holenum)
    if abs(location[0] - start[0]) < 50 and abs(location[1] - start[1]) < 50:
        return (500,random.randint(-3,3))
    #check if in starting spot, then return max option
    references = {(90,195,190): "water", (0,0,0): "bounds", (215,230,185): "green", (110,140,80): "rough",(175,155,105): "sand", (165,185,130): "fairway", (255,255,255): "bunker", (225,225,195): "bunker"}
    affects = {"water": "stroke_penalty", "bounds": "stroke_penalty", "green": (100,random.randint(-3,3)), "rough": (150,random.randint(-10,10)), "fairway": (300,random.randint(-5,5)), "bunker": (50,random.randint(-20,20)), "sand": (300,random.randint(-6,6))}
    filename = image_chooser(holenum)
    img = Image.open(filename)
    try:
        color = img.getpixel(location)
    except:
        return "stroke_penalty"
    closest = None
    close_by = 756
    for ref in references:
        color_dist = abs(ref[0]-color[0]) + abs(ref[1]-color[1]) + abs(ref[2]-color[2])
        if color_dist < close_by:
            close_by = color_dist
            closest = ref
    #color correction, as the fairway and sand are only different by the green color
    course_part = references[closest]
    if course_part == "sand":
        if color[2] > 115:
            course_part = "fairway"
    return affects[course_part]


if __name__ == '__main__':

    pass
