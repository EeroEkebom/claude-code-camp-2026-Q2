---
name: play-mud
description: Play tbaMUD on behalf of the user — navigate rooms, find locations, buy items, fight monsters, gain XP, level up, and pursue long-running goals. Use this skill whenever the user gives any in-game goal: "find X", "go to Y", "buy Z", "defeat the [monster]", "get me to level 7", "grind XP", "explore Midgaard", "where is the temple", "check my character", or any task that requires connecting to and interacting with the MUD at localhost:4000. Also use this skill to resume a previous session — if player.md has an active goal, pick up from there without asking the user to repeat themselves.
---

# play-mud — tbaMUD Agent Skill

## 1. Start every session by reading memory

Before connecting to the MUD, read both memory files:
- `~/.claude/skills/play-mud/data/player.md` — character state, active goal, progress so far
- `~/.claude/skills/play-mud/data/world.md` — known map, monsters, shops, trainers

This lets you resume exactly where the last session ended without re-exploring. If the files are empty, this is a fresh start — run `score` and `look` after connecting to establish baseline state.

## 2. Connection

- **Host:** localhost  **Port:** 4000
- **Username:** dummy  **Password:** helloworld
- **Helper script:** `~/.claude/skills/play-mud/scripts/mud_cmd.sh`

```bash
bash ~/.claude/skills/play-mud/scripts/mud_cmd.sh "look"
bash ~/.claude/skills/play-mud/scripts/mud_cmd.sh "score"
bash ~/.claude/skills/play-mud/scripts/mud_cmd.sh "consider rat"
bash ~/.claude/skills/play-mud/scripts/mud_cmd.sh "kill rat" "look"
```

The script handles authentication automatically. Each call is a fresh connection.

## 3. Long-goal workflow

When the user sets a goal like "reach level 7" or "defeat the city guard", break it into a sequence of short-term steps:

1. **Read memory** — what level are we, where did we leave off, what's the active goal?
2. **Assess** — run `score` to check current XP, HP, and level
3. **Plan the next step** — one concrete action (e.g. "kill rats in the alley until I level up")
4. **Execute** — use the script, one exchange at a time, reading responses carefully
5. **Update memory** — after each meaningful action, write current state to player.md and world.md
6. **Report progress** — tell the user what was accomplished, what's next, and what the blockers are

For goals that take multiple sessions, the memory files are what allow you to pick up later. Write them thoroughly.

## 4. Commands

### Navigation
| Command | What it does |
|---|---|
| `look` | Describe current room and exits |
| `go <dir>` / `n s e w u d` | Move in a direction |
| `score` | Character stats: level, XP, HP, mana, move |
| `inventory` | List carried items |
| `who` | Players online |

### Combat
| Command | What it does |
|---|---|
| `consider <target>` | Assess whether you can beat this enemy — always do this first |
| `kill <target>` | Initiate combat |
| `flee` | Escape from combat (may fail — try again if so) |
| `rest` | Recover HP/mana slowly (safe rooms only) |
| `sleep` | Recover HP/mana faster (safe rooms only) |
| `wake` | Wake up from sleep |

### Shopping / economy
| Command | What it does |
|---|---|
| `list` | Items for sale in current shop |
| `buy <item>` | Purchase an item |
| `sell <item>` | Sell an item to a shopkeeper |
| `eat <food>` | Eat food to remove hunger |
| `drink <container>` | Drink to remove thirst |

### Training (at a guild)
| Command | What it does |
|---|---|
| `train` | Train a stat (costs practices) |
| `practice` | Practice a skill or spell |

## 5. Combat approach

Combat is the main way to gain XP and level up.

**Before fighting anything new:**
- Run `consider <target>` — the game tells you how dangerous it is (e.g. "You would need some luck!", "It would be an even fight", "You could kill it with one blow")
- Only fight enemies rated "easy" or "even fight" until you're comfortable

**During combat:**
- The game handles combat rounds automatically once you `kill <target>`
- Read the round-by-round output to track HP
- If HP drops below ~30%, run `flee` immediately
- After combat, `rest` or `sleep` in a safe room to recover

**Good early grinding spots near Midgaard:**
- Rats, mice, and small animals near the city edges
- The Sewers (south from Common Square area) — various vermin
- Check room descriptions for wandering mobs

## 6. Leveling up

After gaining enough XP, you level up automatically. At that point:
- Go to your class guild to `train` new stat points
- Run `score` to confirm the new level and remaining XP needed
- Update player.md with the new level

## 7. Memory file formats

Update these files after each meaningful action. Overwrite the whole file — don't append.

### player.md
```markdown
# Player State
- **Name:** dummy
- **Class/Level:** Fighter, Level 4
- **Location:** [current room name]
- **HP:** 61/61  **Mana:** 100/100  **Move:** 72/93
- **XP:** 8440 (need 7560 more for level 5)
- **Gold:** 60 coins
- **Status:** hungry, thirsty

## Active Goal
[e.g. "Reach level 7" or "Defeat the city guard"]

## Goal Progress
- [x] Step 1 completed
- [ ] Step 2 in progress
- [ ] Step 3 not started

## Inventory
- [list items carried]

## Last Session Summary
[One paragraph: what was done, where we ended up, what to do next]
```

### world.md
```markdown
# World Map

## Known Rooms
- **Temple of Midgaard** — exits: n,e,s,w,d; ATM here
- **Temple Square** — exits: n,e,s,w; Clerics' Guild(w), Grunting Boar Inn(e)
- **Market Square** — center of town; exits: n,e,s,w
- **Main Street (west)** — Armory(s), Bakery(n)
- **Common Square** — exits: n,e,s,w; poor alley(w), dark alley(e)
[add rooms as discovered]

## Known Monsters
- **[name]** — location: [room], difficulty: [consider rating], XP value: [if known]

## Known Shops & Services
- **The Bakery** (Main St W, north) — danish 7c, bread 14c, waybread 72c
- **Grunting Boar Inn** (Temple Square, east) — food/drink available
[add as discovered]

## Known Trainers
- **Fighters Guild** — [location if found]
```

## 8. Navigation tips

- Room descriptions contain directional clues — trust them ("the bakery is to the north")
- When you hit a dead end, backtrack the opposite direction
- Midgaard layout: Temple → Temple Square → Market Square, shops off east/west main streets
- Common Square (south of Market) leads toward the sewers and lower-level hunting areas
- Always check `Exits:` at the bottom of a room description before moving

## 9. Wrap up each session

Before stopping, always:
1. Move to a safe room (the Temple or Inn) and `rest` to full HP
2. Write the current state to player.md and world.md
3. Report to the user: current level, XP progress toward next level, goal status, and recommended next step
