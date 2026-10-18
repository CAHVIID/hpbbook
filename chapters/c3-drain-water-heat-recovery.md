# Drain water heat recovery

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## Introduction 

When you take a shower, about 8 L of water at 40 °C leaves the shower head every minute. A few seconds later the same water runs down the drain at 35–38 °C, having lost only a few kelvin on its way through the air and over your skin. At the same moment, 8 L of cold water at about 10 °C enters the house to replace it. A drain water heat recovery unit is a heat exchanger between these two flows. It needs no storage, no pump and no control, because the two flows are there at the same time and stop at the same time. It only works for tappings with that property, and in a home that means showers. A bath is filled first and emptied later, and a kitchen sink or a washbasin draws little water at a time.

{numref}`fig-dwhr-installed` shows a vertical unit installed in a basement and how it is connected in a house.

:::::{figure}
:label: fig-dwhr-installed

::::{grid} 2 2 2 2

```{image} figures/c3/dwhr-vertical-photo.jpg
:alt: Photo of a vertical drain water heat recovery unit in a basement. A black plastic drain stack comes down from the floor joists, and about 1.5 m of it is replaced by a copper pipe wrapped in a tight copper coil. Two thin copper pipes run from the ends of the coil up to the ceiling: cold water in at the bottom, preheated water out at the top. Below the unit the drain continues into the floor.
:width: 80%
:align: center
```

```{image} figures/c3/dwhr-equal-flow-diagram.png
:alt: Diagram of a two-storey house. Shower water runs down a black drain pipe through a copper coil in the storey below. Cold water, shown in blue, enters the house at the bottom, flows up through the coil and leaves it as green preheated water. The preheated water goes both to the cold side of the shower mixer and to the water heater, which sends red hot water to the mixer.
:width: 80%
:align: center
```

::::

A vertical drain water heat recovery unit. Left: installed in a basement; the copper coil around the drain carries the cold water upwards. Photo: Recycle9876, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Hot_water_heat_recycling_unit.jpg), public domain. Right: connected so that the preheated water feeds both the shower and the water heater (equal flow, connection 3 below). Diagram: Ashp uk, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Waste_Water_Heat_Recovery_in_the_most_efficient_%27equal_flow%27_configuration.png), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
:::::

## How a unit works

{numref}`fig-dwhr-units` shows the two main types.

**Vertical units** replace about 1.5–2 m of the vertical drain pipe below the shower. The inner pipe is copper. Water falling down a vertical pipe does not fill it, but spreads into a thin film that clings to the wall, so almost all of the copper surface is wetted by a thin, fast-moving layer of warm water. The cold water flows upwards in a coil or a narrow annulus around the pipe, in counterflow to the drain water. This is a good heat exchanger, and the best vertical units recover 70 % of the heat that could at most be recovered. The catch is that a vertical unit needs a storey of straight vertical drain below the shower, which means a basement or a floor below. It suits a house with a basement and an apartment block where the bathrooms are stacked.

**Horizontal units** sit in the floor, under a shower tray or in a channel drain. They fit a slab-on-ground house and a bathroom renovation. In a channel drain, the heat exchanger is a row of copper tubes along the bottom of the channel, with the cold water flowing inside them against the direction of the drain water. The drain water flows around and over the tubes in a shallow layer. The unit is short, typically 0.7–0.9 m, and the water in the channel moves slowly, so it has less length and less turbulence to give off its heat than the falling film in a vertical pipe. Some manufacturers add turbulators between the tubes to stir the flow. The lower the shower flow, the thinner the water layer around the tubes and the higher the effectiveness. The better horizontal units still reach about 60 %.

