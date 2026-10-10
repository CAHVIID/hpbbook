# Ceiling fans

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## Introduction

A ceiling fan does not lower the air temperature. It raises the air speed around the occupants, which increases their convective and evaporative heat loss ({numref}`fig-fan-airflow`). About 0.5 m/s gives a cooling effect of roughly 2 °C {cite:p}`raftery2020`, so a room at 28 °C with the fan running can feel like 26 °C without it. In the cooling strategy ([](05-cooling-strategy.md)), the fan is the step after reducing gains and venting, and before active cooling.

:::{figure} figures/ch07/ceiling-fan-airflow.png
:label: fig-fan-airflow
:alt: Side view of a room with a ceiling fan blowing a jet of air down to the floor, where it spreads out towards the walls and returns slowly to the ceiling. A seated occupant near the fan is in the moving air.
:width: 90%

A ceiling fan seen from the side. The jet hits the floor, spreads towards the walls and returns slowly along the walls and ceiling. The air temperature is unchanged; the occupant is cooled by the air movement.
:::

Two consequences follow. A fan only helps when someone is in the room. And it removes no heat from the building, so the gains must still be limited and removed by other means.

## Air speed and thermal comfort

### Operative temperature ignores air speed

Thermal comfort depends on metabolic rate, clothing, air temperature, mean radiant temperature, air speed and humidity. The **operative temperature**, the usual design value for overheating, combines only the air and mean radiant temperatures. It is the same with or without a fan, so the effect of a fan needs a comfort model that includes air speed.

### PMV, SET and the cooling effect

The **Predicted Mean Vote (PMV)** {cite:p}`iso7730` predicts the mean thermal sensation from −3 (cold) to +3 (hot). EN 16798-1 {cite:p}`en16798` uses it to define comfort categories:

| Category | PMV range | Typical use |
| --- | --- | --- |
| I | −0.2 to +0.2 | High expectations |
| II | −0.5 to +0.5 | New buildings and renovations |
| III | −0.7 to +0.7 | Moderate expectations |

PMV was fitted to still-air experiments and underestimates the cooling above about 0.2 m/s, mainly because it has no real sweating response. ASHRAE 55 {cite:p}`ashrae55` therefore uses the **Standard Effective Temperature (SET)** from a two-node body model. The **cooling effect** is the drop in air and radiant temperature that gives the same SET in still air as the room has with the fan running. PMV is then calculated at the lowered temperatures. The cooling effect grows quickly at low air speed and levels off at high speed. ASHRAE 55 caps the average air speed at 0.8 m/s unless occupants control the fan.

SET works like the wind chill in a weather forecast: "it is 0 °C, but with the wind it feels like −6 °C." Wind chill is an empirical rule for cold, windy weather. SET does the same job indoors with a model of the body. It converts any combination of air speed, radiation, humidity and clothing into the temperature of a standard still-air room that would put the body in the same state, meaning the same skin temperature and skin wettedness. Skin temperature drives the feeling of warm or cold, and skin wettedness drives the sticky, too-warm discomfort. Two rooms with the same SET therefore feel equally warm, whatever the cause.

### Worked example: the cooling effect of a fan

{numref}`tab-ce-example` follows one seated person (1.2 met, 0.5 clo, 50% RH) through three rooms, calculated with Gagge's two-node model as used in ASHRAE 55 (pythermalcomfort).

:::{table} Two-node model results for one person in three rooms. Heat flows per m² of skin.
:label: tab-ce-example
:align: center

| | Room A | Room B | Room C |
| --- | --- | --- | --- |
| Air and mean radiant temperature | 28 °C | 28 °C | 25.2 °C |
| Air speed | 0.1 m/s | 0.5 m/s (fan) | 0.1 m/s |
| Heat lost from the skin (W/m²) | 64 | 64 | 64 |
| ...by convection and radiation (W/m²) | 32 | 37 | 43 |
| ...by evaporation (W/m²) | 32 | 28 | 21 |
| Skin temperature (°C) | 34.5 | 34.2 | 34.0 |
| Skin wettedness (–) | 0.27 | 0.16 | 0.16 |
| SET (°C) | 27.9 | 24.9 | 24.9 |
:::

The body must lose about 64 W/m² in all three rooms. In the warm, still room A, little heat leaves by convection, so the body sweats and 27% of the skin is wet, which is felt as too warm and sticky. In room B the fan raises convection and evaporation, and the wettedness drops to 16%. Room C is the still-air room that puts the body in the same state as room B. It is found by lowering the air and radiant temperature until the SET matches, which happens at 25.2 °C. The cooling effect of the fan is therefore 28 − 25.2 = 2.8 °C.

You do not need to interpret the SET value itself. It is only the yardstick for "same state" when the two model runs, with and without the fan, are compared. The number used in design is the cooling effect in °C.

