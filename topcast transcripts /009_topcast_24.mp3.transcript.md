# Transcript: 009_topcast_24.mp3

**Transcribed**: 2026-01-13 19:32  
**Model**: whisper-base  
**Duration**: 1:02:53

---

[00:00] Hi there pinball fans, it's your fever clown crusty, and you're listening to Norman Shaggy on the Topcast.

[00:06] The greatest pinball show ever made.

[00:10] Hey, can I get my money now? I'm such a whore.

[00:15] Celebrity boys impersonated, you're listening to Topcast.

[00:19] This old pinball's online radio. For more information, visit them anytime.

[00:24] www.marvin3m.com.

[00:27] Last Topcast.

[00:35] Today on Topcast, we have an interview with a Williams programmer and system architect

[00:40] that worked there starting in 1993 up to 1999.

[00:44] He worked on such games as Corvette, Johnny Mnemonic, and NBA Fastbreak in addition to developing

[00:52] all the operating system level code for pinball 2000.

[00:58] So we're going to be talking to him right now and hookah says perspective on the software development

[01:03] at Williams Valley at the time in the 1990s.

[01:06] Special guest, special guest, special guest, special guest, special guest, special guest,

[01:12] So I'd like to welcome Tom Uban, who was the lead programmer for Corvette, Johnny Mnemonic,

[01:20] and NBA Fastbreak in addition to doing all the pinball 2000 operating system level code for

[01:28] revenge from Mars and Star Wars Episode 1 in addition to any of the games following that.

[01:33] And so let's get Tom on the line. Give him a call right now and see how he's doing.

[01:38] Let's get Tom on the line.

[01:41] See what's up with Tom.

[01:48] Hello. Tom, you were, you started working at Williams in 1993, but part of that,

[01:57] you kind of had a long history of computer software engineering.

[02:02] And you also went to school at Purdue where you got your doubly and at the same time you knew Ted Estes too, right?

[02:10] Ted worked for me at Purdue. I worked for the engineering computer department,

[02:16] computer network, ECN, and maintained terminals and printers and stuff.

[02:22] And Ted was going to school there and he worked part-time for me cleaning printers and things like that.

[02:27] So was he a good worker?

[02:29] Ted? Yeah, he was fine.

[02:31] I just had to ask.

[02:33] So you graduated in 85 with your doubly?

[02:37] That's correct.

[02:39] And then where did you go to work?

[02:41] Then I went down to Champaign or Van and worked for Google computers writing unix operating systems software.

[02:49] How long did that last?

[02:53] Almost two years, something like that about two years.

[02:57] And then where did you head to?

[02:59] Then I went out and lived out east for five or six years working initially for both Veronica Newman.

[03:06] I remember them, they were the ones that brought back the sound on the erase of Nixon tapes.

[03:14] Oh, okay. Were you involved with that project?

[03:16] No, no, I worked for advanced computer, now advanced computer incorporated, which was a subsidiary of them.

[03:25] Did you get any privy information on the Nixon thing at all?

[03:29] No, I didn't really know anything about that.

[03:31] It's just one of the things that they were well known for.

[03:33] They did a lot of government contract work.

[03:36] I worked on massively parallel computer that was built by the company and worked on a software for that, operating systems software for that.

[03:47] So I was primarily an operating system guy.

[03:50] So then you came back to the Midwest for work for Williams about after that?

[03:54] That's right, Ted gave me a call one day.

[03:56] We kept in touch. Ted lived in Champagne for a while also.

[04:03] And so we kept in touch over the years and Ted gave me a call one day looking for people to work at Williams.

[04:08] And I said, sure.

[04:10] So I had in 1990 I had switched to doing consulting on my own.

[04:16] And so I was out there for three years doing consulting when Ted gave me the call and we moved back at that point.

[04:23] So in 93 you started at Williams.

[04:26] I mean what was your position in your title or what were you doing there?

[04:31] Basically everyone was software engineer.

[04:33] They weren't really big on official titles.

[04:36] So we could pretty much make up whatever title we wanted because it was the same job either way.

[04:41] But basically it was software programmer and I was working on game software.

[04:46] Everyone always started out in order to get initiated into the whole thing by writing some kind of test code for one of the devices.

[04:56] And the first thing I wrote program for was the pencil slicer or carrot slicer.

[05:03] What everyone would call it, finger chopper thing in Papa.

[05:07] If you recall there was this big metal plate with holes in it to spun around and this was all right all through you.

[05:13] Yeah, I know you talking about the test software that resided in the game as well as what was used in the quality test lab to make sure the device wouldn't fail over time.

[05:26] That was the first thing I wrote and then I started working on games with George Gomez on Corvette was the first game.

[05:36] Yeah, I noticed you did software for three games. You did Corvette in 94.

[05:41] Johnny Minnoneck in 95. I can never say that name right.

[05:47] Yeah, and NBA Fastbreaking 97 and those are all Gomez games right?

[05:52] Right, I worked primarily on Gomez games.

[05:54] I also worked on a game that was never released. It was armed and dangerous which was a linked non-involved like game.

[06:04] And it went through three or four iterations.

[06:07] I think some of the whitewoods are still out there somewhere.

[06:12] So was a WPC 95 architecture type thing?

[06:17] Yeah, and the play field design changed drastically over three iterations.

[06:24] I think it was initially it was kind of pinball like and had these continuous ball feeds of pinball size balls.

[06:33] On left and right, both left and right of the flipper.

[06:38] And then it switched to this rapid fire type situation.

[06:46] I think there were five eighths and nylon balls or something like that.

[06:51] And there were gates that you were shooting at in these tanks that were aiming back.

[06:55] It was always tank themed.

[06:58] Part of what I did when I was writing that software was write some linking code that let two games link up.

[07:06] And that's the code that I used in NBA in order to do the linked NBA game which some people may know about.

[07:15] Right, we'll get to that just a second.

[07:17] Let's back up to the Corvette thing and also your some more early experiences at Williams.

[07:25] So you know, I Williams you were writing everything in 68.09 assembler right?

[07:30] That's right. Everything was assembly and WPC.

[07:33] Right. So I mean, how did that compare to your prior experiences with software?

[07:39] I'd always been a low level software programmer.

[07:42] So, you know, during up ranks and stuff, I've done quite a bit of assembly here and there.

[07:48] I went when it was necessary. Not my favorite thing, but you know, part of the deal.

[07:55] So it wasn't hard for me and after you do it for a little bit, you get pretty used to it.

[08:02] And the whole system was pretty well designed.

[08:05] It was running Larry de Mars Apple system.

[08:10] Yeah, what the advanced pinball programming language environment or something like that?

[08:14] Logic executive, I think is what it was.

[08:16] Executive executive. So yeah, it was a great environment.

[08:20] Easy to program in. A lot of fun.

[08:23] And I mean, was this challenging compared to the other stuff you did?

[08:28] It sounded like this was almost a walk in the park.

