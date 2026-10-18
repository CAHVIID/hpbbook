# Domestic hot water

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## Introduction

For most of the twentieth century, domestic hot water was a small item in the heat budget of a Danish house. A typical older house with energy label D needs around 150 kWh of space heating per m² of floor area per year. Hot water adds 13 kWh/m², less than a tenth of the total.

Better houses have changed the picture ({numref}`fig-dhw-share`). Insulation, airtightness and heat recovery ventilation have cut the space heating demand of a passive house to 15 kWh/m², and of a house in the Danish low-energy class to about 10 kWh/m². The hot water demand has not changed, because it depends on the people living in the house and not on its envelope. A family takes the same showers in a passive house as in a house from 1965. In a passive house hot water is therefore close to half of the heat demand, and in a low-energy class house it is more than half.

:::{figure} figures/c2/dhw-share.*
:label: fig-dhw-share
:alt: Horizontal stacked bar chart of net heat demand per m² floor area per year. A house with energy label D has 150 kWh/m² of space heating and 13 kWh/m² of hot water, so hot water is 8 %. A passive house has 15 kWh/m² of space heating, so hot water is 46 %. A house in the Danish low-energy class has 10 kWh/m² of space heating, so hot water is 57 %.
:width: 100%

Net heat demand for space heating and domestic hot water in three Danish house standards. The label D value is an estimate for a 150 m² house in the middle of the D band. The hot water demand is the Be18 calculation value of 250 L/m² per year heated from 10 °C to 55 °C {cite:p}`build213`. Losses from the tank and pipes are not included. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dhw_share.py)
:::

:::{admonition} Hot water in Building Code
:class: dropdown
The Danish energy frame calculation (Be18) uses a fixed hot water demand of 250 L per m² of heated floor area per year, heated from 10 °C to 55 °C {cite:p}`build213`. With the average properties of water between 10 °C and 55 °C this is

$$
Q = \bar\rho\,V\,\bar c_p\,(\theta - \theta_c) = \frac{994 \cdot 0.250 \cdot 4.182 \cdot (55 - 10)}{3600} = 13.0 \text{ kWh/(m}^2\,\text{year)}
$$

For a 150 m² house it amounts to 2000 kWh per year, or about 100 L of 55 °C water per day which is a reasonable figure for a family of three or four.

However, measured hot water use varies by a factor of two or three between households of the same size, and it depends much more on the number of occupants, their age and their habits than on the floor area.
:::

<!-- The temperature also matters. A floor heating system in a low-energy house runs at 30–35 °C (Chapter C1). Hot water must be stored at 50–55 °C or more to keep Legionella bacteria from growing. When the same heat pump supplies both, the hot water is the expensive part of its work, because the efficiency of a heat pump falls as the temperature it delivers rises. In an all-electric low-energy house, hot water can easily use as much electricity as space heating.

There are two ways to cut the cost of hot water, and this chapter is built around them:

- **Use less heat.** Shower water leaves the house at about 30 °C, at the same moment as cold water comes in. A drain water heat recovery unit passes that heat to the incoming cold water. This is Part A of the chapter.
- **Buy the heat at the right time.** Electricity prices vary over the day, with a peak in the early evening, which is exactly when many families shower. A well-sized hot water tank can be charged in cheap hours and emptied in expensive ones. This is Part B.

The next section sets out how much hot water a dwelling uses and how fast it is drawn, which both parts build on.
 -->

## How much hot water?

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
| Bathtub | 12 | 40 | 120 | 4.2 | 24.9 |
:::

These powers are far larger than anything else in the heating system of a low-energy house. The whole house may need only 2–3 kW of space heating on the coldest day, and a heat pump sized for that cannot heat a shower as it runs. There are two ways out:

- **Instantaneous heating.** District heating can deliver 30–40 kW through a heat exchanger in a flat station, so the water is heated as it is used and nothing is stored.
- **Storage.** A heat pump or a small boiler heats a tank slowly, over hours, and the tank delivers the high power during the tapping. The tank decouples the power the heat source must deliver from the power the user draws.

<!-- Storage is what makes it possible to choose *when* the heat source runs, which is the topic of Part B. Showers are what make drain water heat recovery worthwhile, which is the topic of Part A. They are the largest single hot water use in most homes, and they are the one use where the warm waste water flows to the drain at the same moment as the cold water comes in.
 -->