:::{figure} figures/c3/dwhr-units.png
:label: fig-dwhr-units
:alt: Two schematic sections. Left, a vertical unit in section: a copper drain pipe with air in the middle, a thin film of warm drain water running down the inside of the wall, and a copper coil with cold water wound around the outside. Drain water enters at the top at 37 °C and leaves at the bottom at 18 °C; cold water enters at the bottom at 10 °C and leaves at the top at 29 °C. Right, a horizontal unit in a shower channel drain, shown along the channel and in a cross-section: shower water falls through the grate and runs along the channel over a row of copper tubes in the channel bottom, in which the cold water flows the opposite way. Drain water leaves at 24 °C, cold water enters at 10 °C and leaves at 24 °C. The cross-section shows the drain water flowing around and over the tubes. A legend gives orange for warm drain water, blue for cold drinking water and brown for the copper walls.
:width: 100%

A vertical unit (left) and a horizontal unit in a shower channel drain (right). Temperatures are for an 8 L/min shower with equal flow on both sides, an effectiveness of 0.70 for the vertical unit and 0.50 for the horizontal one. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dwhr_figures.py)
:::

Both types must keep the drinking water safe if the wall between the two flows fails. Certified units therefore have a double wall with a vented gap between the drain water and the drinking water, so a leak shows up as water dripping out of the gap rather than as sewage in the drinking water. The drain side gets a film of soap, skin fat and hair over time. A vertical unit is largely self-cleaning, because the falling water scours the wall, while a horizontal unit needs the grate and the channel cleaned as part of normal bathroom cleaning. On the cold side, the unit adds a pressure loss of about 0.1–0.4 bar at shower flow.

## Effectiveness

How good a unit is, is expressed by its *effectiveness*: the heat it actually transfers, divided by the most heat that could be transferred.

The most that could be transferred is the heat that would cool the drain water all the way down to the cold water temperature, or warm the cold water all the way up to the drain water temperature, whichever flow has the smaller heat capacity rate $C = \rho\,\dot V\,c_p$.

When *the two flows are equal* (connection 3 below), the heat flow transferred [W] is

$$
\Phi = \varepsilon\, C\,(\theta_d - \theta_c)
\qquad\text{and}\qquad
\varepsilon = \frac{\theta_p - \theta_c}{\theta_d - \theta_c}
$$ (eq-dwhr-eps)

where $\theta_d$ is the drain water temperature entering the unit, $\theta_c$ the cold water temperature and $\theta_p$ the temperature of the preheated cold water leaving it.

With drain water at 37 °C, cold water at 10 °C and $\varepsilon = 0.6$, the cold water leaves the unit at $\theta_p = 10 + 0.6 \cdot 27 = 26$ °C.


The Passive House Institute certifies drain water heat recovery units at **equal flow on both sides, 8 L/min**, and sorts them into efficiency classes from phA+ to phC {cite:p}`phi-dwhr`.

