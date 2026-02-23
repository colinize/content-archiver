---
title: INTRO TO ARDUINO
date: 2017-01-11
url: https://www.pinballnews.com/site/2017/01/11/intro-to-arduino
source: Pinball News
era: wordpress
---

**WHAT IS AN ARDUINO?**

Great question! There are several versions (different board configurations) of the Arduino. An unofficial Arduino board is called a clone. We will be using a Five volt, ATmega328, Arduino Nano clone.

An Arduino is a standalone computer based on either the ATmega168 or ATmega328 **micro**–**c**ontroller (**µC**); the 328 being the more recent and powerful.  The ATmega**328** is a micro-chip using **32** Kbits of flash memory and **8** bit AVR processing.

We “talk” to the ATmega328, via USB, on computers using Windows or Apple software (among other software types). To program the ATmega, we use a simplified version of the C/C++ programming language. Fortunately, we don’t have to be programmers to use Arduino boards. We can use the Arduino **I**ntegrated **D**evelopment **E**nvironment (**IDE**) to create and upload our programs (sketches).

**AN ARDUINO CAN’T REALLY BE A COMPUTER, CAN IT?**

Another great question and yes . . . yes it can!

The requirements for a machine to be a computer are:
– Clock [Crystal oscillating at 16 MHz (16,000,000 cycles per second)]
– Input (Mini-B USB Jack)
– Output [On-board **L**ight **E**mitting **D**iodes (**LED**s)]
– Power Source (+5 Volts of direct current provide by the computer’s USB port)
– Processor [ATmega328 Microcontroller (AT328)]
– **R**andom **A**ccess **M**emory (**RAM**) [2 kilo-bytes (2,000 bytes) SRAM]
– **R**ead **O**nly **M**emory (**ROM**) [32 kilo-bytes (32,000 bytes) EEPROM]

**WHERE IS ALL THAT STUFF?**

Yet, another great question. Here’s one in return. “What did you have for breakfast, a great big bowl of great questions?”

Look at the two following pictures to see different parts of the “5 Volt Nano”:
– 16 Mhz Crystal (SMD Crystal)
– **A**nalog Pins (**A**0 through **A**7)
– **D**igital Pins (**D**2 through **D**13)– **L**ight **E**mitting **D**iodes (**LED**s)
– LED Pin (**D13**)– **Microc**ontroller – ATmega328 (**µC**)
– Other Pins(Various)– Reset Button (RST)

[![Source: https://wiki.eprolabs.com/images/6/67/Nano.jpg](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/21.jpg)](Source:%C2%A0https://wiki.eprolabs.com/images/6/67/Nano.jpg)

[![Source: http://www.pighixxx.com/test/portfolio-items/nano/?portfolioID=314](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/22.jpg)](http://www.pighixxx.com/test/portfolio-items/nano/?portfolioID=314)

**WHAT CAN WE DO WITH THIS THING?**
We can do simple projects, like we are going to do, flash an LED. Or, even make complicated machines.

**HOW DO WE GET STARTED?**
To program our ‘Duino, download the free software from Arduino. (But, feel free to donate.)

[![Link: https://www.arduino.cc/en/Main/Software](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/23.jpg)](https://www.arduino.cc/en/Main/Software)

Link: https://www.arduino.cc/en/Main/Software

Remember where you saved the programs and if there is a shortcut.

Follow these instructions for your computers.
Link: <https://www.arduino.cc/en/Guide/HomePage>

Follow these instructions for our boards.
Link: <https://www.arduino.cc/en/Guide/ArduinoNano>

**WHEN ARE WE GOING TO HAVE FUN?**

Soon, let’s plug in our Nano boards.

First, plug the USB-A to Mini-B cable into your computers. Next, touch the metal of the mini-end. This will help make your Nano safe from **E**lectro**s**tatic **D**ischarge (**ESD**).

ESD is the shock we sometimes feel when we touch a metal door knob during the winter. Most of us don’t like the winter zaps. Imagine how our poor little Nano boards feel.

Let’s load the first program, the “blink sketch”. Hold your Nano by the edges of its breadboard and connect it to your computer via a USB cable. Push or pull the connector end. Never wiggle the connector or pull the cord.

**OPEN the ARDUINO SOFTWARE**
Open the Arduino software and wait for the welcome (splash) screen to finish.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/24.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/24.jpg)

After the welcome screen we should see a window similar to the next picture.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/25.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/25.jpg)

Navigate (drill down): File Examples 0.1Basics Blink

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/26.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/26.jpg)

We should now see a second window, with the new one overlapping the first one; similar to the next picture.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/27.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/27.jpg)

Select: Tools Board: (“Arduino/Gunuino Uno”) Arduino Nano

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/28.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/28.jpg)

Select: Tools Processor: “ATmega328” ATmega328

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/29.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/29.jpg)

Select: Tools Port Com (As usually automatically chosen by our computers.)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/30.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/30.jpg)

**BLINK (On Board LED)**

Go back to or reopen the Blink window. (Select: File Examples 01.Basics Blink)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/31.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/31.jpg)

The Blink window should be in front showing something similar to the following.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/32.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/32.jpg)

Either maximize the window or use the scroll bars to view the sketch “Blink”.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/33.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/33.jpg)

Click the rightwards arrow (→) to upload and run the Blink sketch.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/34.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/34.jpg)

Observe the built in light (LED on pin 13.) blinking.

**NEW WINDOW**

