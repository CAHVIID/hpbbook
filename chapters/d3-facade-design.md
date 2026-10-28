# D3 Façade design for daylight and low cooling demand

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D3.1 Introduction

The heating demand of the course row house has been reduced to a very low level. The same envelope retains solar gains in summer, and in the 2050 climate the cooling demand becomes the governing design criterion. The façade determines the solar gain and is therefore the first step of the cooling strategy ([](d2-cooling-strategy.md)). Solar gain that is not admitted through the façade does not have to be removed by ventilative cooling ([](d4-ventilative-cooling.md)) or offset by ceiling fans ([](d6-ceiling-fans.md)).

Daylight and solar gain are transmitted through the same glazing, and a smaller window, a lower g-value or a deeper overhang reduces both. BR18 allows daylight to be documented by climate-based simulation to EN 17037, which expresses the requirement as one metric, sDA300. The metric can be used as a constraint when cooling and heating demand are minimised.

## D3.2 Solar gains through the façade

The solar gain through a window is

$$
\Phi_{sol} = g \, F_{sh} \, A_g \, I_{\perp}
$$ (eq-d3-solar)

where $g$ is the total solar energy transmittance of the glazing (–), $F_{sh}$ the shading factor of overhangs and fins (–, 1 without shading), $A_g$ the glazed area (m²) and $I_{\perp}$ the solar irradiance on the façade (W/m²). The glazing properties $g$, $U_g$ and $\tau_v$ are defined in [](a3-glazing.md). The $g$-value given in product data applies at normal incidence. It decreases with the angle of incidence, slowly up to about 50° and steeply above 60°, because the reflection at each pane increases. Simulation tools such as IDA ICE account for this; hand calculations with the normal-incidence value overestimate the gain when the sun strikes the glass at a large angle.

{numref}`fig-d3-radiation` shows the monthly solar radiation on façades of different orientation in the Annex 80 Copenhagen TMY for 2041–2060.

```{figure} figures/d3/facade-radiation.*
:name: fig-d3-radiation
:alt: Line chart of monthly solar radiation from January to December on south, east or west, north and horizontal surfaces. Horizontal peaks at about 170 kWh per square metre in July. South is flat at 90 to 100 from April to July. East and west peak at about 105 in July. North peaks at about 65 in July. Annual totals are 776 south, 640 east and west, 390 north and 991 horizontal.

Monthly solar radiation on vertical façades and the horizontal, Annex 80 Copenhagen TMY 2041–2060 (isotropic sky, ground reflectance 0.2). Script: {download}`d3_facade_figures.py <code/d3_facade_figures.py>`.
```

## D3.3 Fixed shading: overhangs and side fins

The fixed shading elements considered are an overhang above the window and side fins at its edges ({numref}`fig-d3-variables`).

```{figure} figures/d3/design-variables.*
:name: fig-d3-variables
:alt: Left, a section of the 4 m deep, 2.5 m high zone with the window in the façade, an overhang above it and the daylight plane dotted across the room. Right, an elevation of the 4 m wide façade with a window, an overhang above it and a side fin on each side, and the largest possible window of 3.8 by 1.5 m dashed.

The façade design variables: window size, glazing, overhang and side fins.
```

An overhang shades according to the profile angle $\Omega$, which is the solar altitude projected onto the vertical plane perpendicular to the façade:

$$
\tan \Omega = \frac{\tan \alpha}{\cos \gamma}
$$ (eq-d3-profile)

where $\alpha$ is the solar altitude and $\gamma$ the angle between the sun's azimuth and the façade normal. An overhang of depth $d$ placed at the window head shades a window of height $H$ completely when

$$
d \tan \Omega \geq H .
$$ (eq-d3-overhang)

