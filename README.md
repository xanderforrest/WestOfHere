<h1>West of Here</h1>
A Spaghetti Western inspired click'n'shoot platformer.

![The current state of the game](https://i.imgur.com/HV5F9hz.png)

West Of Here is an open source Western themed platformer with a built in level editor, designed to have gamemodes built
upon itself. The only dependency (apart from the Python 3 standard library) is Pygame 1.9.6, with a backend for GUI
management being expanded upon commit by commit. There is a [Discord Server](https://discord.gg/xepTmRg) 
to keep up to date with development and to get help or support.
<br><br>
The project has been expanded upon over the past month to its current state in which gamemodes can be built and level
editing is in place. However, there are still many features left to be implemented to make the experience more streamlined
for users. 
<h2>Quick Start</h2>
You can clone/download this repo's master branch which is kept stable - dependencies can be installed by navigating
to the downloaded directory and entering the command:

>pip -r install requirements.txt

From there, you can run the main.py file to launch the game. Take a look at the basic example of a game mode - WorldRunner.py
in the gamemodes directory to see how they are structured. In the future more documentation will be added for creating and
implementing your own gamemodes into West Of Here, for now, if you'd like to contribute, join our Discord server and I can
help you get set up.

<h2>Roadmap</h2>
<li><del>Tilemap Creator</del> (think Mario Maker, <del>with a smaller budget</del>)</li>
<li>Parallax</li>
<li><del>Gun Animations</del> + Logic (reloading, <del>delays</del>)</li>
<li>Enemy logic</li>
<li>More options in gamemode selection from Main Menu</li>
<li>Documentation for setting up your own gamemodes and standard practises
<br>
<h2>Credits</h2>
I've tried to do as much of the game myself as possible, but quickly realised I'm pretty bad at art.<br><br>
I commissioned an artist to draw and animate the main character, and another to design the buildings and
tileset the game uses. 
<br><br>
I found a font on fontspace under the SIL Open Font License, meaning I'm allowed to use it commercially.
This is used for the title and other text in the game.<br>
https://www.fontspace.com/press-start-2p-font-f11591

<br><br>
The sound effects in the game currently come from The Dollars Trilogy movies, so will have to be changed
if there is ever a more official release than here on Github.
<br><br>
The soundtrack over the top is from the youtuber OkamiDeluxe, who I am trying to find a way to contact but
allowed numerous other people to use their track with credit so I am hoping they'd be ok with me doing this
as a temporary solution. 
<br>
Their channel can be found here: https://www.youtube.com/user/OkamiDeluxe/<br>
And the video itself: https://www.youtube.com/watch?v=WDdZLk7pRfI