:::{admonition} Rules of thumb
:class: tip
- The cold water temperature is on average 10 C, which is ok for most calculations, but actually fluctuates between 8-17 C throughout the year.
- 1 L of water warmed by 1 K takes about 1.15 Wh. 100 L warmed by 45 K takes about 5 kWh.
- One 8-minute shower uses about 60 L of 40 °C water, which is 40 L of 55 °C water and about 2 kWh of heat.
- Hot water use is about 30–40 L of 55 °C water per person per day, or about 550–750 kWh per person per year before losses.
- The Be18 calculation value is 13 kWh/m² per year, about 2000 kWh per year for a 150 m² house.
- A shower draws about 15–20 kW while it runs, several times the design heat load of a low-energy house.
:::

## Hot water heaters

Four types of hot water heater are common in Danish single-family houses. They differ in where the heat comes from and in what else the unit does.

**Electric water heater.** A tank with an electric heating element and a thermostat. Each kWh of hot water costs one kWh of electricity, plus the standing loss of the tank, which is set by the insulation and the tank temperature. The electric water heater is the reference for the other solutions in this book.

:::{dropdown} Example: Metro Therm water heaters
The range runs from 14 to 288 L, insulated with polyurethane foam, with a thermostat that can be set up to about 65 °C {cite:p}`metrotherm-waterheaters`.
:::

**Hot water heat pump.** A tank with a small air-to-water heat pump on top. The heat pump takes its air through ducts, either outdoor air or exhaust air from the house. The COP at an air temperature of 20 °C is typically around 3 to 4. With outdoor air, the COP falls in winter, when the air is cold. With exhaust air, the heat source is close to room temperature all year, but the air flow is limited by the ventilation.

:::{dropdown} Example: MetroAir Aqua
The MetroAir Aqua heats a tank of 190 or 260 L with 1.6 kW of heat pump capacity. The COP is 3.7 and 4.1 at an air temperature of 20 °C for the two tank sizes {cite:p}`metrotherm-overview2025`.
:::

**Heat pump for space heating and hot water.** An air-to-water or ground source heat pump that serves both the floor heating and a hot water tank, often built into the indoor unit. The heat pump switches between floor heating at about 35 °C and charging the tank at 50–55 °C. The COP is lower when it heats hot water than when it heats the floor, because the condensing temperature is higher. The share of the year's heat that goes to hot water grows as the space heating demand falls, so in a low-energy house the COP for hot water matters as much as the SCOP for space heating.

:::{dropdown} Example: Kronoterm Adapt 2
An air-to-water heat pump with an outdoor unit of 2 to 18 kW and the natural refrigerant R290. The SCOP is up to 6.22 at a flow temperature of 35 °C (EN 14825, average climate), and the flow temperature can reach 75 °C {cite:p}`kronoterm-adapt`. With the HYDRO C2 indoor unit, the hot water tank is built into the indoor unit.
:::

**Compact unit.** A compact unit combines balanced ventilation with heat recovery, an exhaust-air heat pump and a hot water tank in one cabinet. The heat pump takes heat from the exhaust air after the heat exchanger and uses it for the hot water and, in some units, the supply air. The heat source is limited by the ventilation air flow, so the unit suits houses with a small heating demand, such as passive houses. Because ventilation, heat pump and tank share one cabinet, the parts are harder to reach and replace than in separate units, and a fault in one part can take ventilation and hot water out of service together.