At 55.7 °N the noon altitude is $90° - 55.7° + \delta$: 58° at the summer solstice, 34° at the equinoxes and 11° at the winter solstice ({numref}`fig-d3-overhang`a). Towards south the noon sun is high in summer and low in winter, so an overhang blocks the summer sun and admits the winter sun. A 1.0 m overhang over a 1.1 m high, 2.3 m wide south window shades the entire window at noon when $\Omega > 47.7°$, i.e. from late April to mid-August. The overhang has the same length as the window, so in the morning and afternoon the sun reaches the glass past its ends. The overhang reduces the annual direct radiation on the window from 420 to 162 kWh/m² (−61 %) and the radiation from May to August by 85 % (164 to 24 kWh/m²). From November to February the reduction is 22 % (65 to 51 kWh/m²), which increases the heating demand ({numref}`fig-d3-overhang`b).

```{figure} figures/d3/overhang.*
:name: fig-d3-overhang
:alt: Left, a section of the south window, 1.1 m high on a 0.9 m sill, with a 1.0 m overhang at its head, 2.3 m long like the window. Noon sun rays past the overhang tip at 58 degrees in June reach below the sill, at 34 degrees in March and September they shade the upper half of the window, and at 11 degrees in December they reach almost the whole window. Right, monthly bars of direct radiation on the window with and without the overhang. With the overhang it is 5 to 8 kWh/m² per month from May to August instead of about 40, and only slightly reduced from November to February.

(a) Noon sun past a 1.0 m overhang at 55.7 °N. (b) Direct radiation on a 2.3 m wide south window with and without the overhang, Annex 80 Copenhagen TMY 2041–2060. The overhang is as long as the window, so sun from the side passes its ends; diffuse radiation is not reduced.
```

On east and west façades the irradiance is highest when the sun is low and $\gamma$ is close to zero, so $\Omega \approx \alpha$ is small and an overhang has little effect. Fixed elements block sun at near-normal incidence poorly. Side fins are effective only on narrow windows, as shown below, and movable shading or a lower g-value is normally required. Side fins shade according to the horizontal angle $\gamma$. Towards south they block the low morning and evening sun, which reaches the glass at grazing incidence; towards north they block the low summer sun from north-east and north-west.

A fin of depth $d$ on each side of a window of width $W$ shades a strip of width $d \tan \gamma$ on the side facing the sun, and the window is fully shaded when $d \tan \gamma \geq W$. Towards south the effect is small ({numref}`fig-d3-side-fins`). For the 2.3 m wide south window, 0.5 m fins on both sides reduce the direct radiation from May to August by 23 % (164 to 125 kWh/m²) and the annual radiation by 19 %, compared with 85 % in summer for the 1.0 m overhang. The fins shade only in the morning and afternoon. Around noon, when the gain is highest, $\gamma$ is small and the fins provide almost no shading.

```{figure} figures/d3/side-fins.*
:name: fig-d3-side-fins
:alt: Left, a plan of a 2.3 m wide south window with a 0.5 m fin on each side. The sun on 21 June at 09:00, 64 degrees east of south, passes the east fin tip and shades a strip of about 1.0 m of the glass; at 14:00, 47 degrees west of south, it passes the west fin and shades about 0.5 m. Right, monthly bars of direct radiation on the window with and without the fins. The fins reduce it by roughly 10 to 20 percent in every month, and no month comes near zero.

(a) Sun past 0.5 m side fins on a south window on 21 June (solar time), plan. (b) Direct radiation on the south window with and without the fins, Annex 80 Copenhagen TMY 2041–2060. The fins are taken as infinitely tall; diffuse radiation is not reduced. Compare with the overhang in {numref}`fig-d3-overhang`.
```

On east and west façades only the fin on the south side of the window is effective, because the sun is on the north side only early in the morning and late in the evening ({numref}`fig-d3-side-fins-split`). The irradiance on an east façade is highest in the early morning, when the sun is low and $\gamma$ is small. A single 0.5 m fin on a 2.3 m window reduces the direct radiation from May to August by 10 % (east 161 to 145, west 172 to 155 kWh/m²).

The shaded strip $d \tan \gamma$ is a larger fraction of a narrow window. Dividing the 2.3 m window into two 1.15 m windows, each with a fin, keeps the glass area and doubles the shaded fraction. The reduction from May to August increases to 18 % on the east façade (132 kWh/m²) and 17 % on the west façade (142 kWh/m²), and the annual reduction from 15 % to 26 %. Sun at near-normal incidence is still not blocked. Closely spaced vertical louvres apply the same principle, and movable shading also blocks the sun at near-normal incidence.

