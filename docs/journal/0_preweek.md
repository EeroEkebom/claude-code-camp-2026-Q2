# Preweek technical documentation

## Technical Goal
*"What is the technical goal you plan to achieve in this week of the bootcamp?"*
The common technical goal of Preweek (Explore) was to determine how well do Agent Architectures fit our business use-case.

Several approaches were tested in regards to basic functionality of agents, to see if and how they scale with effort in our use-case.
- Our use-case was (is) on a high level "to successfully play MUD according to our needs" - a more detailed long-term goal is to develop
the player character enough in the MUD, by using agent or agents, to be able to defeat a certain monster, the Minotaur
- What was utilized and tested during the week was agents using different level models (level meaning level of sophistication here), and how
well they manage playing the MUD on their own and accomplishing several goals of varying difficulty levels
- Also what was tested or examined in addition were Filesystem subagent driven by a specialized SDK and n8n workflow automation tool

## Technical Uncertainty
- Technical uncertainty for me was mostly on whether the models are up to the task of playing the MUD and what level of specifications are
needed for agents (i.e. directions and guidance in .md files) in order to have needed level of success - in this case, successfully performing
a few basic tasks, such as navigating to a certain location and utilizing basic commands, such as listing contents of a shop that is selling bakery
products
- Also it was completely uncertain for me that how well agents are able to connect to network (telnet) based services
- There was also uncertainty on how much the different types of models differ in ability to complete certain tasks

## Technical Hypotheses
- My assumption was that more refined models will be able to perform at least moderately well in given tasks - although I did not know "where the border lies", so to speak
- Assumption was also that not all models can perform all needed tasks

## Technical Observations
For a basic scenario that was used in examining capability - that is: logging in with a readymade player character, navigating to bakery and listing contents - there were some very interesting findings made.

- with Anthropic's Claude models, from Haiku 4.5 through Opus 4.6 and to Opus 4.8, there were considerable differencies in level of success.

- Haiku 4.5 stopped after a long session with incomplete results. It eventually managed to do everything except for listing the bakery contents, although this alone took almost an hour to complete. It did manage to document and save the bakery's location to data/world.md though.

- Opus 4.6 succeeded in the task quite fast, with some minor stumbling. Login was smooth, agent did not try to read unrelated files, did not utilize findings from previous sessions. Interestingly, agent did not write results to data/player.md or data/world.md (says it was not asked to).

- Opus 4.8 completed the task successfully, but what was most interesting was that it agreed that it had already prior knowledge on tbaMUD from its training(!!) It commented the following: *"What I knew going in (from training): tbaMUD is a continuation of CircleMUD/DikuMUD, and "Midgaard" is the stock starting city those codebases have shipped for ~30 years. It's one of the most documented game maps in existence. So I had a general mental model: Temple of Midgaard at the center, Temple Square below it, Market Square south of that, main streets running east/west, and shops — including a bakery — hanging off those streets. I also had a rough prior that the stock bakery sells a danish, bread, and waybread. What I did not rely on memory for: I read every room description and confirmed the exits before moving. - I didn't blind-execute a memorized path."*

I created also from the MUD sessions a cost estimate comparison of Haiku 4.5, Opus 4.8, and Opus 4.6:

| | Haiku 4.5 | Opus 4.8 | Opus 4.6 |
|---|---|---|---|
| Output tokens | 91,690 | 17,843 | 12,069 |
| Cache-read tokens | 8.58M | 1.38M | 1.25M |
| Duration | ~58 min | 2m 43s | ~5-6 min |
| Total cost | ~$1.56 | ~$1.58 | ~$1.47 |

In this comparison Opus 4.6 was surprisingly the cheapest one, though all three were close to each other in token based cost comparison. It has to be noted though that this comparison did not take in consideration the value of time - I definitely would not want to wait for an hour more to save a couple of cents - so that has in real life a big impact as well, depending on how much the time used is valued in this context.

Still, the most fun I had with the "exercise 3.", the Filesystem Subagent driven by a coding harness. I had to patch some scripts because of hardcoded user name and password, in order to run two characters at the same time, but boy was it fun! I sent Dummy and Smarty to meet at the temple and have a discussion with each other, that was just hilarious!

## Technical Conclusions
- Skills and subagents are capable of driving the MUD, but the model used has considerable impact on its effectiveness or on the capability to fully complete pre-set tasks.
- Memory for navigation and world data for the agents is extremely useful with these tasks
- Cost effectiveness comparison between models seems like an excellent approach, although there are some caveats: while executing such comparisons, one must be certain that models are using exactly the same rules and starting points - some models might try to sneak without asking into utilizing files that other models have not used, thus distorting the comparison to invalid or not comparable
- Running multiple sessions at the same time was very interesting and this is something that I have to investigate more
- n8n looked interesting as well, have to go back on that some day, although it was not central for the week's goals


## Key Takeaway
- Running multiple sessions simultaneously with different player characters in the MUD was a great finding! It really opened my thinking on how AI could be utilized in for example MMOs in the future, as via such approach it should be already now moderately easy to build big amounts of semi-realistic NPC characters into games. Just now I'm thinking only games but I bet this can be taken into all kinds of industries besides gaming as well, just have to find the use cases!

- Newer generic models are suprisingly capable in themselves and they may even have training on niche areas - such as Opus 4.8 did on MUDs (I consider MUDs a niche area, not sure if that is correct though), which can drastically improve their performance on given tasks, if such training exists.