:::{dropdown} Example: Nilan Compact P
The Compact P has a 180 L tank in a cabinet of 900 × 610 × 2065 mm. The counterflow heat exchanger has a temperature efficiency of up to 95 % {cite:p}`nilan-compactp`. The unit is certified as a Passive House component at air flows of [92 m³/h](https://database.passivehouse.com/en/components/details/heatpump/nilan-as-compact-p-arbeitspunkt-92-m3h-0390ch03) and [172 m³/h](https://database.passivehouse.com/en/components/details/heatpump/nilan-as-compact-p-arbeitspunkt-172-m3h-0391ch03).
:::

The Danish Energy Agency keeps an official list of heat pumps sold in Denmark, Varmepumpelisten, with the tested efficiency of each product {cite:p}`sparenergi-varmepumpelisten`. It is the place to compare heat pumps of the types above.

% REVIEW LATER (Christian, 2026-10-16): check the note on servicing compact units such as the Nilan Compact P. The MetroAir Aqua data are for the 201 and 301 models; check them against the 202 and 302 in the link.

## Electricity prices over the day

A household on an hourly contract pays the spot price of the hour plus a set of fixed and time-dependent charges. In eastern Denmark (DK2) in 2026, the price per kWh is

$$
p(t) = \big(p_{spot}(t) + p_{net}(t) + p_{TSO} + p_{tax}\big)\,(1 + 0.25)
$$ (eq-dhw-price)

where $p_{spot}$ is the day-ahead price of the hour, $p_{net}$ the network tariff of the local grid company, $p_{TSO}$ Energinet's system and network tariffs (7.2 + 4.3 øre/kWh {cite:p}`energinet2026tariffs`), $p_{tax}$ the electricity tax and 0.25 the VAT. The electricity tax was 72.7 øre/kWh until 2025. In 2026 and 2027 it is cut to the EU minimum of 0.8 øre/kWh {cite:p}`skm2025elafgift`, which makes the hourly part of the price far more important than before.

Two of the terms change over the day ({numref}`fig-dhw-price-day`):

- **The spot price** follows the balance between demand and wind and solar production. On a typical weekday it has one peak in the morning and a higher one at 17–20, when people come home and cook and solar production falls away. It is lowest at night and, on sunny days, at midday.
- **The network tariff** is a fixed time-of-use tariff. Radius charges, in winter (October to March), 11 øre/kWh at 00–06, 32 øre/kWh at 06–17 and 21–24, and 96 øre/kWh at the peak 17–21. In summer, the peak tariff is less than half of that {cite:p}`bolius2026tariffs`.

The two peaks coincide. On the day in {numref}`fig-dhw-price-day`, the consumer price runs from 1.17 DKK/kWh at 03:00 to 4.68 DKK/kWh at 19:00, a factor of four. The family of four draws 57 % of its hot water heat at 06–08 and 37 % at 17–21, in the most expensive hours of the day. Heated as it is used, its hot water costs on average 2.38 DKK/kWh of electricity. This is the price weighted by the hot water heat drawn in each hour, and it is higher than the daily average of 1.89 DKK/kWh. Heated at night, 00–06, it costs 1.22 DKK/kWh, half as much.

:::{figure} figures/c2/dhw-price-day.*
:label: fig-dhw-price-day
:alt: Two bar charts sharing an hourly axis from 0 to 24. Top: consumer electricity price per hour, stacked from spot price, network tariff, Energinet tariffs and tax, and VAT. It is about 1.2 DKK/kWh at night, peaks at 2.8 DKK/kWh at 07–08, is about 1.4 DKK/kWh at midday, and peaks at 4.7 DKK/kWh at 19–20. A dashed line marks the daily average of 1.89 DKK/kWh, a dotted line the night average 00–06 of 1.22 DKK/kWh and a dash-dotted line the price weighted by hot water use, 2.38 DKK/kWh. Bottom: hot water heat for the family of four, with 2.9 kWh at 06–07, 1.45 kWh at 20–21 and small amounts in other hours.

Top: consumer price of electricity in DK2 over one day, from the spot price of 30 September 2025, the Radius winter tariff and the charges and taxes of 2026. The dashed line is the daily average consumer price, 1.89 DKK/kWh, the dotted line the average at night, 00–06, 1.22 DKK/kWh, and the dash-dotted orange line the price weighted by the hot water heat drawn in each hour, 2.38 DKK/kWh. Bottom: hot water heat drawn by the family of four in the tank sizing example, per hour. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dhw_price_day.py)
:::

The saving from charging at night depends on the heat source. With an electric water heater, the family uses 5.7 kWh of electricity a day for hot water, and charging at 00–06 instead of at the time of use reduces the cost by 6.6 DKK on this day. With a heat pump at a COP of 2.5, the reduction is 2.6 DKK a day. Both values are upper limits, since they are based on a single day with a large price spread, neglect the standing loss, and assume a heat source that can deliver the shower power directly. Over a year, the saving is of the order of a few thousand DKK with a resistance heater and about a thousand DKK with a heat pump.

### The primary energy factor and CO₂ over the day

The Danish energy frame (BR18) uses one fixed primary energy factor for electricity, 1.9. The real factor changes from hour to hour with the production mix. Each source $i$ gets a non-renewable primary energy factor, and the factor of the mix in hour $t$ is

$$
f_{P,nren}(t) = \frac{\sum_i E_i(t)\, f_{P,nren,i}}{\sum_i E_i(t)}
$$ (eq-dhw-pef)

where $E_i(t)$ is the electricity from source $i$ in hour $t$. Wind and solar have a non-renewable factor of zero. Fossil plants have a factor close to $1/\eta$. The CO₂ intensity behaves the same way, and for this reason it serves as a proxy for CO₂ in this book.

