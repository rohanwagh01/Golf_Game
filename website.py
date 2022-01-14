import sys
sys.path.append("/var/jail/home/team36/golfgame")
from database_manager import get_score_table, get_winner, get_score, get_ball_location, get_all_users, get_active_users, get_color, get_state, niceuserlist, locationchooser, get_hole


maingame = '''
<!DOCTYPE html>
<html>
<body>
  <style>

  </style>

  <body style="background-color:black;">

  <h1 style="color:red;">MIT GOLF</h1>

  <b style="color:lightseagreen;">Current Users: ''' +niceuserlist()+ ''' </b>
  <br>
  <br>
  <b style="color:royalblue;">''' + get_score_table() + '''</b>
  <br>

  <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
    <input type="hidden" name="action" value="menu">
    <input type="submit" value="Menu" style="color:DarkSlateGray;">
  </form>
  <br>

  <canvas id="myCanvas" width="1440" height="700" style="border:1px solid #000000;">
  Your browser does not support the HTML canvas tag.</canvas>


<script>
let prevlocations = [0,0];
let locations = [0,0];
let colors = ["red"];
let counter = 0;

let intervalId = null;
let varCounter = 0;
let temp = [];

var xpos = 0;
var ypos = 0;
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
const image = document.getElementById('source');
var background = new Image();
background.src = "''' + locationchooser(get_hole()) + '''";


function getTime() {

  getinfo();

counter = 0;
for (let k = 0; k < prevlocations.length; k++){
if (prevlocations[k] != locations[k])
  counter++;
}
if (counter > 0){
drawstuff();
}

prevlocations = [];
for (let j = 0; j < locations.length; j++)
  prevlocations.push(locations[j]);



locations = [];
colors = [];

refresh();
setTimeout(getTime, 5000);


}

function getinfo(){
  var req = new XMLHttpRequest();
var url = "http://608dev-2.net/sandbox/sc/team36/golfgame/functiontester.py?action=inforequest";
  req.onreadystatechange = function() {
      if (req.readyState == 4 && req.status == 200) {
          var response2 = req.responseText;
          var balloc  = JSON.parse(response2);

          for (let j = 0; j < balloc.length; j++){
          locations.push(balloc[j][0],balloc[j][1]);
          colors.push(balloc[j][2]);

        }

      }
  }
  req.open("GET", url, true);
  req.send();
}



function refresh(){
  var req = new XMLHttpRequest();
  var url = "http://608dev-2.net/sandbox/sc/team36/golfgame/functiontester.py?action=needrefresh";
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var response3 = req.responseText;
            if (response3 == 1){
                location.reload();
                console.log("RELOADED");
            }
        }
    }
    req.open("GET", url, true);
    req.send();
}

function drawGolfball(){

     if(varCounter < 190) {
          varCounter++;

          if (varCounter > 15){
          ctx.clearRect(0, 0, 1440, 506);
          ctx.drawImage(background, 0, 0, 1440, 506, 0, 0, 1440, 506);
          }

          for(let ttz = 0; ttz<locations.length; ttz +=2){
            let delta_x = (locations[ttz] - temp[ttz]);
            let delta_y = (locations[ttz+1] - temp[ttz+1]);
            temp[ttz] = temp[ttz] + (delta_x)/22;
            temp[ttz+1] = temp[ttz+1] + (delta_y)/22;

            ctx.beginPath();
            ctx.fillStyle = 'white';
            ctx.arc(temp[ttz],temp[ttz+1],7,0,2*Math.PI);
            ctx.stroke();
            ctx.fill();
            ctx.beginPath();
            ctx.fillStyle = colors[ttz/2];
            ctx.arc(temp[ttz],temp[ttz+1],5,0,2*Math.PI);
            ctx.stroke();
            ctx.fill();

          }

          window.requestAnimationFrame(drawGolfball);
     }
     else{
       ctx.clearRect(0, 0, 1440, 506);
       ctx.drawImage(background, 0, 0, 1440, 506, 0, 0, 1440, 506);
       for(let ttz = 0; ttz<locations.length; ttz +=2){

         ctx.beginPath();
         ctx.fillStyle = 'white';
         ctx.arc(locations[ttz],locations[ttz+1],7,0,2*Math.PI);
         ctx.stroke();
         ctx.fill();
         ctx.beginPath();
         ctx.fillStyle = colors[ttz/2];
         ctx.arc(locations[ttz],locations[ttz+1],5,0,2*Math.PI);
         ctx.stroke();
         ctx.fill();
       }


     }

}

function drawstuff(){

    temp = [];
    for (let j = 0; j < prevlocations.length; j++)
      temp.push(locations[j]);

    ctx.globalCompositeOperation='source-over';
    //ctx.clearRect(0, 0, 1440, 506);
    //ctx.drawImage(background, 0, 0, 1440, 506, 0, 0, 1440, 506);

    for(let ttz = 0; ttz<locations.length; ttz +=2){

      ctx.beginPath();
      ctx.fillStyle = 'white';
      ctx.arc(locations[ttz],locations[ttz+1],7,0,2*Math.PI);
      ctx.stroke();
      ctx.fill();
      ctx.beginPath();
      ctx.fillStyle = colors[ttz/2];
      ctx.arc(locations[ttz],locations[ttz+1],5,0,2*Math.PI);
      ctx.stroke();
      ctx.fill();
    }
     varCounter = 0;
      window.requestAnimationFrame(drawGolfball);
}


setTimeout(getTime, 10); //call right away on page load
</script>


</body>
</html>
'''
#########################################################

