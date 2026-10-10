# Domestic hot water

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## Introduction

For most of the twentieth century, domestic hot water was a small item in the heat budget of a Danish house. A typical older house with energy label D needs around 150 kWh of space heating per m² of floor area per year. Hot water adds 13 kWh/m², less than a tenth of the total.

Better houses have changed the picture ({numref}`fig-dhw-share`). Insulation, airtightness and heat recovery ventilation have cut the space heating demand of a passive house to 15 kWh/m², and of a house in the Danish low-energy class to about 10 kWh/m². The hot water demand has not changed, because it depends on the people living in the house and not on its envelope. A family takes the same showers in a passive house as in a house from 1965. In a passive house hot water is therefore close to half of the heat demand, and in a low-energy class house it is more than half.

:::{figure} figures/ch04/dhw-share.*
:label: fig-dhw-share
:alt: Horizontal stacked bar chart of net heat demand per m² floor area per year. A house with energy label D has 150 kWh/m² of space heating and 13 kWh/m² of hot water, so hot water is 8 %. A passive house has 15 kWh/m² of space heating, so hot water is 46 %. A house in the Danish low-energy class has 10 kWh/m² of space heating, so hot water is 57 %.
:width: 100%

Net heat demand for space heating and domestic hot water in three Danish house standards. The label D value is an estimate for a 150 m² house in the middle of the D band. The hot water demand is the Be18 calculation value of 250 L/m² per year heated from 10 °C to 55 °C {cite:p}`build213`. Losses from the tank and pipes are not included.
:::

:::{admonition} Hot water in Building Code
:class: dropdown
The Danish energy frame calculation (Be18) uses a fixed hot water demand of 250 L per m² of heated floor area per year, heated from 10 °C to 55 °C {cite:p}`build213`. With equation {eq}`eq-dhw-energy` and the average properties of water between 10 °C and 55 °C this is

$$
Q = \bar\rho\,V\,\bar c_p\,(\theta - \theta_c) = \frac{994 \cdot 0.250 \cdot 4.182 \cdot (55 - 10)}{3600} = 13.0 \text{ kWh/(m}^2\,\text{year)}
$$

For a 150 m² house it amounts to 2000 kWh per year, or about 100 L of 55 °C water per day which is a reasonable figure for a family of three or four.

However, measured hot water use varies by a factor of two or three between households of the same size, and it depends much more on the number of occupants, their age and their habits than on the floor area.
:::

<!-- The temperature also matters. A floor heating system in a low-energy house runs at 30–35 °C (Chapter 3). Hot water must be stored at 50–55 °C or more to keep Legionella bacteria from growing. When the same heat pump supplies both, the hot water is the expensive part of its work, because the efficiency of a heat pump falls as the temperature it delivers rises. In an all-electric low-energy house, hot water can easily use as much electricity as space heating.

There are two ways to cut the cost of hot water, and this chapter is built around them:

- **Use less heat.** Shower water leaves the house at about 30 °C, at the same moment as cold water comes in. A drain water heat recovery unit passes that heat to the incoming cold water. This is Part A of the chapter.
- **Buy the heat at the right time.** Electricity prices vary over the day, with a peak in the early evening, which is exactly when many families shower. A well-sized hot water tank can be charged in cheap hours and emptied in expensive ones. This is Part B.

The next section sets out how much hot water a dwelling uses and how fast it is drawn, which both parts build on.
 -->

<!-- ## How much hot water?

### Energy in a tapping

The heat needed to warm a mass $m$ of water from the cold water temperature $\theta_c$ to the temperature $\theta$ at the tap is

$$
Q = m\,c_p\,(\theta - \theta_c)
$$ (eq-dhw-energy)

where $m = \rho\,V$. Both the density $\rho$ and the specific heat capacity $c_p$ of water vary with temperature. Between 10 °C and 55 °C the density falls from 999.7 to 985.7 kg/m³, while $c_p$ stays close to 4.18 kJ/(kg·K). For hot water calculations we use the averages over that range, $\bar\rho = 994$ kg/m³ and $\bar c_p = 4.182$ kJ/(kg·K). One litre of water warmed by 1 K then takes 4.16 kJ, or 1.15 Wh. The cold water from Danish waterworks is about 8–10 °C as a yearly average, with a seasonal swing from around 5 °C in late winter to 15 °C in late summer.

