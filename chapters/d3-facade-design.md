# D3 Façade design for daylight and low cooling demand

:::{warning} Under revision
This chapter is being reworked and may change substantially. Sections marked *Outline* are not yet written.
:::

## D3.1 Introduction

The row house has been optimised to a very low heating demand. The same envelope that keeps heat in during winter keeps solar gains in during summer, and in the 2050 climate the cooling demand, not the heating demand, becomes the design problem. The façade is where the solar gain enters, so it is the first step of the cooling strategy ([](d2-cooling-strategy.md)): every kilowatt-hour that the façade keeps out is one that ventilative cooling ([](d4-ventilative-cooling.md)) and ceiling fans ([](d6-ceiling-fans.md)) do not have to deal with.

The difficulty is that solar gain and daylight come through the same glass. A smaller window, a lower g-value or a deeper overhang cuts both. Since BR18, daylight can be documented with climate-based simulation to EN 17037, so the daylight requirement becomes a number, sDA300, that can be traded against cooling and heating demand in an optimisation.

The running case is the critical centre zone of the course row house: 4 × 4 m floor, 2.5 m room height, prefabricated constructions with U = 0.1 W/(m²K), and one façade facing north or south. The four design variables are the window size, the glazing, the overhang depth and side fins ({numref}`fig-d3-variables`).

```{figure} figures/d3/design-variables.*
:name: fig-d3-variables
:alt: Left, a section of the 4 m deep, 2.5 m high zone with the window in the façade, an overhang above it and the daylight plane dotted across the room. Right, an elevation of the 4 m wide façade with a window, an overhang above it and a side fin on each side, and the largest possible window of 3.8 by 1.5 m dashed.

The centre zone and the four façade design variables.
```

## D3.2 Solar gains through the façade

The solar gain through a window is

$$
\Phi_{sol} = g \, F_{sh} \, A_g \, I_{\perp}
$$ (eq-d3-solar)

where $g$ is the total solar energy transmittance of the glazing (–), $F_{sh}$ the shading factor of overhangs and fins (–, 1 without shading), $A_g$ the glazed area (m²) and $I_{\perp}$ the solar irradiance on the façade (W/m²). The glazing properties $g$, $U_g$ and $\tau_v$ are defined in [](a3-glazing.md).

How much radiation reaches the façade depends on its orientation ({numref}`fig-d3-radiation`). In the Annex 80 Copenhagen TMY for 2041–2060, a south façade receives 776 kWh/m² a year and a north façade 390 kWh/m². In summer the picture changes: from May to August, east and west façades receive 380 kWh/m², as much as south (372 kWh/m²), and even north receives 241 kWh/m². The summer sun rises in the north-east and sets in the north-west, so the north façade gets low morning and evening sun, and east and west get the low sun head-on. South is the façade that gains the most in winter, but not the one that gains the most in summer.

```{figure} figures/d3/facade-radiation.*
:name: fig-d3-radiation
:alt: Line chart of monthly solar radiation from January to December on south, east or west, north and horizontal surfaces. Horizontal peaks at about 170 kWh per square metre in July. South is flat at 90 to 100 from April to July. East and west peak at about 105 in July. North peaks at about 65 in July. Annual totals are 776 south, 640 east and west, 390 north and 991 horizontal.

Monthly solar radiation on vertical façades and the horizontal, Annex 80 Copenhagen TMY 2041–2060 (isotropic sky, ground reflectance 0.2). Script: {download}`d3_facade_figures.py <code/d3_facade_figures.py>`.
```

A solar-control coating on the outer pane (surface 2) reflects most of the near-infrared half of the solar spectrum, which carries heat but no light. It lowers $g$ more than $\tau_v$, so the selectivity

$$
S = \frac{\tau_v}{g}
$$ (eq-d3-selectivity)

rises. Clear triple glazing has $S \approx 1.4$–$1.5$. The best solar-control coatings approach $S \approx 2$, close to the physical limit, because a glazing that lets all visible light through and blocks all infrared still transmits about half the solar energy.