Danish electricity emitted on average 124 g CO₂-eq/kWh in 2025, counted on consumption and including imports. Single hours ranged from 36 to 363 g/kWh. In winter, the average day goes from 130 g/kWh at 01:00 to 166 g/kWh at 16:00, and in summer from 81 to 100 g/kWh {cite:p}`electricitymaps2025dk`. Price and CO₂ often point the same way, because the expensive evening hours are also the hours with more fossil production and imports. But they are not the same signal. A windy afternoon can be cheap and clean while the night after it is calm and dirty. A charging strategy that follows the price is therefore not automatically the one with the lowest CO₂.

For hand calculations, the hourly data can be reduced to a few periods of the day. Scale the BR18 factor by the mean CO₂ intensity $c$ of each period, relative to the daily mean $\bar c$, weighted by the length of each period:

$$
f_{P}(t) = 1.9\,\frac{c(t)}{\bar c}
$$ (eq-dhw-pef-co2)

{numref}`fig-dhw-pef-periods` shows the result for Denmark in 2021, in four periods of the day. The night, 22–06, gets a factor of 1.66, the day, 06–17, 2.05, and the evening, 17–22, 1.95. Averaged over the 24 hours, the factor is 1.9. The spread is only about ±10 % around 1.9, much smaller than the spread in price, which is why a charging strategy saves far more money than primary energy.

% REVIEW LATER (Christian, 2026-10-14): the periods 17-22 and 22-24 do not match the Radius tariff periods 17-21 and 21-24. Regroup when the hourly 2021 DeclarationEmissionHour data is available.

:::{figure} figures/c2/dhw-pef-periods.*
:label: fig-dhw-pef-periods
:alt: Bar chart of the primary energy factor of electricity over the day, with bar widths equal to the length of each period. 00–06: 1.66 (99 g CO₂/kWh). 06–17: 2.05 (122 g/kWh). 17–22: 1.95 (116 g/kWh). 22–24: 1.67 (100 g/kWh). A dashed line marks the fixed BR18 factor of 1.9.

Time-varying primary energy factors for electricity, from the mean CO₂ emission intensity of Danish electricity (DK1 and DK2) in four periods of the day in 2021 {cite:p}`eds-declarationemissionhour`, scaled so that the factor averaged over the 24 hours equals the BR18 factor of 1.9 (daily mean 113 g/kWh). [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dhw_pef_periods.py)
:::

## Sizing the tank as a thermal battery

A hot water tank is a battery for heat. When it is charged, the heat source runs. When hot water is drawn, the tank delivers. If the tank is big enough, the two no longer have to happen at the same time, and the heat pump can run in the hours when electricity is cheap or has a low primary energy factor. The question is how big "big enough" is.

The heat a fully charged tank holds, counted from the cold water temperature, is

$$
Q_{tank} = \bar\rho\,V\,\bar c_p\,(\theta_{set} - \theta_c)
$$ (eq-dhw-store)

Not all of it can be used. Between the hot water at the top and the cold water at the bottom there is a mixing zone, the thermocline, and water from that zone is too cold for a shower. The tank is "empty" for the user long before all of it is at $\theta_c$. We account for this with a usable fraction $\eta_{use}$, typically 0.8–0.9 for a well-stratified tank and lower for a tank that mixes when it is charged.

### Sizing by hand in four steps

The method compares, hour by hour, the heat the tank has to deliver with the heat the charging strategy puts in. It is the same method used to size water reservoirs, and it needs nothing more than a spreadsheet with one row per hour.

**Step 1. Hourly heat demand.** From the tapping profile, add up the heat drawn in each hour, $Q = \rho\,V\,c_p\,(\theta - \theta_c)$, using the volume and use temperature of each tapping. Add the standing loss of the tank as a constant amount per hour, $\Phi_{loss} = UA\,(\theta_{set} - \theta_{room})$. The sum over the day is the heat the tank must receive, $Q_{day}$.

**Step 2. Hourly charging.** Spread $Q_{day}$ evenly over the hours the charging strategy allows. With $N$ allowed hours, the heat source must deliver $\Phi_{ch} = Q_{day}/N$ during those hours. This is the first check of the design: if $\Phi_{ch}$ is larger than the heat output of the heat pump, the strategy cannot work, whatever the tank size.

**Step 3. Cumulative curves.** Add up the demand and the charging hour by hour, and plot both cumulative curves over the day. The difference between them, charge minus demand, is the change in the heat stored in the tank since midnight. The tank must never hold less than nothing, so lift the charge curve until it just touches the demand curve from above. The largest vertical gap between the two curves is then the heat the tank must store, $Q_{store}$. In a spreadsheet, this is simply the maximum minus the minimum of the column "cumulative charge − cumulative demand".

