# Ceiling fans

:::{danger} Obsolete
This is the old version of the ceiling fans chapter. It is kept for reference and may be removed. See the new chapters on cooling strategy and ceiling fans.
:::

## Introduction

Summers are also getting warmer, and heat waves are getting longer and more intense. The easy answer to overheating is air-conditioning, but it adds investment, electricity use, refrigerants and maintenance to buildings that previously needed none. This chapter looks at a cheaper and much more energy-efficient alternative: the ceiling fan.

### Fans cool people, not rooms

A ceiling fan does not lower the air temperature. Its motor even adds a little heat to the room. What it does is raise the air speed around the occupants ({numref}`fig-fan-airflow-old`). Higher air speed increases the heat loss from the skin by convection and evaporation, so people feel cooler at the same temperature. A design air speed of about 0.5 m/s gives a cooling effect of roughly 2 °C {cite:p}`raftery2020`. In other words, a room at 28 °C with a fan running can feel like 26 °C without one.

:::{figure} figures/ch07/ceiling-fan-airflow.png
:label: fig-fan-airflow-old
:alt: Side view of a room with a ceiling fan blowing a jet of air down to the floor, where it spreads out towards the walls and returns slowly to the ceiling. A seated occupant near the fan is in the moving air.
:width: 90%

A ceiling fan seen from the side. The fan blows a jet of air down to the floor, where it spreads towards the walls and returns slowly along the walls and ceiling. The air temperature is unchanged; the occupant is cooled by the air movement.
:::

Two consequences follow:

- A fan only helps when someone is in the room. A fan running in an empty room wastes energy.
- A fan cannot remove heat from the building. Heat must still be kept out or removed by other means, otherwise the temperature keeps rising until the fan is no longer enough.

### Where fans fit in the cooling strategy

Ceiling fans are one step in a cooling hierarchy, where each step is cheaper and simpler than the next:

1. **Reduce the heat gains**: shading, solar-control glazing and sensible window areas (chapter 1).
2. **Remove heat passively**: ventilative cooling with opening windows and night cooling of the thermal mass (chapter 5).
3. **Raise the air speed**: ceiling fans let occupants accept a higher temperature (this chapter).
4. **Cool actively**: mechanical cooling, only for what is left.

Used this way, the fan becomes the first cooling stage that runs before any active cooling starts. It can push the temperature at which air-conditioning is needed up by a couple of degrees, or remove the need for it altogether. The energy saved typically exceeds the fan's own energy use by a factor of 10 to 100 {cite:p}`raftery2020`.

The chapter first explains how air speed affects thermal comfort and how a ceiling fan moves air. It then covers fan performance, sizing and placement, control, and energy use compared with air-conditioning. It ends by showing how to model fans when the simulation tool does not support elevated air speed, with a worked example from the course row house.

## Air speed and thermal comfort

### How the body loses heat

The body must reject the heat it produces to stay at a stable core temperature. It does so in four ways, listed in order of decreasing size under normal indoor conditions {cite:p}`raftery2020`:

- **Radiation** to the surrounding surfaces.
- **Convection** to the surrounding air. In still air, convection is driven only by the small buoyant flow around the warm body, so a layer of still air acts almost like insulation. Moving air breaks up this layer and increases the convective heat loss.
- **Evaporation** of sweat from the skin. The rate depends on the humidity of the air and increases with air speed.
- **Conduction** to surfaces we touch, which is usually small.

A ceiling fan increases two of these mechanisms, convection and evaporation. That is why moving air feels cooler, even though its temperature is unchanged.

### Six factors of thermal comfort

Thermal comfort depends on six factors: metabolic rate, clothing insulation, air temperature, mean radiant temperature, air speed and humidity. The first two describe the person and the last four describe the room.

The **operative temperature** combines the air temperature and the mean radiant temperature into one number. It is the usual design value, and BR18 overheating hours are counted on it. It does not include air speed, however, so the operative temperature in a room is the same with or without a fan. To capture the effect of a fan, we need a comfort model that includes air speed.

### PMV and elevated air speed

The **Predicted Mean Vote (PMV)** {cite:p}`iso7730` predicts the average thermal sensation of a large group of people on a scale from −3 (cold) through 0 (neutral) to +3 (hot). It takes all six factors as input. EN 16798-1 {cite:p}`en16798` uses PMV ranges to define comfort categories:

