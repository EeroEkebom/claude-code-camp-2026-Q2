# Bakery Menu — Midgaard, tbaMUD

## Full Menu

The Bakery is located on Main Street, Midgaard. The baker sells the following items (all quantities unlimited):

| # | Item              | Price (gold coins) |
|---|-------------------|--------------------|
| 1 | A danish pastry   | 7                  |
| 2 | A bread           | 14                 |
| 3 | A waybread        | 72                 |

## Route from Temple to Bakery

Starting point: The Temple Of Midgaard (default spawn point)

1. `s` — Temple → Temple Square
2. `s` — Temple Square → Market Square
3. `w` — Market Square → Main Street
   - Room description confirms: "the bakery is to the north"
4. `n` — Main Street → The Bakery

Total: 4 moves.

### Key Landmarks Along the Route

- **The Temple Of Midgaard** — spawn point; marble hall with ATM
- **Temple Square** — marble fountain, Clerics' Guild (west), Grunting Boar Inn (east)
- **Market Square** — central square with a peculiar statue; roads in all directions
- **Main Street** — bakery to the north, Armory to the south, Market Square to the east
- **The Bakery** — sweet scent of danish and fine bread; only exit is south back to Main Street

## Script Calls

Total script calls to `mud_cmd.sh`: **9**

| Call | Commands Sent          | Outcome                                                       |
|------|------------------------|---------------------------------------------------------------|
| 1    | `look`                 | Failed — multiple login detected (lingering nc process)       |
| 2    | `look` (after 5s wait) | Failed — multiple login detected again                        |
| 3    | (killed pids) `look`   | Success — character already in The Bakery; room description obtained |
| 4    | `list`                 | Obtained full menu: 3 items with prices                       |
| 5    | `go south` + `look`    | Timing issue; ended up showing bakery again                   |
| 6    | `s`                    | Moved south to Main Street; confirmed "bakery is to the north"|
| 7    | `e`                    | Moved east to Market Square                                   |
| 8    | `n`                    | Moved north to Temple Square                                  |
| 9    | `n`                    | Moved north to The Temple Of Midgaard (starting point)        |

Note: Calls 1–2 failed due to lingering nc connections from previous sessions; calls 6–9 were used to trace the route back from the bakery to the Temple in order to document the path.