[08:31] Well, it's completely different and it used to be a different part of my brain.

[08:37] Because they're in pinball and game software, you get to do a lot of creative work.

[08:44] And so that was fun to be able to exercise the creativity that I have.

[08:49] And then see people enjoy it or not.

[08:52] And that was a lot of fun to do that.

[08:55] Not to mention that you know, you pack and lock this stuff into a game in a very short time.

[09:01] So it was definitely, definitely a lot of work to be able to do that in time that we had to do it in.

[09:08] Did you ever have to do any display graphic work?

[09:12] Yeah, on all the WPC games, the first one, Corvette, Bill Crop,

[09:18] and I programmed together to build it the display work.

[09:23] And I did the game and stuff.

[09:26] And then on the follow-up games, I did the other two games.

[09:31] I did all the work myself.

[09:33] And so that entailed both graphics and game software.

[09:37] So you did all the artwork for...

[09:41] We don't do the artwork.

[09:44] We do the animation of...

[09:48] So they provide the frames?

[09:50] Right, there's dot guys like Scott Swamy-Anne and such,

[09:53] which created the dots, the actual dot themselves, Adam Ryan.

[09:58] And then we would take those and program them to flip through in the right sequence

[10:04] or move little spiked guys around on it or whatever it is.

[10:08] It was always different.

[10:10] And often while there's also wipes, which are where it goes from one frame to another,

[10:16] which are generally pretty much just some kind of programmatic effect.

[10:22] Was there a set of standard, like animation tools and wipes in that in Larry's Apple system?

[10:29] Or is this stuff you all had to write?

[10:32] There were a set of standard wipes and things like that that people would use,

[10:37] but everyone always wanted to make their game a little bit different and more fresh.

[10:42] So it was pretty standard to come up with another wipe or two for each game that you did just to give it a new feel.

[10:48] But you'd certainly utilize the ones that existed already as well.

[10:52] And after you've used it in a game, then typically everyone would feel like they could use it in another game later on too.

[11:00] So you mean once you wrote one, you'd give it to Larry and then he kind of puts it into his Apple system?

[11:06] Well, we just pooled all the software.

[11:08] Everyone had access to all the other games and such, so you could use whatever was there.

[11:14] You might ask them if they felt weird about it or not.

[11:17] But generally everyone would share.

[11:19] Certainly after it was out in the game already.

[11:21] Now, on Corvette, were there any particular challenges that that game gave you on a subject?

[11:29] You don't want to suffer or hardwood level or whatever?

[11:33] The biggest challenge in that game was the engine.

[11:35] George wanted the engine to shake.

[11:38] And so the normal thing would have been, of course, to just take a coil and flop it up and down or take a motor and make it rock back and forth.

[11:48] But for some reason I felt compelled not to do it that way and talked them into letting people build this piece of electronics

[11:57] that works kind of like a speaker coil works where you have magnets driven in an analog fashion rather than digitally on or off.

[12:07] And it has feedback and so it kind of rocked the engine that way.

[12:12] And getting that sort to work right in a production environment, cheap production environment like a pinball game turned out to be more work than I expected not to mention doing that and programmed the game my first game.

[12:25] So that was pretty thrilling and cupped me up a lot of nights and when it came down to the wire it was very close to being thrown out of the game.

[12:34] Oh really? You mean because there wasn't enough time to perfect it or something?

[12:38] Yeah, it was close to the wire if not being able to make it.

[12:42] It is a cool effect though.

[12:44] The way the engine shakes is, you know, when you open the hood of the car and you hit the gas, you don't really see the engine move a lot, especially on this.

[12:54] It is certainly not a new car but an old car they kind of have a rock tool and it does kind of mimic that.

[13:01] Yeah, of course, you know, it wasn't good enough just as an effect for George.

[13:05] He wanted to be able to play the ball with it too.

[13:08] So we had the ball in there and the shaking actually made the ball stay in the engine and move in there so you could see it.

[13:16] Which is all very cool and that's why George is such a good designer because he comes up with these great ideas.

[13:21] It's just a question of being able to implement them.

[13:24] So who's the whole idea to rock the engine was that starting out as George's idea and then it kind of took it over and...

[13:32] Well, it was all certainly George's idea.

[13:35] We had Tom Capera, the mechanical engineer and I had to come up with a way to make it work.

[13:41] So we worked on that for quite a while and I talked to him into the electronic driver scheme that we used.

[13:49] Was it cheaper to do it the way you did it compared to...

[13:52] Yeah, probably not but it was kind of cool to do it.

[13:56] So looking back on it there, you sorry you did that way, the big picture?

[14:00] Not that it actually all worked and everything I'm not.

[14:03] It's a time I was pretty sorry I haven't gotten on that road but...

[14:06] Right, because you probably just going to have two coils just to kind of throw it either way.

[14:12] And then it would have been kind of like the path of whatever out of Indiana Jones.

[14:19] Flop, flop, flop, wouldn't have been any control really.

[14:24] Even if you had the engine mounted on some sort of like rubber, you know, grommets or something like that,

[14:30] it would still be kind of floppy.

[14:32] I'm thinking so but it's hard to tell.

[14:35] You might have been able to put springs in there or something and gotten a similar effect but I'm not sure.

[14:39] Right, you know really now it's hard to guess.

[14:42] What about the two cars on the racetrack?

[14:46] How, you know, was that... I assume that was George's idea too, right?

[14:50] Yeah, well, you know we actually had a...

[14:53] The three of us, Tom Kepera, George and I and Bill was involved too.

[14:59] Probably the sound guy to some extent and the artist.

[15:03] We all had a pretty good group that just sat down and figured out what to put in the game.

[15:08] George usually had these, you know, these ideas pretty clear but you know we brainstormed.

[15:13] So it's hard for me to say that it was... everything was definitely all George and...

[15:16] But I think that, you know, it was mostly George and we all had ideas that we kind of threw in there

[15:21] and said, hey, would it be cool to have this or that, you know.

[15:24] And it's a car racing theme and all that.

[15:27] Kepera may have come up with a track. I'm not sure.

[15:30] He certainly designed it. That was a masterpiece of mechanical design.

[15:35] Yeah, it's kind of... The chief too is just big injection molded thing.

[15:39] Never had to fix one of the racetracks before.

[15:42] I think they pretty much work.

[15:44] Yeah, pretty much. Yeah. Your motor every once in a while, you got to fix that.

[15:49] But that's actually pretty robust too.

[15:51] Yeah, when it's working, it's pretty robust, I think.

[15:53] Yeah, the little rubber spark plug leads on it tend to break off.

[15:58] Right, right, but that's not really anybody's fault, you know what I mean?

[16:02] Yeah, it's just where. Yeah, it's just kind of how it is.

[16:05] Right, so was there anything in that game?

[16:07] I mean, I know there were supposed to be drop targets in the game and that kind of mixed out somehow, right?

[16:13] Well, you know, that's the old running gag, right?

