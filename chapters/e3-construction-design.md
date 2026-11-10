# Construction design

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

The box buildings in [Box building systems for type houses](e1-box-buildings.md) are light timber structures. This chapter shows, approximately, how joist size and holes for ducts affect the deflection of floors and roofs, and the principle of wind stability. The estimates are meant for early design, to check that the dimensions in a floor plan or section are realistic. They do not replace the structural design, which includes loads, safety factors, strength, vibration and fire and is done by a structural engineer.

## E3.1 Joist height, load and centre distance

Floor and roof joists in a box span across the box, from one long wall to the other, about 4 m. Each joist carries the load on a strip of floor as wide as the centre distance (c/c), usually 0.6 m. In light timber floors the deflection, not the strength, usually decides the joist height. {numref}`fig-joist-height` shows how the deflection of a solid joist depends on its height, the load and the centre distance; a common limit for floors is 1/400 of the span.

:::{figure} figures/e3/joist-height.*
:label: fig-joist-height
:alt: Midspan deflection of a solid 45 mm wide joist over a 4 m span against joist height from 150 to 350 mm, with the limit L/400 = 10 mm as a dotted line. (a) Loads of 1.0, 2.0 and 3.0 kN per square metre at c/c 0.6 m: the curves cross 10 mm at about 172, 217 and 248 mm height. (b) Centre distances of 0.3, 0.45 and 0.6 m at 2.0 kN per square metre: the curves cross 10 mm at about 172, 197 and 217 mm.
:width: 100%

Deflection of a solid joist (45 mm wide, span 4.0 m) as a function of joist height, (a) for different loads and (b) for different centre distances. Floor in a dwelling: about 2.0 kN/m² (self-weight plus people and furniture). Approximate hand calculation, $E$ = 11 000 MPa. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/e3_construction_figures.py)
:::

## E3.2 Solid joists and I-joists

An I-joist has two flanges of solid timber or LVL joined by a thin web of OSB or hardboard. The flanges sit at the top and bottom, where timber contributes most to the stiffness, and the web carries the shear force. At the same height a solid joist is somewhat stiffer, but the I-joist uses about half the timber ({numref}`fig-joist-deflection`). For the same stiffness an I-joist is made a little higher.

:::{figure} figures/e3/joist-deflection.*
:label: fig-joist-deflection
:alt: (a) Cross-sections drawn to scale with area A and second moment of area I, in pairs of equal height: solid 45 by 220 mm, A 9.9 thousand square millimetres, I 40 million mm to the fourth; I-joist 220, A 5.3, I 34; solid 45 by 300, A 13.5, I 101; I-joist 300, A 6.2, I 74. The I-joists have 45 by 45 mm flanges and a 10 mm web. (b) Midspan deflection against span from 2 to 6 m for the four sections at 2.0 kN per square metre and c/c 0.6 m, including shear deformation, with the limits L/300 and L/400 as dotted lines. At 4 m: I-joist 220 about 13 mm, 45 by 220 about 10 mm, I-joist 300 about 6 mm, 45 by 300 about 4 mm.
:width: 100%

Solid joists and I-joists of equal height: sections and midspan deflection. I-joists with 45 × 45 mm flanges and a 10 mm OSB web; $E$ = 11 000 MPa. Approximate hand calculation. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/e3_construction_figures.py)
:::

## E3.3 Joists across or along the box

The joists of a box can span across the box, between the long walls, or along it, between the gables. In a box of 4 × 12 m the span is about 4 m or about 12 m ({numref}`fig-joist-direction`). The direction also decides which walls carry the floor and the roof.

:::{figure} figures/e3/joist-direction.*
:label: fig-joist-direction
:alt: (a) Plan of a 4 by 12 m box with joists at c/c 0.6 m across the box, carried by the long walls, span about 4 m. (b) The same box with joists along the box, carried by the gables, span about 12 m. (c) Midspan deflection on a logarithmic axis against span from 2 to 13 m for a solid 45 by 295 joist and an I-joist 45 by 295 at 2.0 kN per square metre and c/c 0.6 m, with the limit L/400 dotted and vertical lines at 4 m (short way) and 12 m (long way). At 4 m: about 4 and 6 mm. At 12 m: about 310 and 420 mm, against a limit of 30 mm.
:width: 100%