titlescreen = '''
<!DOCTYPE html>
<html>
<body>
  <style>

  </style>

  <body style="background-color:black;">

  <h1 style="color:red;">MIT GOLF</h1>

  <b style="color:royalblue;">Current Users: ''' +niceuserlist()+ ''' </b>
    <br>

    <form action="/sandbox/sc/team36/golfgame/pair.py" method="post">
        <input type="submit" value="Begin Pairing" style="color:DarkSlateGray;">
    </form>
    <br>
    <br>

    <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
        <input type="hidden" name="action" value="update">
        <input type="hidden" name="clear" value="1111">
        <input type="submit" value="Clear Users" style="color:DarkSlateGray;">
    </form>
  <br>
  <br>
     <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
        <input type="hidden" name="action" value="update">

        <input type="radio" id="easy" name="difficulty" value="EASY">
        <label for="easy" style="color:green;">Easy</label><br>
        <input type="radio" id="medium" name="difficulty" value="MEDIUM">
        <label for="medium" style="color:orange;">Medium</label><br>
        <input type="radio" id="hard" name="difficulty" value="HARD">
        <label for="hard" style="color:red;">Hard</label>
        <br>

        <input type="radio" id="weather" name="weather" value="1">
        <label for="weather" style="color:grey;">Weather on</label><br>
        <input type="radio" id="weather" name="weather" value="0">
        <label for="weather" style="color:grey;">Weather off</label><br>

        <input type="submit" value="Update Weather and Difficulty" style="color:DarkSlateGray;">
     </form>
  <br>
  <br>
     <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
         <input type="hidden" name="action" value="start">
         <input type="submit" value="START THE GAME" style="color:DarkSlateGray;">
     </form>
  </body>
  </html>
'''

####################################################

pairingscreen = '''

<!DOCTYPE html>
<html>
<body>

<body style="background-color:black;">

<h1 style="color:red;">PLEASE PAIR</h1>
<br>
<b style="color:royalblue;">Current Users: </b>
  <br>
<p id="current_users" style="color:royalblue;"></p>

<br>
<br>
<form action="/sandbox/sc/team36/golfgame/pair.py" method="post">
    <input type="submit" value="Finish Pairing" style="color:DarkSlateGray;">
</form>

</body>
<script>
function getTime() {
  var req = new XMLHttpRequest();
  var url = "http://608dev-2.net/sandbox/sc/team36/golfgame/functiontester.py?action=niceuserlist";

    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == 200) {
            var response = req.responseText;
            document.getElementById('current_users').innerHTML = response;
        }
    }
    req.open("GET", url, true);
    req.send();
    setTimeout(getTime, 900);
}

setTimeout(getTime, 10); //call right away on page load
</script>

</html>

'''

menuscreen = '''
<!DOCTYPE html>
<html>
<body>
  <style>

  </style>

  <body style="background-color:black;">

  <h1 style="color:red;">MENU</h1>


    <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
        <input type="hidden" name="restart" value="rip">
        <input type="submit" value="RESTART GAME" style="color:DarkSlateGray;">
    </form>
  <br>
     <form action="/sandbox/sc/team36/golfgame/game.py" method="post">

        <input type="radio" id="easy" name="difficulty" value="EASY">
        <label for="easy" style="color:green;">Easy</label><br>
        <input type="radio" id="medium" name="difficulty" value="MEDIUM">
        <label for="medium" style="color:orange;">Medium</label><br>
        <input type="radio" id="hard" name="difficulty" value="HARD">
        <label for="hard" style="color:red;">Hard</label>
        <br>

        <input type="radio" id="weather" name="weather" value="1">
        <label for="weather" style="color:grey;">Weather on</label><br>
        <input type="radio" id="weather" name="weather" value="0">
        <label for="weather" style="color:grey;">Weather off</label><br>

        <input type="submit" value="Update Weather and Difficulty" style="color:DarkSlateGray;">
     </form>
  <br>
     <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
         <input type="hidden" name="skip" value="gitskipped">
         <input type="submit" value="SKIP HOLE" style="color:DarkSlateGray;">
     </form>
  <br>
     <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
         <input type="hidden" name="return" value="gitresumed">
         <input type="submit" value="RESUME GAME" style="color:DarkSlateGray;">
     </form>
  </body>
  </html>
'''

winscreen = '''
<!DOCTYPE html>
<html>
<body>
  <style>

  </style>

  <body style="background-color:black;">

  <h1 style="color:red;">GAME OVER</h1>
    <b style="color:royalblue;">The winner is ''' +get_winner()+ ''' with a score of ''' + str(get_score(get_winner())) +'''.</b>
    <br>
    <br>
    <b style="color:royalblue;">''' + get_score_table() + '''</b>
    <br>
    <br>
    <br>
    <form action="/sandbox/sc/team36/golfgame/game.py" method="post">
        <input type="hidden" name="restart" value="rip">
        <input type="submit" value="RESTART GAME" style="color:DarkSlateGray;">
    </form>

  </body>
  </html>
'''
#this is a tezt
#another test

def getmaingame():
    return maingame
def gettitlescreen():
    return titlescreen
def getpairingscreen():
    return pairingscreen
def getmenuscreen():
    return menuscreen
def getwinscreen():
    return winscreen




def request_handler(request):

    return winscreen


" /var/jail/home/team36/golfgame/Images/hole1.jpeg"
