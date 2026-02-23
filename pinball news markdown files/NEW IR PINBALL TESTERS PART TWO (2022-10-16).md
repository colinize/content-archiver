---
title: "NEW IR PINBALL TESTERS: PART TWO"
date: 2022-10-16
url: https://www.pinballnews.com/site/2022/10/16/new-ir-pinball-testers-part-two
source: Pinball News
era: wordpress
---

Welcome to the second part of Todd Andersen’s article detailing how to build and program an infra-red (IR) tester transmitter and receiver.

[The first part](https://www.pinballnews.com/site/?p=25980) showed the components used, why they were selected, and how to connect them to build the two devices.

Now it’s time to program the microcontrollers to pulse the IR transmitter’s LED and indicate with the in-built LED when the receiver detects IR radiation.

Back to Todd…

---

Don’t worry if you haven’t programmed before. I took advantage of the easy-to-use [Arduino IDE (Integrated Development Environment)](https://www.arduino.cc/en/software), and you can too. If needed, a troubleshooting section is included at the end of this second part.

**Getting Started**

Use of a good quality programming cable and a USB hub is highly recommended. These did, indeed, fix the major issue of my Windows 10 computer not automatically detecting any ATtiny85-based board I was using as a **P**lug and **P**lay **(PnP)** device. See the [Digistump wiki](http://digistump.com/wiki/digispark) for even more help getting started.

**Programming**

When first trying to programming these ATtiny85-based boards I went through multiple drivers and board configuration files to get Windows 7 and 10 to play nice.

I was only partly successful until I either updated the Arduino Integrated Development Environment (IDE) to the latest version or, in the case of Windows 10, it just ‘felt’ like these non-native boards should be detected as PnP devices.

In both of these cases, my uploading to the boards stopped-at-start. I also found myself fighting Windows 10 every time it decided it had to be upgraded; against my requesting it not to. And, with Windows 11 already here, I had to find a permanent solution.

As brought up at the start of this article,that solution was to simply employ an inexpensive USB hub between whichever computer and whichever ATtiny85 board variety I tried to connect.

Any cheap USB hub, powered or unpowered, should do the trick. My first attempt’s success rate was anecdotally only about ten percent. In fact, it usually took three attempts to be successful, so a little patience and doggedness was required.

Instructions at this point assume you have the [Arduino](https://www.arduino.cc/en/software) [I](https://www.arduino.cc/en/software)[D](https://www.arduino.cc/en/software)[E](https://www.arduino.cc/en/software)[software](https://www.arduino.cc/en/software) on your computer and Digstump boards selected in Arduino. If not, Digstump has an incredibly detailed but easy-to-follow [tutorial](http://digistump.com/wiki/digispark/tutorials/connecting) for both requirements.

Instructions from this point also assume you have rudimentary experience using the Arduino software.

If not, Pinball News has already covered the use of Arduino software in a [previous article](https://www.pinballnews.com/learn/pinduino/index.html).

Instructions from this point also assume you are programming a Digistump Digispark clone board. However, the code found later on in this article can be easily modified to work with genuine Arduino boards and alternative clone boards if you wish.

Open whichever version of the Arduino IDE you are using. It should automatically open and fill your entire computer screen.

* Go to ‘Tools’ in the **U**pper **L**eft **H**and **(ULH)** corner.
* Go down to ‘Board’.
* Go down and over to ‘Digistump AVR Boards’.
* Select ‘Digispark (default – 16.5 Mhz)’ with either a left mouse click or by pressing ‘Enter’ on your keyboard.

[![Selecting the appropriate board](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/21a-new-ir-testers-1024x624.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/21a-new-ir-testers.jpg)

Selecting the appropriate board

If your board can be programmed by the Arduino IDE, it will probably already have the manufacturer’s test program (known as a ‘sketch’) on it. Therefore, its on-board LED may be blinking when you first plug your board in to your computer’s USB port.

Verify you can load your own sketch by testing your board with Arduino’s built in ‘Blink’ sketch.

* While still in Arduino, left mouse click ***File*** in the **ULH** corner.
* Go down to ***Examples***
* Go down and over to ***01 Basics***
* Go down and over to ***Blink***
* Select ***Blink*** with either a left mouse click or by pressing Enter on your keyboard

[![Loading the Blink sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/22a-new-ir-testers-1024x577.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/22a-new-ir-testers.jpg)

Loading the Blink sketch

The ‘Blink’ sketch will automatically pop up.

This is the how the ‘Blink’ small-sized popup window looks:

[![The Blink sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/23-new-ir-testers-1009x1024.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/23-new-ir-testers.jpg)

The Blink sketch pop-up

To make programming easier, you may want to make the sketch window fit your computer monitor’s entire screen. This is done by simply left-clicking the ‘Maximize’ box in the **U**pper **R**ight **H**and **(URH)** corner.

[![The Blink sketch window when maximised](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/24a-new-ir-testers-1024x577.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/24a-new-ir-testers.jpg)

The Blink sketch window when maximised

Once the “Blink” sketch is up on your screen, you will do your first bit of programming by slightly modifying it – adding just one line of programming syntax to the freshly opened sketch.

The purpose of this new line is to let the program know which pin on the Digispark clone board has its built in [**L**ight **E**mitting **D**iode **(LED)**](https://www.pinballnews.com/learn/leds.html).

**Digispark Clone Model Identification**

Three models of the Digispark clone boards have been shipped. They have no feature differences, only a different connection for the on-board LED.

From the Digispark section of the Digistump  [Wiki](http://digistump.com/wiki/digispark/tutorials/modelbi2c) . . .

|  |
| --- |
| “*You can identify your [model](http://digistump.com/wiki/digispark/tutorials/modelbi2c) by the presence of ‘rev2’, ‘rev4’, or nothing on the top (the side with the gold connectors) of the USB end of the Digispark. Also, there is a ‘rev3’ version in circulation; this is actually counterfeit (i.e. a clone which falsely uses the Digispark trade name), although functionally it seems to match the (true) revisions 2 and 4. Rev2 or Rev4 marking: The on-board LED is connected to P1 This board should cause no conflicts with any devices, but remember the LED is on pin 1 not pin 0! No marking: The on-board LED is connected to P0.*” |

Note: Most Digispark clones will have their on-board LEDs connected to Arduino pin designation 1 (for board designation PB1). If this is not the case for yours, use 0 (for board designation PB0) in the #define you will add to the ‘Blink’ sketch.

**Test Your Boards**

Use your mouse wheel or the slide bar on the right side to go the bottom of the sketch.

[![The bottom of the Blink sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/25a-new-ir-testers-1024x574.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/25a-new-ir-testers.jpg)

The bottom of the Blink sketch

Notice the **(empty space)** between  . . .

```
https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/
(empty space)
// the setup function runs once when you press reset or power the board
```

In place of the empty space, add:

```
#define LED_BUILTIN 1
```

So it now reads:

```
https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/
#define LED_BUILTIN 1
// the setup function runs once when you press reset or power the board
```

[![The on-board LED is defined](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/26a-new-ir-testers-1024x576.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/26a-new-ir-testers.jpg)

The on-board LED is defined

LED\_BUILTIN is the on-board LED specified in [Digispark Clones Model Identification](http://digistump.com/wiki/digispark/tutorials/modelbi2c). Here we have selected the default of ‘1’.

The Digispark clone board’s built-in LED is now identified in the sketch.

Click the Upload Right Arrow (►) or use the Ctrl+U keyboard shortcut.

At the bottom of the window, you will be told to, “Plug in device now”.

[![Plug in your board at this point](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/27-new-ir-testers-1024x576.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/27-new-ir-testers.jpg)

Plug in your Sender board at this point

[![The same message a little clearer](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/28-new-ir-testers-1024x249.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/28-new-ir-testers.jpg)

The same message as above but a little clearer

This “Flash write error” (below) at the bottom of the window is to be expected.

[![No cause for alarm](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/29-new-ir-testers-1024x244.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/29-new-ir-testers.jpg)

No cause for alarm

If you get some sort of a “flash write error” it’s actually a good sign. This is due to ‘bit-banging’ or technology incompatibility issues. But, it means your board is probably working. Just follow the instructions that will follow the error – and simply try again.

On the second try, by looking at the bottom of the window you can see a second error.

[![Another try, another error](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/30-new-ir-testers-1024x210.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/30-new-ir-testers.jpg)

Another try, another error

Chances are, this won’t reconnect. Simply close the Arduino IDE software, reopen it, and try again.

You know what they say? You can see by checking the bottom of the window that…

[![Third time’s a charm!](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/31-new-ir-testers-1024x396.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/31-new-ir-testers.jpg)

Third time’s a charm!

**Program Your Boards**

* Open new instance/widow of the Arduino IDE.
* Go to ***File*** and go down to and click on ***New*** (or use Ctrl+n).
* A new Arduino window will pop up, which you can maximise.

[![A new empty sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/32-new-ir-testers.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/new-ir-testers/32-new-ir-testers.jpg)

A new empty sketch

Select and copy (***Ctrl+c***) the **ATTinyUniqueBlinkPattern** sketch in the grey box below.

Click anywhere in the sketch window and use ***Ctrl+a*** to select all of the default sketch.

Use ***Ctrl+v*** to paste the copied **ATTinyUniqueBlinkPattern** sketch so it replaces the blank sketch.

Use the same procedure as above to upload this sketch to the Sender board.

```
//ATTinyUniqueBlinkPattern.INO
// Author: Pinball News
// Website: https://www.pinballnews.com/
// Creation Date: 16-SEP-22

// This code is in the public domain.
// Please feel free to: copy, distribute, or modify this sketch.

// This very simple program (Arduino sketch) makes an ATtiny85 based board blink both its onboard LED and attached IR LED a unique pattern.

// This unique pattern of seven blinks is different than any signal in a pinball machine; therefor helpful for diagnostics / troubleshooting.

// The built-in / onboard LED is on pin 0 for Digispark Model B . . . and . . . that LED is on pin 1 for Digispark Model A or EDAtiny.

// Change the number in "digitalWrite(1, HIGH);" to match the onboard LED pin number for your specific board.

void setup() {
pinMode(1, OUTPUT);       // This is Pin 1 / PB1 on the ATtiny85 board and the Anode / +5 volt connection for the Ir Diode.
pinMode(0, OUTPUT);       // This is Pin 0 / PB0 on the ATtiny85 board and Cathode / GND connection for the Ir Diode.
digitalWrite(0, LOW);        // In this application: 0, LOW, and GND are all the same thing.
delay (10);                           // This short delay is important and allows the ATtiny itself to think about how it is going to best work for you.
}

void loop() {
// 1st Blink                        // This blink is similar to all 7; therefore only this 1st Blink will be fully commented.
  digitalWrite(1, HIGH);   // This turns on the ATtiny onboard LED and Ir LED by making the voltage HIGH / +5 Volts.
  delay(175);                     // This holds / keeps the ATtiny LEDs turned on.
  digitalWrite(1, LOW);   // This turns the LEDs off by making the voltage LOW / GND.
  delay(175);                     // This keeps the LEDs turned off.
// 2nd Blink                      // Lather, rinse, repeat.
  digitalWrite(1, HIGH);
  delay(175);
  digitalWrite(1, LOW);
  delay(175);
// 3rd Blink
  digitalWrite(1, HIGH);
  delay(175);
  digitalWrite(1, LOW);
  delay(175);
// 4th Blink
  digitalWrite(1, HIGH);
  delay(175);
  digitalWrite(1, LOW);
  delay(175);
// 5th Blink
  digitalWrite(1, HIGH);
  delay(175);
  digitalWrite(1, LOW);
  delay(175);
    delay(500);
// 6th Blink
  digitalWrite(1, HIGH);
  delay(150);
  digitalWrite(1, LOW);
  delay(150);
// 7th Blink
  digitalWrite(1, HIGH);
  delay(150);
  digitalWrite(1, LOW);
  delay(150);
delay(2000);
}
```

Follow the same procedure to paste the **ATtiny85IrReceiver** sketch below into another new window and upload it to the Receiver board.

```
//ATtinyIrReceiver.INO

// Author: Pinball News
// Website: https://www.pinballnews.com/
// Creation Date: 17-SEP-22

// This code is in the public domain.
// Please feel free to: copy, distribute, or modify this sketch.

// This very simple program (Arduino sketch) makes an ATtiny85 based board light its onboard LED when an IR source is present.

// The builtin / onboard LED is on pin 0 for Digispark Model B . . . and . . . that LED is on pin 1 for Digispark Model A or EDAtiny

// Change the number in "digitalWrite(1, HIGH);" to match the onboard LED pin number for your specific board.

//  Connections for the Phototransistor / 10 KOhm resistor follow . . .
//  +5V pin on the ATtiny85 board / the Collector of the Ir Transistor.
//  PB2 pin on the ATtiny85 board and the Emitter of the Ir Transistor / 10 KOhm resistor connection.
//  PB0 pin on the ATtiny85 board and the other side of the 10 KOhm resistor.

void setup() {
  pinMode(A1, INPUT);       // This is PB2 on the ATtiny85 board and Pin A1 in the Arduino sketch.
  pinMode(1, OUTPUT);      // This is PB1 on the ATtiny85 board, the onboard LED and Pin 1 in the Arduino sketch.
  pinMode(0, OUTPUT);      // This is PB0 on the ATtiny85 board and Pin 0 in the Arduino sketch.
  digitalWrite (0, LOW);      // This grounds the other side of the 10 KOhm resistor.
    delay (10);                        // This short delay is important and allows the ATtiny itself to think about how it is going to best work for you.
}

void loop() {
analogRead(A1);              //This reads the value Ir light detected by theg Ir Transistor.
if(analogRead(A1) > 33)  {
  digitalWrite(1, HIGH);  //This turns ON the onboard LED when Ir light is detected.
  }
else  {
digitalWrite(1, LOW);     //This turns OFF the LED onboard when no Ir light is detected.
  }
}
```

**Troubleshooting and ‘Got-Ya’s**

1. Is it worth having to retry programming the same board? With: changing technology, the prices of other boards, and their unavailability – yes – but YMMV.
2. Buy fresh new Digispark clone boards from a dependable dealer. Still expect that ten percent of your boards simply will not work.
3. The names of the individual ATTiny85 pins vary upon how they are referenced: physical, designation, and use.
4. Use a good quality, male USB 2.0 A-male to a USB 2.0 Micro-B male cable, that can handle both power and data.
5. Use a cheap USB hub between your computer and your boards.
6. Don’t plug in your chosen ATtiny85 clone boards until the you get the Arduino prompt to do so from your computer.
7. Be patient and allow the Digispark bootloader and the Arduino IDE time to do their work.
8. Close the Arduino program and open it up for a second or even third try.
9. Even when battery-powered, your ATtiny85 board it will still try to ‘talk’ to your computer for a few seconds each time power is applied.
10. Test your IR Sender and Receiver boards with each other. If either either do not work, check to make sure you have placed your components with correct orientation.
11. Your IR Receiver is responsive enough to be tested with a standard TV IR remote.
12. The beam angles of the IR components are quite narrow, therefore the testers work best when kept parallel to the IR switches under test.

**Digistump Digispark Wiki**

**Pinball Repair Guides**

**Conclusion**
With your ATtiny85-based clone boards built, programmed, and tested, you should be able to use them to troubleshoot Infrared (IR) switches in pinball machines.

This concludes the second, software-related half of this pair of Pinball News articles. Please follow **[this link](https://www.pinballnews.com/site/?p=25980)** to view the first half covering the hardware’s details.