```{list-table} Triple glazings for the assignment (centre-of-glass values).
:header-rows: 1
:name: tab-d3-glazing

* - Glazing
  - $U_g$ (W/(m²K))
  - $g$ (–)
  - $\tau_v$ (–)
  - $S$ (–)
* - Pilkington S3 (reference)
  - 0.6
  - 0.49
  - 0.71
  - 1.45
* - Suncool 70/35
  - 0.6
  - 0.34
  - 0.63
  - 1.85
* - Suncool 66/33
  - 0.6
  - 0.32
  - 0.59
  - 1.84
```

Going from the reference glazing to Suncool 66/33 cuts the solar gain by 35 % and the light by 17 %. Below $\tau_v \approx 0.5$ the glazing looks dark from inside and the window must grow to keep sDA300, which brings back the solar gain.

:::{admonition} Rules of thumb
- In Copenhagen, 1 m² of south glazing with $g = 0.49$ admits about 180 kWh of solar heat from May to August; with $g = 0.32$, about 120 kWh.
- East and west façades receive as much summer radiation as south, and are harder to shade.
- Selectivity above 2 is not available; keep $\tau_v \geq 0.5$.
:::

## D3.3 Fixed shading: overhangs and side fins

An overhang shades according to the sun's profile angle $\Omega$, the sun's altitude projected onto a vertical plane perpendicular to the façade:

$$
\tan \Omega = \frac{\tan \alpha}{\cos \gamma}
$$ (eq-d3-profile)

where $\alpha$ is the solar altitude and $\gamma$ the angle between the sun's azimuth and the façade normal. An overhang of depth $d$ placed at the window head shades a window of height $H$ completely when

$$
d \tan \Omega \geq H .
$$ (eq-d3-overhang)

At 55.7 °N the noon altitude is $90° - 55.7° + \delta$: 58° at the summer solstice, 34° at the equinoxes and 11° at the winter solstice ({numref}`fig-d3-overhang`a). Towards south the noon sun is high in summer and low in winter, so an overhang blocks the summer sun and admits the winter sun. The 1.2 m overhang over the 1.1 m south window of the worked example shades the whole window whenever $\Omega > 42.5°$, which at noon is from mid-April to the end of August. Over the year it cuts the direct radiation on the window from 420 to 91 kWh/m², and from May to August it removes all of it. From November to February it removes 28 % (65 to 47 kWh/m²), which is the heating penalty ({numref}`fig-d3-overhang`b).

```{figure} figures/d3/overhang.*
:name: fig-d3-overhang
:alt: Left, a section of the south window, 1.1 m high on a 0.9 m sill, with a 1.2 m overhang at its head. Noon sun rays past the overhang tip at 58 degrees in June reach below the sill, at 34 degrees in March and September they shade the upper half of the window, and at 11 degrees in December they reach almost the whole window. Right, monthly bars of direct radiation on the window with and without the overhang. With the overhang it is zero from May to August and only slightly reduced from November to February.

(a) Noon sun past a 1.2 m overhang at 55.7 °N. (b) Direct radiation on the south window with and without the overhang, Annex 80 Copenhagen TMY 2041–2060. The overhang is taken as infinitely long; diffuse radiation is not reduced.
```

Towards east and west the sun meets the façade at low altitude with $\gamma$ near zero, so $\Omega \approx \alpha$ is small and an overhang does little. There the sun must be blocked sideways, by side fins, or by movable shading. Side fins shade according to the horizontal angle $\gamma$; towards south they cut the low morning and evening sun, which reaches the glass at grazing angles anyway, and towards north they cut the low summer sun from north-east and north-west.

A fin of depth $d$ on each side of a window of width $W$ shades a strip of width $d \tan \gamma$ on the side the sun comes from, so the window is fully shaded when $d \tan \gamma \geq W$. Towards south the effect is small ({numref}`fig-d3-side-fins`). For a 2.8 m wide south window, 0.6 m fins on both sides cut the direct radiation from May to August by 23 % (164 to 126 kWh/m²) and over the year by 19 %, compared with 100 % in summer for the 1.2 m overhang. The fins act only in the morning and afternoon, when the sun is far to the side. Around noon, when the gain peaks, $\gamma$ is small and the fins shade almost nothing.

