# Bakery in Midgaard - Results

## The Bakery Menu

| # | Item | Price (coins) |
|---|------|--------------|
| 1 | A danish pastry | 7 |
| 2 | A bread | 14 |
| 3 | A waybread | 72 |

All items are available in unlimited quantity.

Raw output from `list` command:
```
 ##   Available   Item                                               Cost
----------------------------------------------------------------------------
  1)  Unlimited   A danish pastry                                       7
  2)  Unlimited   A bread                                              14
  3)  Unlimited   A waybread                                           72
```

## Route to the Bakery

Starting location: By The Temple Altar (north end of Temple of Midgaard)

| Step | Direction | Room Arrived At |
|------|-----------|----------------|
| 1 | s (south) | The Temple Of Midgaard |
| 2 | s (south) | The Temple Square |
| 3 | s (south) | Market Square |
| 4 | w (west) | Main Street ("the bakery is to the north") |
| 5 | n (north) | **The Bakery** |

Total steps: 5 moves (s, s, s, w, n)

### Bakery Room Description
> You are standing inside the small bakery. A sweet scent of danish and fine bread fills the room. The bread and Danish are arranged in fine order on the shelves, and seem to be of the finest quality. A small sign is on the counter.
>
> Exits: s

The baker NPC is present, as is an oozing green gelatinous blob.

## Connection Calls

Total nc/socket connection attempts: **6**

| Call # | Method | Outcome |
|--------|--------|---------|
| 1 | nc | Connected, got banner and login prompt |
| 2 | nc | Login timing issues, "y" sent prematurely caused confusion |
| 3 | nc | "dummy" recognized as valid character; "Multiple login detected" due to active prior session |
| 4 | nc | Permission denied (tool rejection) |
| 5 | Python socket (mud_client.py) | Logged in, navigated but only went north from temple altar (wrong direction) |
| 6 | Python socket (mud_client2.py) | Full successful navigation: temple -> square -> market -> main street -> **bakery**; retrieved menu via `list` |