An alternative source is the [searchable product list of Natural Resources Canada](https://spl-lpi.nrcan-rncan.gc.ca/en-US/product/?product=Drain-WaterHeatRecovery&page=1) {cite:p}`nrcan-dwhr`. It lists many more units, mostly vertical ones from North American makers, tested to the Canadian standard CSA B55.1. For each unit it gives the heat recovery efficiency (the same quantity as the effectiveness here), the heat recovery rate in kW, the length and diameter, and an energy credit for two shower flows. The test conditions differ from the Passive House test, so compare units within one list, not across the two.


{numref}`tab-dwhr-products` shows two certified units of different types at a different price points.

:::{table} Two drain water heat recovery units certified by the Passive House Institute. Effectiveness and pressure loss are the certified values at 8 L/min with equal flow {cite:p}`phi-dwhr`. Prices are unit prices from web shops in October 2026, without installation.
:label: tab-dwhr-products
:align: center

| Unit | Type | PHI class | Effectiveness at 8 L/min | Pressure loss (bar) | Unit price |
|---|---|---|---|---|---|
| Showersave QB1-21XE | Vertical, 2.1 m | phA | 0.70 | 0.26 | £662 incl. VAT |
| Joulia-Inline 5 | Channel drain | phC | 0.41 | 0.28 | €3,005 incl. VAT |
:::



### The ε-NTU method

The ε-NTU method is used when the two flows are *not* equal.

Then, a heat exchanger is described by two numbers. The *heat capacity ratio* compares the two flows,

$$
C_r = \frac{C_{min}}{C_{max}}, \qquad C = \rho\,\dot V\,c_p
$$

and the *number of transfer units* compares the heat transfer surface with the smaller flow,

$$
NTU = \frac{UA}{C_{min}}
$$

where $UA$ is the overall heat transfer coefficient times the area, in W/K. A large $NTU$ means a large surface for the flow it has to heat.

For a counterflow heat exchanger, the effectiveness follows from these two numbers alone:

$$
\varepsilon = \frac{1 - \exp\left[-NTU\,(1 - C_r)\right]}{1 - C_r\,\exp\left[-NTU\,(1 - C_r)\right]}
$$ (eq-dwhr-ntu-general)

and the heat transferred is $\Phi = \varepsilon\,C_{min}\,(\theta_d - \theta_c)$.

When the flows are equal, $C_r = 1$, then equation {eq}`eq-dwhr-ntu-general` becomes 0/0. Taking the limit $C_r \to 1$ gives the much simpler

$$
\varepsilon = \frac{NTU}{1 + NTU}
\qquad\Longleftrightarrow\qquad
NTU = \frac{\varepsilon}{1 - \varepsilon}
$$ (eq-dwhr-ntu)

The second form turns a certified effectiveness into the size of the heat exchanger. A unit certified at $\varepsilon = 0.60$ at 8 L/min has $NTU = 0.60/0.40 = 1.5$, so its $UA$ equals the heat capacity rate of 12 L/min of water.

Now feed the same unit with unequal flows. Take the shower from before, 8 L/min at 40 °C with drain water at 37 °C and cold water at 10 °C, but connect the unit so that the preheated water goes only to the cold inlet of the shower mixer (connection 1 in {numref}`fig-dwhr-connections` below). The water heater delivers 55 °C and is still fed with cold mains water.

**Step 1: the mixer sets the cold-side flow.** All 8 L/min go down the drain, but only the cold part of the shower water passes the unit. A thermostatic mixer blends a flow $\dot V_h$ of hot water at 55 °C with a flow $\dot V_p$ of preheated water at $\theta_p$, so that the mix is 40 °C. A mass and energy balance on the mixer gives

$$
\dot V_h + \dot V_p = 8 \text{ L/min}, \qquad
\dot V_h \cdot 55 + \dot V_p\,\theta_p = 8 \cdot 40
\qquad\Rightarrow\qquad
\dot V_p = 8\,\frac{55 - 40}{55 - \theta_p} \text{ L/min}
$$ (eq-dwhr-mixer)

The warmer the preheated water, the more of it the mixer takes. Without the unit, $\theta_p = 10$ °C and $\dot V_p = 2.67$ L/min. With $\theta_p = 30$ °C, $\dot V_p = 4.8$ L/min.

**Step 2: the heat exchanger sets the preheat temperature.** The drain side carries 8 L/min and the cold side $\dot V_p$, so the cold side has the smaller heat capacity rate, $C_{min} = \rho c_p \dot V_p$.

The size of the unit, $UA$, comes from its certificate: $\varepsilon = 0.60$ at equal flows of 8 L/min gives $NTU = 1.5$, so $UA = 1.5 \cdot \rho c_p \cdot 8 = \rho c_p \cdot 12$ L/min.

It is convenient to write $UA$ as the heat capacity rate of 12 L/min of water, because $\rho c_p$ then cancels in $NTU$. $UA$ is assumed unchanged, since the drain side still carries the 8 L/min of the test. Then

$$
NTU = \frac{12}{\dot V_p}, \qquad C_r = \frac{\dot V_p}{8}
$$

and equation {eq}`eq-dwhr-ntu-general` gives $\varepsilon$. The effectiveness then gives the preheat temperature. The heat transferred can be written in two ways: from the definition of effectiveness, and as the heat picked up by the cold water, which warms from $\theta_c$ to $\theta_p$:

$$
\Phi = \varepsilon\,C_{min}\,(\theta_d - \theta_c) = C_{cold}\,(\theta_p - \theta_c)
$$

Here the cold side is the smaller flow, $C_{cold} = C_{min}$, so $C_{min}$ cancels:

$$
\theta_p = \theta_c + \varepsilon\,(\theta_d - \theta_c) = 10 + \varepsilon \cdot (37 - 10)
$$ (eq-dwhr-tp)

This is the same expression as for equal flows in equation {eq}`eq-dwhr-eps`. It holds whenever the cold side is the smaller flow. If the cold side were the larger flow, $C_{min}$ would be the drain side, and the cold water would be heated by only $\varepsilon\,C_r\,(\theta_d - \theta_c)$.

**Step 3: solve the two together.** Equation {eq}`eq-dwhr-mixer` needs $\theta_p$ to give the flow, and step 2 needs the flow to give $\theta_p$. The simplest way is to guess $\theta_p$, compute the flow, compute a new $\theta_p$, and repeat ({numref}`tab-dwhr-iteration`). The first guess, no preheat, gives a small flow, which the large unit heats almost to the drain temperature. That makes the mixer take much more preheated water in the next round, which is then heated less. The guesses swing back and forth around the answer and settle after about eight rounds.

```{list-table} Iteration for connection 1, unit with $\varepsilon = 0.60$ at equal flow 8 L/min
:header-rows: 1
:label: tab-dwhr-iteration

* - Round
  - Guess $\theta_p$ (°C)
  - $\dot V_p$ (L/min)
  - $NTU$
  - $C_r$
  - $\varepsilon$
  - New $\theta_p$ (°C)
* - 1
  - 10.0
  - 2.67
  - 4.50
  - 0.33
  - 0.97
  - 36.1
* - 2
  - 36.1
  - 6.35
  - 1.89
  - 0.79
  - 0.70
  - 28.9
* - 3
  - 28.9
  - 4.59
  - 2.61
  - 0.57
  - 0.83
  - 32.4
* - 4
  - 32.4
  - 5.30
  - 2.26
  - 0.66
  - 0.77
  - 30.9
* - …
  -
  -
  -
  -
  -
  -
* - 10
  - 31.3
  - 5.07
  - 2.37
  - 0.63
  - 0.79
  - 31.3
```

In practice the next guess can be taken halfway between the old and the new $\theta_p$, which removes the swings and gets within 0.1 K in five rounds.

**Step 4: check and compare.** The answer is $\theta_p = 31.3$ °C on a cold-side flow of 5.07 L/min, and indeed $8 \cdot 15/(55 - 31.3) = 5.07$ L/min. Compared with the balanced connection:

| | Balanced (connection 3) | Mixer only (connection 1) |
|---|---|---|
| Cold-side flow | 8.0 L/min | 5.07 L/min |
| $C_r$ | 1 | 0.63 |
| $NTU$ | 1.5 | 2.37 |
| Effectiveness $\varepsilon$ | 0.60 | 0.79 |
| Preheated water $\theta_p$ | 26.2 °C | 31.3 °C |
| Drain water leaving the unit | 20.8 °C | 23.5 °C |
| Heat recovered $\Phi$ | 9.0 kW | 7.5 kW |

The effectiveness rises from 0.60 to 0.79 and the cold water gets 5 K warmer, but the heat recovered falls from 9.0 kW to 7.5 kW, because less water is heated. The drain water leaves the unit warmer, which shows that more heat goes down the drain. A higher effectiveness does not mean more heat recovered: always compare $\Phi$, not $\varepsilon$, when the flows differ.



## Connecting the unit

The preheated water can go to three places ({numref}`fig-dwhr-connections`):

1. **To the cold side of the shower mixer only.** The water heater is still fed with cold mains water.
2. **To the water heater only.** The shower mixer is still fed with cold mains water.
3. **To both.** All the water that ends up in the shower has passed through the unit, so the flow on the cold side equals the flow down the drain. This is called *equal flow* or *balanced* connection.

:::{figure} figures/c3/dwhr-connections.png
:label: fig-dwhr-connections
:alt: Three schematics side by side, each with a water heater at 55 °C, a shower mixer at 40 °C, an 8 L/min shower, a drain at 37 °C and a DWHR unit. In connection 1, preheated water (5.1 L/min at 31 °C) goes only to the mixer, and the heat from the water heater is cut by 45 %. In connection 2, preheated water (5.3 L/min at 31 °C) goes only to the water heater, and the heat is cut by 46 %. In connection 3, preheated water (8.0 L/min at 26 °C) goes to both, and the heat is cut by 54 %.
:width: 100%

The three ways of connecting a drain water heat recovery unit with an effectiveness of 0.60 at 8 L/min. Shower at 40 °C and 8 L/min, drain water at 37 °C, cold water at 10 °C, water heater at 55 °C. Calculated with the model in the dropdown at the end of the section. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dwhr_figures.py)
:::


