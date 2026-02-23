---
title: "NEW IR PINBALL TESTERS: PART ONE"
date: 2022-10-16
url: https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-one
source: Pinball News
era: wordpress
---

Infrared (IR) transmitters and receivers are vital components used in many electronic pinball machines since 1987. Commonly referred to as ‘opto-switches’ or simply ‘optos’, paired-up transmitters and receivers allow contactless sensing of movement in order to register a target hit, detection of a ball’s position or the sensing of movement by a mechanical device.

However, useful as these components are, they do have one characteristic which makes it difficult to troubleshoot them (or the circuit of which they form a part). The infrared light they either transmit or sense is usually invisible to the human eye.

That makes it tricky to tell whether an IR transmitter is radiating as intended, and whether an IR receiver is detecting IR radiation correctly.

Back in 2006, Todd Andersen of Pinball Renaissance in Minnesota wrote an article describing how to build your own matching IR transmitter and IR receiver to aid with testing. When the associated button is pressed, these car-fob-sized devices would either transmit a constant IR beam, or light an LED to indicate the detection of IR radiation, thus allowing you to diagnose faults with both IR transmitters and receivers.

While extremely useful and functional, much has changed in the world of electronics in the past sixteen years. The availability of the component parts has changed as has the cost, while newer methods have become easily afforded.

So, Todd has looked anew at the problem and devised an alternative, automated, more modern and more readily-available alternative you can build at home.

In this first article he looks at the hardware used in his design, how the components are chosen, and includes links to the components’ suppliers for more information, while the second part concentrates on the software needed, providing code you can use immediately or modify to your own requirements.

Over to Todd…

---