At the tap, the user mixes hot water from the tank with cold water to get the temperature they want, typically 38–40 °C for a shower and 45 °C for washing up. The fraction of hot water in the mix follows from an energy balance:

$$
f_h = \frac{\theta_{mix} - \theta_c}{\theta_h - \theta_c}
$$ (eq-dhw-mix)

With the tank at 55 °C and cold water at 10 °C, a 40 °C shower is two-thirds hot water and one-third cold. Equation {eq}`eq-dhw-energy` gives the same energy whether it is applied to the mixed water at 40 °C or to the hot water fraction at 55 °C, so either can be used. What matters is to be clear which one a consumption figure refers to. Water use statistics are usually given at the tap, while calculation standards usually give litres at 55 °C or 60 °C.
 -->


### Power when tapping

The energy per day is modest. The power during a tapping is not. The heat flow needed to warm water flowing at a volume flow $\dot V$ is

$$
\Phi = \rho\,\dot V\,c_p\,(\theta - \theta_c)
$$ (eq-dhw-power)

{numref}`tab-dhw-tappings` shows the energy and the power for some typical tappings. A shower at 8 L/min needs about 17 kW while it runs, and filling a bath needs about 25 kW.

:::{table} Energy and power for typical tappings, with cold water at 10 °C.
:label: tab-dhw-tappings
:align: center

| Tapping | Flow (L/min) | Temperature (°C) | Volume (L) | Energy (kWh) | Power while tapping (kW) |
|---|---|---|---|---|---|
| Washing hands | 5 | 35 | 3 | 0.09 | 8.7 |
| Washing up by hand | 6 | 45 | 10 | 0.40 | 14.5 |
| Shower, 8 minutes | 8 | 40 | 64 | 2.2 | 16.6 |
| Bath | 12 | 40 | 120 | 4.2 | 24.9 |
:::

These powers are far larger than anything else in the heating system of a low-energy house. The whole house may need only 2–3 kW of space heating on the coldest day, and a heat pump sized for that cannot heat a shower as it runs. There are two ways out:

- **Instantaneous heating.** District heating can deliver 30–40 kW through a heat exchanger in a flat station, so the water is heated as it is used and nothing is stored.
- **Storage.** A heat pump or a small boiler heats a tank slowly, over hours, and the tank delivers the high power during the tapping. The tank decouples the power the heat source must deliver from the power the user draws.

<!-- Storage is what makes it possible to choose *when* the heat source runs, which is the topic of Part B. Showers are what make drain water heat recovery worthwhile, which is the topic of Part A. They are the largest single hot water use in most homes, and they are the one use where the warm waste water flows to the drain at the same moment as the cold water comes in.
 -->
:::{admonition} Rules of thumb
:class: tip

- 1 L of water warmed by 1 K takes about 1.15 Wh. 100 L warmed by 45 K takes about 5 kWh.
- One 8-minute shower uses about 60 L of 40 °C water, which is 40 L of 55 °C water and about 2 kWh of heat.
- Hot water use is about 30–40 L of 55 °C water per person per day, or about 550–750 kWh per person per year before losses.
- The Be18 calculation value is 13 kWh/m² per year, about 2000 kWh per year for a 150 m² house.
- A shower draws about 15–20 kW while it runs, several times the design heat load of a low-energy house.
:::

## Drain water heat recovery

When you take a shower, about 8 L of water at 40 °C leaves the shower head every minute. A few seconds later the same water runs down the drain at 35–38 °C, having lost only a few kelvin on its way through the air and over your skin. At the same moment, 8 L of cold water at about 10 °C enters the house to replace it. A drain water heat recovery unit is a heat exchanger between these two flows. It needs no storage, no pump and no control, because the two flows are there at the same time and stop at the same time. It only works for tappings with that property, and in a home that means showers. A bath is filled first and emptied later, and a kitchen sink or a washbasin draws little water at a time.

### How a unit works

{numref}`fig-dwhr-units` shows the two main types.

**Vertical units** replace about 1.5–2 m of the vertical drain pipe below the shower. The inner pipe is copper. Water falling down a vertical pipe does not fill it, but spreads into a thin film that clings to the wall, so almost all of the copper surface is wetted by a thin, fast-moving layer of warm water. The cold water flows upwards in a coil or a narrow annulus around the pipe, in counterflow to the drain water. This is a good heat exchanger, and the best vertical units recover 70 % of the heat that could at most be recovered. The catch is that a vertical unit needs a storey of straight vertical drain below the shower, which means a basement or a floor below. It suits a house with a basement and an apartment block where the bathrooms are stacked.

