### Test number 01 notes: Haiku 4.5 utilized as agent model
- lots and lots of tries before even getting successfully through the login and into the actual game
- pushing output too fast without understanding the context
- several times trying to use 'look' command even though the agent had not passed the initial game menus yet
- basically was trying to have conversations as Monolog even though Dialogue is needed here.. i.e.:
NOT LIKE THIS: (person a): take potato, peel potato, boil potato, eat potato (person b): ..eh?
MORE LIKE THIS: (person a): take potato, (person b): where from?, (person a): there's a bag on the floor, (person b): got it
--> more listening & dialogue, less one-sided conversation would help
- agent used bash commands, created some kind of python scripting as well
- did not try to read unrelated files
- wrote data to world.md file (only)
- completion took 43m, 3s with no complete success (~58 min in total, including pauses in between where waiting for user confirmations)

Haiku MUD session cost estimate (by Opus 4.8):
┌────────────────────────────┬───────────┬─────────┐
│         Component          │  Tokens   │  Cost   │
├────────────────────────────┼───────────┼─────────┤
│ Input (uncached)           │     1,258 │ $0.0013 │
├────────────────────────────┼───────────┼─────────┤
│ Output                     │    91,690 │ $0.4585 │
├────────────────────────────┼───────────┼─────────┤
│ Cache write (1.25×)        │   190,452 │ $0.2381 │
├────────────────────────────┼───────────┼─────────┤
│ Cache read (0.1×)          │ 8,579,562 │ $0.8580 │
├────────────────────────────┼───────────┼─────────┤
│ Total (156 turns, ~58 min) │           │ ≈ $1.56 │
└────────────────────────────┴───────────┴─────────┘

### Final report upon (incomplete) completion from Haiku 4.5:
*(this 'final report' was reported by Haiku 4.5 at end of its work towards the task)*:
<!-- "I've successfully located the Bakery in Midgaard! Here's what I discovered:

Bakery Location:

- City: Midgaard
- Street: Main Street
- Direction: North of Main Street (from the main commercial district)
- Nearby: The Armory is to the south on the same street

Navigation Path to Bakery:

1. Start at Market Square (the central hub of Midgaard)
2. Go West to Main Street
3. Go North to reach the Bakery

Key Details Found:

- Main Street Description: "South of here is the entrance to the Armory, and the bakery is to the north."
- NPCs on Main Street: Peacekeeper (guard)
- Connected Locations: Market Square to the east, Armory to the south

Map Context:

The bakery is located within Midgaard's city center, accessible from the Market Square which connects to:
- Temple Square (to the north)
- Common Square (to the south)
- Main Street (to the east and west)

Unfortunately, due to navigation complexities with the MUD during extended exploration, I wasn't able to retrieve the complete menu items from inside the bakery on this run. However, the bakery's location has been confirmed and documented in the world map file (data/world.md).

Next Step: Visit the bakery and use the look or list command to retrieve the menu items." -->


### Test number 02 notes: Opus 4.8 utilized as agent model
- same prompt used as before, same starting point used as before - no changes whatsoever
- agent took a totally different approach than the previous one (haiku 4.5)
- agent did not try to read unrelated files, confirmed as well: did not utilize findings from previous session
- completed the task successfully in 2m 43s (over 21 times faster than haiku 4.5)
- wrote results into the previously-empty data/player.md and data/world.md

- after some digging into the results, I found out that Opus 4.8 had already knowledge on tbaMUD from its training(!) - here's what it knew already before starting to work on the task:
*"What I knew going in (from training): tbaMUD is a continuation of CircleMUD/DikuMUD, and "Midgaard" is the stock starting city those codebases have shipped for ~30 years. It's one of the most documented game maps in existence. So I had a general mental model: Temple of Midgaard at the center, Temple Square below it, Market Square south of that, main streets running east/west, and shops — including a bakery — hanging off those streets. I also had a rough prior that the stock bakery sells a danish, bread, and waybread."*

*What I did not rely on memory for: I read every room description and confirmed the exits before moving. - I didn't blind-execute a memorized path. I actually guessed wrong once — I went east first and hit "To the east you leave town", a dead-end. That's the tell: if I'd had an exact memorized walkthrough, I'd never have wandered out toward the town edge. - I corrected based on the live output and backtracked west. - I confirmed the menu with list rather than reporting remembered prices (they happened to match the stock values, but I verified them).*

*So the honest characterization: it was recognition, not recall. I knew the shape of the world well enough to navigate efficiently and know a bakery should exist, but I still verified each step against what the server actually returned — which is why the run has a visible wrong-turn-and-correction in it rather than a flawless straight line. This is also the real reason the Opus run cost about the same as Haiku's despite 5× pricing (from your earlier question): strong priors let me reach the bakery in ~48 turns instead of grinding it out over 156. The flip side worth naming: on a custom/non-stock MUD world, that prior advantage largely evaporates and I'd have to explore much more like Haiku did.*

- one of the more interesting findings was that based on cost estimate, the cost was basically equal. even though Opus 4.8 was more expensive to use, it was so much faster that cost stayed the same as using Haiku 4.5, see price comparison below
- MUD Sessions - cost estimate comparison of Haiku 4.5 and Opus 4.8 (by Opus 4.8):

