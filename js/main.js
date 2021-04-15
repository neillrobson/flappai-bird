/* eslint-disable */
var debugmode = true;

var states = Object.freeze({
   SplashScreen: 0,
   GameScreen: 1,
   ScoreScreen: 2,
   SaveDataScreen: 3
});

var currentstate;

var collisionPosition = 10;

var gravity = 0.25;
var velocity = 0;
var position = 180;
var rotation = 0;
var jump = -4.6;
var flyArea = $("#flyarea").height();

var score = 0;
var highscore = 0;

var startTime = 0;
var duration = 0;
var savedata = [];

var pipeheight = 90;
var pipewidth = 52;
var pipeInterval = 1400;
var pipes = new Array();

gravityMultiplier = 1;
pipeHeightMultiplier = 1;
pipeIntervalMultiplier = 1;

var replayclickable = false;

//sounds
var volume = 30;
var soundJump = new buzz.sound("assets/sounds/sfx_wing.ogg");
var soundScore = new buzz.sound("assets/sounds/sfx_point.ogg");
var soundHit = new buzz.sound("assets/sounds/sfx_hit.ogg");
var soundDie = new buzz.sound("assets/sounds/sfx_die.ogg");
var soundSwoosh = new buzz.sound("assets/sounds/sfx_swooshing.ogg");
buzz.all().setVolume(volume);

//loops
var loopGameloop;
var loopPipeloop;

$(document).ready(function() {
   if(window.location.search == "?debug")
      debugmode = true;
   if(window.location.search == "?easy")
      pipeheight = 200;

   //get the highscore
   var savedscore = getCookie("highscore");
   if(savedscore != "")
      highscore = parseInt(savedscore);

   //get save data if any
   var saveDataEncoded = getCookie("savedata");
   if (saveDataEncoded != "") {
      savedata = JSON.parse(atob(saveDataEncoded));
   }

   //retrieve collision Position
   var savedCollisionPosition = getCookie("collisionPosition");
   if(savedCollisionPosition != "")
      collisionPosition = parseInt(savedCollisionPosition);

   //start with the splash screen
   showSplash();
});

function showSplash()
{
   currentstate = states.SplashScreen;

   //set the defaults (again)
   velocity = 0;
   position = 180;
   rotation = 0;
   score = 0;

   //update the player in preparation for the next game
   $("#player").css({ y: 0, x: 0 });
   updatePlayer($("#player"));

   soundSwoosh.stop();
   soundSwoosh.play();

   //clear out all the pipes if there are any
   $(".pipe").remove();
   pipes = new Array();

   //make everything animated again
   $(".animated").css('animation-play-state', 'running');
   $(".animated").css('-webkit-animation-play-state', 'running');

   //fade in the splash
   $("#splash").transition({ opacity: 1 }, 2000, 'ease');
}

function startGame()
{
   currentstate = states.GameScreen;

   //fade out the splash
   $("#splash").stop();
   $("#splash").transition({ opacity: 0 }, 500, 'ease');

   //update the big score
   setBigScore();

   //debug mode?
   if(debugmode)
   {
      //show the bounding boxes
      $(".boundingbox").show();
      $(".botPipeBox").show();
      $(".topPipeBox").show();
   }

   //start up our loops
   var updaterate = 1000.0 / 60.0 ; //60 times a second
   loopGameloop = setInterval(gameloop, updaterate);
   loopPipeloop = setInterval(updatePipes, pipeInterval);

   // Mark the start time of this run
   startTime = Date.now();

   //jump from the start!
   playerJump();
}

function updatePlayer(player)
{
   //rotation
   rotation = Math.min((velocity / 10) * 90, 90);

   //apply rotation and position
   $(player).css({ rotate: rotation, top: position });
}

