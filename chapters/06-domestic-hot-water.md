# Domestic hot water

<!-- ## Learning objectives

After this chapter you can:

- estimate the annual hot water heat demand of a dwelling, and explain why it becomes a large share of the heat demand in a low-energy house
- calculate the energy and the power needed for a tapping, and explain why the power, not the energy, decides how a hot water system is built
- explain how a drain water heat recovery unit works, calculate its effectiveness and its annual saving, and judge when it pays back
- read a tapping profile and an hourly electricity price profile, and explain why the two are badly matched
- size a hot water tank and its heat pump so the tank can be charged in cheap hours, and estimate the saving
- describe how hygiene (Legionella) and heat pump efficiency limit the tank temperature
 -->

## Introduction

For most of the twentieth century, domestic hot water was a small item in the heat budget of a Danish house. A typical older house with energy label D needs around 150 kWh of space heating per m² of floor area per year. Hot water adds 13 kWh/m², less than a tenth of the total.

Better houses have changed the picture ({numref}`fig-dhw-share`). Insulation, airtightness and heat recovery ventilation have cut the space heating demand of a passive house to 15 kWh/m², and of a house in the Danish low-energy class to about 10 kWh/m². The hot water demand has not changed, because it depends on the people living in the house and not on its envelope. A family takes the same showers in a passive house as in a house from 1965. In a passive house hot water is therefore close to half of the heat demand, and in a low-energy class house it is more than half.

:::{figure} figures/ch06/dhw-share.*
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

<!-- The temperature also matters. A floor heating system in a low-energy house runs at 30–35 °C (Chapter 5). Hot water must be stored at 50–55 °C or more to keep Legionella bacteria from growing. When the same heat pump supplies both, the hot water is the expensive part of its work, because the efficiency of a heat pump falls as the temperature it delivers rises. In an all-electric low-energy house, hot water can easily use as much electricity as space heating.

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

:::{figure} figures/ch06/tank-sizing-curves.*
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