| Category | PMV range | Typical use |
| --- | --- | --- |
| I | −0.2 to +0.2 | High expectations, sensitive occupants |
| II | −0.5 to +0.5 | Normal expectations, new buildings and renovations |
| III | −0.7 to +0.7 | Moderate expectations |

The original PMV model was developed for still air and underestimates the cooling effect of air speeds above about 0.2 m/s. ASHRAE 55 {cite:p}`ashrae55` therefore uses the **Standard Effective Temperature (SET)** for elevated air speed. SET translates all six factors into a single equivalent temperature. The **cooling effect** of a fan is the drop in air and radiant temperature that gives the same SET in still air as the room has with the fan running. In other words, it is how many degrees warmer the room can be with the fan, for the same comfort.

The cooling effect grows quickly at low air speeds and levels off at higher speeds. A design air speed of 0.5 m/s gives roughly 2 °C cooling effect for a typical office worker {cite:p}`raftery2020`. That is about half the relative air speed a person feels just by walking slowly through still air.

ASHRAE 55 caps the average air speed at 0.8 m/s when occupants cannot control the fan themselves. With occupant control, higher speeds are allowed, because people turn the fan down when it gets too much.

:::{tip}
Explore the effect of air speed yourself in the CBE Thermal Comfort Tool: <https://comfort.cbe.berkeley.edu>. Start at 26 °C, 50% relative humidity, 1.2 met and 0.5 clo, then raise the air speed from 0.1 to 0.8 m/s and watch the PMV and the comfort zone move.
:::

### The adaptive comfort model

PMV was developed from climate chamber experiments with people in steady conditions, and it suits mechanically conditioned buildings. In naturally ventilated buildings and homes, people adapt. They change clothing, open windows and get used to the season. They therefore accept higher temperatures in summer than PMV predicts.

The **adaptive model** in EN 16798-1 links the comfortable operative temperature to the running mean outdoor temperature, $\theta_{rm}$:

```{math}
:label: eq-adaptive-old
\theta_{c} = 0.33\,\theta_{rm} + 18.8
```

For category II, the upper limit is $\theta_c + 3$ °C. The adaptive model applies to buildings without mechanical cooling, where occupants have access to operable windows and can adapt their clothing. This makes it more suitable for residences than PMV.

EN 16798-1 also allows the upper limit to be raised when occupants can increase the air speed, for example with a ceiling fan. The allowed increase grows with air speed, from about 1.2 °C at 0.6 m/s to about 2.2 °C at 1.2 m/s.

:::{admonition} Which model should I use?
:class: note

- **PMV with SET** when you know the clothing and activity and want to quantify the effect of a specific air speed. This is what the course PMV script does.
- **Adaptive model** for overheating assessment in naturally ventilated homes, with the air speed allowance when fans are installed.

Both are available in the CBE Thermal Comfort Tool.
:::

### Draught or welcome breeze?

The same air movement that cools on a warm day is felt as draught on a cool day. ISO 7730 {cite:p}`iso7730` predicts the percentage of people dissatisfied due to draught, the **draught rate**:

```{math}
:label: eq-draught-old
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37\,v\,T_u + 3.14)
```

where $t_a$ is the local air temperature (°C), $v$ the mean air speed (m/s) and $T_u$ the turbulence intensity (%). The model was developed for cool and neutral conditions, with air temperatures of 20 to 26 °C and air speeds below 0.5 m/s. It does not apply to a warm person who has chosen to turn on a fan. In warm conditions, people generally welcome air movement, as long as they can control it.

Draught does matter when the fan runs while the room is cool, for example in the morning after night cooling. This is why the fan should be controlled by temperature and occupant choice, and why a low minimum speed is important (see the Control and integration section).

## Airflow from a ceiling fan

### The fan jet

A ceiling fan draws air from above and pushes it down as a jet. The flow is an example of an **impinging jet** and has three parts ({numref}`fig-fan-airflow-old`):