### Effectiveness increases with lower shower flow

A unit with $\varepsilon = 0.70$ has $NTU = 0.70/0.30 = 2.3$, and one with $\varepsilon = 0.41$ has $NTU = 0.7$. When the shower flow rises, $C$ rises in proportion. $UA$ also rises, because faster water transfers heat better, but less than in proportion. So $NTU$ falls, and the effectiveness with it. {numref}`fig-dwhr-effectiveness` (left) shows this for the two units of {numref}`tab-dwhr-products`, assuming $UA$ grows with the square root of the flow. A low-flow shower head therefore saves twice: it uses less hot water, and the unit recovers a larger share of the heat in the water that is used.


{numref}`fig-dwhr-effectiveness` (right) shows the saving for all three connections over the range of certified effectiveness. The balanced connection is always best. For units with a low effectiveness, connection 2 (to the water heater) is slightly better than connection 1; for the best units it is the other way round. In practice the choice is often made by the pipe layout. Connection 1 needs only a short pipe from the unit to the shower mixer, and connection 2 needs a pipe from the unit to the water heater, which may be far away. Connection 3 needs both, and it is the one to aim for in a new building.
:::{figure} figures/c3/dwhr-effectiveness.png
:label: fig-dwhr-effectiveness
:alt: Two line charts. Left: effectiveness against shower flow from 4 to 14 L/min for the two certified units, each falling with flow and passing through its certified value at 8 L/min: Showersave QB1-21XE (vertical) from 0.77 to 0.64, Joulia-Inline 5 (channel) from 0.50 to 0.34. Right: percentage of shower heat saved against certified effectiveness from 0.3 to 0.75 for the three connections; equal flow rises from 27 % to 68 %, the other two from about 23–25 % to 55–57 %, crossing near 0.66. Dashed vertical lines mark Joulia-Inline at 0.41 and Showersave at 0.70.
:width: 100%