**Step 4. Volume.** Solve equation {eq}`eq-dhw-store` for the volume, with the usable fraction:

$$
V = \frac{Q_{store}}{\bar\rho\,\bar c_p\,(\theta_{set} - \theta_c)\,\eta_{use}}
$$ (eq-dhw-volume)

Round up to the next standard tank size.

The method is a first estimate. It assumes the tank is either hot or cold, with a fixed usable fraction, and that the heat source charges evenly over its allowed hours. In a real tank, the thermocline grows while the tank sits, the heat pump is switched by a thermostat at a sensor partway up the tank, and the standing loss depends on how much of the tank is hot. The tank simulator in [](appendix-dhw-tank.md) handles all of this, so the hand estimate should always be checked there.

### Worked example: night charging for a family of four

A family of four uses the profile "Family of 4, morning and evening" from the tank simulator ([](appendix-dhw-tank.md)): two showers at 06:30–07:00, one at 20:00, and small tappings during the day. Three showers a day, rather than one per person, matches the Be18 calculation value for a 150 m² house; measured Danish households shower even less {cite:p}`marszal2021`. The tank is kept at 55 °C, the cold water is 10 °C, and the tank has $UA = 1.2$ W/K in a room at 20 °C. How large a tank is needed if the heat pump may run only between 00:00 and 06:00? How large is it with uniform charging over the whole day?

**Step 1.** The tappings add up to 5.73 kWh per day. Of that, 2.91 kWh is drawn between 06:00 and 07:00 and 1.45 kWh between 20:00 and 21:00. The standing loss is $1.2 \cdot (55 - 20) = 42$ W, or 1.01 kWh per day. So $Q_{day} = 6.74$ kWh.

**Step 2.** With night charging, $N = 6$ h and $\Phi_{ch} = 6.74/6 = 1.12$ kW. With uniform charging, $\Phi_{ch} = 6.74/24 = 0.28$ kW. Both are well within the 3 kW of a small heat pump - as long as the heatpump is not tasked with space heating also.

**Step 3.** {numref}`fig-dhw-tank-sizing` shows the cumulative curves. With night charging, the tank receives all of the day's heat by 06:00, before any hot water has been used. The gap is largest at 06:00, just before the morning showers: $Q_{store} = 6.49$ kWh. With uniform charging, the charge curve has to be lifted by 1.34 kWh so that it stays above the demand after the morning showers, where the two curves touch at 08:00. The gap is largest at 06:00, just before the two morning showers: $Q_{store} = 2.77$ kWh. With one shower in the evening, the morning peak is now the one that sets the size.

:::{figure} figures/c2/tank-sizing-curves.*
:label: fig-dhw-tank-sizing
:alt: Two plots of cumulative heat over a day. In both, the orange demand curve is nearly flat except for a large step at 06–07 (two showers) and a smaller step at 20–21 (one shower). Left, uniform charging: the blue charge curve is a straight line lifted to touch the demand curve at about 08:00, and the largest gap, 2.8 kWh or about 63 L, is at 06:00. Right, night charging: the blue curve rises steeply from 0 to 6.7 kWh between 00 and 06 and is flat after that; the largest gap, 6.5 kWh or about 147 L, is at 06:00.

Cumulative charge and cumulative demand for the family of four, with uniform charging (left) and night charging 00–06 (right). The largest vertical gap is the heat the tank must store. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/tank_sizing_curves.py)
:::

**Step 4.** With $\eta_{use} = 0.85$ and 1.155 Wh/(L·K):

$$
V_{night} = \frac{6490}{1.155 \cdot (55 - 10) \cdot 0.85} = 147 \text{ L}, \qquad V_{uniform} = \frac{2770}{1.155 \cdot 45 \cdot 0.85} = 63 \text{ L}
$$

Night charging needs a tank more than twice as large, because the tank has to carry the whole day's hot water, including the evening shower, from 06:00 to 20:00.

**Check in the simulator.** With the default 3 kW heat pump and a sensor at 60 % of the tank height, the simulator gives:

| Charging strategy | Tank size | Unmet hot water demand | Standing loss |
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

## Hot water in apartment buildings

