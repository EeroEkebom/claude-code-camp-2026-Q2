# World State — Midgaard, tbaMUD

## Known Rooms

### The Reception (login lobby)
- Description: Standing in the reception; staircase leads down to the entrance hall. Exit north to the Cryogenic Center. Small sign on counter, ATM in the wall, a Peacekeeper and a receptionist NPC present.
- Exits: n, d
- d → Entrance Hall Of The Grunting Boar Inn
- IMPORTANT: On reconnect, the game places the character HERE, not at the last
  in-world room recorded in memory. Always `look` after connecting to verify
  actual location before assuming memory's "Current Location" still holds.

### The Entrance Hall Of The Grunting Boar Inn
- Description: Entrance hall of the Grunting Boar Inn, simple furniture. Post Office to the north, bar to the east, staircase up to the Reception, Temple Square to the west.
- Exits: n, e, w, u
- u → The Reception
- w → Temple Square

### The Temple Of Midgaard
- Description: Southern end of the temple hall. Marble blocks, ancient wall paintings. ATM in the wall. Reading Room to the west, donation room alcove to the east.
- Exits: n, e, s, w, d
- s → Temple Square

### Temple Square
- Description: Huge marble steps lead to temple gate. Clerics' Guild to the west, Grunting Boar Inn to the east, Market Square to the south.
- Exits: n, e, s, w
- n → Temple of Midgaard
- s → Market Square
- e → Entrance Hall Of The Grunting Boar Inn
- Blue marble fountain here

### Market Square
- Description: Famous Square of Midgaard. Peculiar statue in the middle. North to temple square, south to common square, east/west is the main street.
- Exits: n, e, s, w
- n → Temple Square
- w → Main Street (West)
- e → Main Street (Central)

### Main Street (West)
- Description: Main street of Midgaard. Armory entrance to the south, bakery to the north, Market Square to the east.
- Exits: n, e, s, w
- n → The Bakery
- e → Market Square

### Main Street (Central)
- Description: Main street crossing through town. General store to the north, main street continues east, market place to the west, Pet Shop through a small door to the south.
- Exits: n, e, s, w
- w → Market Square
- e → Main Street (East)

### Main Street (East)
- Description: Weapon shop to the north, Guild of Swordsmen to the south. East leaves town. West leads to Market Square (via Main Street (Central)).
- Exits: n, e, s, w
- w → Main Street (Central)
- s → The Entrance Hall To The Guild Of Swordsmen

### The Entrance Hall To The Guild Of Swordsmen
- Description: Fighters' guild entrance. Bar to the east, main street to the north. ATM in the wall. A knight guards the entrance.
- Exits: n, e
- n → Main Street (East)
- FIGHTERS GUILD — this is dummy's (Fighter class) training guild.

### The Bakery
- Description: Small bakery with a sweet scent of danish and fine bread. Bread and Danish arranged on shelves. Small sign on the counter. Baker NPC here.
- Exits: s
- s → Main Street
- SHOP: sells food items (see menu below)
- Confirmed again via Temple → Temple Square → Market Square → Main Street (West) → Bakery route; every room description/exit matched this file exactly, no corrections needed.

## General Tips
- If the character was `rest`ing/sitting at the end of a prior session, movement commands will fail ("Nah... You feel too relaxed to do that.."). Issue `stand` first before trying to move.
- HP/move regen resumes normally once standing, even while thirsty — thirst does not appear to block regen by itself (contradicts a hypothesis from an earlier session).
- Thirsty status persists across sessions and requires gold or a free water source to fix; the Temple Square fountain has not yet been tested as a drinkable source.

## Known Shops

### The Bakery — Menu
| # | Item            | Price (gold) | Quantity  |
|---|-----------------|--------------|-----------|
| 1 | A danish pastry | 7            | Unlimited |
| 2 | A bread         | 14           | Unlimited |
| 3 | A waybread      | 72           | Unlimited |