```{figure} figures/d3/side-fins.*
:name: fig-d3-side-fins
:alt: Left, a plan of a 2.8 m wide south window with a 0.6 m fin on each side. The sun on 21 June at 09:00, 64 degrees east of south, passes the east fin tip and shades a strip of about 1.2 m of the glass; at 14:00, 47 degrees west of south, it passes the west fin and shades about 0.6 m. Right, monthly bars of direct radiation on the window with and without the fins. The fins reduce it by roughly 10 to 25 percent in every month, and no month comes near zero.

(a) Sun past 0.6 m side fins on a south window on 21 June, plan. (b) Direct radiation on the south window with and without the fins, Annex 80 Copenhagen TMY 2041–2060. The fins are taken as infinitely tall; diffuse radiation is not reduced. Compare with the overhang in {numref}`fig-d3-overhang`.
```

Fixed shading also blocks part of the sky, so it costs diffuse daylight all year, and this is what usually limits the overhang depth when sDA300 is a constraint.

Movable shading (external blinds, screens, shutters) can block more sun when it matters and give the full window back on overcast days. It needs control and depends on the occupants, so this chapter keeps to fixed elements; shutters for heat waves are a later step of the cooling strategy.

:::{admonition} Rules of thumb
- Towards south at 55–56 °N, an overhang at the window head with depth $d \approx H$ shades the window completely around noon from late April to late August.
- Overhangs work towards south. Towards east and west, use fins, movable shading or a lower g-value.
:::

## D3.4 Daylight: sDA300 and what drives it

BR18 requires daylight in habitable rooms. It can be documented by simulation to EN 17037: an illuminance of at least 300 lx on at least 50 % of the reference plane for at least 50 % of the daylight hours,

$$
\mathrm{sDA}_{300,50\%} \geq 50\ \% .
$$ (eq-d3-sda)

The reference plane is 0.85 m above the floor. BR18 also accepts a simple rule for unobstructed rooms: a glass area of at least 10 % of the floor area, increased when the light transmittance is below 0.75. With a 15 % frame, that is a window-to-floor ratio of about 12 %. EN 17037 also allows the daylight factor route, with a target of about 2 % in the Danish climate, but climate-based modelling is the only one that responds to orientation and to the actual sky.

Climate-based daylight modelling in IDA ICE calculates the illuminance in a grid of points on the reference plane for every daylight hour of the weather file, with the Radiance ray tracer, and counts the share of the plane that reaches 300 lx for half the hours. The result depends on:

- **Window head height and area.** Daylight reaches roughly twice the head height into the room, so with a 4 m deep room and a head at 2.0–2.4 m the whole floor can be lit.
- **Light transmittance.** The illuminance scales with $\tau_v$.
- **Overhangs and fins**, which cut the sky view of the window.
- **Orientation.** South has more direct sun, so it reaches sDA300 with a smaller window than north.
- **External obstructions**, such as the neighbouring row of houses.

The target is enough daylight, not as much as possible. Every point of sDA above 50 % is glass area that also lets in solar gain. Potin {cite:p}`potin2023` recommends sDA300 > 50 % in bedrooms and sDA500 > 50 % in living rooms, and not much more. In the optimisation the daylight constraint is therefore usually active: the best design sits just above 50 %.

## D3.5 Cooling demand as the objective

In the zone model, an ideal cooler removes exactly the heat needed to hold the room at the cooling set point, and an ideal heater supplies exactly the heat needed to hold the heating set point. The annual cooling demand $Q_C$ (kWh/m² floor) is the sum of the heat removed. It is not the electricity of a real cooling system, which would be $Q_C$ divided by its efficiency. It measures the surplus heat the façade lets in, and that is why it is a good objective for comparing façades.

The heating demand $Q_H$ is the second objective, because almost everything that cuts solar gain in summer also cuts useful solar gain in winter. With U = 0.1 W/(m²K) walls and the other surfaces of the zone adiabatic, the window dominates both numbers, so the zone shows the effect of the façade alone.

The weather file is the Annex 80 Copenhagen TMY 2041–2060 ([](d1-weather-files.md)). The 2050 climate is more critical than 2090 for this study, because it combines higher temperatures with more solar radiation.

## D3.6 Multi-objective optimisation

The design variables span a large space. Seven window sizes, five glazings, five overhang depths, four fin depths and two orientations already give 7 × 5 × 5 × 4 × 2 = 1,400 combinations, and each needs an energy and a daylight simulation. A full factorial study of this size is impractical, and most of its runs are far from any useful design.

