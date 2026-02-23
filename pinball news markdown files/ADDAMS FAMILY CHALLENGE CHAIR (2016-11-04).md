---
title: ADDAMS FAMILY CHALLENGE CHAIR
date: 2016-11-04
url: https://www.pinballnews.com/site/2016/11/04/addams-family-challenge-chair
source: Pinball News
era: wordpress
---

**The story starts a few years back during a lull at work, while partaking in a favourite pastime; scouring Ebay looking for anything and everything – things I must have, things I don’t need and things I never even knew existed.**

I usually start in the pinball section of course, but then I have to scour arcade machines too. This day I came across a large wooden chair resembling something out of an American prison. Think Stephen King’s *The Green Mile*. The chair was non-working, only a few miles away and, most importantly, cheap.

The more I looked at the pictures, the more I knew I had to have this ex-amusement machine. I didn’t care that it was a non-working example. It was super cool in just being a chair and would look great in any gameroom environment.

Having travelled far and wide to buy pinballs, the proximity of a few miles just over the bridge was telling me to get in the car and check it out.

It was being sold by an amusement specialist who had an array of ‘bandits’, boxing machines and all sorts of other arcade goodies. Sitting in the corner, covered in dirt ‘n dust, sat ‘The Original Shocker’.

This particular example had served its time on location at Blackpool’s Pleasure Beach; well, that’s what its stickers said.

These were produced by a firm in the UK called Nova Productions. The company had gone bust, nobody fixed the circuit boards, and the story went that this chair donated its innards to help keep another game running. The chair had sacrificed itself for another. I had to have this chair.

The sellers were keen to let the Ebay auction run its course, and any cheeky offers had been quickly turned down. I went home and made by auction bid, crossed my fingers and hoped no one else wanted it.

Well, the arcade gods were on my side as not a single other bid was made, and we are talking a cheap opening price. When the auction ended the following week I won the chair, and then had to ‘fess-up at home to another crazy purchase.

The chair arrived and I placed it into deep storage at the back of my garage, under the usual knickknacks that live in everybody’s over-full garages. There had been no point turning it on as it was missing its motherboard. I thought I would do some more searching and see if I could find the missing parts, although if I was unsuccessful it still worked as a chair.

I shared my recent purchase with my friends at Northern Lights Pinball (NLP) to see if they could put out feelers to see if we could get the game back to life. I was even searching for non-working examples of the circuit boards as I have some very clever and resourceful friends.

Nothing seemed to be available. I even had a phone conversation with an operator who had three of these chairs – all in non-working condition. He didn’t have a good word to say about Nova Productions. He wished me well in my search but he wouldn’t sell me any of his non-working parts. This project could probably take some time.