Left: effectiveness at equal flow against shower flow for the two units in {numref}`tab-dwhr-products`, from the certified value at 8 L/min with $UA$ proportional to the square root of the flow. Right: share of the shower heat saved for the three connections, with the two units marked, for an 8 L/min shower at 40 °C, drain water at 37 °C and cold water at 10 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dwhr_figures.py)
:::

## How much does it save?

The annual saving is the shower heat times the saving fraction:

$$
Q_{saved} = s\,Q_{shower}
$$ (eq-dwhr-annual)

where $Q_{shower}$ is the heat for showers over the year, $Q = \rho\,V\,c_p\,(\theta_{mix} - \theta_c)$ summed over all showers. Showers are the largest single use of hot water in most homes, typically half to two-thirds of the hot water heat. One 8-minute shower at 8 L/min and 40 °C takes 2.2 kWh ({numref}`tab-dhw-tappings`). A person who showers on three days out of four uses about 600 kWh a year for showers, and a balanced unit with $\varepsilon = 0.5$ saves 45 % of that, about 270 kWh per person per year.

The saving varies over the year with the cold water temperature. With cold water at 5 °C in late winter, the unit with $\varepsilon = 0.5$ warms it by 16 K; at 15 °C in late summer, by 11 K. The *fraction* saved hardly changes (equation {eq}`eq-dwhr-saving` gives 46 % and 44 %), because the shower also needs more heat in winter.