```{figure} figures/d3/side-fins-split.*
:name: fig-d3-side-fins-split
:class: col-page-right
:alt: Two rows, east façade on top and west below. Left, plan of one 2.3 m window with a 0.5 m fin on its south side; middle, plan of two 1.15 m windows separated by 0.3 m of wall, each with a 0.5 m fin on its south side, with the sun's rays on 21 June at two hours and the shaded strips. Right, monthly bars of direct radiation on the glass without fins, with one window and fin, and with two windows and fins; the split window cuts the summer radiation about twice as much as the single window.

Side fins on the south side of east (top) and west (bottom) windows. (a, d) One 2.3 m window with one 0.5 m fin. (b, e) The same glass split into two 1.15 m windows with 0.3 m of wall between them, each with a 0.5 m fin. Plans with the sun on 21 June (solar time). (c, f) Direct radiation on the glass, Annex 80 Copenhagen TMY 2041–2060. Same assumptions as {numref}`fig-d3-side-fins`.
```

Fixed shading also obstructs part of the sky and reduces the diffuse daylight throughout the year. When sDA300 is a constraint, this usually limits the overhang depth.

Movable shading (external blinds, screens, shutters) can block more of the sun when required and leave the window unobstructed on overcast days. It requires control, either automatic or by the occupants. This chapter considers fixed elements only; shutters for heat waves belong to a later step of the cooling strategy.

:::{admonition} Rules of thumb
- Towards south at 55–56 °N, an overhang at the window head with depth $d \approx H$ shades the window completely around noon from late April to mid-August.
- Overhangs are effective towards south. Towards east and west, fins are effective only on narrow windows; use movable shading or a lower g-value.
:::

## D3.4 Fixed shading: solar-coatings

A solar-control coating on the outer pane (surface 2) reflects most of the near-infrared part of the solar spectrum, which carries about half of the solar energy but no visible light. The coating reduces $g$ more than $\tau_v$, and the selectivity

$$
S = \frac{\tau_v}{g}
$$ (eq-d3-selectivity)

increases. Clear triple glazing has $S \approx 1.4$–$1.5$. Solar-control coatings reach $S \approx 2$, which is close to the theoretical limit: a glazing that transmits all visible light and blocks all infrared radiation still transmits about half of the solar energy.

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

Replacing the reference glazing with Suncool 66/33 reduces $g$ by 35 % and $\tau_v$ by 17 % ({numref}`tab-d3-glazing`). Below $\tau_v \approx 0.5$ the room appears dark from the inside, and a larger window is needed to meet sDA300, which increases the solar gain again.

A coating also changes the colour of the transmitted daylight. In a Danish pilot study, 18 subjects assessed the daylight in a scale model of an office behind six glazings ({numref}`fig-d3-glazing-lt-rating`) {cite}`dubois2003`. Some subjects found the colour unacceptable at $\tau_v$ of 0.66–0.70, and most subjects at 0.50. The ratings did not follow $\tau_v$ alone: the reference glazing at 0.77 was rated higher than a coated glazing at 0.79.

```{figure} figures/d3/glazing-lt-rating.*
:name: fig-d3-glazing-lt-rating
:alt: Dot chart of six glazings, light transmittance on the x-axis from 45 to 85 percent and rated daylight quality on the y-axis. The reference glazing at 77 percent is rated excellent; A at 79 and D at 76 percent good; E at 66 and B at 70 percent moderate, colour unacceptable to some; C at 50 percent poor, colour unacceptable to most.

Light transmittance of six glazings against the rated quality of the daylight behind them, 18 subjects, 1:7.5 scale model of an office under overcast skies {cite}`dubois2003`. Manufacturers' $\tau_v$; categories as summarised by the authors. A small pilot study, so indicative only. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/d3_glazing_lt_rating.py)
```

:::{admonition} Rules of thumb
- In Copenhagen, 1 m² of south glazing with $g = 0.49$ admits about 180 kWh of solar heat from May to August; with $g = 0.32$, about 120 kWh.
- Selectivity above 2 is not available; keep $\tau_v \geq 0.5$.
:::