:::{tip}
Try it in the CBE Thermal Comfort Tool (<https://comfort.cbe.berkeley.edu>): 26 °C, 50% RH, 1.2 met, 0.5 clo, then raise the air speed from 0.1 to 0.8 m/s.
:::

### The adaptive model

In homes without mechanical cooling, occupants adapt by opening windows and changing clothes, and accept higher temperatures than PMV predicts. The adaptive model in EN 16798-1 links the comfort temperature to the running mean outdoor temperature $\theta_{rm}$:

```{math}
:label: eq-adaptive
\theta_{c} = 0.33\,\theta_{rm} + 18.8
```

The category II upper limit is $\theta_c + 3$ °C. With elevated air speed, the limit may be raised by about 1.2 °C at 0.6 m/s up to about 2.2 °C at 1.2 m/s. Use PMV with SET to quantify a specific air speed, and the adaptive model for overheating assessment of free-running homes.

### Draught

The ISO 7730 draught rate {cite:p}`iso7730` predicts the percentage dissatisfied with draught:

```{math}
:label: eq-draught
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37\,v\,T_u + 3.14)
```

with $t_a$ the air temperature (°C), $v$ the mean air speed (m/s) and $T_u$ the turbulence intensity (%). It was developed for 20 to 26 °C and below 0.5 m/s, and does not apply to a warm person who has turned on a fan. It matters when the fan runs in a cool room, for example after night cooling, which is why the fan needs temperature control and a low minimum speed.

## Airflow from a ceiling fan

The fan produces an **impinging jet** ({numref}`fig-fan-airflow`). Below the blades the jet narrows and travels down at often more than 1 m/s. At the floor it stops at a stagnation point under the fan centre and turns sideways. It then spreads radially along the floor, slows down, rises along the walls and returns along the ceiling. The cooling is therefore largest under the fan and fades with distance.

In a 5.5 m × 5.5 m room with a 1.5 m fan, the effect at seated body height has almost gone one fan diameter (1.5 m) from the fan centre {cite:p}`raftery2020`.

Larger fans give a deeper spreading zone and a more uniform air speed in the room. Uniformity matters where people sit in fixed places, such as offices and classrooms, and matters little in a bedroom with one occupant in control. Furniture and kitchen cabinets block the spreading flow and leave sheltered zones.

Fan airflow is turbulent and fluctuates as the blades pass. The comfort models in this chapter use only the mean air speed, averaged over time and over ankle, waist and head height (0.1, 0.6 and 1.1 m for a seated person), and ignore the fluctuations. Laboratory studies suggest that fluctuating air feels cooler than steady air at the same mean speed, so using the mean is likely on the safe side.

## Fan performance

A datasheet gives the diameter, the speeds, the airflow (usually only at maximum speed) and the electric power. US datasheets give airflow in CFM (1 CFM = 1.699 m³/h), and many EU datasheets in m³/min.

For a given fan, airflow $Q$, power $P$ and rotational speed $n$ follow the fan laws:

```{math}
:label: eq-fan-laws
\frac{Q_2}{Q_1} = \frac{n_2}{n_1}, \qquad \frac{P_2}{P_1} = \left(\frac{n_2}{n_1}\right)^3
```

Small motors have losses that do not follow the cube law, so the real power at low speed is higher than predicted, especially for AC motors. The **efficacy** is the airflow per watt:

```{math}
:label: eq-efficacy
\eta_{fan} = \frac{Q}{P}
```

It falls as speed increases. The Fanco Breeze AC 132 moves 375 m³/h per W at low speed and 201 m³/h per W at high speed ({numref}`tab-fan-data`).

:::{table} Ceiling fan data at the highest speed, from manufacturer datasheets. Airflow in CFM has been converted to m³/h.
:label: tab-fan-data
:align: center

| Fan | Motor | Diameter (m) | Airflow at max (m³/h) | Power at max (W) | Efficacy at max (m³/h per W) | Power at min (W) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Westinghouse Contractor's Choice 7303800 | AC | 1.32 | 7,260 | 65 | 112 | – | Datasheet in lecture 17.1 |
| Minka Aire Light Wave F844 | AC | 1.32 | 7,720 | 67.5 | 114 | – | [Modern Fan Outlet](https://www.modernfanoutlet.com/minkaaire-wave-f844-sl.html) |
| Fanco Breeze AC 132 | AC | 1.32 | 9,030 | 45 | 201 | 15 | [Universal Fans](https://universalfans.com.au/online/fanco-breeze-ac-ceiling-fan-with-wall-control-black-52/) |
| Fanco Breeze AC 122 | AC | 1.22 | 9,940 | 44 | 226 | 16.5 | Lecture 17.1, worked example |
| Hunter Erling 52850 | DC | 1.32 | 8,680 | 23.6 | 368 | 1.7 | [Hunter](https://www.hunterfan.com/products/ceiling-fans-erling-energy-star-with-led-light-52-inch-1001569), [ENERGY STAR](https://www.energystar.gov/productfinder/product/certified-ceiling-fans/details/3530991) |
| CasaFan Eco Genuino 122 | DC | 1.22 | 6,630 | 11.3 | 587 | 3.2 | [CasaFan](https://www.casafan.de/deckenventilator-eco-genuino/x312223) |
| CasaFan Eco Genuino 152 | DC | 1.52 | 9,220 | 16.6 | 555 | 3.3 | [ventilator.de](https://www.ventilator.de/deckenventilatoren/casafan/eco-genuino/eco-genuino-152/315229-eco-genuino-152-mw-ms) |
:::

DC fans move two to five times more air per watt than AC fans of the same diameter, and draw only 2 to 3 W at minimum speed against about 15 W. Datasheet values come from different test methods (DOE in the US, IEC 60879 in the EU), so check the manufacturer's own datasheet before using a number.

## Cooling effect and cooling fan efficiency

### Cooling fan efficiency

The datasheet airflow says nothing about the air speed at the occupant. ASHRAE Standard 216 therefore rates fans by the **cooling fan efficiency (CFE)**:

```{math}
:label: eq-cfe
CFE = \frac{\text{cooling effect}}{\text{fan power}} = -\frac{\Delta t_{eq}}{P_f}
```

where $\Delta t_{eq}$ is the whole-body cooling effect (°C, negative) and $P_f$ the fan power (W).

### Cooling effect versus distance

{numref}`fig-ce-distance` shows the cooling effect for a seated occupant from measured air speeds under a 1.5 m fan {cite:p}`raftery2019`, calculated with the SET method at 28 °C, 50% RH, 1.2 met and 0.5 clo.

:::{figure} figures/ch07/cooling-effect-distance.png
:label: fig-ce-distance
:alt: Line chart of cooling effect against horizontal distance from the fan centre for maximum and half fan speed. At maximum speed the cooling effect is about 4.5 °C within 0.6 m of the centre, falls to about 3.5 °C at 1.5 m and 2.7 °C at 6 m. At half speed the values are about 3.6, 2.3 and 1.3 °C.
:width: 90%

Cooling effect for a seated occupant versus horizontal distance from the centre of a 1.5 m ceiling fan. Air speeds from {cite:t}`raftery2019`; cooling effect with the SET method at 28 °C, 50% RH, 1.2 met and 0.5 clo.
:::

The effect is largest within about 0.4 D of the centre, drops sharply at the edge of the jet (0.5 D to 1 D) and then falls slowly. Halving the fan speed costs only about 1 °C under the fan but cuts the power far more, so medium speed is often the most efficient. Place the fan within one diameter of where people sit, for example over the bed.

### Predicting the air speed in a room

{cite:t}`raftery2019` fitted regression models to full-scale tests. With fan diameter $D$, room width $R$ and ceiling height $C$ (all in m), the fan air speed from the rated airflow $Q$ (m³/s) is

```{math}
:label: eq-sf
S_F = \frac{4\,Q}{\pi D^2}
```

and the room-average air speed for seated occupants is

```{math}
:label: eq-so-avg
S_{O,avg} = S_F \left(0.25 + 0.99\,\frac{D}{R} - 0.06\,\frac{C}{D} + 0.11\,\frac{D}{1.7} + 0.024\right)
```

valid for downward flow with at least 0.2 D between blades and ceiling. In a typical residential room the bracket is about 0.5. {numref}`tab-cfe` applies the model to a 4.5 m × 4.5 m living room with a 2.7 m ceiling and the blades at 2.4 m.

:::{table} Estimated room-average air speed, cooling effect and CFE at maximum speed for a seated occupant in a 4.5 m × 4.5 m room (C = 2.7 m, H = 2.4 m). Cooling effect at 28 °C, 50% RH, 1.2 met, 0.5 clo.
:label: tab-cfe
:align: center

| Fan | Motor | $S_F$ (m/s) | $S_{O,avg}$ (m/s) | Cooling effect (°C) | Power (W) | CFE (°C per W) |
| --- | --- | --- | --- | --- | --- | --- |
| Westinghouse Contractor's Choice | AC | 1.47 | 0.78 | 3.5 | 65 | 0.05 |
| Minka Aire Light Wave | AC | 1.57 | 0.83 | 3.6 | 67.5 | 0.05 |
| Fanco Breeze AC 132 | AC | 1.83 | 0.97 | 3.9 | 45 | 0.09 |
| Hunter Erling 52850 | DC | 1.76 | 0.93 | 3.8 | 23.6 | 0.16 |
| CasaFan Eco Genuino 152 | DC | 1.41 | 0.85 | 3.7 | 16.6 | 0.22 |
| CasaFan Eco Genuino 122 | DC | 1.58 | 0.77 | 3.5 | 11.3 | 0.31 |
:::

All six fans give 3.5 to 3.9 °C, but their CFE differs by a factor of six. Because the cooling effect levels off, extra airflow buys little cooling, so choose a fan by its power at the speed you need, not by its maximum airflow.