**Horizontal units** sit in the floor, under a shower tray or in a channel drain. They fit a slab-on-ground house and a bathroom renovation. In a channel drain, the heat exchanger is a row of copper tubes along the bottom of the channel, with the cold water flowing inside them against the direction of the drain water. The drain water flows around and over the tubes in a shallow layer. The unit is short, typically 0.7–0.9 m, and the water in the channel moves slowly, so it has less length and less turbulence to give off its heat than the falling film in a vertical pipe. Some manufacturers add turbulators between the tubes to stir the flow. The lower the shower flow, the thinner the water layer around the tubes and the higher the effectiveness. The better horizontal units still reach about 60 %.

:::{figure} figures/ch04/dwhr-units.png
:label: fig-dwhr-units
:alt: Two schematic sections. Left, a vertical unit in section: a copper drain pipe with air in the middle, a thin film of warm drain water running down the inside of the wall, and a copper coil with cold water wound around the outside. Drain water enters at the top at 37 °C and leaves at the bottom at 18 °C; cold water enters at the bottom at 10 °C and leaves at the top at 29 °C. Right, a horizontal unit in a shower channel drain, shown along the channel and in a cross-section: shower water falls through the grate and runs along the channel over a row of copper tubes in the channel bottom, in which the cold water flows the opposite way. Drain water leaves at 24 °C, cold water enters at 10 °C and leaves at 24 °C. The cross-section shows the drain water flowing around and over the tubes. A legend gives orange for warm drain water, blue for cold drinking water and brown for the copper walls.
:width: 100%

A vertical unit (left) and a horizontal unit in a shower channel drain (right). Temperatures are for an 8 L/min shower with equal flow on both sides, an effectiveness of 0.70 for the vertical unit and 0.50 for the horizontal one.
:::

Both types must keep the drinking water safe if the wall between the two flows fails. Certified units therefore have a double wall with a vented gap between the drain water and the drinking water, so a leak shows up as water dripping out of the gap rather than as sewage in the drinking water. The drain side gets a film of soap, skin fat and hair over time. A vertical unit is largely self-cleaning, because the falling water scours the wall, while a horizontal unit needs the grate and the channel cleaned as part of normal bathroom cleaning. On the cold side, the unit adds a pressure loss of about 0.1–0.4 bar at shower flow.

### Effectiveness

How good a unit is, is expressed by its *effectiveness*: the heat it actually transfers, divided by the most heat that could be transferred. The most that could be transferred is the heat that would cool the drain water all the way down to the cold water temperature, or warm the cold water all the way up to the drain water temperature, whichever flow has the smaller heat capacity rate $C = \rho\,\dot V\,c_p$. When the two flows are equal, the heat flow transferred is

$$
\Phi = \varepsilon\, C\,(\theta_d - \theta_c)
\qquad\text{and}\qquad
\varepsilon = \frac{\theta_p - \theta_c}{\theta_d - \theta_c}
$$ (eq-dwhr-eps)

where $\theta_d$ is the drain water temperature entering the unit, $\theta_c$ the cold water temperature and $\theta_p$ the temperature of the preheated cold water leaving it. With drain water at 37 °C, cold water at 10 °C and $\varepsilon = 0.6$, the cold water leaves the unit at $10 + 0.6 \cdot 27 = 26$ °C.

The Passive House Institute certifies drain water heat recovery units at equal flow on both sides, 8 L/min, and sorts them into efficiency classes from phA+ to phC {cite:p}`phi-dwhr`. {numref}`tab-dwhr-products` shows five certified units of different types.

:::{table} Five drain water heat recovery units certified by the Passive House Institute. Effectiveness and pressure loss are the certified values at 8 L/min with equal flow {cite:p}`phi-dwhr`. Prices are unit prices from web shops in October 2026, without installation; no Danish dealer was found.
:label: tab-dwhr-products
:align: center

| Unit | Type | PHI class | Effectiveness at 8 L/min | Pressure loss (bar) | Unit price |
|---|---|---|---|---|---|
| Showersave QB1-21XE | Vertical, 2.1 m | phA | 0.70 | 0.26 | £662 incl. VAT |
| ACO ShowerDrain X2.2 PHI | Channel drain | phB | 0.60 | 0.25 | not found |
| Zypho Slim 50 DW | Under shower tray | phB | 0.54 | 0.38 | £896 incl. VAT |
| Zypho PiPe 60 DW | Vertical, 1.6 m | phB | 0.53 | 0.07 | €982 |
| Joulia-Inline 5 | Channel drain | phC | 0.41 | 0.28 | €3,005 incl. VAT |
:::