## D3.5 Daylight requirement and sDA300

BR18 requires daylight in habitable rooms. Compliance can be documented by simulation to EN 17037: an illuminance of at least 300 lx on at least 50 % of a reference plane 0.85 m above the floor for at least 50 % of the daylight hours,

$$
\mathrm{sDA}_{300,50\%} \geq 50\ \% .
$$ (eq-d3-sda)

For unobstructed rooms BR18 also accepts a glass area of at least 10 % of the floor area, increased when the light transmittance is below 0.75.

sDA300 increases with window area and head height, light transmittance and a southern orientation, and decreases with overhangs, fins and external obstructions. Daylight penetrates to a depth of about twice the head height. The requirement is a minimum, and sDA above 50 % corresponds to glazing that also admits solar gain. In the optimisation the daylight constraint is therefore normally active, and the optimal design is close to sDA300 = 50 %.

## D3.6 Multi-objective optimisation

Seven window sizes, five glazings, five overhang depths, four fin depths and two orientations give 7 × 5 × 5 × 4 × 2 = 1,400 combinations, each requiring an energy and a daylight simulation. A full factorial study of this size is impractical, and most of the runs are far from a useful design.

The problem is stated as

$$
\min_{x} \; \big( Q_C(x),\; Q_H(x) \big) \quad \text{subject to} \quad \mathrm{sDA}_{300}(x) \geq 50\ \%
$$ (eq-d3-moo)

where $x$ is a combination of the design variables, and $Q_C$ and $Q_H$ are the annual cooling and heating demand (kWh/m²) of the zone with an ideal cooler and heater. Cooling and heating demand are objectives to be minimised. Daylight is a constraint that must be satisfied; exceeding it has no value.

The two objectives conflict, so there is no single optimal design. A design is Pareto-optimal if no other feasible design is better in one objective without being worse in the other. The Pareto-optimal designs form the Pareto front ({numref}`fig-d3-pareto`). A design that is not on the front can be improved in one objective without a penalty in the other, whereas the choice between designs on the front is a trade-off. One method is to convert both demands to the electricity use of the actual systems, $Q_H/\mathrm{COP} + Q_C/\mathrm{EER}$, and select the design on the front with the lowest total.

```{figure} figures/d3/pareto-concept.*
:name: fig-d3-pareto
:alt: Scatter plot with heating demand on the x-axis and cooling demand on the y-axis. Feasible designs with sDA300 of at least 50 percent are filled dots above a curved line, the Pareto front, running from high cooling and low heating at the top left to low cooling and high heating at the bottom right. Infeasible designs are open circles below the front. One point on the front is marked as the chosen design.

A Pareto front of cooling against heating demand (concept, not simulation results). Designs with too little daylight lie below the front; they would have lower cooling demand but are not allowed.
```

The infeasible designs lie below the front: small windows and glazings with low $\tau_v$ give a lower cooling demand but do not meet the daylight constraint. For this reason the constraint is normally active at the optimum.

The optimisation in IDA ICE (AutoMOO in the parametric runs) uses the role assigned to each output, objective or constraint, to direct new runs towards the feasible part of the front. A few hundred runs therefore resolve the front better than the same number distributed over a full grid. The drawback is that trends away from the front are not resolved. The parametric sweep in D3.7 provides these trends.

## D3.7 Parametric sweep and design guideline

An optimisation such as AutoMOO returns one design for one room. It does not show how close the neighbouring designs are, or which variable has the largest effect. A parametric sweep over a coarse grid shows these trends. Plotted against one variable, the results form a design guideline that can be applied to other rooms and projects without further simulation.

The window-to-floor ratio is used as the independent variable,

$$
\mathrm{WFR} = \frac{A_w}{A_{floor}},
$$ (eq-fac-wfr)

where $A_w$ is the window area including the frame (m²) and $A_{floor}$ the floor area of the room (m²). WFR is usually fixed early in the design and can be transferred between rooms of different size.

### Parameter grid