We can copy and paste the sketch we are working on, in a new window. Just, do the following.

Select: File New (As shown in the following picture.)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/35.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/35.jpg)

When the new window appears, select and copy over the entire existing sketch. (See the picture.)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/36.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/36.jpg)

**FLASH the LED (Don’t save at this time.)**

Copy and paste the following “FLASH” code into a new sketch window and upload that new sketch.

void setup()
{
pinMode(13,OUTPUT);
digitalWrite(2,HIGH);
delay(1000);
digitalWrite(2,LOW);
}

void loop()
{
}

The Arduino software will automatically try to get us to save out new sketches. For now, we will cancel out of this action.

While our sketches are being uploaded to our Nano boards, observe the RX and TX LEDs flashing.

If we missed the flash of the LED just after loading the sketch, we can quickly press and release the reset button. What happens each time we press the button?

**BLINK the LED (Don’t save at this time.)**

Copy and paste the following “BLINK” code into our open sketch windows and upload that new sketch.

void setup() // one-time setup
{
pinMode(13,OUTPUT); // define pin 13 as an output
}

void loop() // continuously loop
{
digitalWrite(13,HIGH); // p13 HIGH (LED ON)
delay(500); // wait 500 ms (Wait 1/2 second)
digitalWrite(13,LOW); // p13 LOW (LED OFF)
delay(500); // 500 mSec delay (Wait 1/2 second)
}

Now what happens each time we press our reset buttons?

**NEW WINDOW with OLD SKETCH**

Multiple sketchbook windows can be open simultaneously. We can use this to our advantage by copy / paste the sketch we are working on in a second window. The first window is used to save our progress. The second window is used to troubleshoot (edit) our code. Once we have selected our entire program to be edited, do the following.

Select: File New (As shown in the following picture.)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/37.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/37.jpg)

Then, when the new window appears, select and copy over the entire starting sketch. (See the picture.)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/38.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/38.jpg)

**FLASH CHANGED to DOUBLE BLINK**

Paste the “**BLINK the LED**” sketch into to new window. We can identify our new and unsaved window / sketch by observing its tab. The tabs of new windows are labeled “sketch\_(current date)(letter)”. The letter increments for each new window opened.

1. So, our first new window is “sketch\_(current date)a”.
2. Our second new window is “sketch\_(current date)b”.
3. Our third new window is “sketch\_(current date)c”.
4. And, so on . . .

Use this new window technique and add two forward slashes (//) to “BLINK” just before the second “delay”. This is called “commenting out” code. It is very useful for troubleshooting our sketches.

void setup() // one-time setup
{
pinMode(13,OUTPUT); // define pin 13 as an output
}

void loop() // continuously loop
{
digitalWrite(13,HIGH); // p13 HIGH (LED ON)
delay(500); // wait 500 ms (Wait 1/2 second)
digitalWrite(13,LOW); // p13 LOW (LED OFF)
//delay(500); // 500 mSec delay (Wait 1/2 second)
digitalWrite(13,HIGH); // p13 HIGH (LED ON)
delay(1000); // wait 1000 ms (Wait 1 second)
digitalWrite(13,LOW); // p13 LOW (LED OFF)
delay(1000); // wait 1000 ms (Wait 1 second)
}

We will use the reset button to try the sketch with one line (//delay(500); // 500 mSec delay (Wait 1/2 second)) commented out and without being commented out.

**SAVE THE SKETCH**

The tab of our saved sketch will have the name we chose to call the sketch. When we open the Arduino software, the most recently used program will load.

Add two forward slashes (//) to the very top of the “FLASH CHANGED TO DOUBLE BLINK” sketch.  After the slashes, name the program something that is meaningful. We will save the sketch as named. If we add “.ino” to the end of the name, it will be easier to look for in the future; as Arduino sketches are “.ino” files. Copy the entire name and “**Save As**” . . .”.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/39.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/39.jpg)

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/40.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/40.jpg)

The sketch we just saved should look something like this picture.

[![](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/41.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/41.jpg)

**SAVE LOCATION**

Arduino sketches automatically get saved to a “sketchbook”, in the following default location, on Windows machines.

***Computer C: Users (User Name) Documents Arduino***

**TWO LIBRARIES and TWO SKETCHBOOK FOLDERS**

Try not to confuse Arduino Libraries (Sketches to be included in other sketches.) with your Library of sketches. Not to make things more confusing, this is the Library folder in the Sketchbook folder. Each sketch will have its own sketch folder; as well.

**PLAY TIME!**

Now that we have saved programs, and know how to work on them without losing what works, try: duplicating the “digitalWrite” commands, or changing “delay” times, or adding delays. Have fun!

**WHAT RESOURCES ARE AT OUR DISPOSAL?**

ATmega328 Datasheet Summary
<https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/Atmel-42735-8-bit-AVR-Microcontroller-ATmega328-328P_Summary.pdf>

Arduino Nano User Manual, V2.3
<https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/ArduinoNanoManual23.pdf>

Arduino Microcontroller Guide, Ver. Oct-20
W. Durfee, University of Minnesota
[www.me.umn.edu/courses/me2011/arduino/](http://www.me.umn.edu/courses/me2011/arduino/)

Arduino Programming Notebook, V 1.1, First Edition August 2007
Written and Compiled by Brian W. Evans
<https://www.pinballnews.com/site/wp-content/uploads/learn/pin-uino/arduino_notebook_v1-1.pdf>
