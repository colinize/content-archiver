---
title: P3 ADDS INTERNET CONNECTIVITY
date: 2020-05-23
url: https://www.pinballnews.com/site/2020/05/23/p3-adds-internet-connectivity
source: Pinball News
era: wordpress
---

[Multimorphic](https://www.multimorphic.com/) has added internet capability to its *[Cosmic Cart Racing](https://www.pinballnews.com/site/2018/03/22/cosmic-cart-racing/)* game, allowing owners of the P3 pinball platform with the *Cosmic Cart Racing* game kit to compete against other players anywhere in the world.

Closed-network gameplay on the P3 had been demonstrated at pinball shows for several years, but using the internet to connect P3 machines has been a more recent development – one which added a greater challenge.

[![Multimorphic had a large display featuring four linked P3 machines playing Cosmic Cart Racing](https://www.pinballnews.com/site/wp-content/uploads/shows/tpf-2019/219-texas-pinball-festival-2019-1024x683.jpg)](https://www.pinballnews.com/site/wp-content/uploads/shows/tpf-2019/219-texas-pinball-festival-2019.jpg)

Multimorphic demonstrating four linked P3 machines at the Texas Pinball Festival 2019

Now Multimorphic has released a public beta version of the *Cosmic Cart Racing* software (V2.1.0.29) which gives to option to play against internet opponents rather than the game’s artificial-intelligence bots. Multimorphic also plan to roll out internet games to their *Heads Up!* pitch-and-bat title once that game is officially released.

To find out more about how the new internet connectivity works, Pinball News spoke to Multimorphic’s head, Gerry Stellenberg.

[![Gerry Stellenberg](https://www.pinballnews.com/site/wp-content/uploads/shows/tpf-2019/142-texas-pinball-festival-2019-1024x684.jpg)](https://www.pinballnews.com/site/wp-content/uploads/shows/tpf-2019/142-texas-pinball-festival-2019.jpg)

Gerry Stellenberg

**We began by asking him how long the team at Multimorphic had been working on adding internet-connected gameplay to the P3?**

He replied, “*I’ve spent most of my professional career in the data networking industry; so it shouldn’t be a surprise to hear we’ve planned on having network connectivity since the very beginning.  We designed the P3 development framework with networking in mind, and every single P3 we’ve ever shipped has a Wi-Fi adapter.  We first showed networked P3s running HeadsUp! at TPF 2017 and then 4-machine Cosmic Cart Racing in 2019, but those were both connecting over local private networks.  We’ve been working on the internet component for the last year or so.*“

**So, **P3** machines were already internet-ready, and no changes need to be made to get online?**

**Gerry:** “*All *P3*s are ready to go.  Customers that haven’t already done so just need to enter their Wi-Fi credentials into the Wi-Fi setup section of the System Manager application.*“

[![The announcement of the new feature](https://www.pinballnews.com/site/wp-content/uploads/news/p3-adds-internet-connectivity/01-p3-adds-internet-connectivity-1024x680.jpg)](https://www.pinballnews.com/site/wp-content/uploads/news/p3-adds-internet-connectivity/01-p3-adds-internet-connectivity.jpg)

The announcement of the new feature

**Presumably a multi-hop internet connection with variable delays and bandwidth has the potential to be more problematic than a local network.  What issues do you face connecting over the internet that you wouldn’t have on a closed network?**
**Gerry:** “*From a low level / technical perspective, internet connectivity is incredibly complex.  Understanding the details of TCP/UDP protocols, transactions over public network transports, interactions with firewalls and routers, error correction/recovery, variable latencies, node discovery, etc is not for the faint of heart.  That said, networking features are super common in the computing and gaming industries, and most people implementing network-enabled apps don’t need to know any of the low-level details.  We’ve put a lot of work into our P3 framework code to handle the network intricacies, but game developers shouldn’t need to worry about much more than what data their game needs to synchronize across machines and how often to send it.*“

**Do you exchange much data during a typical multi-player game of *Cosmic Cart Racing*?**
**Gerry:** “*If you’re concerned that playing a networked *P3* game might impact somebody in another room streaming a TV show, in most cases it won’t.  I don’t know what a future game’s needs will be, but we spend a lot of time optimizing bandwidth requirements for networked games.  Generally speaking, if a game needs to synchronize a lot of data, it’s doomed to fail.*“

**Is the ‘ping time’ or a slow connection an issue?**
**Gerry:** “*Not when they’re small.* 🙂*Latency is no big deal for things like online leaderboards, software updates and such, but if you’re playing Cosmic Cart Racing across two machines on the internet, things work best when data gets to each machine relatively quickly.*“

**Does it make any difference if you’re using a **using a wired or wireless connection**?**
**Gerry:** “*Without going too deep into discussions about bandwidth and latency, the answer for networked **P3** games is ‘No’.  Wired networks are generally known to have more bandwidth and less latency than wireless networks (exceptions apply), but a well-designed network game should work fine with either.*“

**Do players need a connection with a static IP address?**
**Gerry:** “*No, our networking code handles all discovery and translations.  You can even play through a mobile hotspot if you want, you know, for those times when you take your **P3** camping.*“

**When you initiate a multi-player internet game of *Cosmic Cart Racing*, who does the hosting of the game?  Is it hosted centrally on a Multimorphic server, or does one of the P3s act as the host?**
**Gerry:** “*We’ve built the system to allow for both.*Cosmic Cart Racing *designates one of the **P3**s to host the game.  Other games we have in the queue might use a central host.  It depends on the needs of the game and the environment it wants to maintain.*“

**So, what is the process for both starting a new – and joining an existing – multi-player ***Cosmic Cart Racing*** game?**
**Gerry:** “*Upon choosing to play an ‘Internet Game’, you’ll see a list of available sessions that other **P3*s* are hosting.  If you see one you like (the host can pick certain details, like which racetrack to use and how many laps to race), you can join that session.  Otherwise, you can create and host your own session and wait for players to join.  Oh, and the internet features are tied into the **P3**‘s profile system and ask you to select a player profile before you can host or join again.  It’s much more fun to play against ‘Matt’ than it is to play against ‘**P3** #328546′.*“

**If someone is hosting a multi-player game and twenty people all try to join, what happens?**
**Gerry:** “*Since* Cosmic Cart Racing *allows up to four players per race, the first three of those twenty will join the game, and seventeen will be rejected and have to look for another session to join.*“

**Is the gameplay for a multi-player connected *****Cosmic Cart Racing***** game different to a regular game against virtual opponents?**
**Gerry:** “*No, races and racers follow the same rules regardless of who or what is acting as a player.  The only difference is whether the racer progresses and collects/uses powerups by hitting pinball shots (human) or by following an algorithm (AI).*“

**Given the different set-ups of every pinball machine, is it possible to compete fairly against another opponent on a different ****P3****?**
**Gerry:** “*I suppose it depends on your definition of ‘fairly’.  Do two tennis players compete fairly if one’s racket is lighter or strung more tightly than another’s?*
 *We have a lot of cool features in the P3, many of which are patented, to quantify the setup and behaviour of the machine and also to track how the player is completing shots.  The *P3* knows the angle of the playfield, how strong your flippers are, how fast balls move on the playfield, and a whole lot more.  In fact, if you’ve ever played* Lexy Lightspeed – Escape From Earth *with the glass off, you’ve probably had it call you a cheater!*

*How this data is used might vary.  Some games might force machines to be set up similarly before they’ll allow a connection.  Other games might tell the players how differently their machines are set up and let them decide to play against each other or not.  Some games might even actively handicap one machine to make it match the other machine’s performance, though there are a lot of perception and messaging ramifications to work through in that case.*

*For tournaments, some directors might configure games to do automatic handicapping, whereas others might just have the machines tell the tournament director how differently the machines were behaving (or that one person cheated on x% of his shots) and let the TD decide what to do.*

*So yes, I believe even high-level tournaments could be run fairly.  That said, I’ve always loved playing online spades and trying to beat people who I knew were cheating.  So, I’d have fun either way.* 🙂*I personally don’t understand cheater mentalities; why would somebody feel good about winning when using their hand to activate switches?  Regardless, the *P3* can identify the cheater.  So far we’ve held back on our public shaming Easter eggs.*“

**Are the results of internet-connected games recorded centrally?**
**Gerry:** “*Not currently, and they won’t be without us making it clear and allowing you to opt in or out.  We’re pretty big on privacy, and your data is none of our business unless we’re specifically working together on something.*“

**So there aren’t any overall ranking systems or central records available yet?**
**Gerry:** “*Our focus is currently on fun, value-adding gameplay features rather than statistics, but we have a long list of planned networking features that do include player and game data.*“

**This new connectivity is being released in a public beta version of software.  What feedback about the beta code do you hope to get from players and machine owners?**

**Gerry:** “*We’re calling this a beta only because we might run into some weird problems when we encounter topology and timing scenarios we didn’t expect.  We’re not harvesting user data.  For game-specific performance data, we get everything we need through ‘internal’ testing, which currently includes endpoints on multiple continents.*“

**When this is out of public beta and made into a full official release, will it continue be a free update for ****P3**** owners?**
**Gerry:** “*Yes,* Cosmic Cart Racing’s *internet head-to-head gameplay will be free to all* Cosmic Cart Racing *game kit owners.  We’re not looking to nickel and dime our loyal customers.  We’re more interested in giving more people more reasons to buy into the *P3* ecosystem and expand their game libraries.*“**

**Once you are happy with the new feature, are you planning to retrofit internet access and gameplay into any other Multimorphic games?**

**Gerry:** “*It’s something we’ve discussed.  If we do it, we’ll do it in very specific ways.  We’re not interested in changing the entire gaming experience or hacking something in just to tick off a ‘network-enabled’ box.  We’re more interested in designing games or specific features in games to work well in networked configurations.  That said, we’ll also continue creating traditional-style games, like Heist, our newest P3 game kit, and making sure there’s a lot of content on the P3 for everybody to enjoy.*“

To showcase the new internet connectivity, Multimorphic is hosting a WAN party for Cosmic Cart Racing owners. The party takes place later today (Saturday 23rd May, 2020) at 4pm US Central Time (10pm GMT).

[![The WAN party to launch the new internet connectivity feature](https://www.pinballnews.com/site/wp-content/uploads/news/p3-adds-internet-connectivity/02-p3-adds-internet-connectivity-1024x680.jpg)](https://www.pinballnews.com/site/wp-content/uploads/news/p3-adds-internet-connectivity/02-p3-adds-internet-connectivity.jpg)

The WAN party to launch the new internet connectivity feature

To join the party, make you have the latest version of software installed and start an internet game during the hour from 4pm to 5pm Central Time.