What the saved heat is worth depends on how the water is heated. With an electric resistance heater, every kWh of heat saved is a kWh of electricity saved. With a heat pump that delivers hot water at a COP of 2.5, it is only 0.4 kWh of electricity. Drain water heat recovery therefore pays back two to three times faster in a house with an electric water heater than in a heat pump house. In a heat pump house, it competes with the heat pump: both are ways of not buying the same kWh of heat.

Drain water heat recovery also helps when the tank is used as a thermal battery, as in [Domestic hot water](c2-domestic-hot-water.md). It cuts the heat drawn from the tank during each shower, by about half with a good balanced unit, so the tank needs to store less heat to cover the evening showers from a charge in cheap hours. A smaller tank also has a smaller standing loss.

<!-- :::{admonition} Rules of thumb
:class: tip

- Certified units have an effectiveness of 0.4–0.7 at 8 L/min. The best vertical and horizontal units are not far apart, but the spread within each type is large.
- Effectiveness falls as the flow rises: about 0.05 lower at 12 L/min than at 8 L/min.
- With equal flow, a unit saves about 0.9 times its effectiveness of the shower heat. Feeding only the mixer or only the water heater saves about a sixth less.
- A good balanced unit saves 200–300 kWh of heat per person per year.
- A saved kWh of heat is worth a kWh of electricity with a resistance heater, but only about 0.4 kWh with a heat pump.
:::
 -->
## Worked example: channel drain or vertical pipe?

A family of four in a 150 m² house takes three showers a day, the same as in the tank sizing example in [Domestic hot water](c2-domestic-hot-water.md). Each shower lasts 8 minutes at 8 L/min and 40 °C, and the cold water is 10 °C on average. They are rebuilding the bathroom and consider two options:

- **A.** A Joulia-Inline 5 channel drain ($\varepsilon = 0.41$), connected to the shower mixer only, because the water heater is on the other side of the house (connection 1).
- **B.** A Showersave QB1-21XE vertical unit ($\varepsilon = 0.70$) in the basement below the bathroom, connected to both the mixer and the water heater (connection 3).

How much heat and electricity does each save per year, with an electric water heater and with a heat pump at a COP of 2.5? What are the simple paybacks with electricity at 2.50 DKK/kWh?

**Shower heat.** One shower takes $64 \cdot 1.155 \cdot (40 - 10) = 2\,217$ Wh. Three a day for a year is $3 \cdot 365 \cdot 2.217 = 2\,428$ kWh.

**Option B.** Balanced connection, so equation {eq}`eq-dwhr-saving` applies directly:

$$
\theta_p = 10 + 0.70 \cdot (37 - 10) = 28.9 \text{ °C}, \qquad s = \frac{28.9 - 10}{40 - 10} = 0.63
$$

The unit saves $0.63 \cdot 2\,428 = 1\,529$ kWh of heat per year.

**Option A.** Only the cold-water side of the mixer passes the unit, so the flows are unbalanced and the mixing ratio depends on the preheat. Solving the model in the dropdown gives a preheat to 27.2 °C on a cold-side flow of 4.3 L/min, and $s = 0.31$. The unit saves $0.31 \cdot 2\,428 = 752$ kWh of heat per year. Connected for equal flow, the same unit would have saved 37 %.