[16:16] The designer would always put drop target somewhere so that when management came by and said,

[16:21] this was too expensive. We got to take something out, you'd have something to take out.

[16:25] That's what happened. Really?

[16:27] Yeah, actually my game here at home has the drop targets in it, so.

[16:31] Yeah, I retrofitted my game with the, my quarterback with the drop targets too.

[16:36] It wasn't that tough to do, really.

[16:38] Yeah, it's, you know, the programming is still there, it's just a matter of wiring it up and sticking it up.

[16:43] I'm not convinced it makes a big difference in the game. It's kind of interesting, but.

[16:46] Right, yeah, it's not, it's not a huge deal.

[16:49] Yeah, you know, but it is kind of cool to have them.

[16:52] I mean, so that was the running gag.

[16:55] Everybody would put drop targets in the game so there was something to take out that, you know,

[16:59] could be taken out without, you know, weepy eyes, huh?

[17:03] Yeah, pretty much.

[17:05] They do that on every game management come in and go, that's too expensive.

[17:08] Oh, yeah, that was difficult.

[17:10] Really? It wasn't always drop targets, but it was always something of that nature.

[17:13] Right, right. Well, was there anything else in the game that got, you know, nixed out that, you know, you were sorry to see go?

[17:19] Corvette, I don't recall anything else that got thrown out.

[17:23] George would be the person to ask that question.

[17:25] What about some of your memories on that?

[17:27] When you, when you were doing that, you know, you, you get to put the prototype,

[17:33] 1996 Corvette up in the, in the translator, whatever.

[17:37] I mean, did you guys have any interesting experiences working with GM or anything in that respect?

[17:42] I think it was pretty smooth.

[17:44] There was actually an earlier version of the, of the back glass, which had had some other cars in it that,

[17:52] that GM nixed couldn't be on them because it was, you know, you can't have that in a GM licensed thing.

[17:59] So, there is a, there were some trans lights made, the prototype trans lights made with the alternate artwork.

[18:09] And are you saying that there were nine GM cars?

[18:12] Yeah, I think there was some other car in there like a Ford Cobra or something like that or anything like that.

[18:17] Right, right.

[18:19] So then when you get done with Corvette, you went to Johnny.

[18:23] Another, another Gomez game.

[18:25] How did, you know, any interesting experiences with that, you know, especially that glove thing.

[18:29] I mean, who came up with that?

[18:31] Man.

[18:32] Yeah.

[18:33] Yeah, it'd be cool if the ball, if the glove would catch the ball.

[18:38] Great idea.

[18:39] Brilliant.

[18:40] So, yeah, that I think that was another George idea, of course.

[18:44] As I recall, we're all really excited about the theme and, you know, a counter-reason and movie.

[18:49] What could be wrong with that after all his success?

[18:53] We love the story because we'd all read the book or the short story.

[18:59] And George was on a plane coming back from some show or something with Neil and Neil's all hot to do that license.

[19:06] So George says, yeah, I'll take the license.

[19:09] We're talking about Neil and the cast for all that.

[19:12] I believe so.

[19:13] I think that's how it goes.

[19:14] Okay.

[19:15] And then we do the license and the movie comes out and it bombs.

[19:21] So we're pretty bummed about that even though I think the game turned out pretty good.

[19:25] Yeah, the movie was odd, I would say.

[19:28] It was very, very strange.

[19:30] Strange game?

[19:31] Oh, no, the movie was.

[19:33] Yeah, the movie was a little bit.

[19:35] Yeah, the movie was really odd.

[19:36] A little bit odd.

[19:37] Yeah, really odd.

[19:38] The game, I used to own one.

[19:41] I don't own it anymore.

[19:44] I never really had a problem with the glove.

[19:47] I think when I got it, a couple of the windows were bad and I replaced the windows and pretty much the glove worked.

[19:53] I think if you keep the threaded rods lubricated, you're pretty good.

[19:58] Right.

[19:59] And the matrix where you kind of got to drop the ball into that, you know, kind of like that tick-tick-toe board type thing.

[20:07] And then how it spits the balls out of that, that was all kind of neat.

[20:11] Yeah, it does.

[20:12] It does compare his idea to do the ball thing like that.

[20:15] Right.

[20:16] But the one thing that you always notice in that game is the lane change.

[20:20] And like, you know, you hit the flipper buttons, change the lane change and it's like,

[20:24] God, you can almost count the seconds before you see the light changes.

[20:27] Is that, you know, the bog or whatever?

[20:31] Yeah, that was the bog.

[20:32] I didn't have time to fix that before it went out.

[20:35] Is that something that was fixable though?

[20:37] It probably was fixable.

[20:39] I just didn't, you know, there was so little time to do that game and I was doing it all myself.

[20:43] And there were other things that seemed more important at the time, but in retrospect,

[20:48] that was probably something that should have been higher priority.

[20:51] Right.

[20:52] So I was the only one that noticed that, huh?

[20:54] No, you know, you're not the only one.

[20:56] I think Steve Richie probably complained about that as much as anybody.

[20:59] Okay.

[21:00] And was there anything else in that game that got left out or whatever?

[21:04] What else was...

[21:06] Not that I remember, but there probably was.

[21:09] I mean, was that game, you know, when it was all said and done, were you happy with that game when it was done?

[21:14] I was happy to be done with it.

[21:17] So that game, what didn't exactly, wasn't the thrill to work on, huh?

[21:22] Yeah, actually, it wasn't bad.

[21:24] I've enjoyed all the games I worked on there.

[21:26] It was, it was certainly the most, I put more work in that game than a lot of the others.

[21:31] Not, you know, just straight time because, you know, it just took a lot of work to get the game to be finished in the time that we're doing it.

[21:42] It was a show game, I think.

[21:44] And...

[21:46] So you mean you had to work in it?

[21:48] Some of those games during what we called a game hell, we'd be working like six or seven days a week.

[21:57] You'd get home at like two or three in the morning, wake up at seven and go back to work.

[22:02] Right, you know, we'd put in 110, 120 hours a week.

[22:07] Were you okay with that much crunch?

[22:11] Well, yeah, there wasn't much choice.

[22:13] Well, I mean, to be able to do your other jobs, I mean, you know, you certainly were...

[22:17] God, man, you were robust enough, you could probably work anywhere, you know?

[22:21] Yeah, that's probably true.

[22:23] But it really was a thrilling experience to work with all these creative people.

[22:27] You know, everyone was putting in time that was pretty serious and doing their bit.

[22:35] But it was, you know, it was like the steamroll that you couldn't stop.

[22:41] Just the excitement of doing it and getting it done and having it finished.

[22:45] It was great time.

[22:47] Did you ever, you know, when you're programming in a summer, I mean, at the end of the day,

[22:52] you know, everything you had to fit into what a 4-megapump.

[22:56] So you got...

[22:57] Yeah, unless you were a couple games head 8 megs, but...

[22:59] Right.

[23:00] All our Rs head for.