The table holds two surprises. The type matters less than the individual design: the best channel drain beats the shorter of the two vertical pipes. And price says nothing about performance: the most expensive unit has the lowest effectiveness.

#### The ε-NTU method

A heat exchanger is described by two numbers. The *heat capacity ratio* compares the two flows,

$$
C_r = \frac{C_{min}}{C_{max}}, \qquad C = \rho\,\dot V\,c_p
$$

and the *number of transfer units* compares the heat transfer surface with the smaller flow,

$$
NTU = \frac{UA}{C_{min}}
$$

where $UA$ is the overall heat transfer coefficient times the area, in W/K. A large $NTU$ means a large surface for the flow it has to heat. For a counterflow heat exchanger, the effectiveness follows from these two numbers alone:

$$
\varepsilon = \frac{1 - \exp\left[-NTU\,(1 - C_r)\right]}{1 - C_r\,\exp\left[-NTU\,(1 - C_r)\right]}
$$ (eq-dwhr-ntu-general)

and the heat transferred is $\Phi = \varepsilon\,C_{min}\,(\theta_d - \theta_c)$. When the flows are equal, $C_r = 1$ and equation {eq}`eq-dwhr-ntu-general` becomes 0/0. Taking the limit $C_r \to 1$ gives the much simpler

$$
\varepsilon = \frac{NTU}{1 + NTU}
\qquad\Longleftrightarrow\qquad
NTU = \frac{\varepsilon}{1 - \varepsilon}
$$ (eq-dwhr-ntu)

The second form turns a certified effectiveness into the size of the heat exchanger. A unit certified at $\varepsilon = 0.60$ at 8 L/min has $NTU = 0.60/0.40 = 1.5$, so its $UA$ equals the heat capacity rate of 12 L/min of water.

Now feed the same unit with unequal flows: 8 L/min of drain water, but only the 5.33 L/min that goes to the water heater on the cold side (connection 2 below). If $UA$ stays the same, $NTU = 12/5.33 = 2.25$ and $C_r = 5.33/8 = 0.67$, and equation {eq}`eq-dwhr-ntu-general` gives $\varepsilon = 0.77$. The smaller cold flow is heated to $10 + 0.77 \cdot 27 = 30.8$ °C instead of 26.2 °C, but the heat transferred falls from 9.0 kW to 7.7 kW, because less water is heated. A higher effectiveness does not mean more heat recovered: always compare $\Phi$, not $\varepsilon$, when the flows differ.

#### Why effectiveness falls with flow

A unit with $\varepsilon = 0.70$ has $NTU = 0.70/0.30 = 2.3$, and one with $\varepsilon = 0.41$ has $NTU = 0.7$. When the shower flow rises, $C$ rises in proportion. $UA$ also rises, because faster water transfers heat better, but less than in proportion. So $NTU$ falls, and the effectiveness with it. {numref}`fig-dwhr-effectiveness` (left) shows this for the five units of {numref}`tab-dwhr-products`, assuming $UA$ grows with the square root of the flow. A low-flow shower head therefore saves twice: it uses less hot water, and the unit recovers a larger share of the heat in the water that is used.

### Connecting the unit

The preheated water can go to three places ({numref}`fig-dwhr-connections`):

1. **To the cold side of the shower mixer only.** The water heater is still fed with cold mains water.
2. **To the water heater only.** The shower mixer is still fed with cold mains water.
3. **To both.** All the water that ends up in the shower has passed through the unit, so the flow on the cold side equals the flow down the drain. This is called *equal flow* or *balanced* connection.

:::{figure} figures/ch04/dwhr-connections.png
:label: fig-dwhr-connections
:alt: Three schematics side by side, each with a water heater at 55 °C, a shower mixer at 40 °C, an 8 L/min shower, a drain at 37 °C and a DWHR unit. In connection 1, preheated water (5.1 L/min at 31 °C) goes only to the mixer, and the heat from the water heater is cut by 45 %. In connection 2, preheated water (5.3 L/min at 31 °C) goes only to the water heater, and the heat is cut by 46 %. In connection 3, preheated water (8.0 L/min at 26 °C) goes to both, and the heat is cut by 54 %.
:width: 100%