function gameloop() {
   var player = $("#player");

   //update the player speed/position
   velocity += gravity;
   position += velocity;

   //update the player
   updatePlayer(player);

   //create the bounding box
   var box = document.getElementById('player').getBoundingClientRect();
   var origwidth = 34.0;
   var origheight = 24.0;

   var boxwidth = origwidth - (Math.sin(Math.abs(rotation) / 90) * 8);
   var boxheight = (origheight + box.height) / 2;
   var boxleft = ((box.width - boxwidth) / 2) + box.left;
   var boxtop = ((box.height - boxheight) / 2) + box.top;
   var boxright = boxleft + boxwidth;
   var boxbottom = boxtop + boxheight;

   //if we're in debug mode, draw the bounding box
   if(debugmode)
   {
      var boundingbox = $("#playerbox");
      boundingbox.css('left', boxleft);
      boundingbox.css('top', boxtop);
      boundingbox.css('height', boxheight);
      boundingbox.css('width', boxwidth);
   }

   //did we hit the ground?
   if(box.bottom >= $("#land").offset().top)
   {
      collisionPosition = 10;
      playerDead();
      console.log("hit ground");

      console.log("collisionPosition: " + collisionPosition);
      setCookie("collisionPosition", collisionPosition, 999);
      return;
   }

   //have they tried to escape through the ceiling? :o
   var ceiling = $("#ceiling");
   if(boxtop <= (ceiling.offset().top + ceiling.height()))
      position = 0;

   //we can't go any further without a pipe
   if(pipes[0] == null)
      return;

   //determine the bounding box of the next pipes inner area
   var nextpipe = pipes[0];
   var nextpipeupper = nextpipe.children(".pipe_upper");
   var nextpipelower = nextpipe.children(".pipe_lower");

   var pipetop = nextpipeupper.offset().top + nextpipeupper.height();
   var pipeleft = nextpipeupper.offset().left - 2; // for some reason it starts at the inner pipes offset, not the outer pipes.
   var piperight = pipeleft + pipewidth;
   var pipebottom = pipetop + pipeheight;

   // var topTopPipe = nextpipeupper.offset().top;
   // var leftTopPipe = nextpipeupper.offset().left - 2;
   // var widthTopPipe = pipewidth;
   // var heightTopPipe = topTopPipe + nextpipeupper.height();

   // var topBottomPipe = nextpipeupper.offset().top + nextpipeupper.height() + pipeheight;
   // var leftBottomPipe = nextpipeupper.offset().left - 2;
   // var widthBottomPipe = pipewidth
   // var heightBottomPipe = topBottomPipe - pipeheight;

   if(debugmode)
   {
      var boundingbox = $("#pipebox");
      boundingbox.css('left', pipeleft);
      boundingbox.css('top', pipetop);
      boundingbox.css('height', pipeheight);
      boundingbox.css('width', pipewidth);

      // var boundingbox2 = $("#topPipeBox");
      // boundingbox2.css('left', leftTopPipe);
      // boundingbox2.css('top', topTopPipe);
      // boundingbox2.css('height', heightTopPipe);
      // boundingbox2.css('width', widthTopPipe);


      // var boundingbox3 = $("#botPipeBox");
      // boundingbox3.css('left', leftBottomPipe);
      // boundingbox3.css('top', topBottomPipe);
      // boundingbox3.css('height', heightBottomPipe);
      // boundingbox3.css('width', widthBottomPipe);


   }

   //have we gotten inside the pipe yet?
   if(boxright > pipeleft)
   {
      //we're within the pipe, have we passed between upper and lower pipes?
      if(boxtop > pipetop && boxbottom < pipebottom)
      {
         //yeah! we're within bounds

      }
      else if(boxtop<pipetop)
      {
         collisionPosition = 11;
         playerDead();
         console.log("Collision with upper pipe");
         console.log("collisionPosition: " + collisionPosition);
         setCookie("collisionPosition", collisionPosition, 999);
         return;
      }
      else if(boxtop < pipebottom)
      {
         collisionPosition = 12;
         playerDead();
         console.log("Collision with lower pipe");
         console.log("collisionPosition: " + collisionPosition);
         setCookie("collisionPosition", collisionPosition, 999);
         return;
      }
      
      else
      {
         //no! we touched the pipe
         collisionPosition = 13;
         playerDead();
         console.log("hit pipe, catch all");

         console.log("collisionPosition: " + collisionPosition);
         setCookie("collisionPosition", collisionPosition, 999);
         return;
      }
   }


   //have we passed the imminent danger?
   if(boxleft > piperight)
   {
      //yes, remove it
      pipes.splice(0, 1);

      //and score a point
      playerScore();
   }
}

