---
title: New Kids on the Block
date: 2005-11-06
url: https://www.pinballnews.com/news/lego.html
source: Pinball News
era: legacy
---

Story  dated
November 6, 2005
.

Pinball is all about a spherical object rolling around on a smooth surface, so the thought of building a pinball game from Lego doesn't immediately seem like one of the better ideas.

But that's exactly what Gerrit Bronsveld & Martijn Boogaarts from The Netherlands have achieved.

The two showed their creation at the recent LegoWorld exhibition in Zwolle in The Netherlands where more than 500 children got the chance to play it over the six days of the event.

Obviously, the ball itself couldn't be made from lego blocks and a regular 1 1/16" steel pinball was just too heavy for the Lego motors, so a 1" glass ball was used as the main playing ball and a regular steel ball was used for the tilt mechanism. But the rest of the game is 99.99% pure Lego.

The new ball mechanism

But don't think Lego is just coloured plastic blocks because it's developed into far more that that, with motors, sensors, controller boards and its own programming language.  All this along with over 20,000 Lego blocks went into making a fully functional pinball game with true coin operation, three flippers, ramps, specials and extra balls.

Lego flippers

To discover how they did it, Pinball News went straight to the main men themselves.  Gerrit and Martijn  explained the operation of the game.

"When the right coin (50 Euro Cent) is inserted (others are rejected!) the machine will reset itself and the first ball is given. The user then will have to use the kicker to launch the ball into the playfield."

Lego ball plunger

"In total 3 balls are given but there is a good chance to earn extra balls. When the player has scored enough points (500) the Black Hole is opened and the yellow extra ball sign will start flashing. The player has then 30 seconds to get the ball in the Black Hole."

The Black Hole

"When he succeeds the extra ball sign will be lit and an extra ball will be given, as soon the current ball is lost. The next extra ball chance is given for every 1000 points extra, so at 1500, 2500, 3500 points and so forth."

The game's backbox includes a P-I-N-B-A-L-L feature where the player collects letters to spell out the word.

"You will get an extra PINBALL letter when shooting over the upper lane You will have to do this 6 times as both LL's are lit at the same time due to output limitations of the RCX unit (it would cost an extra RCX to light all seven letters separately). Once all P I N B A LL letters are lit you will enter the Special Mode (red Special lamp starts flashing. The Special will give you 1000 points (and the chance for an extra ball)."

"Interesting extras are the Rotation Bumpers and the Auto Kickback. The rotation bumpers are activated when they are touched (using a rotation sensor) and give the ball extra speed, angle change and unexpected behavior. The Auto Kickback will shoot the ball automatically out of the kickback hole which gives an extra dimension to the game."

At the heart of the control system are the RCX units shown above on the backbox.

"For those who are not familiar with Lego, RCX is the Lego Mindstorms computer. It can be programmed with embedded software and once the program is loaded  it can run autonomously.

There are different ways of programming an RCX using Visual Basic, Java, NQC (Not Quite C) and Lego's own graphical programming tool supplied with the RCX-kit. It has 3 analog inputs (10 bit A/D converters) and 3 analog outputs with duty-cycle control to create different output power levels.

In the program are touch sensors (analog switches, even with different resistor values so they are stackable), rotation sensors (it counts revolutions on a axis), light sensors (to measure light levels and detect some color differentiation) and temperature sensors. What's very neat is the fact you can communicate between different RCX units using IR (infra-red) messages. This gives endless possibilities and is THE real power of an RCX.

In the Pinball machine 13 separate RCX units are used. The reason we need so many RCX units is due to the fact an RCX has only 3 inputs (although most have 2 sensors  connected in parallel to it) and 3 outputs. We used 50 lamps and 24 motors so every input and output is used to the max. Every RCX unit have the same operation modes which are controlled by the main RCX (we have called this the Game Controller), 4 RCX units have been used for display, 5 + 1 to collect points and one for the flippers (3 in total) and one for the 'new ball' mechanism and for the auto kickback.

To control 13 RCX units at the same time appeared to be impossible.  The IR communication protocol used in the RCX is like Ethernet. There can be only one sender but there can be many (in practice we have tested this up to seven) listeners. The main problem we faced was that many RCX units wanted to report 'points' to the game controller but at the same time the game controllers needed to control the operation modes like the coin-in process and the tilt interrupt. This resulted in IR conflicts and lost messages.

All processes are very important as you don't want to miss a coin-in from the user and when the Pinball Machine is abused the Tilt protection mechanism must also be activated at all times. In the meantime points are collected using 5 separate RCX units broadcasting the points. (Hit Target, Top Gates, Bottom Gates, Rotation Bumpers and Drop Down Targets) and you don't want to miss points, do you?

The solution was both complex and effective. A Point Collector RCX was placed between the point-broadcasters and the Game Controller. The Points Collector is placed in a separate communication chamber. Both communication chambers communicate with each other using a direct feedback loop."

The two infra-red chambers

"The second big challenge was to overcome the point collected and the points representation.

We first wanted to recreate 7-segment LED displays using LEGO lamps like we used for the PINBALL letters. But to make a reasonable sized display of 4 digits (0000-9999) would already require 28 outputs = 10 RCX units. So finally we decided to use a 5-digit (00000-99999) mechanical display plus one 'digit' for status information.

Each digit is a cylinder like in a slot machine), this only needed 2 RCX units. But a mechanical display is very slow compared to the points collected. So it was a real challenge to come up with a system to guarantee that the display and the 'internal' points are equal."

In total, the game used over 100 metres of wire, 13 RCX units, 8 light sensors, 13 rotation sensors, 18 touch sensors and 24 motors, all of which took over 300 hours to assemble.

The result is an amazing pinball machine demonstrating the power and flexibility of the Lego system along with the ingenuity and creative skills of its creators.

Back
to the news index

Back
to the front page