The problem is stated as

$$
\min_{x} \; \big( Q_C(x),\; Q_H(x) \big) \quad \text{subject to} \quad \mathrm{sDA}_{300}(x) \geq 50\ \%
$$ (eq-d3-moo)

where $x$ is a combination of the design variables. Cooling and heating demand are objectives: they should be as low as possible. Daylight is a constraint: it must be met, and there is no value in exceeding it.

The two objectives conflict, so there is no single best design. A design is Pareto-optimal if no other feasible design is better in one objective without being worse in the other. The Pareto-optimal designs form the Pareto front ({numref}`fig-d3-pareto`). Every design off the front can be improved for free; choosing among designs on the front is a trade-off. One way to choose is to convert both demands to the electricity of the actual systems, $Q_H/\mathrm{COP} + Q_C/\mathrm{EER}$, and pick the design on the front with the lowest total.

```{figure} figures/d3/pareto-concept.*
:name: fig-d3-pareto
:alt: Scatter plot with heating demand on the x-axis and cooling demand on the y-axis. Feasible designs with sDA300 of at least 50 percent are filled dots above a curved line, the Pareto front, running from high cooling and low heating at the top left to low cooling and high heating at the bottom right. Infeasible designs are open circles below the front. One point on the front is marked as the chosen design.

A Pareto front of cooling against heating demand (concept, not simulation results). Designs with too little daylight lie below the front; they would have lower cooling demand but are not allowed.
```

The infeasible designs lie below the front: small windows and dark glazing would give lower cooling demand, but fail the daylight constraint. This is why the constraint is usually active at the optimum.

IDA ICE's optimisation (AutoMOO in the parametric runs) uses the roles given to each output, objective or constraint, to steer new runs towards the feasible part of the front, so a few hundred runs resolve the front better than the same number spread over a full grid. The price is that the trends away from the front are not visible. The brute-force sweep in D3.7 gives those trends.

## D3.7 A façade guideline from a brute-force sweep

An optimisation such as AutoMOO returns one design for one room. The design is good, but the reason for it is hidden: you do not see how close the neighbouring designs are, or which variable did the work. A brute-force sweep over a coarse grid shows the trends instead. Plotted against one variable, it becomes a guideline you can reuse for the next room, the next house and the next project without simulating again.

The window-to-floor ratio is the natural x-axis,

$$
\mathrm{WFR} = \frac{A_w}{A_{floor}},
$$ (eq-fac-wfr)

where $A_w$ is the window area including the frame (m²) and $A_{floor}$ the floor area of the room (m²). WFR is the number an architect controls first, and it carries over between rooms of different size.

### The sweep

For the 4 × 4 × 2.5 m centre zone, the window is scaled in both width and height from a maximum opening of 3.8 × 1.5 m with the sill fixed at 0.9 m and the window centred on the façade. With $s = \sqrt{\mathrm{WFR} \cdot A_{floor} / 5.7\ \mathrm{m^2}}$, the window is $3.8s$ wide and $1.5s$ high, so WFR runs from 5 % (1.42 × 0.56 m) to 35 % (3.77 × 1.49 m) in steps of 5 %.

A grid of 7 WFR × 3 glazings × 3 overhang depths (0, 0.6 and 1.2 m) gives 63 runs per orientation, 126 for north and south. Side fins are left out: towards north and south they block little sun and mainly cost daylight. They belong in a sweep of an east or west façade.

Each run needs two simulations. Cooling and heating demand come from the zone with an ideal heater and cooler. Comfort must come from the same zone without the cooler, because a zone held at the cooling set point never overheats. In IDA ICE this is a second parametric run on a copy of the model with the cooler removed.

### Normalising the outputs

Energy, daylight and comfort have different units, so each is divided by a value that gives 1 a meaning:

$$
n_D = \frac{\mathrm{sDA}_{300}}{50\ \%}, \qquad
n_C = \frac{Q_C}{Q_{C,ref}}, \qquad
n_H = \frac{Q_H}{Q_{H,ref}}, \qquad
n_T = \frac{h_{II}}{h_{II,ref}}
$$ (eq-fac-norm)