[23:01] I mean, was it ever an issue where there just wasn't enough space?

[23:05] Oh, yeah, there was always trade-offs.

[23:07] You'd either throw out some pictures or maybe some sounds or...

[23:11] I guess the sound was in different shape.

[23:13] Let's see, you throw out some pictures possibly or throw out some chunk of code that, you know, you didn't really need.

[23:19] One of the wipes or something or some of the wipes you weren't using that were some of the standard system.

[23:24] You could take some of that stuff out or move stuff around or rewrite some code some of the way or...

[23:30] Yeah, certainly.

[23:32] Okay, and it was...

[23:33] I mean, when you were doing that stuff, I mean, you know, was it ever a point where you just didn't have enough space where you said,

[23:41] man, I just...

[23:42] I really need the next size up e-prom or whatever.

[23:45] Well, I never got to the point where I had to force that as an issue.

[23:51] I just worked around it and made my code fit.

[23:54] Right.

[23:55] Right.

[23:56] There were some other constraints that were more system design oriented like...

[24:03] And now I was part of the problem with the...

[24:06] The bog was that there was only a certain amount of space that was available for the low-level interrupt handling routines and stuff like that.

[24:14] So that was usually what the ran into as a real problem was making all that fit in that a lot of space.

[24:21] Now, the 60809, though, can really only access what?

[24:27] 64K bytes of information.

[24:31] So to get it into a 4-megaprom, which is 512K bytes, you got to page it, right?

[24:39] All banks, which, yeah.

[24:40] And it was that like a...

[24:42] It was that in just a simple thing to do, part of the Apple code or something you really had to manage.

[24:48] Actually, the Apple code made it pretty painless.

[24:51] There were regions of space and you had to keep certain things in the same regions to make it work right.

[24:59] But as far as calling it, calling out of one space into another space, it was all transparent pretty much by based on macros that were written.

[25:08] So it really wasn't too bad.

[25:11] And Larry had that all laid out ahead of time, huh?

[25:14] Yeah, they had that figured out for us.

[25:17] Right.

[25:18] So it really...

[25:19] It sounds like it wasn't too bad to do all that at the assembly language then in that large of a space.

[25:25] No, not too bad at all.

[25:27] Okay.

[25:28] All right, so then you would...

[25:30] And another thing, you said you...

[25:33] All three of these games were Gomez games.

[25:35] And actually your fourth game, Revenge from Mars was a Gomez game too.

[25:40] I mean, was that...

[25:42] I was having a game code on that. I was just a system guy on that.

[25:45] Okay.

[25:46] But I mean, was this a conscious effort on your part to stay with George?

[25:50] Or was that just how it worked out?

[25:53] Both George and I started roughly at the same time and they kind of paired us together as a new team.

[26:00] And we worked together pretty well, so we just stuck it that way and that's how it worked out.

[26:09] Okay.

[26:10] So it was when George was doing Monster Bash, which was his last WPC game, I was starting to work on the new system and stuff.

[26:21] So that's when Lyman took over and did that with him.

[26:26] Okay.

[26:27] Now, NBA Fast Break, tell me about that game.

[26:30] Fast Break was a fun game.

[26:33] We did some new stuff in that that people...

[26:36] Some people like, some people didn't like, the whole scoring thing, which I think was great personally.

[26:44] Some people didn't like because it was, you know, not pinball.

[26:48] Yeah, it's like, it didn't give you a pinball score, it gave you a basketball score.

[26:52] Exactly.

[26:53] But as a result, if you've ever played with another person, like, you know, in a two-player game or four-player game, whatever it is,

[27:01] you can really, with the low score, you're like, man, all I gotta do is get, you know, one more basket or two more baskets and I'll be beaten to the sky.

[27:09] You knew exactly where you had to go to win.

[27:12] And I think that that, you know, made a big difference and made it a lot of fun.

[27:16] And I've seen a lot of people enjoy that.

[27:19] Well, what about, I noticed in the last Rob revision for NBA Fast Break, there's an auction where you can have both a traditional pinball score on and the basketball score.

[27:30] And that's when I owned my NBA Fast Break. That's always how I had my setup.

[27:34] You're right.

[27:35] Yeah, I also did what, I also did what the combo because it seemed like it was the best of both worlds.

[27:39] You know, you had, you know, you had this relative pinball score and you had the basketball score.

[27:46] Yeah, I don't recall who said to do that or if we just decided it was a good thing to do, but I never run mine that way actually,

[27:54] but we put it in there just to try and, you know, satisfy the rest of the world.

[27:58] Right, just to balance out everything or whatever.

[28:01] Yeah.

[28:02] Okay, now whose idea was it to put the whole length thing in?

[28:06] The which length?

[28:08] The length where you could have two NBA...

[28:10] How the length thing?

[28:13] You know, recall came up with that idea.

[28:16] But you implemented it, right?

[28:18] Yeah, I implemented it and my name's on the patent, so it was me, I don't remember.

[28:22] Now how come that never made it into any other games?

[28:25] You know, someone else, Stern, I think, has some linked stuff now, although it's not used for a gameplay, like it just used for their...

[28:33] For the turn of its system.

[28:35] Right.

[28:36] But I mean, why did that, you know, that could have been, you know, interesting in some other games too.

[28:40] Gee, you think that might have been a good idea?

[28:42] You know, it...

[28:44] We barely got it through marketing said that it would be a good thing at the show.

[28:49] And we ran the people running the show, me and George and Karen and those guys.

[28:56] We did a tournament where we gave away some NBA stuff like a watch and a basketball and sports bag or something like that.

[29:07] I forgot exactly what we ran a tournament at the show trying to show off the whole linked thing and the tournament play.

[29:16] And how did it go?

[29:17] Which was the first that game had, you know, had a tournament play system in the two.

[29:20] Right.

[29:21] And...

[29:22] But the whole marketing group never really saw it, figured it out or got behind it or anything.

[29:29] I don't know why that was, you know, they were...

[29:31] Maybe that's why Williams went down the tank. They just kind of sat and answered their phones and didn't really work pro-active very well.

[29:37] Right. Right.

[29:38] No, I thought it was pretty cool.

[29:40] I mean, you don't see a lot of people that have two NBA fast breaks. It's, you know, the only downside of it.

[29:46] Yeah, the problem with that whole idea is that, you know, you're wasting two slots in a small tight bar.

[29:52] It's not going to happen.

[29:54] Right.

[29:55] You can see it maybe at a Dave and Buster or something, whether there's lots of RAM.

[29:58] Right. Right. Right.

[30:00] So, I mean, the whole cabling system in that that was available through probably through park sales,

[30:06] did they, did you ever get numbers on how many of those they sold?

[30:09] I think we gave them away with the games.

[30:12] Really? Because everyone I've seen, I've never seen the cable.

[30:15] You know, everyone, I've had actually a number of NBAs and I've never seen the cabling in any of them.

[30:22] You know, so I...

