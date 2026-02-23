---
title: PINBALL BALL DETECTOR - ALTERNATIVE MICROCONTROLLERS
date: 2024-02-02
url: https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-alternative-microcontrollers
source: Pinball News
era: wordpress
---

**Introduction**

In his new two-part article ([Part One](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/), [Part Two](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-two/)), Todd Andersen shows us how to build a microcontroller-based pinball ball detector to trigger add-ons such as toppers or enhanced lighting effects. His article focuses on building a system around an Arduino Uno microcontroller but, as he explains, other microcontrollers can be used instead.

In this addendum he examines several alternatives to the Arduino Uno, describing how they have their unique features and requirements, and provides the sketches to make them read the IR sensor input module and control the relay output module.

---

As only just a few pins are needed to make the Arduino-based pinball detector featured in [Part One](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/) and [Part Two](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-two/), a few different microcontroller boards could be used instead.

In addition to the genuine Arduino Uno board, I have had success using various standalone microcontrollers, Digistump Digispark and clone boards, LilyTiny clone boards, ATtiny88 boards and clones, Arduino clone boards, and Raspberry Pi Pico.

Here are some suggestions listed from the smallest board to the largest:

1. [**ATtiny85**](https://www.arrow.com/en/research-and-events/articles/attiny85-arduino-tutorial)
   Click [here](https://highlowtech.org/?p=1695) for details of how to add this board to the Arduino IDE
    .
2. [**Digistump Digispark USB-MICRO**](http://digistump.com/)
   Follow these two Pinball News links for more detailed information: [Link 1](https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-one/) and [Link 2](https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-two/)
   Click [here](https://github.com/digistump/DigistumpArduino) and [here](http://digistump.com/wiki/digispark/tutorials/connecting) for details of how to add this board to the Arduino IDE
    .
3. **[Digistump Digispark USB-A](http://digistump.com/)**
   Follow these two Pinball News links for more detailed information: [Link 1](https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-one/) and [Link 2](https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-two/)
   Click [here](https://github.com/digistump/DigistumpArduino) and [here](http://digistump.com/wiki/digispark/tutorials/connecting) for details of how to add this board to the Arduino IDE
    .
4. [**Digistump Digispark Pro**](http://digistump.com/)
   Follow [this link](http://digistump.com/) for more detailed information
   Click [here](https://github.com/digistump/DigistumpArduino) and [here](http://digistump.com/wiki/digispark/tutorials/connectingpro) for details of how to add this board to the Arduino IDE
    .
5. **[Nano – MH-ET LIVE Attiny88](https://github.com/MHEtLive)**
   See [details below](#tiny-88-nano)
   Click [here](https://handsontec.com/dataspecs/module/Arduino/Arduino%20Tiny%2088.pdf) and [here](https://mhetlive.nodebb.com/topic/47/mh-et-live-tiny88-16-0mhz) for details of how to add this board to the Arduino IDE
    .
6. **[Nano – Atmega328P](https://github.com/UnfinishedStuff/CH340C)**
   Follow these Pinball News links for more detailed information: [Link 1](https://www.pinballnews.com/site/2022/12/24/pinball-add-on-controller-part-one/) and [Link 2](https://www.pinballnews.com/site/2022/12/24/pinball-add-on-controller-part-two/)
   This board is supported in the standard Arduino IDE installation
    .
7. **[Nano – LGT8F328P](https://github.com/RalphBacon/LGT8F328P-Arduino-Clone-Chip-ATMega328P/blob/master/README.md)**
   See [details below](#lgt8f328p)
   Click [here](https://github.com/dbuezas/lgt8fx) for details of how to add this board to the Arduino IDE
    .
8. **[Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)**
   See [details below](#raspberry-pi-pico)
   Click [here](https://github.com/earlephilhower/arduino-pico) for details of how to add this board to the Arduino IDE
    .
9. **[Uno](https://blog.devgenius.io/using-arduino-ide-with-unofficial-arduino-clones-bearing-ch340-chip-752d1b90810d)**
   Follow these Pinball News links for more detailed information: [Link 1](https://www.pinballnews.com/site/2017/01/11/intro-to-arduino/) and [Link 2](https://www.pinballnews.com/site/2017/01/12/pin-uino/)
   This board is supported in the standard Arduino IDE installation

This list also, coincidentally, is listed from the hardest to the easiest to use.

**Bonus board:** The ‘VCC-GND Studio YD-RP2040’ is a RP2040-based Arduino Nano sized microcontroller board. And, it has an RGB LED output.

……10. [**Nano – YD-RP2040**](https://github.com/micropython/micropython/pull/12281)
 ………….See [details below](#yd-rp2040)
 ………….Click [here](https://github.com/earlephilhower/arduino-pico) for details of how to add this board to the Arduino IDE

Because the YD-RP2040 is RP2040 microcontroller-based, it can be programmed much like the Raspberry Pi Pico.

This tenth bonus board is more expensive than the first eight (or nine, if you use an Uno clone board rather than a genuine Arduino Uno). It costs more than the fiver or tenner the other nine boards cost, but even with its own associated add-ons it’s still much more affordable than many commercially available pinball add-ons or toppers.

Let’s take a look at a selection of four of those alternative microcontrollers.

**TINY 88 NANO**

**Introduction**

This MH-ET LIVE Tiny88 is an ATtiny88-based microcontroller similar to the ATMega328p-based Nano microcontroller, but with fewer capabilities and at a lower price.

[![The MH-ET LIVE Tiny88 microcontroller](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/201-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/201-pinball-ball-detector.jpg)

The MH-ET LIVE Tiny88 microcontroller

**Boards**

The ‘Tiny88’ is similar to the standard Arduino Nano (and clones) boards, but with a different pin arrangement.

[![Tiny88 Nano front and back](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/202-pinball-ball-detector-1024x919.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/202-pinball-ball-detector.jpg)

Tiny88 Nano front and back

**Arduino IDE**

Only a few years after its introduction, the Tiny88 microcontroller is almost fully supported in the [Arduino IDE](https://mhetlive.nodebb.com/topic/47/mh-et-live-tiny88-16-0mhz).

[![The microcontroller's selection in the Arduino IDE](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/250-pinball-ball-detector-1024x595.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/250-pinball-ball-detector.jpg)

The microcontroller’s selection in the Arduino IDE

**Building**

Rather than explaining further, we will get to putting together and showing the controller.

**Sketch**

The Tiny88 sketch below is laid out to include hardware connections. See lines #12 – #15 and #17 – #20.

[![The sketch for the Tiny88 microcontroller](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/205-pinball-ball-detector-629x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/205-pinball-ball-detector.jpg)

The sketch for the Tiny88 microcontroller ball detector

**Entire Sketch**

You can view or copy the full sketch for the Tiny88 here.

```
//Tiny88PIrSens.INO

/*
Pinball News
https://www.pinballnews.com/
February, 2024
This example code is in the public domain.
*/

//Input Module pins
// irSensorPwr  =  5V
// irSensorGnd  =  GND
int irSensorOut  =  3;

//Output Module pins
// relayPwr  =  5V
// relayPGnd  =  GND
int relayIn  =  0;

// Change as needed
int Dwell  =  777;

// Setup
void setup ()
{
  pinMode (irSensorOut, INPUT_PULLUP);
    digitalWrite (irSensorOut, HIGH);
  pinMode (relayIn, OUTPUT);
    digitalWrite (relayIn, LOW);
}

// Loop
void loop ()
{
  if (digitalRead (irSensorOut) == LOW)
  {
    digitalWrite (relayIn, HIGH);
    digitalWrite (LED_BUILTIN, HIGH);
      delay (Dwell);
  }
  else
  {
    digitalWrite (relayIn, LOW);
    digitalWrite (LED_BUILTIN, LOW);
  }
}
```

**Finished Controller**

With hardware and software together, we have a finished Tiny88 microcontroller-based prototype ball detector.

[![IR sensor module, relay module and Tiny88 board all powered - but not activated](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/206-pinball-ball-detector-1024x728.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/206-pinball-ball-detector.jpg)

IR sensor module, relay module and Tiny88 board all powered – but not activated

[![IR sensor module, relay module and Tiny88 board all powered and also triggered](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/207-pinball-ball-detector-1024x728.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/207-pinball-ball-detector.jpg)

IR sensor module, relay module and Tiny88 board all powered and also triggered

---

**LGT8F328P NANO**

**Introduction**

This LGT8F328P-based microcontroller is similar to ATMega328p-based microcontroller, but with additional capabilities and at a lower price.

[![LGT8F328P's features](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/211-pinball-ball-detector-1024x627.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/211-pinball-ball-detector.jpg)

LGT8F328P’s features

**Boards**

Some versions of this LGT8F328P module are pin-for-pin compatible with the standard Arduino Nano (and clones) board. This makes them convenient for using on some of the inexpensive Nano breakout boards available.

[![Tired old ATMega328p Nano board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/212-pinball-ball-detector-1024x467.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/212-pinball-ball-detector.jpg)

Tired old ATMega328p Nano board

[![Shiny new LGT8F328P Nano board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/213-pinball-ball-detector-1024x425.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/213-pinball-ball-detector.jpg)

Shiny new LGT8F328P Nano board

**Breakout Boards**

Several relatively-inexpensive breakout boards (a.k.a. ‘shileds’) are available to aid connections to the Nano board.

[![A remotely-powered Breakout board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/214-pinball-ball-detector-1024x793.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/214-pinball-ball-detector.jpg)

A remotely-powered Breakout board

[![A simpler unpowered breakout board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/215-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/215-pinball-ball-detector.jpg)

A simpler unpowered breakout board

**Arduino IDE**

Only a few years after its introduction, the LGT8F328P microcontroller is almost fully supported in the [Arduino IDE](https://github.com/dbuezas/lgt8fx).

[![The microcontroller's selection in the Arduino IDE](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/204-pinball-ball-detector-1024x583.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/204-pinball-ball-detector.jpg)

The microcontroller’s selection in the Arduino IDE

**Building**

This article will be taking advantage of an already existing [pinout](https://en.wikipedia.org/wiki/Pinout) arrangement to create our pinball controller – modified from previous articles. Rather than explaining any further, we will get to putting together and showing the controller.

**Sketch**

The LGT8F328P sketch below is laid out to include the hardware connections. See lines #10 – #13 and #15 – #18. For simplicity, all the connections are kept on one side of the board, with only one connection doubled-up.

[![The sketch for the LGT8F328 microcontroller ball detector](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/216-pinball-ball-detector-616x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/216-pinball-ball-detector.jpg)

The sketch for the LGT8F328 microcontroller ball detector

**Entire Sketch**

```
//LGT8F328PIrSens.INO

/*
Pinball News
https://www.pinballnews.com/
February, 2024
This example code is in the public domain.
*/

//Input Module pins
// irSensorPwr  =  3.3 Volt
// irSensorGnd  =  GND
int irSensorOut  =  A0;

//Output Module pins
// relayPwr  =  5.0 Volt
// relayPGnd  =  GND
int relayIn  =  A7;

// Change as needed
int Dwell  =  777;

// Setup
void setup ()
{
  pinMode (irSensorOut, INPUT_PULLUP);
    digitalWrite (irSensorOut, HIGH);
  pinMode (relayIn, OUTPUT);
    digitalWrite (relayIn, LOW);
}

// Loop
void loop ()
{
  if (digitalRead (irSensorOut) == LOW)
  {
    digitalWrite (relayIn, HIGH);
    digitalWrite (LED_BUILTIN, HIGH);
      delay (Dwell);
  }
  else
  {
    digitalWrite (relayIn, LOW);
    digitalWrite (LED_BUILTIN, LOW);
  }
}
```

**Finished Controller**

With hardware and software together, we have a finished LGT8F328P-based microcontroller prototype ball detector.

[![Sensor and relay modules and the LGT8F328P board all powered, but not activated](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/217-pinball-ball-detector-1024x715.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/217-pinball-ball-detector.jpg)

Sensor and relay modules and the LGT8F328P board all powered, but not activated

[![Sensor and relay modules and the LGT8F328P board all powered, and also triggered](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/218-pinball-ball-detector-1024x715.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/218-pinball-ball-detector.jpg)

Sensor and relay modules and the LGT8F328P board all powered, and also triggered

---

**RASPBERRY PI PICO**

**Introduction**

This RP2040 based microcontroller is similar to ATMega328p based microcontroller, but available at a lower price.

[![RP2040 features](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/240-pinball-ball-detector-1024x660.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/240-pinball-ball-detector.jpg)

RP2040 features

**Boards**

Some versions of this RP2040 microprocessor module can be used with inexpensive breakout boards.

[![Raspberry Pi Pico front and back](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/241-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/241-pinball-ball-detector.jpg)

Raspberry Pi Pico front and back

**Breakout Boards**

Several relatively-inexpensive breakout boards are available.

[![A remotely-powered breakout board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/242-pinball-ball-detector-1024x696.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/242-pinball-ball-detector.jpg)

A remotely-powered breakout board

[![An unpowered breakout board with LED indicators](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/243-pinball-ball-detector-1024x798.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/243-pinball-ball-detector.jpg)

An unpowered breakout board with LED indicators (shown lit for clarity)

**Arduino IDE**

Only a few years after its introduction, the RP2040 microcontroller is almost fully supported and compatible in the [Arduino IDE](https://arduino-pico.readthedocs.io/) software.

[![The Raspberry Pi Pico in the Arduino IDE](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/244-pinball-ball-detector-1024x547.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/244-pinball-ball-detector.jpg)

The Raspberry Pi Pico in the Arduino IDE

**Building**

Rather than explaining further, we will get to putting together and demonstrating the controller.

**Sketch**

The Raspberry Pi Pico sketch below is laid out to include hardware connections. See lines #12 – #15 and #17 – #20.

To make things simpler, connections are kept on just one side of the board, while no connections are doubled-up.

[![The sketch in the Arduino IDE](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/245-pinball-ball-detector-651x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/245-pinball-ball-detector.jpg)

The sketch in the Arduino IDE

**Entire Sketch**

Here’s the full sketch you can copy and paste:

```
//RaspberryPiPicoIrSens.INO
/*
Pinball News
https://www.pinballnews.com/
February, 2024
This example code is in the public domain.
*/

//Input Module pins
// irSensorPwr  =  3v3OUT
// irSensorGnd  =  GND
int irSensorOut  =  28;

//Output Module pins
// relayPwr  =  VBUS
// relayPGnd  =  GND
int relayIn  =  22;

// Change as needed
int Dwell  =  777;

// Setup
void setup ()
{
  pinMode (irSensorOut, INPUT_PULLUP);
    digitalWrite (irSensorOut, HIGH);
  pinMode (relayIn, OUTPUT);
    digitalWrite (relayIn, LOW);
}

// Loop
void loop ()
{
  if (digitalRead (irSensorOut) == LOW)
  {
    digitalWrite (relayIn, HIGH);
      delay (Dwell);
  }
  else
  {
    digitalWrite (relayIn, LOW);
  }
}
```

**Finished Controller**

With hardware and software together, we have a finished RP2040-based prototype controller.

[![Sensor and relay modules and Pico all powered, but not activated](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/246-pinball-ball-detector-1024x682.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/246-pinball-ball-detector.jpg)

Sensor and relay modules and Pico all powered, but not activated

[![Sensor and relay modules and Pico all powered and also activated](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/247-pinball-ball-detector-1024x682.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/247-pinball-ball-detector.jpg)

Sensor and relay modules and Pico all powered and also activated

---

**YD-RP2040 NANO**

**Introduction**

The VCC-GND Studio YD-RP2040 is an RP2040-based microcontroller board similar to the ATMega328p-based Nano microcontroller board.

This board is the first used in this series of articles to include an on-board multi-colour light – its own RGB LED module.

With the use of this added LED module (called a ‘[NeoPixel](https://learn.adafruit.com/adafruit-neopixel-uberguide?gad_source=1)‘), we have switched from a behind-the-scenes controller to a module which may be playfield or backbox top mounted to add visual effect(s).

And, we don’t have to stop with the single LED NeoPixel of this module. NeoPixels come in a wide variety of [forms](https://learn.adafruit.com/adafruit-neopixel-uberguide/form-factors), any of which could be added to give complex lighting effects to the playfield or backbox. The single NeoPixel is only used here as a very singular example to give you some idea of what NeoPixels can do.

[![The VCC-GND Studio YD-RP2040's features](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/221-pinball-ball-detector-1024x531.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/221-pinball-ball-detector.jpg)

The VCC-GND Studio YD-RP2040’s features

**Boards**

Some boards utilizing the RP2040 module, such as the ones below, include NeoPixel(s). The top board also includes a button (labelled ‘USR’) which we can use as a convenient manually-activated input device for easy prototype testing.

[![Boards with at least one NeoPixel](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/222-pinball-ball-detector-1024x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/222-pinball-ball-detector.jpg)

Boards with one or more NeoPixels

[![The features of the VCC-GND Studio YD-RP2040 board](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/251-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/251-pinball-ball-detector.jpg)

The features of the VCC-GND Studio YD-RP2040 board

**Breakout Boards**

On a related note, NeoPixel breakout boards are also available for the Raspberry Pi Pico.

![Raspberry Pi Pico wearing an LED matrix ‘hat’](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/223-pinball-ball-detector-1024x646.jpg)

Raspberry Pi Pico wearing an LED matrix ‘hat’

**Arduino IDE**

This RP2040-based microcontroller board is supported in the [Arduino IDE](https://arduino-pico.readthedocs.io/), as a ‘Sparkfun ProMicro RP2040’ board.

[![The RP2040-based microcontroller board in the Arduino IDE](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/224-pinball-ball-detector-1024x547.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/224-pinball-ball-detector.jpg)

The RP2040-based microcontroller board in the Arduino IDE

**Sketch**

We will have to investigate the well-commented sketch further.

Let’s first give credit where due, to Adafruit Industries who provided their own example; the original [‘buttoncycler’ sketch](https://github.com/adafruit/Adafruit_NeoPixel/blob/master/examples/buttoncycler/buttoncycler.ino).

[![The edited 'buttoncycler' sketch with the required library and definitions](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/233-pinball-ball-detector-794x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/233-pinball-ball-detector.jpg)

The edited ‘buttoncycler’ sketch with the required library and definitions

This sketch requires a few things.

* Line #34: Inclusion of the “[Adafruit\_NeoPixel.h](https://github.com/adafruit/Adafruit_NeoPixel)” library.
  *Note: If a NeoMatrix were used instead, the [Adafruit\_NeoMatrix.h](https://github.com/adafruit/Adafruit_NeoMatrix) library must be included instead.*
* Line #42: Defining of the “BUTTON\_PIN”.
  *Note: Do not hook a microcontroller directly to the switches on your pinball machine as damage to one or both may occur.*
* Line #44: Defining of the “PIXEL\_PIN”.
   and
* Line #46: Defining of the “PIXEL\_COUNT”.

There is also a setup required for your selected NeoPixel brightness.

* Line #66: Setting the brightness of the NeoPixel via “strip.setBrightness”.
  *Note: This value is user-selectable from ‘0’ (off) to ‘255’ (maximum brightness).*

[![The chosen brightness of 15 out of 255, for prototyping purposes](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/253-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/253-pinball-ball-detector.jpg)

The chosen brightness of 15 out of 255, for prototyping purposes

Once defined, the brightness level is set for the entire sketch.

Shown below is the main loop where nine different lighting effects are configured in a wrap-around set. These cases can be changed and/or added to as you deem necessary.

[![The main loop with the different light shows](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/235-pinball-ball-detector-838x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/235-pinball-ball-detector.jpg)

The main loop with the different light shows

The main disadvantage of this easy example is that, once started, each case must complete. That is, pushing the USR button (or triggering the input pin with a IR module) will not advance to the next light show while the previous one is still running.

Here’s the entire sketch:

```
// ArduinoNeoPixelButton.INO

/*
Lightly edited by Pinball News
February, 2024
*/

/*
Original example code from Adafruit Industries
Adafruit Industries
http://adafruit.com
Adafruit_NeoPixel/examples/buttoncycler
/buttoncycler.ino
*/

/*
Adafruit_NeoPixel.h
adafruit/Adafruit_NeoPixel
https://github.com/adafruit/Adafruit_NeoPixel
*/

/*
The Magic of NeoPixels
https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels
*/

// Simple demonstration on using an input device to trigger changes on your
// NeoPixels. Wire a momentary push button to connect from ground to a
// digital IO pin. When the button is pressed it will change to a new pixel
// animation. Initial state has all pixels off -- press the button once to
// start the first animation. As written, the button does not interrupt an
// animation in-progress, it works only when idle.

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Digital IO pin connected to the button. This will be driven with a
// pull-up resistor so the switch pulls the pin to ground momentarily.
// On a high -> low transition the button press logic will execute.
#define BUTTON_PIN  24

#define PIXEL_PIN   23  // Digital IO pin connected to the NeoPixels.

#define PIXEL_COUNT 1   // Number of NeoPixels

// Declare our NeoPixel strip object:
Adafruit_NeoPixel strip(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);
// Argument 1 = Number of pixels in NeoPixel strip
// Argument 2 = Arduino pin number (most are valid)
// Argument 3 = Pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)

boolean oldState = HIGH;
int     mode     = 0; // Currently-active animation mode, 0-9

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  strip.begin(); // Initialize NeoPixel strip object (REQUIRED)
  strip.show(); // Initialize all pixels to 'off'
  strip.setBrightness(15); // Set BRIGHTNESS to 15 (max = 255)
}

void loop() {
  // Get current button state.
  boolean newState = digitalRead(BUTTON_PIN);

  // Check if state changed from high to low (button press).
  if((newState == LOW) && (oldState == HIGH)) {
    // Short delay to debounce button.
    delay(20);
    // Check if button is still low after debounce.
    newState = digitalRead(BUTTON_PIN);
    if(newState == LOW) {      // Yes, still low
      if(++mode > 8) mode = 0; // Advance to next mode, wrap around after #8
      switch(mode) {           // Start the new animation...
        case 0:
          colorWipe(strip.Color(  0,   0,   0), 50);    // Black/off
          break;
        case 1:
          colorWipe(strip.Color(255,   0,   0), 50);    // Red
          break;
        case 2:
          colorWipe(strip.Color(  0, 255,   0), 50);    // Green
          break;
        case 3:
          colorWipe(strip.Color(  0,   0, 255), 50);    // Blue
          break;
        case 4:
          theaterChase(strip.Color(127, 127, 127), 50); // White
          break;
        case 5:
          theaterChase(strip.Color(127,   0,   0), 50); // Red
          break;
        case 6:
          theaterChase(strip.Color(  0,   0, 127), 50); // Blue
          break;
        case 7:
          rainbow(10);
          break;
        case 8:
          theaterChaseRainbow(50);
          break;
      }
    }
  }

  // Set the last-read button state to the old state.
  oldState = newState;
}

// Fill strip pixels one after another with a color. Strip is NOT cleared
// first; anything there will be covered pixel by pixel. Pass in color
// (as a single 'packed' 32-bit value, which you can get by calling
// strip.Color(red, green, blue) as shown in the loop() function above),
// and a delay time (in milliseconds) between pixels.
void colorWipe(uint32_t color, int wait) {
  for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
    strip.setPixelColor(i, color);         //  Set pixel's color (in RAM)
    strip.show();                          //  Update strip to match
    delay(wait);                           //  Pause for a moment
  }
}

// Theater-marquee-style chasing lights. Pass in a color (32-bit value,
// a la strip.Color(r,g,b) as mentioned above), and a delay time (in ms)
// between frames.
void theaterChase(uint32_t color, int wait) {
  for(int a=0; a<10; a++) {  // Repeat 10 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in steps of 3...
      for(int c=b; c<strip.numPixels(); c += 3) {
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
    }
  }
}

// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait) {
  // Hue of first pixel runs 3 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 3*65536. Adding 256 to firstPixelHue each time
  // means we'll make 3*65536/256 = 768 passes through this outer loop:
  for(long firstPixelHue = 0; firstPixelHue < 3*65536; firstPixelHue += 256) {
    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}

// Rainbow-enhanced theater marquee. Pass delay time (in ms) between frames.
void theaterChaseRainbow(int wait) {
  int firstPixelHue = 0;     // First pixel starts at red (hue 0)
  for(int a=0; a<30; a++) {  // Repeat 30 times...
    for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      // 'c' counts up from 'b' to end of strip in increments of 3...
      for(int c=b; c<strip.numPixels(); c += 3) {
        // hue of pixel 'c' is offset by an amount to make one full
        // revolution of the color wheel (range 65536) along the length
        // of the strip (strip.numPixels() steps):
        int      hue   = firstPixelHue + c * 65536L / strip.numPixels();
        uint32_t color = strip.gamma32(strip.ColorHSV(hue)); // hue -> RGB
        strip.setPixelColor(c, color); // Set pixel 'c' to value 'color'
      }
      strip.show();                // Update strip with new contents
      delay(wait);                 // Pause for a moment
      firstPixelHue += 65536 / 90; // One cycle of color wheel over 90 frames
    }
  }
}
```

**Finished Controller**

For the software portion, the “BUTTON\_PIN”, “PIXEL\_PIN”, “PIXEL\_COUNT”, and “NeoPixel strip object” were all selected to match the hardware we are using – in this case, the VCC-GND Studio YD-RP2040.

If you wanted to use a different board or alternative NeoPixel type, you would have to select the pin values and NeoPixel object to match.

The VCC-GND Studio YD-RP2040 was chosen as an example board for its singular NeoPixel and pre-mounted user button. By referring to the previous Pinball Ball Detector set of articles in this series ([Part One](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/) and [Part Two](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-two/)) you can determine how to add the IR and relay modules to almost any controller module, and get those modules to work in conjunction with the detection of pinball(s) inside your pinball machine.

With hardware and software together, we have a finished RP2040-based prototype controller.

[![The YD-RP2040 board powered with NeoPixel at 'case 0' (OFF)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/236-pinball-ball-detector-1024x602.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/236-pinball-ball-detector.jpg)

The YD-RP2040 board powered with NeoPixel at ‘case 0’ (OFF)

[![The YD-RP2040 board powered with NeoPixel at 'case 7' (Rainbow)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/237-pinball-ball-detector-1024x602.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/237-pinball-ball-detector.jpg)

The YD-RP2040 board powered with NeoPixel at ‘case 7’ (Rainbow)