1. **The fan jet.** Just below the blades, the jet narrows to a diameter slightly smaller than the fan itself. It then travels down towards the floor with high air speed, often above 1 m/s directly below the fan.
2. **The impingement zone.** When the jet hits the floor, it stops at a **stagnation point** under the fan centre and turns sideways. Air speeds right at the stagnation point are low.
3. **The spreading zone.** The air then spreads out radially along the floor towards the walls, slowing down as it spreads. It rises along the walls and returns slowly towards the fan along the ceiling.

Outside the jet and the spreading zone, the air in the room moves much more slowly. The highest air speeds, and therefore the largest cooling effect, are felt directly under the fan, and the effect fades with distance from it.

Measurements in a 5.5 m × 5.5 m room with a 1.5 m diameter fan illustrate this {cite:p}`raftery2020`. One fan diameter from the centre, the air speed is still high close to the floor, but at 0.5 to 0.7 m height (where a seated person's body is), the fan has almost no effect. The measured velocity field is shown in Gao et al. (2017), <https://doi.org/10.1016/j.buildenv.2017.08.029>.

### Fan size and uniformity

The depth of the spreading zone depends on the fan diameter:

- **Small fans** have a thin spreading zone close to the floor. People sitting directly under the fan feel strong air movement, and people further away feel very little.
- **Large fans** have a deeper spreading zone. For fans of 3 m diameter or more, the spreading zone one fan diameter from the centre is about as high as a standing person. Large fans have lower air speeds directly under the centre, however.

The larger the fan diameter is relative to the room, the more uniform the air speed in the room becomes {cite:p}`raftery2020`.

### Uniform or varied air speeds?

Whether uniform air speeds are desirable depends on how the room is used:

- **Variation is useful** where people can move around, such as a living room, lobby or sports hall. People choose a spot that suits them. A fan can also target a local hot spot, for example near a sunny window or in front of the stove in a kitchen.
- **Uniformity is important** where people sit in fixed places for long periods, such as a shared office or classroom. There is no guarantee that the person who feels warmest sits in the strongest air movement, so use larger fans, more fans or individual control.
- **Neither matters much** in a room with one occupant who controls the fan, such as a bedroom or private office.

### Obstructions and turbulence

Furniture, partitions and kitchen cabinets block the spreading flow along the floor and create sheltered zones with little air movement. Fan positions should take permanent obstructions into account.

The airflow from a ceiling fan is also more turbulent and fluctuating than the air from a ventilation diffuser. Turbulence intensities from ceiling fans are high, and the speed felt by an occupant fluctuates as the blades pass. To measure it, use an omnidirectional, low-speed anemometer with a fast response, and average the speed over at least a few minutes at the heights of the ankles, the seated body and the head (0.1, 0.6 and 1.1 m for seated occupants).

## Fan performance

### What a datasheet tells you

A ceiling fan datasheet usually gives the blade diameter, the number of speeds, the rotational speed (rpm), the airflow and the electric power. The airflow is normally stated only at the highest speed, while the power is sometimes given for every speed. Watch the units:

- US datasheets give airflow in CFM (cubic feet per minute). 1 CFM = 1.699 m³/h = 0.472 L/s.
- European datasheets often give airflow in m³/min. 1 m³/min = 60 m³/h.
- US "Energy use" on the label is a weighted average over the speeds, not the power at high speed.

### Fan laws

For a given fan, the airflow $Q$, the power $P$ and the rotational speed $n$ are linked by the fan laws:

```{math}
:label: eq-fan-laws-old
\frac{Q_2}{Q_1} = \frac{n_2}{n_1}, \qquad \frac{P_2}{P_1} = \left(\frac{n_2}{n_1}\right)^3
```

Halving the speed halves the airflow but cuts the power to one eighth. In practice, small motors have losses that do not follow the cube law, so the power at low speed is higher than the fan laws predict, especially for AC motors.

The **efficacy** of a fan is its airflow per watt, here in m³/h per W:

```{math}
:label: eq-efficacy-old
\eta_{fan} = \frac{Q}{P}
```

Because power grows faster than airflow, efficacy falls as speed increases. The Fanco Breeze AC 132 in {numref}`tab-fan-data-old`, for example, moves 375 m³/h per W at low speed, but only 201 m³/h per W at high speed.

### Data from manufacturers

{numref}`tab-fan-data-old` compares fans from several manufacturers at their highest speed, which is the nominal operating point most datasheets report.

:::{table} Ceiling fan data at the highest speed, from manufacturer datasheets. Airflow in CFM has been converted to m³/h.
:label: tab-fan-data-old
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

Three things stand out:

- **DC motors are far more efficient.** At the same diameter, the DC fans move about two to five times more air per watt than the AC fans.
- **AC fans vary a lot.** Two 1.32 m AC fans with similar airflow differ by a factor of almost two in efficacy.
- **DC fans run much lower at minimum speed.** They draw 2 to 3 W at minimum speed, against about 15 W for AC fans. They also usually have five or six speeds instead of three. A low minimum speed is important for comfort in mild weather (see the Control and integration section).

:::{warning}
Treat manufacturer data with care. US fans are tested to the DOE test procedure and EU fans to IEC 60879, and the two methods do not give identical results. Retailer pages also copy data with errors. Compare fans only at equal diameter and similar airflow, and check the manufacturer's own datasheet before you use a number in a design.
:::

## Cooling effect and cooling fan efficiency

### Airflow is not cooling

The airflow on a datasheet is measured through the fan. It does not say how much air movement an occupant feels. That depends on the fan diameter and speed, the mounting height, the room size and, above all, where the occupant sits relative to the fan. A better measure of what a fan delivers is the **cooling fan efficiency (CFE)**, defined in ASHRAE Standard 216 as the cooling effect divided by the fan power:

```{math}
:label: eq-cfe-old
CFE = \frac{\text{cooling effect}}{\text{fan power}} = -\frac{\Delta t_{eq}}{P_f}
```

where $\Delta t_{eq}$ is the whole-body cooling effect (°C, negative because the occupant is cooled) and $P_f$ the fan input power (W). CFE is in °C per W. To find it, we need the air speed at the occupant and the cooling effect of that air speed.

### Cooling effect versus distance from the fan

{numref}`fig-ce-distance-old` shows the cooling effect felt by a seated occupant at different distances from a 1.5 m ceiling fan. The air speeds are measured values (seated average of 0.1, 0.6 and 1.1 m height) from full-scale laboratory tests {cite:p}`raftery2019`, read off Figure 24 in {cite:t}`raftery2020`. The cooling effect is calculated with the SET method of ASHRAE 55 for a warm summer situation: 28 °C air and mean radiant temperature, 50% relative humidity, 1.2 met and 0.5 clo. The half-speed curve assumes that air speeds scale linearly with fan speed, as the measurements showed.

:::{figure} figures/ch07/cooling-effect-distance.png
:label: fig-ce-distance-old
:alt: Line chart of cooling effect against horizontal distance from the fan centre for maximum and half fan speed. At maximum speed the cooling effect is about 4.5 °C within 0.6 m of the centre, falls to about 3.5 °C at 1.5 m and 2.7 °C at 6 m. At half speed the values are about 3.6, 2.3 and 1.3 °C.
:width: 90%

Cooling effect for a seated occupant versus horizontal distance from the centre of a 1.5 m ceiling fan. Air speeds from {cite:t}`raftery2019`; cooling effect calculated with the SET method at 28 °C, 50% RH, 1.2 met and 0.5 clo.
:::

The curve has three parts, which match the flow pattern described earlier:

- **Under the fan** (within about 0.4 D of the centre), air speeds are highest and the cooling effect is largest. Right at the centre it dips slightly, at the stagnation point.
- **At the edge of the jet** (about 0.5 D to 1 D), the air speed and cooling effect drop sharply.
- **In the spreading zone** (beyond 1 D), the cooling effect falls slowly with distance.

Two observations are useful for design:

- **The cooling effect is not proportional to air speed.** It grows quickly at low speeds and levels off at high speeds. Halving the fan speed reduces the cooling effect by only about 1 °C under the fan, while the fan power drops by much more. Running a fan at medium speed is therefore often the most efficient choice.
- **Sit within about one fan diameter of the centre for the full effect.** In a bedroom, that means placing the fan over the bed rather than in the middle of the room if the two differ.

:::{note}
The cooling effect depends on the conditions. For the CBE reference case (24.4 °C, 0.6 clo, 1.13 met), 0.5 m/s gives about 2 °C. At 28 °C with lighter clothing, the same air speed gives about 2.8 °C. Use the CBE Thermal Comfort Tool to calculate the cooling effect for your own conditions.
:::

### Predicting the air speed in a room

{cite:t}`raftery2019` turned a large set of full-scale laboratory tests into simple regression models for the air speed in a room with a ceiling fan. The models work with dimensionless ratios of fan diameter $D$, room width $R$, ceiling height $C$ and blade height $H$ (all in m). First calculate the fan air speed $S_F$, the average air speed through the area swept by the blades, from the rated airflow $Q$ (m³/s):

```{math}
:label: eq-sf-old
S_F = \frac{4\,Q}{\pi D^2}
```

The room-average air speed for seated occupants is then

```{math}
:label: eq-so-avg-old
S_{O,avg} = S_F \left(0.25 + 0.99\,\frac{D}{R} - 0.06\,\frac{C}{D} + 0.11\,\frac{D}{1.7} + 0.024\right)
```

where 1.7 m is the height of the occupied zone and the term 0.024 applies to seated occupants. The model is valid for fans blowing downwards with at least 0.2 D between the blades and the ceiling. For a typical fan in a residential room, the bracket is about 0.5, so the room-average air speed is about half the fan air speed.

{numref}`tab-cfe-old` applies this model to the fans from {numref}`tab-fan-data-old` in a 4.5 m × 4.5 m living room with a 2.7 m ceiling and the blades at 2.4 m.

:::{table} Estimated room-average air speed, cooling effect and CFE at maximum speed for a seated occupant in a 4.5 m × 4.5 m room (C = 2.7 m, H = 2.4 m). Cooling effect at 28 °C, 50% RH, 1.2 met, 0.5 clo.
:label: tab-cfe-old
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

All six fans give a similar cooling effect of 3.5 to 3.9 °C at maximum speed, but their CFE differs by a factor of six. Because the cooling effect levels off at high air speed, the extra airflow of the stronger fans buys very little extra cooling. The fan power, on the other hand, varies a lot. That is why the power at the speed you actually need matters more than the maximum airflow.

At maximum speed, all six fans exceed the 0.8 m/s that ASHRAE 55 allows without occupant control. In practice, they will run at a lower speed most of the time, where both the power and the cooling effect are lower, and the CFE is higher.

## Sizing and placement

:::{admonition} To be written
:class: dropdown

Diameter of 0.2 to 0.4 times √(floor area). One centred fan serves aspect ratios up to 1.5:1, and larger rooms are split into square fan cells. Clearances: blades at least 2.1 m above the floor, at least 0.2–0.3 m below the ceiling and at least 0.45 m from walls. Coordinate with lighting and sprinklers.
:::

## Control and integration

:::{admonition} To be written
:class: dropdown

The fan is the first cooling stage: the fan starts around 23–24 °C and AC only around 25.5–26.5 °C. Minimum speed should stay below about 0.4 m/s for seated occupants. Occupant control versus automation, interplay with opening windows, and reverse mode for winter destratification.
:::

## Energy and carbon

:::{admonition} To be written
:class: dropdown

Fan energy versus air-conditioning, compared on primary energy as a proxy for carbon. HVAC savings typically exceed fan energy 10 to 100 times.
:::

## Modelling fans

:::{admonition} To be written
:class: dropdown

IDA ICE fixes air speed at 0.1 m/s in its comfort output, so fan effects must be post-processed. The course PMV script with its stepped control is the method.
:::

## Worked example

:::{admonition} To be written
:class: dropdown

One room in the course row house, including a heat-wave year:

1. Pick a fan datasheet and read its diameter, rated airflow and rated power.
2. Check the diameter against the room using the sizing rule and the clearances.
3. Calculate the rated specific fan figure, then air speed and power at low, medium and high, assuming both scale with airflow.
4. Apply the stepped control and compute PMV with and without the fan, plus annual fan energy.
5. Compare with AC using primary energy as a proxy for carbon.
:::

## Summary and exercises

:::{admonition} To be written
:class: dropdown

Rules-of-thumb box, and guiding questions linked to Assignment 04 Q11: How much cooling does a fan give? Is it enough in future Danish summers, including the Annex 80 heat waves? How much energy does a fan in every habitable room use?
:::