[30:24] I know they were available for, basically, for free.

[30:27] So, just hooked into the printer interface.

[30:32] That was just a matter of putting a couple chips in the game and putting a wire cable on and you're good to go.

[30:38] Right. Right.

[30:40] So, then...

[30:41] And there was a whole topper set that they made for it that was special that I've only seen one or two of.

[30:48] What do you mean that's a topper set?

[30:50] There was a special topper that after you had your two games, you know, bolted up next each other.

[30:54] It would cross over and connect the two games.

[30:57] It was like a some kind of art, artistically designed cardboard,

[31:03] header piece or something that goes across the top.

[31:06] All that kind of like a bridge.

[31:08] That's for linked play, yeah.

[31:09] Right. Right.

[31:10] So, those things are rare. It's all money, man.

[31:13] All right. We're going to take a break from talking with Tom Uban of William Software Engineering

[31:18] and we'll be right back after this message.

[31:20] Topcast is brought to you by Pinball Life.

[31:23] Give your Pinball Machine new life with parts from Pinball Life.

[31:26] We ship Pinball Parts worldwide. Pinball Life is located in the Great City of Chicago.

[31:30] And their phone number is 773-202-8758.

[31:35] We have an open door policy and you're welcome to call us with your questions and concerns.

[31:39] 80M-5PM Central Time, Monday through Friday.

[31:43] Their website is at PinballLife.com. Pinball Life.

[31:46] No hassles, just the parts you need fast.

[31:49] Okay, we're back with Tom Uban of William Software Engineering.

[31:54] They give us some more stories about his work experience during the 1990s at Williams and Valley.

[31:59] Now, was there anything in NBA fast break that got left on the floor?

[32:06] You know, in that game, during that design?

[32:10] There may have been, but you know, it's been so long ago.

[32:13] I don't recall, actually. Georgia bail title. You need to interview Georgia.

[32:17] Try to get a hold of them. I will.

[32:20] I mean, were you pretty much when you got done with NBA? Were you happy with how that product came out?

[32:26] Yeah, I thought that was an awesome game. It's probably the favorite of the three WC games that I worked on.

[32:32] And you have each one of these games in your basement or whatever?

[32:36] I do, they're in my arcade.

[32:38] Okay, cool. And okay, so then, what, around 98, you started working on Pinball 2000, right?

[32:45] That's right. Okay.

[32:47] We worked out for 18 months, I think, before they pulled the plug.

[32:51] All right. Now, when George and Pat Lawler were working in Patch Garage for the Hollow Pin thing,

[33:02] were they can, you know, were you pretty any of that before anybody else?

[33:06] Yeah, I don't care that. You didn't.

[33:08] So they just showed up one day at Williams. They said, hey, we got this neat idea.

[33:11] Everybody come on. Let's, we're going to show you. And, you know, that was the first time you saw it too.

[33:15] Pretty much, that's right.

[33:17] Okay. And what did you think when you first saw it?

[33:21] What was your reaction?

[33:23] I thought it was hot shit.

[33:26] And, I mean, who came up with a whole idea to use a PC, you know, as the hardware element opposed to, you know,

[33:37] a customized board set like WPC 95 was.

[33:41] Well, the whole idea was the new system had to be low cost.

[33:45] And we knew that it was going to have a CRT in it.

[33:50] So we needed, you know, more horsepower to drive it than, than like just a basic microprocessor, whatever.

[33:57] The, so the only way we figured we'd be able to do that was to, to have a, you know, PC motherboard and whatever the current,

[34:06] cheapest motherboard was at the time that fit our bill.

[34:11] And had enough power.

[34:13] And then just write this off so that as over time, whatever the current thing is at that price point, which was, you know, the whole motherboard thing pretty much, they cost a hundred bucks, right?

[34:26] And this month it'll be some number of gigahertz and next month it'll be, you know, slightly faster, but it'll still be a hundred bucks.

[34:35] So we knew that it would always cost the same and it would just get faster and it'd be pretty much compatible.

[34:39] We just had to write this off for so that it would drop onto each one.

[34:42] And was that a big challenge, you know, for that as, because, you know, PC hardware got to changes every two weeks.

[34:51] Yeah, that's true.

[34:52] Fortunately, the only thing that was going to be difficult that we saw was, was that the graphics controller and it was going to be changing.

[35:01] And so our plan was, you know, to just go and build the interface so that, however that changed, it would be the same from the game programming standpoint, but we'd be able to put new low level drivers in and utilize whatever the new hardware did.

[35:18] Now, why did you use such a low, you know, VGA style monitor when you could have used literally anything for cost primarily?

[35:28] That was the reason, huh?

[35:29] It's, I think that's a mid-res monitor, isn't it?

[35:33] No, it's VGA.

[35:34] Yeah, but I think at the time it was considered mid-res maybe because we were doing 640x240 or 240x640.

[35:42] So we're pretty high horizontal, comparatively.

[35:46] Well, I don't really know the video game standards, but at the time it was just kind of mid-level resolution anyway,

[35:57] because we were doing a higher horizontal than what they were normally doing.

[36:00] Yeah, I think the normal VGA is like 640x480.

[36:04] Right, but they weren't using VGA in video games at the time either.

[36:07] Right, right.

[36:08] So it was just purely cost.

[36:10] Yeah, it was all cost.

[36:12] You know, here's 200 bucks in the monitor. We can't afford anything more than that.

[36:15] Right.

[36:16] Okay, so now, as far as programming you did everything in what C++ or C++ or something?

[36:22] It was all primarily C++ with a little bit of C.

[36:26] Okay, now, why not assembly language or it just wasn't needed at that time on that machine?

[36:33] There's no excuses, it's assembly language if you don't need to.

[36:36] Right.

[36:37] Because the whole idea, ideally we would write a system where the programmer or even the game designer could fill in some tables and test out ideas and just have it go.

[36:49] You want to build a write it in some sort of object oriented fashion so that you can reuse code.

[36:55] You want to build and make it as easy as possible to make the game fun rather than spending, you know, gods of time writing little detailed code that does stuff over and over.

[37:09] Right.

[37:10] Okay, so now you were the whole, you were basically the man behind the architect and the low level software on pinball 2000, right?

[37:22] Right. I did the operating system and the game code for that with help from a number of other people that trickled into the project over time.

[37:34] Grand West was probably the biggest other contributor.

[37:39] He did the graphics system, which included, well, pretty much all effects, including graphics and lamp and such.

[37:49] Louis Coyars did the, who's up until recently was working out at Pat Waller Design for Stern, did the adjustment and resource management system.

[38:02] Cameron Silver did some of the game, some of the game logic and a number of different things.

[38:15] And Duncan Brown did the drivers that were generic for running the PCIe type stuff.

[38:24] And then Cameron and Duncan went off and did the second game Star Wars episode one.

[38:31] So you didn't do any of the software for Revenge from Mars at all?

[38:34] I didn't do any of the game specific stuff.

