import sys
import sqlite3
import datetime
import math
import json

sys.path.append("/var/jail/home/team36/golfgame")
from database_manager import get_ball_location, get_all_users, niceuserlist, get_active_users, get_color, get_ball_loccol, lastchange, insertchange



def request_handler(request):
    users = get_active_users()
    final = []
    if(request['values']["action"] == "userrequest"):
        usersjson = json.dumps(users, indent = 4)
        return usersjson
    if(request['values']["action"] == "niceuserlist"):
        return niceuserlist()
    if(request['values']["action"] == "requestlocation"):
        if (request['values']["user"] in users):
            location = get_ball_loccol(request['values']["user"])
            locjson = json.dumps(location, indent = 4)
            return locjson
    if(request['values']["action"] == "needrefresh"):
        return lastchange()
    if(request['values']["action"] == "inforequest"):
        for userc in users:
            final.append(get_ball_loccol(userc))
        locjsonf = json.dumps(final, indent = 4)
        return locjsonf
####THIS IS JUST A TESTER BELOW########
    if(request['values']["action"] == "userrequest22"):
        info = [[100,100,"royalblue"],[150,300,"plum"],[500,100,"red"]]
        info2 = [[1000,200,"royalblue"],[170,200,"plum"],[1100,300,"red"]]
        locjson = json.dumps(info, indent = 4)
        locjson2 = json.dumps(info2, indent = 4)

        timenow = datetime.datetime.now()
        seconds = int(timenow.second)
        if seconds%2 == 0:
            return locjson
        else:
            return locjson2

    if(request['values']["action"] == "requestlocation22"):

        location = [100,100,"royalblue"]
        location2 = [900,300,"royalblue"]

        location3 = [150,300,"plum"]
        location4 = [700,400,"plum"]

        locjson = json.dumps(location, indent = 4)
        locjson2 = json.dumps(location2, indent = 4)
        locjson3 = json.dumps(location3, indent = 4)
        locjson4 = json.dumps(location4, indent = 4)
        timenow = datetime.datetime.now()
        seconds = int(timenow.second)
        if seconds%2 == 0:
            if request['values']["user"] == "tanner":
                return locjson
            if request['values']["user"] == "tech":
                return locjson3
        else:
            if request['values']["user"] == "tanner":
                return locjson2
            if request['values']["user"] == "tech":
                return locjson4






"""htmlcode = <!DOCTYPE html>
<html>
<body>

<meta http-equiv="refresh" content="1">

<style>

</style>

<canvas id="myCanvas" width="612" height="473" style="border:1px solid #d3d3d3;">
Your browser does not support the HTML canvas tag.</canvas>

<div style="display:none;">
  <img id="source"
      src="https://media.istockphoto.com/vectors/aerial-view-of-a-golf-course-vector-id476307862?k=6&m=476307862&s=612x612&w=0&h=hr-pwlQxHrAeLQbo8mHbt0xFMxQwxr9s3eE-g4UqDxw="
      width="612" height="473">
</div>

<script>
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
const image = document.getElementById('source');

image.addEventListener('load', e => {
  ctx.drawImage(image, 0, 0, 612, 473, 0, 0, 612, 473);
});

ctx.globalCompositeOperation='destination-over';

ctx.beginPath();
ctx.fillStyle = 'blue';
ctx.arc(100,100,8,0,2*Math.PI);
ctx.stroke();
ctx.fill();
ctx.beginPath();
ctx.moveTo(100, 100);
ctx.lineTo(120, 120);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(120, 120);
ctx.lineTo(120, 113);
ctx.stroke();
ctx.beginPath();
ctx.moveTo(120, 120);
ctx.lineTo(113, 120);
ctx.stroke();
ctx.beginPath();
ctx.fillStyle = 'white';
ctx.arc(100,100,10,0,2*Math.PI);
ctx.stroke();
ctx.fill();

ctx.beginPath();
ctx.fillStyle = 'red';
ctx.arc(500,200,8,0,2*Math.PI);
ctx.stroke();
ctx.fill();
ctx.beginPath();
ctx.fillStyle = 'white';
ctx.arc(500,200,10,0,2*Math.PI);
ctx.stroke();
ctx.fill();

ctx.beginPath();
ctx.fillStyle = 'black';
ctx.arc(550,155,8,0,2*Math.PI);
ctx.stroke();
ctx.fill();
ctx.beginPath();
ctx.fillStyle = 'white';
ctx.arc(550,155,10,0,2*Math.PI);
ctx.stroke();
ctx.fill();


</script>

</body>
</html>
""" #.format((ball_x,ball_y,ball_x,ball_y))