Having previously put myself in your shoes, I’ll summarise two of my main reasons for deciding an [earlier Pinball News article](https://www.pinballnews.com/learn/irtester.html) about building your own IR testers possibly needed an update…

1. **First and foremost, [soldering](https://www.pinballnews.com/learn/soldering/index.html).**
   • Many people can’t solder.
   • Many people don’t want to solder.
   • With this new version, connections can be simply wrapped and hot glued, or even bolted in place.
2. **Technology is changing.**
   • Modern computers (post-2015) do always not play nicely with Arduino devices.
   • Microcontroller technology is now cheaper, smaller, more capable, and newer.
   • Software (sketches) can be easily modified for use with various board/component combinations.

Pinball Renaissance sold a ‘fob’ version of the IR Tester sets – sender and receiver pairs – to pinball hobbyists. These testers were built using discrete electronic components and sold out some time ago.

While fulfilling a special request to make more, I noticed that I lacked enough discrete components to complete said order. At that point, I realised I could update the IR Pinball Testers from all-discrete electronic components, to use newer Arduino clone boards.

Most of the clone boards I had in stock were subsequently made into IR Pinball Testers. These new IR Testers are now sold out as well, with completion of this special request marking these new Arduino clone board based IR Tester sets as no longer available.

Using the Arduino clone boards to complete the special order significantly dwindled my stock of the specific microcontroller clone board I used.

When I shopped reputable mainstream retailers to try to purchase enough boards to replenish stock, I discovered two things. First, assuming in large part due to the global chip shortage, prices had over quadrupled. Second, and again I’m assuming related to the assumed reason behind the first, boards were wildly out of stock.

This forced me to search even harder. In doing so, I discover I could purchase complete Attiny85 microcontroller-based boards for less than the cost of the Attiny85 microcontroller chips alone.

So, I decided to purchase these new-to-me Attiny85 based clone boards.

**Tiny Boards**

To replenish my stock, I found the [EDATtiny](https://www.electrodragon.com/product/attiny85-mini-dev-board-lilytiny-digispark-edatiny/) from [ElectroDragon](https://www.electrodragon.com/). These one inch diameter boards are designed to be ‘wearable’ and feature the ATtiny85 microprocessor, being programmable via the Arduino IDE software.

However, these Chinese clone boards had a 20% failure rate, although the manufacture did refund me for those failed boards.

Per the manufacturer, these red EDATtiny boards are, “*Compatible with lilytiny, digispark bootloader, to upload sketch please add board digispark 16.5mhz in arduino IDE.*”

[![The top and bottom of the EDATtiny board](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/01-new-ir-testers-1024x605.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/01-new-ir-testers.jpg)

The top and bottom of the EDATtiny board

As an alternative, the layout and board colours of the black and purple Lilytiny clone boards (shown below) are only cosmetic differences from the EDATtiny boards I used (shown above). These Lilytiny clone boards should otherwise be identical to the EDATtiny boards.

[![The Lilytiny ATTiny85 boards](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/02-new-ir-testers-1024x576.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/02-new-ir-testers.jpg)

The Lilytiny ATTiny85 boards

All three round boards are actually clones of [Digispark square boards](http://digistump.com/products/1). In fact, and as introduced earlier, DigiStump started it all with their Digispark boards. After all, they are, “*Home of the Digispark*.”

For the price I found for the standalone ATtiny85 chips, I could purchase two complete EDATtiny boards. This included the same shipping and handling costs.

In addition to affordability, I noticed the use of holes and their spacing on these boards made connecting a few discrete electronic components quite easy. I realised this made these boards ideal for pinball hobbyists who may want to build their own IR Tester boards. And, the built-in/onboard LED of the EDATtiny saves us from having to bother with even more discrete electronic components.

For those who want to try this at home, the few supporting discrete electronic components needed can be easily attached without soldering. The legs of these components can be wrapped in place and secured with hot glue. Or, the legs can simply be bolted in place if you prefer.

**Discrete Components**

Here are the additional components you will need:

**IR LED (Sender – 880nm wavelength)**
Industry **P**art **N**umber (**PN)**: QED123
Substitute PNs: QED121, QED122, 276-143, 276-143C
Old WMS Pinball PN: A-16908
*(Note: Some pinball parts sellers may sell this component already mounted on a board.)*
New WMS Pinball PN: 5671-12731-00
*(Note: This is usually sold as just the discrete component itself.)*

![Williams Pinball Ir LED (Sender – 880 nm wavelength)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/10-new-ir-testers-1024x344.jpg)

Williams Pinball IR LED (Sender – 880nm wavelength)

[![IR Transmitter specifications](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/11-new-ir-testers-813x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/11-new-ir-testers.jpg)

IR Transmitter specifications

This diode has polarity. This means it can only operate correctly in circuit when placed in a specific orientation. **The ANODE goes to the +5 Volt source on your ATtiny board; not the +5V pin.**

A 940nm wavelength side-looking version of this photodiode (PN: QEE113) can also be procured. It *should* work in pinball machines and may be useful for getting into smaller spaces like the small slot in between opto-interrupters, as used on drop targets and flipper mechanisms. However, that photodiode has not been tested for use in this article.

**IR Transistor (Receiver – 880nm sensitivity)**
Industry PN: QSD124
Substitute PN: 276-145 or 276-145A
Old WMS Pinball PN: A-16909
*(Note: Some pinball parts sellers may sell this component already mounted on a board.)*
New WMS Pinball PN: 5163-12732-00
*(This is usually sold as just the discrete component itself.)*

[![Williams Pinball IR Transistor (Receiver – 880nm sensitivity)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/03-new-ir-testers-1024x331.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/03-new-ir-testers.jpg)

Williams Pinball IR Transistor (Receiver – 880nm sensitivity)

[![IR Receiver specifications](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/04-new-ir-testers-725x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/04-new-ir-testers.jpg)

IR Receiver specifications

This transistor also has polarity. That means it can only operate correctly in circuit when placed in a specific orientation. **The COLLECTOR (non-flat side) goes to the +5V pin on your ATtiny board.**

A side-looking version of this NPN phototransistor (PN: QSE113 or QSE114) can also be sourced. It *may* be useful for getting into smaller spaces like the small slot between opto-interrupters, as used on drop targets and flipper mechanisms. However, that phototransistor has not been tested for use in this article.

**Resistor (10kΩ/10kOhms – 10,000 Ohms)**
1/4 (0.25) Watt
Axial Leads

[![A 10K Ohms resistor](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/05-new-ir-testers-1024x387.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/05-new-ir-testers.jpg)

A 10k Ohms resistor

**ATtiny85 Datasheet**

Atmel 8-bit AVR Microcontroller with 2/4/8K Bytes In-System Programmable Flash
ATtiny25/V / ATtiny45/V / ATtiny85/V
Rev. 2586Q–AVR–08/2013
The ATtiny85 datasheet can be found, in its entirety, [here](http://www.atmel.com/avr).

I’ll save you from having to look through all 234 pages of the datasheet and show you a summary of the most important part we need to know about the ATtiny85 chip.

[![A small section of the ATtiny85 Datasheet](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/07-new-ir-testers-1024x472.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/07-new-ir-testers.jpg)

A small section of the ATtiny85 Datasheet

The ATtiny85 can handle 40.0 mA of current per Input/Output pin. This is plenty for our simple use.

**Digispark Schematic**

[![The schematic for the Digispark design](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/08-new-ir-testers-1024x632.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/08-new-ir-testers.jpg)

The schematic for the Digispark design

From the schematic above we can see that the Digispark (and most clone boards) have an onboard LED, as previously written about in this article. And, that a resistor (R5) is used to limit that LED’s current.

More general information on [LEDs](https://www.pinballnews.com/learn/leds.html) and more technical information, including limiting the operating current of LEDs, was covered in a previous Pinball News [article](https://www.pinballnews.com/learn/pinduino/).

Taking an excerpt from the second, more technical article:

|  |
| --- |
| ***The following formula is based on [Ohm’s Law](https://en.wikipedia.org/wiki/Ohm's_law). Rdrop = (Vin – Vled) / Iled*** |

When reviewing manufacturer’s specification, you many need to substitute the following technical names in the formula below:

* Voltage In (**Vin**)
  This value is 5.0 for five volt UNO boards.
* LED Voltage (**Vf**)
  See the LED manufacturer’s specifications.
* LED Current (**If**)
  See the LED manufacturer’s specifications.

**R = (Vin – Vf) / If**

Long and short of all that technical mumbo-jumbo is, the onboard LED only uses a few milliamps (mA) of the 40 mA available on each ATtiny85 pin, leaving plenty of current for our use.

**ATTiny85 / Digispark Connections**

[![The ATtiny85 chip connections](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/09-new-ir-testers-1024x492.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/09-new-ir-testers.jpg)

The ATtiny85 chip connections

The **numbers** inside the rectangle are the physical pins of the ATtiny85 chip.
The  **numbers** outside the rectangle are Arduino digital pin designations.
The  **A-numbers**  outside the rectangle are Arduino analog pin designations.

**Digispark Clone Model Identification**

Three models have been shipped. They have no feature differences, only a different connection for the on-board LED.

From the Digispark section of the Digistump [Wiki](http://digistump.com/wiki/digispark/tutorials/modelbi2c) . . .

|  |
| --- |
| “Y*ou can identify your model by the presence of ‘rev2’, ‘rev4’, or nothing on the top (the side with the gold connectors) of the USB end of the Digispark. Also, there is a ‘rev3’ version in circulation; this is actually counterfeit (i.e. a clone which falsely uses the Digispark trade name), although functionally it seems to match the (true) revisions 2 and 4.*  *‘rev2’ or ‘rev4’ marking: The on-board LED is connected to P1. This board should cause no conflicts with any devices, but remember the LED is on pin 1 not pin 0!*  *No marking: The on-board LED is connected to P0.*“ |

Note: Most Digispark clones will have their on-board LEDs connected to P1. If yours is not the case, use 0 (for P0) in the #define you will add to the “Blink” sketch featured in Part Two of this article.

**Putting it all Together**

We can cleverly use all the gathered information and a couple of Arduino programming tricks to deduce a few shortcuts when building ATtiny IR Testers.

**Sender Connections**

The lead associated with the flat spot on the lens of the IR diode goes to PB0 on the sender board.
The other lead of the Diode goes to PB1 on the sender board.

[![The IR LED attached](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/12-new-ir-testers-768x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/12-new-ir-testers.jpg)

The IR diode attached to the transmitter board

**Receiver Connections**

One lead of the IR transistor goes to +5V on the receiver board.
The resistor/transistor combined lead is associated with the flat spot in the lens, and goes to PB2 on the receiver board.

It’s a good tight fit for the other end of the 10kΩ resistor to go to PB0 on the receiver board.

[![The IR transistor attached to the receiver board](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/13-new-ir-testers-808x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/13-new-ir-testers.jpg)

The IR transistor attached to the receiver board

**Changing to Battery Power**

The simplest way to power your tiny IR Testers is to employ the cable you will have used to program your board and a cheap 5 Volt battery bank.

Alternatively, a 9 Volt snap cap and 9 Volt battery can also be used.

[![Adding a 9V battery connector](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/15-new-ir-testers-1024x524.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/15-new-ir-testers.jpg)

Adding a 9V battery connector

When making these battery connections, put the snap cap’s **RED** wire to your board’s **VIN** connection and the snap cap’s **BLACK** wire to your board’s **GND** connection.

![The battery power connections](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/14-new-ir-testers-1024x517.jpg)

The battery power connections

**Completing your Sender and Receiver**

It is recommended you electrically insulate your little boards from possibly shorting to something. Some of you may want to go as far as to create your own custom 3D printed cases. Others may wish to cleverly employ clear heat shrink tubing. While still others may simply want to wrap all exposed metal in clear tape.

**Programming**

Please see the companion to this article to learn how you can program these boards with Arduino.

Sorry, Pinball News cannot provide Arduino coding or troubleshooting advice. However, there are many resources available for you that are listed at the end of this article for your convenience.

**Testing**

Once programmed and powered, the IR Sender and Receiver can be used to test each other.

Below you can see the IR Sender on the left and IR Receiver on the right, with power indicator LEDs glowing brightly, but on-board/built-in LEDs unlit while the boards are booting up.

[![The powered IR Transmitter and Receiver boards](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/16-new-ir-testers-1024x599.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/16-new-ir-testers.jpg)

The powered IR Transmitter and Receiver boards

Pictured below are the Sender on the left and Receiver on the right, this time with power indicator LEDs glowing brightly along with the on-board/built-in LEDs.

![The boards with their in-built controlled LEDs lit](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/17-new-ir-testers-1024x603.jpg)

The boards with their in-built controlled LEDs lit

Once you insulate your IR Tester sets, they will be ready to help you troubleshoot IR LEDs which are used as switches in many pinball machines. The receiver may also be used on its own to verify dead batteries in your television remote.

**Resources**

**Parts Suppliers**

**Learning Links**

**Going Further**

**Pinball Repair Guides**

This concludes the first, hardware-related half of this pair of Pinball News articles.

[**Please follow this link to view the second half, featuring the software details.**](https://www.pinballnews.com/site/?p=26053)