In an apartment building, hot water is produced centrally, in a district heating substation with a tank or a plate heat exchanger, and distributed to the flats through risers. Without circulation, the water in a riser cools between tappings, and the user has to run the tap until hot water arrives. A circulation loop prevents this. A pump keeps the hot water moving through the supply pipes and back to the substation, so that the whole network stays hot at all hours. The return of the loop is kept above 50 °C to limit the growth of Legionella.

The heat lost from the circulation pipes is

$$
\Phi_{circ} = \sum_j \frac{L_j\,(\theta_{w,j} - \theta_{a,j})}{R'_j}
$$ (eq-dhw-circ)

where $L_j$ is the length of pipe section $j$, $\theta_{w,j}$ the water temperature, $\theta_{a,j}$ the surrounding air temperature and $R'_j$ the thermal resistance per metre of insulated pipe. The loss runs 8760 hours a year, whether hot water is used or not.

Measurements show that the loss is large. In Danish apartment buildings, circulation losses were 23–70 % of the heat delivered to the hot water system, and 54–89 % in office buildings {cite:p}`bohm2013`. In 134 Swedish multi-family buildings, the measured loss ranged from 0.5 to 76 kWh per m² of heated floor area per year. The mean was 14 kWh/m² in older buildings and 6 kWh/m² in newer ones, against an assumed 4 kWh/m² {cite:p}`burke2020`. {numref}`fig-dhw-circulation-burke` shows these results together with the earlier Swedish studies that Burke et al. review. All the mean values lie above the design assumption.

% REVIEW LATER (Christian, 2026-10-14): review the content of the Burke figure. It uses the summary values in Burke et al. (2020) and the earlier studies they cite, not per-building data.

:::{figure} figures/c2/dhw-circulation-burke.*
:label: fig-dhw-circulation-burke
:alt: Range chart of measured circulation losses in kWh per m² floor area per year, with a dashed line at the design assumption of 4. Burke et al. 2020, 134 buildings: range 0.5 to 76, mean 6 in newer and 14 in older buildings. Bergqvist, 12 buildings: range 2.3 to 28, mean 9.1. Lindencrona and Lindsköld, 540 buildings: mean 17.4. Alros, 2 buildings: 11 and 37.
:width: 100%

Measured circulation losses in Swedish multi-family buildings. Range and mean values of 134 measurements, and the earlier studies reviewed in the same paper, compared with the 4 kWh/m² per year assumed in design when no calculation is made {cite:p}`burke2020`. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dhw_circulation_burke.py)
:::

{numref}`fig-dhw-share-circulation` adds these mean losses to {numref}`fig-dhw-share`. In a building of the Danish low-energy class, the circulation loss of 6 kWh/m² is 21 % of the net heat demand and 60 % of the space heating demand. Hot water and circulation together are two-thirds of the heat demand.

:::{figure} figures/c2/dhw-share-circulation.*
:label: fig-dhw-share-circulation
:alt: Horizontal stacked bar chart of net heat demand per m² floor area per year, with space heating, domestic hot water and circulation loss. Energy label D: 150 + 13 + 14 kWh/m², hot water 7 % and circulation 8 %. Passive house: 15 + 13 + 6 kWh/m², hot water 38 % and circulation 18 %. Danish low-energy class: 10 + 13 + 6 kWh/m², hot water 45 % and circulation 21 %.
:width: 100%

Net heat demand for space heating, domestic hot water and circulation loss in apartment buildings of three Danish standards. Space heating and hot water as in {numref}`fig-dhw-share`. The circulation loss is the measured mean for older buildings (14 kWh/m², label D) and newer buildings (6 kWh/m², passive house and low-energy class) in Swedish multi-family buildings {cite:p}`burke2020`. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/dhw_share_circulation.py)
:::

Part of the loss is useful in the heating season, because the pipes run inside the heated building. In summer, it adds to the internal heat gains.

## Product links

The links below lead to products that students can use for data sheets and prices in the assignment. They are examples, not recommendations, and prices and data change over time.

- **Electric water heater:** [Metro Therm model 110 type 211 ECO, 98 L](https://www.lavprisvvs.dk/metro-therm-elvandvarmer-model-110-type-211-eco-98-liter-1000027724)
- **Heat pump for space heating and hot water:** [air-to-water heat pumps, including monoblocks](https://www.lavprisvvs.dk/VVS-installationer-Varmeventilation-Varmepumper.html?Type=Luft%2Fvand) and [indoor units with hot water tank](https://www.lavprisvvs.dk/VVS-installationer-Varmeventilation-Varmepumper-Luft-vand-varmepumper.html?Produkt=Varmepumpe+indedel)