[38:38] I built a lot of the framework, which was the game handling code and such for that the games are built on, that's standardized between every game, kind of like what Apple did.

[38:51] But as well as the operating system itself and the low level stuff that made it run on a PC and boot and do all the hub card and update and all that stuff.

[39:06] That was all pretty much mine.

[39:08] Now why use a, you know, the prison card system opposed to just burning off a hard disk?

[39:16] We didn't think a hard disk would survive in a pinball environment.

[39:19] There's too much vibration.

[39:21] Too much vibration failure. We just didn't want that risk not to mention the additional cost.

[39:28] Looking back on it, was that a smart choice?

[39:31] Yeah, I think it was because if we did it today, you could throw in a compact flash that was way bigger than you needed.

[39:38] And wouldn't have had ROMs at all, but it would still be updateable easily and such.

[39:45] Now explain the whole prison system and how that works.

[39:48] You've got, you basically do have ROMs on that with some base level, you know, let's talk about Revenge from Mars as our example.

[39:58] So you've got a prison card with ROMs on it with some base level of Revenge from Mars software, right?

[40:04] Right, it's the main, the card is a simple PCI architecture with a PCS2 style sound system and 72 megabytes of mass ROM, which at the time, I think may even still be the case today, you couldn't have any.

[40:27] So if we were to verify e-proms that were as large as the mass ROMs that we used on that, for 64 megabytes of that was for game image and code.

[40:41] And the other 8 megabytes was for the sound system.

[40:46] And then there's also four megabytes of flash for updates of the game code and our imagery.

[40:53] And another one megabyte, I think, of flash that contained the system for the DCS sound and you could update that as to update any sound stuff you needed.

[41:05] So when you run the update manager, the software actually ends up on the prison card.

[41:11] Yeah, when you boot without an update, it boots out of the mass ROMs.

[41:19] And when you update, it puts new code into the flash and there's a standard set of boot code that comes out of the mass ROMs that checks if there's an update and if there is an update, it loads up that instead.

[41:34] It does a bunch of verification to make sure it looks good and all that.

[41:38] Right, right.

[41:39] And the sound system works similarly, although I don't know the exact details of that that was written by Andy Elow.

[41:47] And this whole system with, I mean, this prison card, was this a prison card custom made for you guys or is this something that was commercially available?

[41:59] No, we designed it in-house. Brad Hymn did the electrical design based on what we figured we needed.

[42:07] So this whole pinwall 2000 from the software and hardware standpoint, this must have been a real, a pretty serious challenge for you.

[42:16] Yeah, it was a big project, especially for the time scale that we did it on.

[42:20] We got the system, we started working on it and got a system out the door and effectively 18 months, year and a half, which is pretty out of control, really.

[42:29] I mean, think about it how long that is.

[42:31] Well, how long do you know how, like for example, you were there when they transitioned from regular WPC or WPC89, whatever you want to call it, to WPC95.

[42:41] Yeah, I just barely caught the end of that.

[42:44] I mean, was the development time on that pretty long?

[42:47] I don't really, I don't know the details on that. I wasn't involved with it.

[42:53] I kind of saw the tail end of that thing happen, but I wasn't involved in that development, so I don't know.

[42:59] Right. So now, what was the biggest challenge when doing the pinball hardware architecture in the operating system? What was the toughest thing to accomplish?

[43:10] I think it was pretty much all uniformly hard. Getting it all done in the time frame that we had, right?

[43:22] We had to make the hardware work, which given Brad's design skills wasn't terribly difficult, but still a big item.

[43:32] A brand new operating system and game environment, all meeting the challenges of a team that started working out before we were done to get revenge out the door.

[43:45] Yeah, it was just one big blur. It was a lot of work, and it turned out really well, I think.

[43:53] Yeah, sure did. I've got a revenge, and I think it's awesome.

[43:58] I have to say one of my biggest disappointments is that, well, in addition, or besides William is turning off the whole pinball thing, which you can justify to some extent based on how much they are losing money wise.

[44:15] But the fact that they didn't organize the sale of the company or the sale of the IPC or any of that, you know, it just mind-boggling right?

[44:30] Here's all this intellectual property that they could have done something with, but didn't.

[44:36] And what's become of it is even crazier right now. Now the patent rights for 10,000 are spread across a couple of different people and corporations, and if someone did want to do pin 2,000 today, I think it would be nearly impossible.

[44:51] Well, it would probably be pretty tough to do that. I don't know. You'd have to port everything to current PC under-hology.

[45:00] I'm just talking technology wise. If you wanted to build a game that had reflective, you know, virtual display thing, independent of whether you utilized existing software and tried to port it, the patents that control the use of that in a pinball game are divided across multiple entities, so no one company has the rights to do it.

[45:24] So you mean it's stern, for example, wanted to go in that direction. They'd have a really tough time because all of them.

[45:29] That's right, because G-none, some of it, and Australian, Wayne, some of it, and I think Williams may still have a piece of it.

[45:39] Yeah, it's a big mess.

[45:41] Yeah, huge mess. So now when Revenge came out, you guys, it was first introduced to what in England, right? At Traitio in England?

[45:52] That's right. Did you go over there when that was happening?

[45:57] Actually, that's one of the disappointments that I didn't choose to do that because I thought it was better time spent on my part to sit in my office and get the pub card, update code, and software update stuff working.

[46:13] I recall working on it. I think it was like a Saturday night or something when those guys were all over there.

[46:17] It was probably like, I don't know, eight or nine at night. I don't think I'm getting that going, and they're all over there on crating games, and I guess it wasn't all that much fun, but certainly more fun to sit in my office.

[46:28] Now the one thing that keeps coming up is the pub card. Why don't we talk about that and what the theory was behind the pub card?

[46:38] I think it was a pretty innovative idea was that you have this isobus card which would have had to have been done differently with newer motherboards that don't have isobus, but the idea is that when you throw an isobus card in a PC, the BIOS, which we actually didn't change.

[46:58] We used existing BIOS boots or executes code out of the ROM that sits on an isocard potentially if that card looks like a graphics card or maybe even some other cards like network cards.

[47:14] What we did was just put a chunk of ROM, of memory, flash memory on a board that plugged in an isocard and a little bit of code there that got executed by the BIOS and we just take over.

[47:27] I should explain that iso means industry standard architecture which was basically the slot configuration for a PC back in the day.

[47:37] That's right. That's how you plugged in your graphics card or your some kind of isocard game controller or whatever.

[47:44] That's all changed now. They don't use ISA or USB or whatever.

[47:51] This pub card, you know, basically people didn't buy the pub card. If you were an operator, you could go down to your distributor and maybe borrow the pub card which would have the latest version of revenge on it and plug it in your machine and it would update it.

[48:06] Is that what the theory was?

[48:08] Most people didn't buy, well I guess there were some people at pot games but for the most part games weren't sold to individuals at the time.