where $Q_C$ and $Q_H$ are the annual cooling and heating demand (kWh/m²), $h_{II}$ the occupied hours above the upper limit of EN 16798-1 adaptive category II in May–September, and the subscript $ref$ the reference window and glazing from Q1.1 of the [cooling assignment](../assignments/cooling/cooling-assignment.md). For daylight, $n_D \geq 1$ meets the requirement. For the other three, $n < 1$ is better than the reference.

All four share one dimensionless axis, so they can be read off one figure per orientation ({numref}`fig-facade-guideline`).

```{figure} figures/d3/facade-guideline-schematic.*
:name: fig-facade-guideline
:alt: Two panels, north and south, with window-to-floor ratio from 5 to 35 percent on the x-axis and normalised value on the y-axis. Daylight rises steeply and levels off near 2. Cooling rises almost linearly. Heating is nearly flat, with a shallow minimum towards south. Comfort is zero up to a threshold and then rises steeply. A dashed line at 1 marks the daylight requirement and the reference design. Shaded bands show the spread over solar-control glazing and overhangs. The minimum window-to-floor ratio is marked where daylight crosses 1.

Expected shape of the façade guideline (schematic, not simulation results). Lines: reference glazing without shading. Bands: spread over solar-control glazing and overhang depth.
```

### What the figure shows

- **Daylight** rises steeply at small WFR and levels off, because the back of the room is lit first and further increases only light parts that already pass. The WFR where $n_D$ crosses 1 is the minimum window for that glazing and shading.
- **Cooling** rises almost linearly with WFR, because the solar gain is proportional to the glazed area. The slope is set by the g-value and, towards south, by the overhang.
- **Heating** changes little. Towards south it has a shallow minimum, where extra solar gain balances the extra heat loss. Towards north it rises with WFR.
- **Comfort** stays near zero up to a threshold, where the free-running zone first exceeds the category II limit, and then rises faster than cooling.

Solar control and overhangs move the daylight and cooling curves down together, so they also move the minimum WFR to the right. The design question is then whether a larger window with solar control beats a smaller window with clear glazing. The figure answers it directly: compare $n_C$ at the two minimum-WFR points.

### The guideline

The result of the sweep is a short table per orientation:

| | North | South |
|---|---|---|
| Minimum WFR, reference glazing | | |
| Minimum WFR, best solar control + overhang | | |
| $n_C$ and $n_T$ at each minimum | | |
| WFR where $h_{II}$ starts to rise | | |
| Recommended combination | | |

The table holds for this climate file, this room depth and this construction. A deeper room needs a larger WFR for the same sDA, and a future climate file moves the comfort threshold to the left.

## D3.8 Running the study in IDA ICE

*Outline:*

- Step by step: the single-zone model, the glazing database, parameters (window height with sill at 0.9 m, glazing type, overhang depth, fins, orientation), output metrics and their roles, "custom" plus "climate-based daylight" simulation, keep generated models, faster settings (tolerance, max time step) [15.2, How-to guide, Assignment 04 Q2].
- Test with a small study first.
- Reading the Explore view (parallel coordinates) and exporting results.
- Pitfalls box: physically impossible parameter combinations, too fine steps, results from earlier runs mixed in, sDA computed on the wrong plane.

## D3.9 Worked example: the row house centre zone

*Outline:*

- Reference: cooling 20.8 kWh/m² north (sDA 65 %) and 53.0 kWh/m² south (sDA 93 %).
- Optimised north: reference glazing, no overhang, 1.4 m window height; sDA 59 %, cooling 15.1 kWh/m² (−27 %).
- Optimised south: g 0.32 glazing, 1.2 m overhang, 1.1 m window height; sDA 53 %, cooling 19.6 kWh/m² (−63 %).
- Heating penalty, and the same designs under today's and the future weather and a heat-wave year.
- Table plus the Pareto figure from section 6.

## D3.10 From one zone to the whole house

*Outline:*

- Carrying the north and south designs back to the full row house; rooms with other depths and uses.
- What is left for ventilative cooling ([](d4-ventilative-cooling.md)) and ceiling fans ([](d6-ceiling-fans.md)).

## D3.11 Guiding questions

*TBA*

- Five to seven questions on the trade-offs, e.g. why the optimal south window is smaller than the north one, and when fins pay off.