The three ways of connecting a drain water heat recovery unit with an effectiveness of 0.60 at 8 L/min. Shower at 40 °C and 8 L/min, drain water at 37 °C, cold water at 10 °C, water heater at 55 °C. Calculated with the model in the dropdown at the end of the section.
:::

In connection 3 the calculation is simple. All the water the shower uses enters the house at $\theta_p$ instead of $\theta_c$, so the heat needed for the shower falls from $C(\theta_{mix} - \theta_c)$ to $C(\theta_{mix} - \theta_p)$. The fraction of the shower heat that is saved is

$$
s = \frac{\theta_p - \theta_c}{\theta_{mix} - \theta_c} = \varepsilon\,\frac{\theta_d - \theta_c}{\theta_{mix} - \theta_c}
$$ (eq-dwhr-saving)

With $\theta_{mix} = 40$ °C, $\theta_d = 37$ °C and $\theta_c = 10$ °C, the last fraction is $27/30 = 0.9$, so a balanced unit saves 90 % of its effectiveness: 63 % of the shower heat for the best unit in {numref}`tab-dwhr-products`, 37 % for the poorest.

In connections 1 and 2 only part of the shower water passes the unit, about two-thirds at these temperatures. The flows in the heat exchanger are no longer equal. The smaller cold-side flow is heated to a higher temperature, so the effectiveness defined on the smaller flow goes up, but less water is heated, and the heat recovered goes down. Connection 1 has a further twist. When the mixer gets warmer cold water, the user's thermostatic mixer takes less hot water and more of the preheated water to hold 40 °C, which changes the flow through the unit again. In {numref}`fig-dwhr-connections`, the two unbalanced connections save 45–46 % of the shower heat, against 54 % for the balanced one.

{numref}`fig-dwhr-effectiveness` (right) shows the saving for all three connections over the range of certified effectiveness. The balanced connection is always best. For units with a low effectiveness, connection 2 (to the water heater) is slightly better than connection 1; for the best units it is the other way round. In practice the choice is often made by the pipe layout. Connection 1 needs only a short pipe from the unit to the shower mixer, and connection 2 needs a pipe from the unit to the water heater, which may be far away. Connection 3 needs both, and it is the one to aim for in a new building.

:::{figure} figures/ch04/dwhr-effectiveness.png
:label: fig-dwhr-effectiveness
:alt: Two line charts. Left: effectiveness against shower flow from 4 to 14 L/min for five certified units, each falling with flow and passing through its certified value at 8 L/min: Showersave QB1-21XE 0.77 to 0.64, ACO ShowerDrain X2.2 0.68 to 0.53, Zypho Slim 50 and Zypho PiPe 60 about 0.62 to 0.46, Joulia-Inline 5 0.50 to 0.34. Right: percentage of shower heat saved against certified effectiveness from 0.3 to 0.75 for the three connections; equal flow rises from 27 % to 68 %, the other two from about 23–25 % to 55–57 %, crossing near 0.66.
:width: 100%

Left: effectiveness at equal flow against shower flow for the five units in {numref}`tab-dwhr-products`, from the certified value at 8 L/min with $UA$ proportional to the square root of the flow. Right: share of the shower heat saved for the three connections, for an 8 L/min shower at 40 °C, drain water at 37 °C and cold water at 10 °C.
:::

### How much does it save?

The annual saving is the shower heat times the saving fraction:

$$
Q_{saved} = s\,Q_{shower}
$$ (eq-dwhr-annual)

where $Q_{shower}$ is the heat for showers over the year, $Q = \rho\,V\,c_p\,(\theta_{mix} - \theta_c)$ summed over all showers. Showers are the largest single use of hot water in most homes, typically half to two-thirds of the hot water heat. One 8-minute shower at 8 L/min and 40 °C takes 2.2 kWh ({numref}`tab-dhw-tappings`). A person who showers on three days out of four uses about 600 kWh a year for showers, and a balanced unit with $\varepsilon = 0.5$ saves 45 % of that, about 270 kWh per person per year.

The saving varies over the year with the cold water temperature. With cold water at 5 °C in late winter, the unit with $\varepsilon = 0.5$ warms it by 16 K; at 15 °C in late summer, by 11 K. The *fraction* saved hardly changes (equation {eq}`eq-dwhr-saving` gives 46 % and 44 %), because the shower also needs more heat in winter.