//Handle keyboard input
$(document).keydown(function(e){
   //space bar!
   if(e.keyCode == 32)
   {
      //in ScoreScreen, hitting space should click the "replay" button. else it's just a regular spacebar hit
      if(currentstate == states.ScoreScreen)
         $("#replay").click();
      else
         screenClick();
   }

   // key pressed is [ or ]
   if(e.keyCode == 219 || e.keyCode == 221)
   {
      modifyPipeHeight(e.keyCode);
   }

   // key pressed is page up or page down
   if(e.keyCode == 33 || e.keyCode == 34)
   {
      modifyGravity(e.keyCode);
   }

   // key pressed is , or .
   if(e.keyCode == 188 || e.keyCode == 190)
   {
      modifyPipeInterval(e.keyCode);
   }

   if (e.key === "q" && !(e.ctrlKey || e.metaKey || e.altKey || e.shiftKey))
   {
      clearSaveData();
   }
});

//Handle mouse down OR touch start
if ("ontouchstart" in window) {
   $(document).on("touchstart", screenClick);

   $("#savedata").on("touchstart", function (e) {
      e.preventDefault();
      e.stopPropagation();
      downloadSaveData();
   });
} else {
   $(document).on("mousedown", screenClick);

   $("#savedata").mousedown(function (e) {
      e.preventDefault();
      e.stopPropagation();
      downloadSaveData();
   });
}

function screenClick()
{
   if(currentstate == states.GameScreen)
   {
      playerJump();
   }
   else if(currentstate == states.SplashScreen)
   {
      startGame();
   }
}

// base gravity was .25
function modifyGravity(key)
{
   // should discuss setting good values for a min and max gravity
   if(key == 33 || key == "increase")
   {
      gravityMultiplier = gravityMultiplier + .01
      gravity = gravity * gravityMultiplier
      console.log("gravity increased to: " + gravity);
   } else {
      gravityMultiplier = gravityMultiplier - .01
      gravity = gravity * gravityMultiplier
      console.log("gravity decreased to: " + gravity);
   }
}

// base pipe interval was 1400
function modifyPipeInterval(key)
{
   // should discuss setting good values for a min and max pipe interval
   if(key == 188 || key == "decrease")
   {
      pipeIntervalMultiplier = pipeIntervalMultiplier - .01
      pipeInterval = pipeInterval * pipeIntervalMultiplier;
      console.log("pipeInterval decreased to: " + pipeInterval)
      clearInterval(loopPipeloop);
      if(currentstate == states.GameScreen)
      {
         loopPipeloop = setInterval(updatePipes, pipeInterval);
      }

   } else {
      pipeIntervalMultiplier = pipeIntervalMultiplier + .01
      pipeInterval = pipeInterval * pipeIntervalMultiplier;
      console.log("pipeInterval increased to: " + pipeInterval)
      clearInterval(loopPipeloop);
      if(currentstate == states.GameScreen)
      {
         loopPipeloop = setInterval(updatePipes, pipeInterval);
      }
   }
}

//base pipe height was 90
function modifyPipeHeight(key)
{
   // should discuss setting good values for a min and max pipeheight
   if(key == 219 || key == "decrease")
   {
      pipeHeightMultiplier = pipeHeightMultiplier - .01
      pipeheight = pipeheight * pipeHeightMultiplier
      console.log("pipeheight decreased to: " + pipeheight)
   } else {
      pipeHeightMultiplier = pipeHeightMultiplier + .01
      pipeheight = pipeheight * pipeHeightMultiplier
      console.log("pipeheight increased to: " + pipeheight)
   }
}