[48:17] There were operators who ran big routes and if they wanted to update their software in their game they would have some number of these cards. They didn't cost anything. They were really simple.

[48:28] You could take this card and plug it into your PC and load it up with the latest software and then take it over to each of your games and update your software in your games.

[48:38] Even though there wasn't USB back then it was almost trying to be a USB flash memory.

[48:50] It would work like that.

[48:56] There's a little less user friendly since you had to open the chassis on a PC and order the plug in a year.

[49:05] Yeah, pre-USB days as it may be.

[49:09] Now when you were doing the software too, you were still developing all the operating system while the guys were doing Star Wars Episode 1 too right?

[49:22] Yeah we continued to make updates and make it better.

[49:26] Now, did you ever get to play Wizard blocks?

[49:30] Sure, I played it a couple times.

[49:33] What did you feel about that game?

[49:35] I thought it was going to be spectacular.

[49:38] So I mean even...

[49:40] He was probably going to be a bad game for you know that he had done in some time.

[49:44] He was really enthusiastic about it.

[49:47] He was going to use some skills that he had a background in theater and such so.

[49:54] He thought that his background in theater with his lighting skills would have fallen directly in line with the buildings of making stuff appear and the virtual area on the screen and behind it.

[50:08] It would have been just an awesome game.

[50:10] How far did he get with that code?

[50:13] Or the whole game for that matter?

[50:15] They had a prototype, I think Gene's got it.

[50:18] Right, but I mean it's not really...it's nowhere near finished right?

[50:21] I don't recall if there was any final artwork you even designed for it.

[50:26] I just don't know the answer to that question.

[50:28] I've only ever seen the white wood.

[50:30] Right, right.

[50:32] So now at Expo 1999 they had the game for Expo was the event from Ernott Revenge Star Wars Episode 1.

[50:41] And didn't you develop some sort of system for the tournament scoring that linked the machines together?

[50:48] Right, Lime and Sheet's wrote some Java code that would run on a PC and communicate with a server that I wrote that ran in, ran on the...

[50:59] ...pinned 2000 box in the game.

[51:03] And they would interact and together we put together a system where you could swipe cards and run a tournament.

[51:12] And we demoed that at the Expo.

[51:17] It went pretty well.

[51:19] Yeah.

[51:20] Give it how much time we didn't have to develop it and how much we didn't actually get to test it out before we went there and tried it.

[51:28] It actually worked pretty well.

[51:30] Yeah, it seemed to work really well actually from what I remember.

[51:34] You know, I mean just from a casual look around.

[51:38] You know, I thought it was pretty impressive.

[51:41] Now let's talk about Black Monday.

[51:44] Were you at work on that Monday?

[51:46] No, I was on vacation.

[51:47] You were on vacation.

[51:49] So...

[51:50] I've done a Southern Indiana, I think, somewhere.

[51:52] So what, I mean, how did that whole thing play out with you?

[51:55] Pat.

[51:58] I mean Jim Patla gave me a call and told me about it.

[52:04] And what, I mean, did you see this coming?

[52:07] No, I didn't see it coming at all.

[52:09] You know, it was obvious that George kind of had some...

[52:12] Yeah, George kept it, mom.

[52:14] Yeah, but he did know about it all ahead of time.

[52:17] Yeah, you know, it might have been partly because I was gone for a few days before people were, you know, like George, we're knowing too.

[52:25] I don't know when he first learned, but I've been gone for like a week or something on my vacation and then I found out.

[52:33] So I was kind of out of the loop for a little bit there.

[52:36] And what was your feeling when that whole thing, you know, when you first got off?

[52:40] You were pissed off?

[52:41] Sure.

[52:42] Okay, now I mean, how during the whole development of pinball 2000, how was management, I mean, how were...

[52:49] What was your perception of their reaction to it?

[52:54] I think everyone thought it was, you know, the best thing since light spread, we reinvented the wheel.

[53:00] And that was how I perceived that our customers were taking it to right up until there was some kind of deal going on with the European sales on Star Wars Episode One,

[53:14] where because management thought it was doing well, as I said, they decided to raise the price or something that I don't know how to do tell them that.

[53:24] Yeah, they raised the price 500 bucks.

[53:26] Yeah, they raised the price and then Europe can't fill a bunch of orders or something like that.

[53:31] Yeah, with the exchange rate, that $500 at the time, the US dollar was much stronger.

[53:38] You know, that equated to a lot more money for them.

[53:41] And they got a lot of, you know, because I guess they were just piling on orders for that game.

[53:46] That whole Star Wars thing was just, you know, that was the first of the new movies.

[53:51] Yeah.

[53:52] Of course, you know, nobody knew about Jar Jar at that point.

[53:57] And that's wrong with Jar Jar.

[53:59] So you think.

[54:01] So, you know, there was a bunch of orders canceled because of that.

[54:06] It almost seemed like to some people would say that that was sabotage, to some degree.

[54:11] I don't know if it was sabotage or just poor business judgment or what.

[54:16] Right.

[54:17] I think, you know, I think that management felt that they needed to get more out of it and they probably felt they could get more out of it based on how well it was doing.

[54:24] And that they didn't expect it to backlash as much as it did.

[54:29] Right.

[54:30] Right.

[54:31] So, were there any other bonehead management moves that kind of, you know, caused some problems?

[54:37] For pretty much 2000?

[54:39] Right.

[54:40] I don't know.

[54:41] You know, other than pulling the plug now.

[54:43] So, they were completely supportive of the whole thing all the way along and then all of a sudden just one day they said, that's it.

[54:50] We're done.

[54:51] Yeah, that was pretty much my perception, but what I'm sure there was, you know, I wasn't, you know, I'm not an accountant or anything.

[54:58] So, I'm sure there was a lot of bleeding going on and they were trying to figure out how to make it, they make money.

[55:05] Not to mention that here's this other lucrative business that they're doing now, running building flop machines.

[55:12] It's like, what are we doing?

[55:14] Why are we losing all this money on this thing when we could just be building these things that turn into gold, right?

[55:18] Right.

[55:19] Even though PIMO was, PIMO 2000 was actually making a money that we actually showed a profitable, or a profitable year or quarter, I can't remember.

[55:26] You know, it seemed like it was doing well.

[55:29] Yeah, I don't know.

[55:31] Maybe the projections didn't look good.

[55:33] I don't, you know, I can't speculate there.

[55:36] It's easy to lay blame and such, but who knows, without, you know, pretty good sized engineering department.

[55:45] So, I'm sure that 8 tons of money, there were things going on that we just didn't know about, right?

[55:53] So, how about, you know, after that, did you stay on for any length of time, or were you just immediately gone?

[55:59] They kept a select number of people to wrap up an archive, and I was chosen to do that.

[56:08] So, I wrapped up an archive for a month, and then we're done.

[56:13] So, we put all this stuff neatly into a room as if they were going to do something useful with it, and then it just evaporated.

[56:19] Right.

[56:20] So, there's a bonehead thing.