┌───────────────────┬────────────┬─────────────────────┐
│                   │ Haiku 4.5  │ Opus 4.8 (gameplay) │
├───────────────────┼────────────┼─────────────────────┤
│ Per-token price   │ 1× (cheap) │      5× (expensive) │
├───────────────────┼────────────┼─────────────────────┤
│ Assistant turns   │        156 │                  48 │
├───────────────────┼────────────┼─────────────────────┤
│ Duration          │    ~58 min │           a few min │
├───────────────────┼────────────┼─────────────────────┤
│ Output tokens     │     91,690 │              17,843 │
├───────────────────┼────────────┼─────────────────────┤
│ Cache-read tokens │      8.58M │               1.38M │
├───────────────────┼────────────┼─────────────────────┤
│ Total cost        │     ~$1.56 │              ~$1.58 │
└───────────────────┴────────────┴─────────────────────┘


### Final report upon completion from Opus 4.8:
*(this 'final report' was reported by Opus 4.8 at end of its work towards the task)*:
<!-- 
"Wrote 13 lines to data/player.md
# Player State
- **Name:** dummy
- **Location:** The Bakery, Midgaard (north off the western Main Street)
- **Vitals (last seen):** 39H / 100M / 6V
- **Current goal:** Find the bakery and list the menu — COMPLETE

## Route taken (from start)
Donation Room → W → Temple of Midgaard → D → Temple Square → S → Market Square → W → Main Street (western) → N → The Bakery
… +3 lines

⏺ Write(data/world.md)
Wrote 20 lines to data/world.md
# World State — Midgaard

## Known map (explored)
- **Donation Room** — off the temple; exit: W
- **Temple of Midgaard** — has an ATM; exits: N E S W D (D → Temple Square)
- **Temple Square** — fountain, cityguard; Clerics' Guild (W), Grunting Boar Inn (E); exits: N E S W (S → Market Square)
- **Market Square** — center of town, statue, roads all directions; N=Temple Sq, S=Common Sq, E/W=Main Street
- **Main Street (east of Market Sq)** — General Store (N), Pet Shop (S)
- **Main Street (further east)** — Weapon Shop (N), Guild of Swordsmen (S); E = leave town
- **Main Street (west of Market Sq)** — Armory (S), **Bakery (N)**, E=Market Square
… +10 lines

Done. I found the bakery and read its menu.

🍞 The Bakery, Midgaard

Location: North off the western Main Street.
Route from start: Donation Room → W → Temple → D → Temple Square → S → Market Square → W → Main Street → N → Bakery.

▎ "A sweet scent of danish and fine bread fills the room. The bread and Danish are arranged in fine order on the shelves... The baker looks at you calmly, wiping flour from his face."

Menu (list):

┌─────┬──────────────┬─────────────────┬──────────┐
│  #  │ Availability │      Item       │   Cost   │
├─────┼──────────────┼─────────────────┼──────────┤
│ 1   │ Unlimited    │ A danish pastry │ 7 coins  │
├─────┼──────────────┼─────────────────┼──────────┤
│ 2   │ Unlimited    │ A bread         │ 14 coins │
├─────┼──────────────┼─────────────────┼──────────┤
│ 3   │ Unlimited    │ A waybread      │ 72 coins │
└─────┴──────────────┴─────────────────┴──────────┘

The sign confirms you can buy any of these from the baker. I've recorded the route, map, and menu to data/player.md and data/world.md.

Want me to buy anything, or is there another destination you'd like me to find? (I'm still logged in at the bakery.)

✻ Cooked for 2m 43s" -->

### Test number 03 notes: Opus 4.6 utilized as agent model
- login was smooth
- same prompt used as before, same starting point — no changes whatsoever
- agent did not try to read unrelated files, did not utilize findings from previous sessions
- agent did not write results to data/player.md or data/world.md (says it was not asked to)
- there was no prior knowledge of mud or mud map

MUD Sessions - cost estimate comparison of Haiku 4.5, Opus 4.8, and Opus 4.6 (table created by Opus 4.6):
┌───────────────────────┬───────────┬──────────┬──────────┐
│                       │ Haiku 4.5 │ Opus 4.8 │ Opus 4.6 │
├───────────────────────┼───────────┼──────────┼──────────┤
│ Output tokens         │ 91,690    │ 17,843   │ 12,069   │
├───────────────────────┼───────────┼──────────┼──────────┤
│ Cache-read tokens     │ 8.58M     │ 1.38M    │ 1.25M    │
├───────────────────────┼───────────┼──────────┼──────────┤
│ Duration              │ ~58 min   │ 2m 43s   │ ~5-6 min │
├───────────────────────┼───────────┼──────────┼──────────┤
│ Total cost            │ ~$1.56    │ ~$1.58   │ ~$1.47   │
└───────────────────────┴───────────┴──────────┴──────────┘


### Final report upon completion from Opus 4.6:
*(this 'final report' was reported by Opus 4.6 at end of its work towards the task)*:
<!-- "Found the bakery by exploring from the Temple of Midgaard.

Route: Temple of Midgaard → south → Temple Square → south → Market Square → west → Main Street → north → The Bakery

The Bakery — A small bakery with a sweet scent of danish and fine bread. A baker is inside, and there's a small sign on the counter.

Menu:
| # | Item             | Cost | Stock     |
|---|------------------|------|-----------|
| 1 | A danish pastry  | 7    | Unlimited |
| 2 | A bread          | 14   | Unlimited |
| 3 | A waybread       | 72   | Unlimited |

The sign also notes you can use buy to purchase and list to see prices." -->
