---
title: PINBALL BALL DETECTOR - PART TWO
date: 2024-02-02
url: https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-two
source: Pinball News
era: wordpress
---

**Introduction**

In the [first part of this article](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/), Todd Andersen showed us how to create a programmable pinball ball detector which can power an add-on or topper so that it reacts when a ball is sensed in a particular location.

This operates using an infrared (IR) module to sense the ball, an Arduino Uno microcontroller, and a relay module to switch the power to the add-on or topper. All these components are cheap, small and readily-available, while the use of a microcontroller provides lots of possibilities for additional inputs and outputs for far more complex interaction with the gameplay.

Before that though, we need to programme the basic functionality of detecting the ball and then switching the power to the add-on or topper.

Back to Todd.

---

I received feedback concerning a previous Pinball News two-part article ([Pinball Add-On Controller: Part One](https://www.pinballnews.com/site/2022/12/24/pinball-add-on-controller-part-one/) and [Pinball Add-On Controller: Part Two](https://www.pinballnews.com/site/2022/12/24/pinball-add-on-controller-part-two/)) being too technical. I hope to rectify that with this pair of follow-up articles.

This article is the second part and it concentrates on the software for the hardware featured in [part one](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/).

I will again be using one of the free software choices preferred by many hobbyists, Arduino IDE. For those not versed in that software, don’t worry. Though Pinball News has covered its use in a previous set of articles ([Intro to Arduino](https://www.pinballnews.com/site/2017/01/11/intro-to-arduino/) and [Pin-‘Uino](https://www.pinballnews.com/site/2017/01/12/pin-uino/)), the information will be covered in a slightly different way in this article.

**Modules**

All of the devices we are using are powered by a five volt supply. We specifically chose them for that reason, plus the way their power indicators light up when the device is correctly powered. See the [hardware part of these articles](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-part-one/) for the power connection details. The devices have also been chosen and configured so their input or output indicators light up when they activated.

We are going to examine each of the three steps – Input, Controller, and Output – in order, by looking at the associated module.

As has been the practise with these articles, each module will be examined by looking at the known information about the inputs and outputs, and then at their practical uses.

|  |
| --- |
| **Input Device – IR Module**  *What we know from the seller*  Input: “Detecting the reflected distance (1mm-25mm applicable)”  Output: “Signal output indicator (while the beam is reflected, outputs low level, indicator lights up)”  *Practical Use*  Input: Pinball is in front of the IR sensor pair  Output: A LOW at the output pin |
|  |

|  |
| --- |
| **Controller Device – Arduino Uno**  *What we know from the seller*  Input: 5 volt-tolerant general purpose Analog and Digital pins.  Output: 5 volt (HIGH) or 0 volt (LOW)  *Practical Use*  Input: Analog pin (A0)  Output: 5 volts (HIGH) at selected digital output pin #13 |
|  |

|  |
| --- |
| **Output Device – Relay Module**  *What we know from the seller*  Input: “High or Low Level Trigger”  Output: “1-Way” (with the indicator lighting up)  *Practical Use*  Input: 5 volts (HIGH) output from digital pin #13 of the Arduino  Output: A Normally Open (NO) connection |
|  |

**Input & Output Chain**

|  |
| --- |
| **IR Module** DO (output) |
|  |
| **Arduino Uno** A0 (input) Digital 13 (output) |
|  |
| **Relay Module** IN (input) COM & NO (output) |

**Software**

To communicate with the Arduino Uno you will need to install the Arduino Integrated Development Environment software, also known as the Arduino IDE.

You can download that software and get the documentation from the [Arduino website](https://www.arduino.cc/en/software).

Once you have installed that, connect the Arduino Uno’s USB port to your computer’s USB port.

Then, start the Arduino IDE software and make sure you have the correct type of microcontroller board selected. The method for doing this has changed with the latest versions of the Arduino IDE software. In older versions you select the board under the Tools menu.

[![Selecting the Arduino Uno board in the Arduino IDE software](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/101-pinball-ball-detector-1024x576.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/101-pinball-ball-detector.jpg)

Selecting the Arduino Uno board in the Arduino IDE software

In newer versions of the Arduino IDE the board can also be selected on the top toolbar.

[![The newer method of selecting your controller in the Arduino IDE software](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/255-pinball-ball-detector-1024x575.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/255-pinball-ball-detector.jpg)

The newer method of selecting your controller in the Arduino IDE software

When writing the code for our ball detector, it’s best to build and test in stages.

Because the IR module can be a little tricky to use to test the code, I used a capacitive switch module instead as the input device to test my starter code. It has the same pins and output level as the IR module we will be using, but only requires a finger’s touch on the sensor to activate rather than a reflective ball.

In the picture below, notice how the onboard yellow LED is lit when I touch the sensor. This LED is connected to the Digital 13 pin which will eventually cause the relay module to activate. The yellow LED indicates the software on the Arduino – called a ‘sketch’ – is working correctly.

[![The yellow LED connected to the Digital 13 pin is lit when the sensor is touched, showing the Arduino sketch is working correctly](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/257-1024x829.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/257.jpg)

The yellow LED connected to the Digital 13 pin is lit when the sensor is touched, showing the Arduino sketch is working correctly

The final sketch is just a slightly built-up version of this test sketch, with additional comments added to help explain how it works.

![The Arduino test sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/104-pinball-ball-detector.png)

The Arduino test sketch

Here is a commented version of the same test sketch.

[![The commented version of the Arduino sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/103-pinball-ball-detector-1024x604.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/103-pinball-ball-detector.jpg)

The commented version of the test Arduino sketch

You can view or download the test Arduino sketch with [this link](https://pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/IrSensModTestSketch.ino).

Although the final sketch is heavily commented for the user, here is an explanation of the sparse code.

|  |
| --- |
| `Line 1              void setup ()` |
| This is the specific way Arduino needs to initialize itself. |

|  |
| --- |
| `Line 3` **`pinMode (13, OUTPUT);`** |
| This sets digital pin #13 as an output rather than an input. Pin 13 was specifically chosen for our project because it is also attached to the onboard LED. This LED is used as an easy indicator of the Arduino doing something. |

|  |
| --- |
| `Line 4              pinMode (A0, INPUT);` |
| This sets Analog pin #0 as an input; rather than an in output. Pin #0 was chosen purely for convenience. |

|  |
| --- |
| `Line 7              void loop ()` |
| This is the specific way Arduino needs to start running the code that follows. |

|  |
| --- |
| `Line 9              if (digitalRead (A0) == LOW)` |
| This asks the microprocessor to watch for a digital low signal on Analog pin #0. This is opposed to an analogRead which would give us a numerical value instead. |

|  |
| --- |
| `Line 11             digitalWrite (13, HIGH);` |
| This makes Digital pin #13 go high. A voltage appears on that pin and, in turn, is used to light the onboard LED and signal the relay module to turn on. |

|  |
| --- |
| `Line 13             else` |
| This line is looking for anything other than a digital low signal on Analog pin #0. |

|  |
| --- |
| `Line 15             digitalWrite (13, LOW);` |
| If anything else than a digital low signal is detected on Analog pin #0, a low state is set on Digital pin #13. This takes voltage away from the onboard LED and extinguishes it, while also turning off the module relay. |

The rest of the symbols are required as part of the syntax for the software to run properly. This includes the semicolons (;) at the end of lines: 3, 4, 11, and 15.

Spaces are ignored, while the use of double forward slashes (//) makes the software ignore whatever comes after them on the same line. So, we can use the space afterward to make notes about the code. A good source to learn the syntax of Arduino sketches is the [Arduino website](https://www.arduino.cc/).

From here, we can get just a little more complex.

[![The final version of the Arduino sketch](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/108-pinball-ball-detector-1024x607.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/108-pinball-ball-detector.jpg)

The final version of the Arduino sketch

This final version, thought not technically the best way to implement this software, it is OK for beginners and hobbyists.

You can view or download the final Arduino sketch with [this link](https://pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/IrSensModFinalSketch.ino).

In this version we have added a short delay (measured in milliseconds) to the digitalWrite (line #19). This delay makes the output more stable by ensuring Digital pin #13 goes HIGH for a minimum amount of time, no matter how briefly the ball is detected by the IR module. This works well to make an LED momentarily flash in a topper or for the contacts of a relay to remain closed long enough to be registered by, say, the switch matrix of a pinball machine.

The value of the ‘dwell’ delay set in line #5 can be adjusted for your own use. For example, the value of 300 might be too long to ‘catch’ two pinballs coming down the same ramp closely together, but the same value may be too short for a specific LED lighting effect.

You can see that the majority of the work was understanding the operation of the three main components and how to link them together. Even for coding the sketch, the majority of the work was in the set up. Just one short section of the code – lines #16 through #19 – did the magic part.

We have described how to make this pinball ball detector using an Arduino Uno, but you can use [other microcontroller boards instead](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-alternative-microcontrollers/). Below you can see all three components working together on a cheap Arduino Nano clone mounted on a screw terminal breakout board, with all three power and status indicator LEDs lit as expected.

[![Tested and ready to install](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/109-pinball-ball-detector-1024x575.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/109-pinball-ball-detector.jpg)

Tested and ready to install

**Summary**

We set up an input on the Arduino. That input was provided by the IR input module. The Arduino saw that input and acted on it. The action was to provide a signal to the output relay module. What you use the relay to switch on and off is left to your creativity.

**Hints-n-Tips**

• One thing to remember is that third-party Arduino clone boards usually don’t have the latest firmware (bootloader) installed. So if you can’t ‘talk’ to your board with the Arduino IDE software, try selecting an older version of the board under Tools/Processor or on the top toolbar.

• Infra Red (IR) input modules with potentiometers for sensitivity adjustment are the most versatile.

• When used on the top the playfield, the better IR module to use will be the vertically-oriented variety, mounted above the point of detection.

• Know whether your input IR module produces a **HIGH** or **LOW** signal and adjust your code accordingly.

• Verify or set the jumper on your output relay module to the ‘H’ (**HIGH**) or ‘**L**‘ (**LOW**) position.

• Double-check all of your connections before first powering your creation.

• Ensure your creation is not electrically shorting against, or physically binding, anything in your pinball machine.

• Changing ambient lighting, in-game lighting or playfield flashers can sometimes give false signals which trigger the IR module. False triggering can usually be fixed by carefully adjusting the sensitivity potentiometer on the IR module. The vertically-oriented IR module has a built in baffle/beam separator making it physically more immune to the effects of ambient light.

• If your IR input module seems to start acting strangely during gameplay, check how its output/signal indicator LED is behaving. This may be an indication that ambient light is interfering with the sensor, in which case you may need to place a little heat shrink tubing around the bodies of the IR sensor pair. Be sure the lenses/tips aren’t obstructed though.

[![Heat shrink tubing around the IR transmitter and receiver, with un-shrunk tubing protecting the module too](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/256-pinball-ball-detector.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/pinball-ball-detector/256-pinball-ball-detector.jpg)

Heat shrink tubing around the IR transmitter and receiver, with un-shrunk tubing protecting the module too

---

While these two parts show you how to use an Arduino Uno to build and programme your ball detector and relay, as Todd say, you can use many other microcontroller in place of the Uno.

Todd has produced an additional article listing many alternatives to the Uno, highlighting four of them to detail their unique properties and providing example sketches.

[Click here to view his list of alternative microcontroller boards.](https://www.pinballnews.com/site/2024/02/02/pinball-ball-detector-alternative-microcontrollers/)