What the saved heat is worth depends on how the water is heated. With an electric resistance heater, every kWh of heat saved is a kWh of electricity saved. With a heat pump that delivers hot water at a COP of 2.5, it is only 0.4 kWh of electricity. Drain water heat recovery therefore pays back two to three times faster in a house with an electric water heater than in a heat pump house. In a heat pump house, it competes with the heat pump: both are ways of not buying the same kWh of heat.

Drain water heat recovery also helps when the tank is used as a thermal battery, later in this chapter. It cuts the heat drawn from the tank during each shower, by about half with a good balanced unit, so the tank needs to store less heat to cover the evening showers from a charge in cheap hours. A smaller tank also has a smaller standing loss.

:::{admonition} Rules of thumb
:class: tip

- Certified units have an effectiveness of 0.4–0.7 at 8 L/min. The best vertical and horizontal units are not far apart, but the spread within each type is large.
- Effectiveness falls as the flow rises: about 0.05 lower at 12 L/min than at 8 L/min.
- With equal flow, a unit saves about 0.9 times its effectiveness of the shower heat. Feeding only the mixer or only the water heater saves about a sixth less.
- A good balanced unit saves 200–300 kWh of heat per person per year.
- A saved kWh of heat is worth a kWh of electricity with a resistance heater, but only about 0.4 kWh with a heat pump.
:::

### Worked example: channel drain or vertical pipe?

A family of four in a 150 m² house takes three showers a day, the same as in the tank sizing example later in this chapter. Each shower lasts 8 minutes at 8 L/min and 40 °C, and the cold water is 10 °C on average. They are rebuilding the bathroom and consider two options:

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

### Guiding questions

- Why does a vertical unit usually have a higher effectiveness than a horizontal one of the same length? Why is the horizontal one still often chosen?
- Explain, with the effectiveness of the unit and the flows on each side, why the balanced connection saves the most.
- A family takes baths instead of showers. How much does a drain water heat recovery unit save, and why?
- A low-flow shower head cuts the flow from 12 to 8 L/min. Does the unit then save more or less heat per shower? Does it save a larger or smaller share?
- Does drain water heat recovery pay back faster in a house with an electric water heater or with a heat pump? What about a flat on district heating?
- Repeat the tank sizing worked example later in this chapter with a balanced unit with $\varepsilon = 0.6$ on all three showers. How much smaller can the tank be with night charging?

:::{dropdown} The shower model behind the figures
The model is a steady state shower at flow $\dot V$ and mixed temperature $\theta_{mix}$, drain water at $\theta_d$, cold water at $\theta_c$ and a water heater at $\theta_h$. The unit is a counterflow heat exchanger described by equation {eq}`eq-dwhr-ntu-general`. $UA$ is fitted to the certified effectiveness $\varepsilon_8$ at 8 L/min and equal flow, $UA_8 = C_8\,\varepsilon_8/(1 - \varepsilon_8)$, and scaled with the drain flow as $UA = UA_8\,(\dot V/8)^{0.5}$. In all three connections the cold side has the smaller (or equal) flow, so the preheat is $\theta_p = \theta_c + \varepsilon\,(\theta_d - \theta_c)$ with $\varepsilon$ evaluated for that flow.

- **Connection 3:** cold-side flow $\dot V$, heat needed $C(\theta_{mix} - \theta_p)$.
- **Connection 2:** cold-side flow $\dot V_h = \dot V(\theta_{mix} - \theta_c)/(\theta_h - \theta_c)$, fixed by the mixer; heat needed $\rho\,\dot V_h\,c_p(\theta_h - \theta_p)$.
- **Connection 1:** cold-side flow $\dot V_c = \dot V(\theta_h - \theta_{mix})/(\theta_h - \theta_p)$, which depends on $\theta_p$. Start with $\theta_p = \theta_c$ and repeat: compute $\dot V_c$, then $\varepsilon$, then a new $\theta_p$, until it no longer changes. Heat needed $\rho\,(\dot V - \dot V_c)\,c_p(\theta_h - \theta_c)$.

The saving fraction is one minus the heat needed with the unit, divided by $C(\theta_{mix} - \theta_c)$. The model keeps $UA$ independent of the cold-side flow, so it slightly flatters the two unbalanced connections: in a real unit, a smaller cold-side flow also gives a lower heat transfer coefficient on that side. The same model in Python can be downloaded here: {download}`dwhr_model.py <code/dwhr_model.py>`.
:::


## A stratified tank simulator