function playerJump()
{
   velocity = jump;
   //play jump sound
   soundJump.stop();
   soundJump.play();
}

function setBigScore(erase)
{
   var elemscore = $("#bigscore");
   elemscore.empty();

   if(erase)
      return;

   var digits = score.toString().split('');
   for(var i = 0; i < digits.length; i++)
      elemscore.append("<img src='assets/font_big_" + digits[i] + ".png' alt='" + digits[i] + "'>");
}

function setSmallScore()
{
   var elemscore = $("#currentscore");
   elemscore.empty();

   var digits = score.toString().split('');
   for(var i = 0; i < digits.length; i++)
      elemscore.append("<img src='assets/font_small_" + digits[i] + ".png' alt='" + digits[i] + "'>");
}

function setHighScore()
{
   var elemscore = $("#highscore");
   elemscore.empty();

   var digits = highscore.toString().split('');
   for(var i = 0; i < digits.length; i++)
      elemscore.append("<img src='assets/font_small_" + digits[i] + ".png' alt='" + digits[i] + "'>");
}

function setMedal()
{
   var elemmedal = $("#medal");
   elemmedal.empty();

   if(score < 10)
      //signal that no medal has been won
      return false;

   if(score >= 10)
      medal = "bronze";
   if(score >= 20)
      medal = "silver";
   if(score >= 30)
      medal = "gold";
   if(score >= 40)
      medal = "platinum";

   elemmedal.append('<img src="assets/medal_' + medal +'.png" alt="' + medal +'">');

   //signal that a medal has been won
   return true;
}

function playerDead()
{
   //Log the run duration
   duration = Date.now() - startTime;

   //stop animating everything!
   $(".animated").css('animation-play-state', 'paused');
   $(".animated").css('-webkit-animation-play-state', 'paused');

   // decrease difficulty is they haven't gotten a bronze medal yet
   if(score < 10){
      console.log("score: " + score);
      if(collisionPosition == 12){
         console.log("CollisionPosition inside dead exp 12: " + collisionPosition)
         modifyGravity("decrease");
      } else if(collisionPosition == 11){
         console.log("CollisionPosition inside dead exp 11: " + collisionPosition)
         modifyGravity("decrease");
         modifyPipeHeight("increase");
         modifyPipeInterval("increase");
      }
   }

   // If we already got gold medal, make it harder for them to get platinum medal
   if(score > 30){
      console.log("score: " + score);
      // doesn't really matter how we died, we just want to increase overall difficulty
      modifyGravity("increase");
      modifyPipeHeight("decrease");
      modifyPipeInterval("decrease");
   }

   //drop the bird to the floor
   var playerbottom = $("#player").position().top + $("#player").width(); //we use width because he'll be rotated 90 deg
   var floor = flyArea;
   var movey = Math.max(0, floor - playerbottom);
   $("#player").transition({ y: movey + 'px', rotate: 90}, 1000, 'easeInOutCubic');

   //it's time to change states. as of now we're considered ScoreScreen to disable left click/flying
   currentstate = states.ScoreScreen;

   //destroy our gameloops
   clearInterval(loopGameloop);
   clearInterval(loopPipeloop);
   loopGameloop = null;
   loopPipeloop = null;

   //mobile browsers don't support buzz bindOnce event
   if(isIncompatible.any())
   {
      //skip right to showing score
      showScore();
   }
   else
   {
      //play the hit sound (then the dead sound) and then show score
      soundHit.play().bindOnce("ended", function() {
         soundDie.play().bindOnce("ended", function() {
            showScore();
         });
      });
   }
}

var previousState;

function downloadSaveData()
{
   if (currentstate != states.GameScreen) { // No pausing for you!!
      download("save.txt", getCookie("savedata"));
   }
}

