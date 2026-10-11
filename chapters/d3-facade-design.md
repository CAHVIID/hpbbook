# D3 Façade design for daylight and low cooling demand

:::{warning} Under revision
This chapter is being reworked and may change substantially. Sections marked *Outline* are not yet written.
:::

## D3.1 Introduction

*Outline:*

- Low-energy houses overheat because of solar gains; the row house already has a very low heating demand, and the 2050 climate makes cooling the design problem [Assignment 04, 16.1].
- Reduce the gains first: the façade decides the gain before any ventilation or fan has to remove it. Step 1 of the cooling strategy ([](d2-cooling-strategy.md)), before ventilative cooling ([](d4-ventilative-cooling.md)) and ceiling fans ([](d6-ceiling-fans.md)).
- The conflict: every measure that cuts solar gain also cuts daylight. Since BR18, daylight can be documented with climate-based simulation to EN 17037, which makes the trade-off something you can optimise.
- The running case: the critical centre zone of the course row house, 4 × 4 × 2.5 m, prefab constructions with U = 0.1 W/m²K, facing north or south.
- Figure: the four design variables on one façade section and elevation (window height, glazing, overhang, side fins).

## D3.2 Solar gains through the façade

*Outline:*

- Sun position over the year in Copenhagen (55.7 °N): noon altitude about 11° in December and 58° in June. Incident radiation on north, east, south, west and horizontal surfaces, from the course weather file.
- Glazing properties: U-value, g-value, light transmittance LT, selectivity LT/g. Solar-control coatings on the outer pane (surface 2) and what they do to g and LT.
- Glazing table for the assignment: reference Pilkington S3 (U 0.6, g 0.49, LT 71 %), Suncool 70/35, 66/33, Coollite and SKN coatings. Keep LT ≥ 50 % [Advice for parametric run].
- Figure: incident radiation by orientation and month; g against LT for the candidate glazings, with lines of constant selectivity.
- Rules-of-thumb box: g-value, selectivity limits (about 2 for double/triple coatings), what LT does to sDA.

## D3.3 Fixed shading: overhangs and side fins

*Outline:*

- Profile angle and how an overhang blocks a high summer sun but admits a low winter sun. Why that works towards south and fails towards east and west, where fins (or movable shading) are needed.
- Overhang depth from the profile angle; the balcony as an overhang. Side fins on one or both sides.
- Fixed shading also cuts diffuse light and so daylight; the heating penalty in winter and shoulder seasons.
- Short note on movable shading (blinds, screens) and why the chapter keeps to fixed elements (robust, no control, no occupant behaviour).
- Figure: section and plan showing profile angle, overhang and fins against the sun path for June, March/September and December.
- Rules-of-thumb box: overhang depth for a given window height towards south.

## D3.4 Daylight: sDA300 and what drives it

*Outline:*

- The BR18 / EN 17037 requirement: at least 300 lux for 50 % of daylight hours on at least 50 % of the reference plane (sDA300,50% > 50 %). The daylight factor route as the alternative.
- Climate-based daylight modelling in IDA ICE: what it calculates and its settings.
- What drives sDA: window head height and area, LT, room depth, overhangs and fins, orientation, external obstructions.
- Why "just enough" daylight: sDA far above 50 % means solar gain you pay for in cooling (Potin: sDA300 > 50 % in bedrooms, sDA500 > 50 % in living rooms, but not much more).
- Figure: sDA300 and cooling demand against window height for the reference glazing, north and south.

## D3.5 Cooling demand as the objective

*Outline:*

- What "cooling demand" means in the zone model: an ideal cooler at a set point, so the number measures the surplus heat the façade lets in, not a real cooling system.
- Heating demand as the second objective: less solar gain means more heating.
- Weather: the 2050 climate file (more critical than 2090), Annex 80 TMY 2041–2060 as in the cooling assignment ([](d1-weather-files.md)).

## D3.6 Multi-objective optimisation

*Outline:*

- Design variables, ranges and steps; why the number of runs explodes in a full factorial study.
- Objectives versus constraints: minimise cooling and heating, constrain sDA300 to 40–60 %.
- The Pareto front: designs where no objective can improve without another getting worse. Choosing one design from the front.
- How IDA ICE concentrates runs near the interesting region when roles are set; sampling versus a full grid.
- Figure: a Pareto front of cooling against heating demand, coloured by sDA, with the feasible region marked.

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
