---
title: "PINBALL ADD-ON CONTROLLER: PART ONE"
date: 2022-12-24
url: https://www.pinballnews.com/site/2022/12/24/pinball-add-on-controller-part-one
source: Pinball News
era: wordpress
---

**Date:** 20th December, 2022

In his recent two-part article about making your own infra-red testers, Todd Andersen introduced the use of cheap microcontrollers to replace the discrete components used in his earlier design.

He showed how microcontrollers can be programmed to provide more flexibility and more inputs/outputs than using discrete components.

This led to the idea of using microcontrollers and additional plug-in modules to control a range of pinball add-ons, such as animated toppers.

Over to Todd to explain how…

---

This is the first part of a two-part article. In this half we deal with *Digispark* and Arduino *Nano* clone board hardware. The *Nano* clone is used for larger and more complicated projects requiring multiple inputs to control multiple outputs.

Both the *Digispark* and *Nano* clone boards operate on +5 Volts. These +5V versions were chosen to allow more freedom from power requirements, however, some versions of these modules – and their peripheral modules – may not use +5 Volts and use [+3.3 Volts](https://forum.arduino.cc/t/powering-arduino-uno-with-3-3v/544396) instead. In this case, use of a [+3.3V power supply](https://docs.arduino.cc/learn/microcontrollers/5v-3v3) or [level shifter](https://learn.sparkfun.com/tutorials/bi-directional-logic-level-converter-hookup-guide/all) may be required.

**No Soldering Needed**

For those who do not wish to solder – or simply for faster hardware assembly – manufacturers of Arduino clone boards have made it easy for you to still use their products by also producing modules and ‘shields’ with pins pre-installed.

‘Shields’ are boards with sockets which mate with the pins on the Arduino clone boards, or vice-versa. Shields are available for both *Digispark* and *Nano* clones. However, there are far more shields for *Nano* clones.

**Nano Boards with Connectors already Soldered**

Arduino clone boards can be purchased with rows of pins, called ‘pin headers’ or just ‘headers’, already installed.

Pictured below is an Arduino *Nano* clone board with pin headers already installed by the manufacturer.

[![An Arduino Clone board with the pin headers on the bottom side](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/022-pinball-add-on-controller-1024x717.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/022-pinball-add-on-controller.jpg)

An Arduino Nano clone board with the pin headers on the bottom side

One of the two single rows of input/output (I/O) pins is visible already installed underneath the board. A second row of pins is installed at the back of the board. The usually-unused double-row header for programming the controller is pre-mounted on the top left side of the board.

**Dupont Wires**

*Dupont Wires* are pre-cut lengths of jumper cable with a pre-installed male or female connector on each end. They are available in male-to-male, male-to-female or female-to-female varieties and are typically around 20cm/8 inches in length.

*Dupont Wires* can be used to make good solderless electrical connections and can even be connected end-to-end to increase their overall length. The connections of these wires can be physically shored with super glue, hot glue, tape, or even heat shrink.

[![A super glued joint](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/009-pinball-add-on-controller-1024x656.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/009-pinball-add-on-controller.jpg)

A super glued joint

[![A taped joint](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/011-pinball-add-on-controller-1024x684.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/011-pinball-add-on-controller.jpg)

A taped joint

[![A heat shrink joint, before and after heat is applied](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/012-pinball-add-on-controller-1024x698.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/012-pinball-add-on-controller.jpg)

A heat shrink joint, before and after heat is applied

**Lever Connectors**

Several different types and configurations of lever connectors are available. The male pins of *Dupont Wires* can be easily slid into and securely fastened by these connectors. Pictured below are two of the many different lever connectors available.

[![1-in/1-out, one lever open but both connector ends unused](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/013-pinball-add-on-controller-1024x745.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/013-pinball-add-on-controller.jpg)

1-in/1-out with one lever open but both connector ends unused

[![1-in/3-out, shown with just the pin ends under the lever arms and housings partially exposed](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/015-pinball-add-on-controller-1024x710.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/015-pinball-add-on-controller.jpg)

1-in/3-out, shown with just the pin ends under the lever arms and housings partially exposed

**Shields with Screw Terminals**

In addition to pins and sockets, various shields are available with the addition of screw terminals. Once again, the male pin ends of *Dupont Wires* can be seated under the connectors and their retaining hardware screwed down to make easy, yet steadfast, solderless connections.

Pictured below is one type of shield with dual rows of both socket and screw header terminals. Simply align the pin numbers on the *Nano* clone board with those on the shield’s sockets to securely nestle the *Nano* clone between the screw terminals.

[![A breakout shield to bring the pin header connections onto screw terminals](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/016-pinball-add-on-controller-1024x748.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/016-pinball-add-on-controller.jpg)

A breakout shield to bring the pin header connections onto screw terminals

Pictured below is an example of another such screw terminal shield, this time populated with a *Nano* clone board ensconced on the board’s sockets. There is also a [ThingM *BlinkM*](https://thingm.com/products/blinkm) RGB LED secured into three of the screw terminals.

[![The shield with the Nano clone controller board installed along with an RGB LED](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/017-pinball-add-on-controller-1024x751.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/017-pinball-add-on-controller.jpg)

The shield with the Nano clone controller board installed along with an RGB LED

In the picture above, a *Nano* and screw shield work together as a programmer for the *BlinkM* programmable LED, which is the predecessor to the *NeoPixel*.

In this configuration, the *BlinkM* LED module can be programmed and tested at the same time. For hobbyists, several different dedicated programming shields are available, although we won’t be covering their use in these articles.

**Other Shields**

Many other types of shield are available for a multitude of purposes: motor control, optical isolation, servo control and Wi-Fi communication are just a few. As with the programming shields though, the use of these other shields will not be covered in these articles, but they provide many options for controlling your pinball add-ons.

**Breakout Shield**

Pictured below is a shield with four rows of sockets and various rows of pins mounted on the top side. The inner set of sockets is for mounting a *Nano* board. On each side of the *Nano* are triple rows of pin connections.

[![A Nano shield with multiple pin headers](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/004-pinball-add-on-controller-1024x719.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/004-pinball-add-on-controller.jpg)

A Nano shield with multiple pin headers

The socket arrangement easily and securely accommodates a *Nano* clone.

The triple pin set arrangement consists of: I/O, +5V and GND which makes this shield handy to use with assorted input and output modules. This is not only because of the arrangement of its pins, but also for that fact that no soldering is required to use it.

On the bottom left of the picture above is an input – a microphone/sound module. On the bottom right is an output – a *NeoPixel* ‘stick’. The stick is just one form factor for *NeoPixels*. [Several are available](https://learn.adafruit.com/make-it-glow-your-first-neopixel-project/choose-your-pixel-type). The [strips and strands](https://learn.adafruit.com/adafruit-neopixel-uberguide/neopixel-strips) are longer than the sticks and are usually more suited to larger pinball projects, such as illuminating toppers.

An adaptable Arduino ‘sketch’ for the pictured sound-to-light configuration is listed in the [software half of this article](https://www.pinballnews.com/site/?p=27475). The adaptability is for both the microphone/sound module input and user selected *NeoPixel* output. Your *Nano* clone can provide the digital signals for many *NeoPixels* but can not provide enough current to power them. Please see the [NeoPixel Überguide](https://learn.adafruit.com/adafruit-neopixel-uberguide) for information on powering [*NeoPixels*](https://learn.adafruit.com/adafruit-neopixel-uberguide/powering-neopixels).

**When You Need More Power and/or Effects**

Pictured below is a mostly solderless electronics test set-up using: a 5V *Nano* clone, a *Nano* I/O shield, a MOSFET power module, and an up-cycled button backlight board; all powered by a rechargeable USB battery pack and designed to be used together as a backlight for a topper on a *Rocky & Bullwinkle & Friends* pinball.

The MOSFET (IRD520) power module can supply much greater current than the *Nano* clone’s individual pin limit of 40mA; yet is controlled by an individual pin. The module is used here to power an entire row of higher-powered white LEDs.

[![Using a power module to drive more current than the Nano clone can supply](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/019-pinball-add-on-controller-1024x768.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/019-pinball-add-on-controller.jpg)

Using a power module to drive more current than the Nano clone can supply

Pictured below is the previous test setup with the addition of a passive infra-red (PIR) module which will detect human movement.

Coding, building and testing in stages – ensuring each stage works as expected before adding the next one – eases and lessens the troubleshooting.

This modular hardware approach makes it easier to add sound and/or voice effects. An MP3 amplifier module could easily be added into this setup.

[![A PIR module is added to detect movement](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/020-pinball-add-on-controller-1024x768.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/020-pinball-add-on-controller.jpg)

A PIR module is added to detect movement

As the test set-up stands, Bullwinkle’s eyes intermittently light up as you approach and play the game.

[![Bullwinkle J. Moose – seen but not heard](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/021-pinball-add-on-controller-1024x689.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-add-on-controller/021-pinball-add-on-controller.jpg)

Bullwinkle J. Moose – seen but not heard

To learn how to program Arduino *Digispark* and *Nano* clone boards to work with most of the modules shown here, please see the [second of this pair of articles](https://www.pinballnews.com/site/?p=27475).