A hot water tank is not simply full or empty. Hot water floats on top of cold water, and a well-designed tank keeps the two apart, with a thin mixing zone, the thermocline, between them. Hot water is drawn from the top while cold mains water flows in at the bottom, so the thermocline moves up as the tank is emptied. The app below follows this hour by hour for one day.

The tank is split into horizontal layers. A heat pump charges it through an external heat exchanger: the charging loop takes water from the bottom of the tank and returns it at mid-height, and there is no circulation loop. A thermostat starts the heat pump when the sensor falls below the setpoint, and it can only run in the hours you allow. The tab *Tapping profiles* shows the predefined days of hot water use, with their sources, and lets you import a profile made with DHWcalc.

```{anywidget} code/dhw-tank.mjs
{}
```

The app runs in your browser. The same model in Python, with comments on every assumption, can be downloaded here: {download}`dhw_tank.py <code/dhw_tank.py>`. Running it prints the daily heat of each profile and the results for the default inputs.


## Sizing the tank as a thermal battery

A hot water tank is a battery for heat. When it is charged, the heat source runs. When hot water is drawn, the tank delivers. If the tank is big enough, the two no longer have to happen at the same time, and the heat pump can run in the hours when electricity is cheap or has a low primary energy factor. The question is how big "big enough" is.

The heat a fully charged tank holds, counted from the cold water temperature, is

$$
Q_{tank} = \bar\rho\,V\,\bar c_p\,(\theta_{set} - \theta_c)
$$ (eq-dhw-store)

Not all of it can be used. Between the hot water at the top and the cold water at the bottom there is a mixing zone, the thermocline, and water from that zone is too cold for a shower. The tank is "empty" for the user long before all of it is at $\theta_c$. We account for this with a usable fraction $\eta_{use}$, typically 0.8–0.9 for a well-stratified tank and lower for a tank that mixes when it is charged.

### Sizing by hand in four steps

The method compares, hour by hour, the heat the tank has to deliver with the heat the charging strategy puts in. It is the same method used to size water reservoirs, and it needs nothing more than a spreadsheet with one row per hour.

**Step 1. Hourly heat demand.** From the tapping profile, add up the heat drawn in each hour with equation {eq}`eq-dhw-energy`, using the volume and use temperature of each tapping. Add the standing loss of the tank as a constant amount per hour, $\Phi_{loss} = UA\,(\theta_{set} - \theta_{room})$. The sum over the day is the heat the tank must receive, $Q_{day}$.

**Step 2. Hourly charging.** Spread $Q_{day}$ evenly over the hours the charging strategy allows. With $N$ allowed hours, the heat source must deliver $\Phi_{ch} = Q_{day}/N$ during those hours. This is the first check of the design: if $\Phi_{ch}$ is larger than the heat output of the heat pump, the strategy cannot work, whatever the tank size.

**Step 3. Cumulative curves.** Add up the demand and the charging hour by hour, and plot both cumulative curves over the day. The difference between them, charge minus demand, is the change in the heat stored in the tank since midnight. The tank must never hold less than nothing, so lift the charge curve until it just touches the demand curve from above. The largest vertical gap between the two curves is then the heat the tank must store, $Q_{store}$. In a spreadsheet, this is simply the maximum minus the minimum of the column "cumulative charge − cumulative demand".

**Step 4. Volume.** Solve equation {eq}`eq-dhw-store` for the volume, with the usable fraction:

$$
V = \frac{Q_{store}}{\bar\rho\,\bar c_p\,(\theta_{set} - \theta_c)\,\eta_{use}}
$$ (eq-dhw-volume)

Round up to the next standard tank size.

The method is a first estimate. It assumes the tank is either hot or cold, with a fixed usable fraction, and that the heat source charges evenly over its allowed hours. In a real tank, the thermocline grows while the tank sits, the heat pump is switched by a thermostat at a sensor partway up the tank, and the standing loss depends on how much of the tank is hot. The simulator handles all of this, so the hand estimate should always be checked there.

### Worked example: night charging for a family of four

A family of four uses the profile "Family of 4, morning and evening" from the simulator: two showers at 06:30–07:00, one at 20:00, and small tappings during the day. Three showers a day, rather than one per person, matches the Be18 calculation value for a 150 m² house; measured Danish households shower even less {cite:p}`marszal2021`. The tank is kept at 55 °C, the cold water is 10 °C, and the tank has $UA = 1.2$ W/K in a room at 20 °C. How large a tank is needed if the heat pump may run only between 00:00 and 06:00? How large is it with uniform charging over the whole day?