**Electricity and payback.** The incremental installed costs are estimates: about 9,000 DKK for option B (unit about 5,700 DKK, plus fitting it into the drain stack and the extra pipe to the water heater), and about 20,000 DKK for option A (unit about 22,400 DKK, minus the 3,000–4,000 DKK of the ordinary channel drain it replaces, plus the cold water connection).

| | Heat saved (kWh/year) | Electricity saved, resistance heater (kWh/year) | Payback (years) | Electricity saved, heat pump COP 2.5 (kWh/year) | Payback (years) |
|---|---|---|---|---|---|
| A: channel drain, to mixer | 752 | 752 | 10.6 | 301 | 27 |
| B: vertical pipe, balanced | 1 529 | 1 529 | 2.4 | 612 | 5.9 |

Option B saves twice the heat at less than half the cost. With a heat pump, option A does not pay back within the lifetime of a bathroom. The example shows the three things that decide the result: the effectiveness of the unit, the connection, and the price of the heat that is saved.

<!-- ## Guiding questions

- Why does a vertical unit usually have a higher effectiveness than a horizontal one of the same length? Why is the horizontal one still often chosen?
- Explain, with the effectiveness of the unit and the flows on each side, why the balanced connection saves the most.
- A family takes baths instead of showers. How much does a drain water heat recovery unit save, and why?
- A low-flow shower head cuts the flow from 12 to 8 L/min. Does the unit then save more or less heat per shower? Does it save a larger or smaller share?
- Does drain water heat recovery pay back faster in a house with an electric water heater or with a heat pump? What about a flat on district heating?
- Repeat the tank sizing worked example in [Domestic hot water](c2-domestic-hot-water.md) with a balanced unit with $\varepsilon = 0.6$ on all three showers. How much smaller can the tank be with night charging?
 -->
:::{dropdown} The shower model behind the figures
The model is a steady state shower at flow $\dot V$ and mixed temperature $\theta_{mix}$, drain water at $\theta_d$, cold water at $\theta_c$ and a water heater at $\theta_h$. The unit is a counterflow heat exchanger described by equation {eq}`eq-dwhr-ntu-general`. $UA$ is fitted to the certified effectiveness $\varepsilon_8$ at 8 L/min and equal flow, $UA_8 = C_8\,\varepsilon_8/(1 - \varepsilon_8)$, and scaled with the drain flow as $UA = UA_8\,(\dot V/8)^{0.5}$. In all three connections the cold side has the smaller (or equal) flow, so the preheat is $\theta_p = \theta_c + \varepsilon\,(\theta_d - \theta_c)$ with $\varepsilon$ evaluated for that flow.

- **Connection 3:** cold-side flow $\dot V$, heat needed $C(\theta_{mix} - \theta_p)$.
- **Connection 2:** cold-side flow $\dot V_h = \dot V(\theta_{mix} - \theta_c)/(\theta_h - \theta_c)$, fixed by the mixer; heat needed $\rho\,\dot V_h\,c_p(\theta_h - \theta_p)$.
- **Connection 1:** cold-side flow $\dot V_c = \dot V(\theta_h - \theta_{mix})/(\theta_h - \theta_p)$, which depends on $\theta_p$. Start with $\theta_p = \theta_c$ and repeat: compute $\dot V_c$, then $\varepsilon$, then a new $\theta_p$, until it no longer changes. Heat needed $\rho\,(\dot V - \dot V_c)\,c_p(\theta_h - \theta_c)$.

The saving fraction is one minus the heat needed with the unit, divided by $C(\theta_{mix} - \theta_c)$. The model keeps $UA$ independent of the cold-side flow, so it slightly flatters the two unbalanced connections: in a real unit, a smaller cold-side flow also gives a lower heat transfer coefficient on that side. The same model in Python can be downloaded here: {download}`dwhr_model.py <code/dwhr_model.py>`.
:::