At the time I also mentioned it to a programming friend a.k.a. Dr Pinball, who has had some success with his [DMD Extender](https://www.pinballnews.com/learn/dmdextender/index.html) kit. He thought that it was quite likely that we could [Raspberry Pi](https://www.raspberrypi.org/) some life into it, but he was too busy at the moment.

Fast forward about eighteen months to 2015. The chair is still sitting in the back of my garage under even more junk and I get a text from my pinball friend Chris ‘ Poibug’ Williams. “*Have you still got that electric chair?*“, he asked.

The NLP think-tank had been having a meeting and were looking for novel ways to play pinball. They had already come up with playing a Flintstones using your feet on a dance mat and putting a Fish Tales side-by-side with its electronic counterpart on Pinball Arcade, with the real-world pinball played via a Playstation joypad.

“*Eh? Yes Chris.*“, I replied. So with a month to go before the NLP held their annual show as part of the huge Play Expo event, four pinheads met in my garage to dig out the chair and come up with a cunning plan.

Our primary objective was to hook up the chair so that it could be used to control a real pinball machine. Which pinball? Well it was obvious and agreed unanimously that *The Addams Family* would be the perfect choice.

The secondary objective was that it would be interactive and, most importantly, FUN!

The first night was spent stripping the chair down and removing the parts to see what we had to work with and come up with a plan to move forward.

The team consisted of me (a.k.a. Mooseman) – an electrician and generally handy-with-a-tool kinda guy, Chris (a.k.a. Poibug) who is an aircraft technician with many years of pinball repairs and service under his belt, Paul Garner (a.k.a. Wizcat) who is a computer programmer, and David Robinson (a.k.a. Dr Pinball) – also a software wizard and DMD Extender designer. We would co-opt others to help as the project continued.

A little history about this kind of amusement is probably needed around now.

The idea of the original game was to sit in a very realistic-looking ‘Old Sparky’ type of electric chair. You put your coins into the machine and then hold on to the two protruding handles which, as the game progresses, will ‘shock’ you. The longer you hold, the more you are ‘shocked’, the louder it gets, the more lights come on, the meter rises ever higher and ultimately smoke is seen rising from your head.

It’s a very visual experience. Totally non-politically-correct, but a lot of fun. The punter isn’t really shocked though – it’s just an illusion of being shocked. The handles contain vibrating motors which oscillate at ever-increasing speeds.

Now, wouldn’t it be good if we could shock the person playing *The Addams Family*?

Having dismantled the two handles, David took them home to see if he could get them to vibrate and work out if switches could be added to control the flippers. In fact, we all went away with various tasks to find, build, or come-up with solutions to make the project work.

I stripped the chair down further and spent an age sanding it to remove its original ‘Shocker’ logo which was stained into the wood. That had to go and something better sourced.

My neighbour, Paul Glending, is a very talented graphic artist and so he was co-opted onto the team to graphically bling the project. He went away and designed the *Addams Family Shocker Challenge* decal, plotted and weeded it all, and fixed it in place in about a week.

[![The Addams Family Challenge artwork](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/11.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/11a.jpg)

The Addams Family Challenge artwork

Good news – both handle motors are in working condition and they vibrate. Bad news – we can only get them to operate at one speed. Good news – it’s the fastest, insane speed. There is also room in the handle to fit two small push button switches.

[![One of the two handles](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/12.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/12.jpg)

One of the two handles

It’s looking like objective one – getting the chair to control the pinball – can be achieved Objective two’s interactivity now needs looking at.

It was decided that, as we had no motherboard, a substitute surrogate mother needed to be found. We settled on the Arduino microcontroller would be a likely candidate, but a board would need to be designed to add all the inputs and outputs we would like to have working on the chair. It was also decided that the DMD technology could be used to activate certain things interactively with the gameplay.

A Raspberry Pi is used on the DMD Extender and this could recognise when certain screens were on the display. The RPi could then tell the Arduino to do something about it. We now had a way to make the chair truly interactive.

The chair is not an ideal height from which to play, so we looked into increasing its height. A skilled woodworker would be needed, and so Darren Ball (a.k.a. Replicas) built us a platform to sit the chair upon to give the player a better viewing angle.

[![The Addams Family Challenge Chair on its base](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/7.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/7a.jpg)

The Addams Family Challenge Chair on its base

The chair’s transformation was now picking up momentum with the four of us meeting after work about twice a week and staying into the wee hours rebuilding and rewiring its various components.

The smoke machine was missing but after searching on the ‘net a model train smoke generator was found to be an exact replacement. This, and a servo motor to control the smoke fluid’s, flow were purchased.

The ammeter didn’t really measure amps but gave the illusion through the use of a servo. Another servo was purchased.

[![The Addams Family Challenge ammeter](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/4.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/4a.jpg)

The Addams Family Challenge ammeter

The lights were changed for lower-power but much brighter LEDs. The sound was to feed through to the chair’s three speakers, so an amplifier had to be found and fitted. Further strobe-type lighting was installed under the chair and an extra vibro motor fitted under the seat.

This chair is going to ROCK!

The *Addams* pinball was fitted with the Raspberry Pi, and this communicates with the Arduino in the chair via a Cat 5 network cable. The sound is channelled down a separate audio cable from the pinball to the chair.

Having got the individual components to work, getting them to all work together was a further challenge that had us scratching our collective heads as the deadline for the NLP show got nearer and nearer.

A few loose wires and a credit dot on the display played some part in the problems, but eventually a working one-of-a-kind *Addams Family Shocker Challenge* debuted at the 2015 Northern Lights Pinball Show, part of the [Play Expo](https://www.pinballnews.com/shows/playexpo2015/index.html) show at EventCity in Manchester.

The chair and game combo was a huge hit, with queues of people waiting to have a go. Screams and giggles could be heard from afar as players were shocked mid-concentration as they were trying to keep the ball alive. As it was so popular, a fundraising bucket was set up and donations collected to supplement the total raised for the worthy charity, [Teenage Cancer Trust](https://www.teenagecancertrust.org/).

The chair lasted well into the first day of the show before losing its power supply. A spare was quickly found, fitted, and on with the fun.

On the Sunday, the second day of the show, one of the handles sadly stopped vibrating. As it was quite dark in the venue and there were lots of wires, it was decided to let the game continue to on to the end without a repair as it was still a great experience.

Fast forward another six months to 2016 and we decided to make some improvements to the chair.

The broken vibration motor was just a loose wire, but this must be eliminated and more smoke was needed, as the train unit wasn’t dramatic enough for us.

The Arduino motherboard was redesigned with Molex connectors incorporated, a new, bigger smoke machine was added along with extra strobe lighting to accentuate the smoke.

[![Inside the The Addams Family Challenge](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/1.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/1a.jpg)

Inside the The Addams Family Challenge

[![The main shaker motor](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/2.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/2a.jpg)

The main shaker motor

[![The new Molex connectors](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/3.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/3a.jpg)

The new Molex connectors

The chair is now up and running, and about to go to the NLP show for 2016.

[![Players at NLP 2016 show enjoying the chair](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/6.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/6a.jpg)

Players at NLP 2016 show enjoying the chair

[![Players at NLP 2016 show enjoying the chair](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/8.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/8a.jpg)

Players at NLP 2016 show enjoying the chair

[![Wednesday Addams gives the chair a try](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/9.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/9a.jpg)

Wednesday Addams gives the chair a try

Comments on the internet have been very positive, and people can’t wait to give it a go again.

[![Credits for the The Addams Family Challenge](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/5-1.jpg)](https://www.pinballnews.com/site/wp-content/uploads/learn/addams-family-challenge-chair/5a.jpg)

Credits for the The Addams Family Challenge