**Step 1.** The tappings add up to 5.73 kWh per day. Of that, 2.91 kWh is drawn between 06:00 and 07:00 and 1.45 kWh between 20:00 and 21:00. The standing loss is $1.2 \cdot (55 - 20) = 42$ W, or 1.01 kWh per day. So $Q_{day} = 6.74$ kWh.

**Step 2.** With night charging, $N = 6$ h and $\Phi_{ch} = 6.74/6 = 1.12$ kW. With uniform charging, $\Phi_{ch} = 6.74/24 = 0.28$ kW. Both are well within the 3 kW of a small heat pump.

**Step 3.** {numref}`fig-dhw-tank-sizing` shows the cumulative curves. With night charging, the tank receives all of the day's heat by 06:00, before any hot water has been used. The gap is largest at 06:00, just before the morning showers: $Q_{store} = 6.49$ kWh. With uniform charging, the charge curve has to be lifted by 1.34 kWh so that it stays above the demand after the morning showers, where the two curves touch at 08:00. The gap is largest at 06:00, just before the two morning showers: $Q_{store} = 2.77$ kWh. With one shower in the evening, the morning peak is now the one that sets the size.

:::{figure} figures/ch04/tank-sizing-curves.*
:label: fig-dhw-tank-sizing
:alt: Two plots of cumulative heat over a day. In both, the orange demand curve is nearly flat except for a large step at 06–07 (two showers) and a smaller step at 20–21 (one shower). Left, uniform charging: the blue charge curve is a straight line lifted to touch the demand curve at about 08:00, and the largest gap, 2.8 kWh or about 63 L, is at 06:00. Right, night charging: the blue curve rises steeply from 0 to 6.7 kWh between 00 and 06 and is flat after that; the largest gap, 6.5 kWh or about 147 L, is at 06:00.

Cumulative charge and cumulative demand for the family of four, with uniform charging (left) and night charging 00–06 (right). The largest vertical gap is the heat the tank must store.
:::

**Step 4.** With $\eta_{use} = 0.85$ and 1.155 Wh/(L·K):

$$
V_{night} = \frac{6490}{1.155 \cdot (55 - 10) \cdot 0.85} = 147 \text{ L}, \qquad V_{uniform} = \frac{2770}{1.155 \cdot 45 \cdot 0.85} = 63 \text{ L}
$$

Night charging needs a tank more than twice as large, because the tank has to carry the whole day's hot water, including the evening shower, from 06:00 to 20:00.

**Check in the simulator.** With the default 3 kW heat pump and a sensor at 60 % of the tank height, the simulator gives:

| Strategy | Tank | Unmet hot water | Standing loss |
|---|---|---|---|
| Night 00–06 | 120 L | 0.36 kWh: the evening shower runs cold | 0.30 kWh/day |
| Night 00–06 | 147 L | 0.02 kWh: the kitchen tap at 22:00 is slightly below 45 °C | 0.40 kWh/day |
| Night 00–06 | 180 L | none | 0.50 kWh/day |
| All hours | 50 L | 0.18 kWh: the second morning shower runs cold | 0.84 kWh/day |
| All hours | 63 L | 0.01 kWh: the kitchen tap at 07:15 is slightly below 45 °C | 0.83 kWh/day |
| All hours | 100 L | none | 0.85 kWh/day |

In both cases the hand estimate is close: the tank it gives delivers every shower at full temperature and falls just short only for one small kitchen tapping right after a peak. One standard size up, it is safe. A smaller tank fails where the method says it will, at the peak that sets the size. Note that the night-charged tank loses less than half of the standing loss we assumed, because it is cold for much of the evening. The uniform case works for a different reason than the method assumes: the heat pump does not charge evenly at 0.28 kW. A thermostat starts it at full power when the sensor has cooled, and during the morning showers its 3 kW output helps cover the draw.

:::{admonition} Rules of thumb
:class: tip

- 1 kWh stored at 55 °C, counted from 10 °C cold water, needs about 20 L of water, or 23 L with a usable fraction of 0.85.
- Charging only at night means storing a full day of hot water: about 40–45 L per person.
- Charging whenever needed, with a thermostat, needs about 20–25 L per person, enough to cover the largest peak.
- The heat pump must deliver at least the daily heat divided by the number of allowed hours, plus a margin.
:::