For the 4 × 4 × 2.5 m centre zone, the window is scaled in both width and height from a maximum opening of 3.8 × 1.5 m with the sill fixed at 0.9 m and the window centred on the façade. With $s = \sqrt{\mathrm{WFR} \cdot A_{floor} / 5.7\ \mathrm{m^2}}$, the window is $3.8s$ wide and $1.5s$ high, so WFR runs from 5 % (1.42 × 0.56 m) to 35 % (3.77 × 1.49 m) in steps of 5 %.

A grid of 7 WFR × 3 glazings × 3 overhang depths (0, 0.6 and 1.2 m) gives 63 runs per orientation, 126 for north and south. Side fins are omitted, because towards north and south they block little sun and mainly reduce daylight. They should be included in a sweep of an east or west façade.

Each run requires two simulations. Cooling and heating demand are taken from the zone with an ideal heater and cooler. Thermal comfort must be evaluated in the same zone without the cooler, because a zone held at the cooling set point does not overheat. In IDA ICE this requires a second parametric run on a copy of the model with the cooler removed.

### Normalisation

Energy, daylight and comfort have different units. Each output is therefore divided by a reference value:

$$
n_D = \frac{\mathrm{sDA}_{300}}{50\ \%}, \qquad
n_C = \frac{Q_C}{Q_{C,ref}}, \qquad
n_H = \frac{Q_H}{Q_{H,ref}}, \qquad
n_T = \frac{h_{II}}{h_{II,ref}}
$$ (eq-fac-norm)

where $Q_C$ and $Q_H$ are the annual cooling and heating demand (kWh/m²), $h_{II}$ the occupied hours above the upper limit of EN 16798-1 adaptive category II in May–September, and the subscript $ref$ the reference window and glazing from Q1.1 of the [cooling assignment](../assignments/cooling/cooling-assignment.md). For daylight, $n_D \geq 1$ meets the requirement. For the other three, $n < 1$ is better than the reference.

The four quantities are dimensionless and can be shown in one figure per orientation ({numref}`fig-facade-guideline`).

```{figure} figures/d3/facade-guideline-schematic.*
:name: fig-facade-guideline
:alt: Two panels, north and south, with window-to-floor ratio from 5 to 35 percent on the x-axis and normalised value on the y-axis. Daylight rises steeply and levels off near 2. Cooling rises almost linearly. Heating is nearly flat, with a shallow minimum towards south. Comfort is zero up to a threshold and then rises steeply. A dashed line at 1 marks the daylight requirement and the reference design. Shaded bands show the spread over solar-control glazing and overhangs. The minimum window-to-floor ratio is marked where daylight crosses 1.

Expected shape of the façade guideline (schematic, not simulation results). Lines: reference glazing without shading. Bands: spread over solar-control glazing and overhang depth.
```

### Expected trends

- **Daylight** increases steeply at small WFR and then levels off, because additional glazing mainly raises the illuminance in parts of the plane that already exceed 300 lx. The WFR at which $n_D = 1$ is the minimum window for the given glazing and shading.
- **Cooling** increases almost linearly with WFR, because the solar gain is proportional to the glazed area. The slope is determined by the g-value and, towards south, by the overhang.
- **Heating** changes little. Towards south it has a shallow minimum where the additional solar gain balances the additional heat loss. Towards north it increases with WFR.
- **Comfort.** $h_{II}$ remains close to zero up to the WFR at which the free-running zone first exceeds the category II limit, and then increases faster than the cooling demand.

Solar-control glazing and overhangs lower the daylight and cooling curves together and therefore shift the minimum WFR to larger values. Whether a larger window with solar-control glazing performs better than a smaller window with the reference glazing is determined by comparing $n_C$ at the two minimum-WFR points.

### Guideline table

The sweep is summarised in one table per orientation:

| | North | South |
|---|---|---|
| Minimum WFR, reference glazing | | |
| Minimum WFR, best solar control + overhang | | |
| $n_C$ and $n_T$ at each minimum | | |
| WFR where $h_{II}$ starts to rise | | |
| Recommended combination | | |

The table applies to this climate file, room depth and construction. A deeper room requires a larger WFR for the same sDA, and a warmer climate file moves the comfort threshold to a lower WFR.