Joists across or along a 4 × 12 m box, and midspan deflection of a 295 mm high joist against span. Note the logarithmic deflection axis. Approximate hand calculation. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/e3_construction_figures.py)
:::

## E3.4 Ducts through I-joists

A duct crossing the joists needs a hole in each joist. Near midspan the hole reduces the bending stiffness of the joist; near the supports the timber above and below the hole bends locally like two short beams ({numref}`fig-ijoist-hole`).

:::{figure} figures/e3/ijoist-hole.*
:label: fig-ijoist-hole
:alt: (a) Elevation of a joist, 295 mm high, simply supported on two supports with a 4.0 m span, a uniform load of 2.0 kN per square metre times c/c 0.6 m, and a round 160 mm hole at distance x from the left support. (b) Solid joist 45 by 295: midspan deflection 4.09 mm without a hole; with the hole it rises from 4.10 mm near the support to 4.13 mm at midspan. (c) I-joist 45 by 295: 6.28 mm without a hole and about 6.29 to 6.30 mm with the hole, almost independent of position. Both y-axes span 0.08 mm.
:width: 100%

Midspan deflection of a solid joist and an I-joist of the same height with a round Ø160 hole for a duct, as a function of the hole position. Note the expanded y-axes. Approximate model: bending and shear of the joist plus local bending of the timber above and below the hole. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/e3_construction_figures.py)
:::

The size and position of holes are also limited by the strength of the joist. I-joist producers publish the allowed size and position of web holes for each product, see for example [STEICO site guidance for follow-on trades](https://www.steico.com/fileadmin/user_upload/English_Media/Content/PDF_Not_PIM_EN/Technical_Documents/Installation_manuals/STEICO_Site_Guidance-For-Follow-On-Trades_EN_i.pdf).

## E3.5 Wind stability

Wind on the facades is carried to the foundation by the floor and roof, which act as horizontal diaphragms, and by the walls in the direction of the load, which act as shear walls. In a timber box the shear walls are the stud walls with gypsum boards. The boards, screwed to the studs along all edges, keep the frame from racking ({numref}`fig-wall-racking`). The racking resistance of a wall depends on the board type, the number of board layers and the screw spacing, and it is proportional to the length of closed wall.

Windows and doors interrupt the boards, and narrow wall pieces between openings add little stiffness. Each long side of a box therefore needs a certain length of closed wall. The walls must also be balanced: if one long side is opened completely, the remaining wall is eccentric to the wind load and the box twists ({numref}`fig-wind-torsion`). Where two boxes are joined into a larger room, only a minor part of the long walls should be removed.

:::{figure} figures/e3/wall-racking.*
:label: fig-wall-racking
:alt: (a) A stud frame without boards under a horizontal wind force at the top racks into a parallelogram. (b) The same frame with gypsum boards screwed to the studs stays rectangular; the board acts as a shear panel, with tension at the windward bottom corner and compression at the leeward corner.
:width: 90%

Gypsum boards as bracing of a stud wall. Schematic.
:::

:::{figure} figures/e3/wind-torsion.*
:label: fig-wind-torsion
:alt: Three plans of a 12 by 4 m box with wind on the left gable. (a) Both long walls closed: each long wall takes half the wind force, no twist. (b) One long side removed: the remaining long wall takes the whole force F, offset from the load, which twists the box; a dashed outline shows the box twisted. (c) A 5 m opening in one long side: the closed wall takes more than half, the opened wall less than half, and the twist is small.
:width: 75%

Wind along a box resisted by the long walls. Schematic.
:::

:::{admonition} Take aways
:class: tip

1. **Light timber joists are sized by deflection.** The deflection falls steeply with joist height and grows with load and centre distance; a 4 m box floor at c/c 0.6 m needs about 45 × 220 mm solid timber or a 300 mm I-joist.
2. **Ducts cross the joists through holes in the web of I-joists.** The allowed hole size and position are given by the producer.
3. **Each long side of a box needs a length of closed wall with boards** to carry the wind; opening one long side completely makes the box twist.
:::