[56:21] Yeah, the evaporation part.

[56:23] Yeah.

[56:24] Yeah, because that, you know, yeah.

[56:27] I mean, that whole thing, I mean, when I go and play the revenge, you know, I think it's, you know, maybe it's, you know, it's not a perfect system, but it's the first game, you know, what do you want, you know?

[56:38] Look, I showed the timeframe was to develop that.

[56:40] Here's a brand new game, on a brand new system, developed in record time, granted they had, you know, pretty good number of people programming it and such, but still, I think it turned out pretty damn good for what it was.

[56:53] And it was, yeah, it's just a shame.

[56:58] Right.

[56:59] So, did you, when you that done, were you tempted to go work with Stern or anybody?

[57:05] I never really went there and approached them to try and work with them, and they never called me, and I don't know what the situation was there at the time, and I've never really attracted.

[57:19] You know, in touch with people, I know that worked there now, but now I never, never went to try and work with Stern.

[57:28] And you don't work in coin-off anymore, right?

[57:30] No, I went after Williams, I did a little bit of consulting for Ted at WMS, and opted not to go over to Midway because I was just kind of pissed off at that time, so I didn't want to continue that.

[57:47] Although I did have a job offer over there, and so I helped get a group of extra involved people employed by Cisco Systems, who I knew some people from both Brannock and M&M that were working for them, and so we opened up the office in Chicago, and that's where Ted and Bill and a number of people are still working.

[58:14] Right, I'll kind of end up there.

[58:16] Right, although I've left there or so.

[58:19] Right, you're doing consulting again?

[58:21] Yeah, I'm doing consulting again now.

[58:23] How's that going? Is that good?

[58:25] Yeah, it is good.

[58:26] Okay, is there anything I've kind of left out of the whole picture here that you know you should throw it in that?

[58:32] I think we've covered it.

[58:34] Okay, all right Tom, well I appreciate the time.

[58:37] I appreciate...

[58:38] More than welcome.

[58:39] Yeah, I appreciate the stories, I mean, we didn't leave anyone's out, did we?

[58:43] Anybody's story?

[58:44] No, I mean, no, I mean, we leave any good stories out of the whole, you know, your whole kind of 1993 to 1999.

[58:52] I was all kinds of stories, but we don't have time for that.

[58:54] Oh, yeah, we do. Come on, man, give me a story.

[58:56] I don't have any good stories.

[58:58] Okay, all right, man.

[59:00] I know you are, but I just don't remember.

[59:02] I've been way too long.

[59:03] Yeah, I'm getting to be an old friend now, I can't remember shit.

[59:05] Yeah, there you go.

[59:06] All right, Tom, well hey, thanks.

[59:08] Oh, there is one actually one other thing that I don't know, I'd like to mention it.

[59:13] And that's the Zoltan project.

[59:16] Oh yeah.

[59:17] Yeah, that was back, that must have been in early 2001 maybe.

[59:23] That was all your fault.

[59:24] Yeah, that was my fault.

[59:25] I had a Zoltan fortune teller, which came out in the late 60s and used a cuisine tape player,

[59:34] which was kind of like a customized, you know, a track.

[59:38] Yeah, I wasn't the, I would say more like a four trackish type thing or something.

[59:42] I don't know what it was.

[59:43] And the loop.

[59:44] Yeah, endless loop tape.

[59:45] And the tapes were always eaten.

[59:47] And I actually hired you to come up with a, you know, kind of like an MP3 solution, sort of speak.

[59:54] But you hire me?

[59:55] Yeah, I think I paid you, didn't I?

[59:57] Oh, yeah, you paid me for a box or two.

[59:59] Oh, come on, man, I gave you some money, didn't I?

[01:00:02] Yeah, you gave me some money for the box, because I don't think you paid me to do the work though.

[01:00:05] I didn't, huh?

[01:00:06] Did I, do I still owe you?

[01:00:08] Not that I recall.

[01:00:09] Do I owe you?

[01:00:10] You bought the first couple boxes, so there you go.

[01:00:12] So I'm okay, we're okay?

[01:00:13] Oh yeah.

[01:00:14] Okay, all right.

[01:00:15] And now you've got people knocking your door down to get one for either they're pepping the clown or for the Zoltan, right?

[01:00:21] Yeah, I sold, I don't know how many, I sold maybe a dozen.

[01:00:25] Man, I get, I still get emails from people wanting to buy them and they're like, you know, throwing money at me and I'm like,

[01:00:30] you're throwing money at the wrong guy.

[01:00:32] You know how much work those things have to put together?

[01:00:34] I have not a clue.

[01:00:35] You know, I know you did all surface melt.

[01:00:38] You couldn't have done, played it through holes to make your soldering life a little easier.

[01:00:42] Oh, I could have in the board a bit of it much harder to do, but then you can't get parts to do what they do today in that scale.

[01:00:48] All right.

[01:00:49] But yeah, no, the surface melt wasn't the problem, it's just, you know, just a lot of time to put it together.

[01:00:56] And I do have a bunch of people queued up to buy some if I produce another batch.

[01:01:02] I keep threatening to do that, but it hasn't happened yet.

[01:01:05] Why don't you have it commercially done?

[01:01:08] Yeah, I hate to think what it would cost to have it commercially done.

[01:01:11] Right.

[01:01:12] Right. Yeah, because it wasn't really that expensive.

[01:01:14] It's just like kind of explained to people what it was is basically, I had all the Zoltan fortunes in MP3 format.

[01:01:21] And then your player actually interfaced, it was a plug and play thing into the machine where you literally just unplugged the original tape player and plugged your box in.

[01:01:34] And your box was a solid state equivalent with no moving parts, nothing to wear out.

[01:01:40] Right. I actually designed the board that was based on, in an effort that I was working on to start a pinball effort.

[01:01:50] And that didn't go anywhere.

[01:01:53] But so I took that design and modified it to do what you wanted.

[01:01:59] And that's pretty much where it came from.

[01:02:02] So I'd already had a lot of the design work done and I just had to hack off some logic that wasn't used for it.

[01:02:09] So I just had to make the design a little bit and make the board.

[01:02:12] Right. Well, it came out great. I mean, I've got one in both my Peppie the Clown and my Zoltan.

[01:02:18] And Buddy in mind has one of those auto test, capital projector auto test, and he wants one for that too.

[01:02:25] Apparently it'll pull just right out of that.

[01:02:27] That's what the guy called me the other day.

[01:02:29] Right. Yeah, that's Bill.

[01:02:30] All right, well Tom, I appreciate the talk. Thanks a lot.

[01:02:33] All right, you're welcome.

[01:02:34] Okay, thank you.

[01:02:35] All right, take care.

[01:02:36] Bye.

[01:02:37] I'd like to thank Tom Uban again for talking to us tonight here on Topcast and giving us his perspective software development during the 1990s at Willie's Valley software.

[01:02:49] And until next time, I hope to see you again on Topcast.
