# World State — COLD RUN (no prior MUD knowledge; reactive exploration only)

## Map discovered by exploration (in visit order)
1. **Temple Of Midgaard** (start) — exits n,e,s,w,d; ATM here
2. By The Temple Altar (n) — exits n(→countryside),s; dead-end branch
3. Midgaard Donation Room (Temple e) — exit w only; dead-end
4. Temple Square (Temple s) — exits n,e,s,w; Clerics' Guild(w), Grunting Boar Inn(e)
5. Market Square (Temple Sq s) — exits n,e,s,w; "center of Midgaard"
6. Main Street E (Market e) — general store(n), Pet Shop(s)
7. Main Street E-end (further e) — weapon shop(n), Guild of Swordsmen(s), e=leave town
8. Common Square (Market s) — poor alley(w), dark alley(e), nasty smell(s) [deferred as low shop-density]
9. Main Street W (Market w) — Armory(s), **"the bakery is to the north"** ← live signpost
10. **The Bakery** (Main St W, n) — baker NPC, sign on counter; exit s

## Path that worked (blind): 
Temple → S → Temple Square → S → Market Square → W → Main Street(W) → N → Bakery
(reached after also exploring N, E-alcove, and the entire E main street first)

## The Bakery — Menu (`list`)
| # | Availability | Item            | Cost |
|---|--------------|-----------------|------|
| 1 | Unlimited    | A danish pastry | 7    |
| 2 | Unlimited    | A bread         | 14   |
| 3 | Unlimited    | A waybread      | 72   |

Identical to the earlier (prior-knowledge) run's findings.