function clearSaveData()
{
   savedata = [];
   setObject("savedata", savedata, 999);
}

function showScore()
{
   //unhide us
   $("#scoreboard").css("display", "block");

   //remove the big score
   setBigScore(true);

   //have they beaten their high score?
   if(score > highscore)
   {
      //yeah!
      highscore = score;
      //save it!
      setCookie("highscore", highscore, 999);
   }

   //update the scoreboard
   setSmallScore();
   setHighScore();
   var wonmedal = setMedal();

   var runMetrics = { startTime, duration, score, gravity, pipeInterval, pipeheight, collisionPosition };
   savedata.push(runMetrics);
   setObject("savedata", savedata, 999);

   //SWOOSH!
   soundSwoosh.stop();
   soundSwoosh.play();

   //show the scoreboard
   $("#scoreboard").css({ y: '40px', opacity: 0 }); //move it down so we can slide it up
   $("#replay").css({ y: '40px', opacity: 0 });
   $("#scoreboard").transition({ y: '0px', opacity: 1}, 600, 'ease', function() {
      //When the animation is done, animate in the replay button and SWOOSH!
      soundSwoosh.stop();
      soundSwoosh.play();
      $("#replay").transition({ y: '0px', opacity: 1}, 600, 'ease');

      //also animate in the MEDAL! WOO!
      if(wonmedal)
      {
         $("#medal").css({ scale: 2, opacity: 0 });
         $("#medal").transition({ opacity: 1, scale: 1 }, 1200, 'ease');
      }
   });

   //make the replay button clickable
   replayclickable = true;
}

$("#replay").click(function() {
   //make sure we can only click once
   if(!replayclickable)
      return;
   else
      replayclickable = false;
   //SWOOSH!
   soundSwoosh.stop();
   soundSwoosh.play();

   //fade out the scoreboard
   $("#scoreboard").transition({ y: '-40px', opacity: 0}, 1000, 'ease', function() {
      //when that's done, display us back to nothing
      $("#scoreboard").css("display", "none");

      //start the game over!
      showSplash();
   });
});

function playerScore()
{
   score += 1;
   //play score sound
   soundScore.stop();
   soundScore.play();
   setBigScore();
}

function updatePipes()
{
   //Do any pipes need removal?
   $(".pipe").filter(function() { return $(this).position().left <= -100; }).remove()

   //add a new pipe (top height + bottom height  + pipeheight == flyArea) and put it in our tracker
   var padding = 80;
   var constraint = flyArea - pipeheight - (padding * 2); //double padding (for top and bottom)
   var topheight = Math.floor((Math.random()*constraint) + padding); //add lower padding
   var bottomheight = (flyArea - pipeheight) - topheight;
   var newpipe = $('<div class="pipe animated"><div class="pipe_upper" style="height: ' + topheight + 'px;"></div><div class="pipe_lower" style="height: ' + bottomheight + 'px;"></div></div>');
   $("#flyarea").append(newpipe);
   pipes.push(newpipe);
}

var isIncompatible = {
   Android: function() {
   return navigator.userAgent.match(/Android/i);
   },
   BlackBerry: function() {
   return navigator.userAgent.match(/BlackBerry/i);
   },
   iOS: function() {
   return navigator.userAgent.match(/iPhone|iPad|iPod/i);
   },
   Opera: function() {
   return navigator.userAgent.match(/Opera Mini/i);
   },
   Safari: function() {
   return (navigator.userAgent.match(/OS X.*Safari/) && ! navigator.userAgent.match(/Chrome/));
   },
   Windows: function() {
   return navigator.userAgent.match(/IEMobile/i);
   },
   any: function() {
   return (isIncompatible.Android() || isIncompatible.BlackBerry() || isIncompatible.iOS() || isIncompatible.Opera() || isIncompatible.Safari() || isIncompatible.Windows());
   }
};
