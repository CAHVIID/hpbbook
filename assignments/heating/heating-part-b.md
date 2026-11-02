# Assignment 3, Part B: Heating

Drain water heat recovery, tank charging and life-cycle costs of heating solutions for the row house from Part A.

Remember to state who was responsible for which part in your submission.

## Aim

The aim of Part B is to find the combination of space heating, ventilation and domestic hot water (DHW) for the row house that has the lowest life-cycle cost and primary energy, in the context of time-varying electricity prices. DHW is a large share of the heat demand in a low-energy house, so the DHW system is treated in detail: tapping profile, tank size, charging time and drain water heat recovery.

## Motivation

The row house needs to be supplied with space heating, DHW and ventilation in a cost, energy and emission-efficient manner.

Primary energy is important to reduce. It counts in the energy frame, and it can be regarded as a proxy for carbon emissions.

Cost is important to reduce over the lifespan of the building, i.e. the life-cycle cost (LCC). New building designs must strike a balance between installation costs, renewal costs and operating costs.

In many new low-energy areas, district heating is not economically feasible because the heat use is low, so the remaining options are a heat pump or direct electric heating. These options also support the general electrification that is necessary to move away from fossil fuels.

However, balancing electricity demand and production is crucial to avoid costly standby of production and storage. Tariff model 3.0, in force since 2024, has daily low-price, mid-price and high-price periods to reduce the strain on the grid. A DHW tank is a thermal battery: it can be charged when electricity is cheap and the primary energy factor (PEF) is low, at night, and used when it is not.

Currently, there are no direct incentives in new houses to reduce operational emissions through flexible operation, but time-varying PEFs in the Building Regulations have been discussed. They would reward buildings and installations that use low-PEF periods.

## Structure

- Primary energy and life-cycle cost of heating solutions
- Energy savings in domestic hot water

## A few notes

- Primary energy is the weighted sum of the electricity use in each tariff period, with the primary energy factors of that period.
- The time-varying electricity tariffs are a guesstimate without (some of the) taxes, as electricity for heating is exempt from most taxes. The high-price period is 17:00–21:00, as in tariff model 3.0.
- The tank simulator is in the book chapter *Domestic hot water*; the method for drain water heat recovery is in the lecture slides and the book chapter *Drain water heat recovery*.

## The three configurations

| | C1 All electric | C2 Floor heating + heat pump | C3 Nilan Compact P |
| --- | --- | --- | --- |
| Space heating | Electric radiators | Hydronic floor heating | Air heating (coil in supply air) |
| DHW | Electric tank | Tank on the same heat pump | Compact P tank, 180 L |
| Heat source | Direct electric | Air-to-water heat pump | Exhaust-air heat pump + element |
| Ventilation | Separate AHU with heat recovery | Separate AHU with heat recovery | Built into the Compact P |

## Questions

Base case: all three scenarios on equal terms, a 180 L tank (the Compact P size) with uniform charging. Each part builds on the previous one.

## H7 LCC of space heating solutions

Primary energy is important to assess to make sure the building complies with the energy frame. Heating cost is important when it comes to assessing the life cycle costs of the installation.

### Q7.1 Calculate the life cycle costs for different space heating systems

*No IDA simulation is necessary.*

Search the internet to find installation costs of different heating solutions. Estimate the lifespan of the installations, and calculate life cycle costs. Use heating cost from QB1

LCC over 100y = investment costs / lifespan x 100 + yearly heating costs x 100. Ignore interest and inflation rates

Fill out the table below.

Which solution has the lowest initial investment and which solution the lowest LCC? Does the use of flex tariffs change which solution that has the lowest LCC?

**Deliverable:** a table like the one below

| Space heating | Estimated lifespan | Investment cost | LCC costs\* - fixed tariffs | LCC costs\* - flex tariffs |
| --- | --- | --- | --- | --- |
| | Years | DKK | DKK | DKK |
| Electrical radiators | | | | |
| Hydronic floor heating with heat pump | | | | |
| Air-heating with heat pump (Compact P) | | | | |

## H9 Drain water heat recovery

Showers are the largest hot water use in most homes, and the water leaves the drain only a few degrees colder than it left the shower head. A drain water heat recovery unit uses this heat to preheat the cold water. How much it saves depends on the unit, how it is connected, and the flow and length of each shower. In H9 you choose a tapping profile for the row house and calculate the saving shower by shower.

### Q9.1 Tapping profile

1. Choose a tapping profile for the row house and state why. There is profile inspiration in the Stratified tank model.
2. Make an hourly profile of hot water heat tapping and plot the cumulative demand profile over 24h
3. Calculate tapping profile's yearly hot water energy kWh/year (x365)

**Deliverable:** cumulative demand profile

### Q9.2 Energy savings from drain water heat recovery

Start from the tapping profile chosen in Q9.1.

1. Find a typical shower in the tapping profile: time, volume at the tap, flow and temperature. Assume that all showers henceforth are the same.
2. Choose a drain water heat recovery unit from the [Passive House component database](https://database.passivehouse.com/en/components/), and apply it using connection "shower mixer (1)", as it allows the hot water to be produced centrally. Note its certified effectiveness ε₈ (at 8 L/min, equal flow). Search for a unit price online. If no price can be found, select a different one.
3. For the shower, calculate the temperature of the preheated water and the heat saved, at the shower's own flow.
4. Add up the shower savings: in kWh/day and kWh/year, and as a share of the profile's total DHW.
5. Plot the cumulative demand profile over 24h and compare to

**Deliverable:** Comparison of cumulative demand profiles from Q9.1 and Q9.2 and yearly energy savings

## H10 Uniform charging versus night charging

A hot water tank is a thermal battery. With uniform charging the heat source runs a little all day, and the tank only has to bridge the peaks in the tapping profile. With night charging the tank is filled when electricity is cheap and the primary energy factor is low, but it must then hold most of the day's hot water. In H10 you start from a 180 L tank, the size in the Nilan Compact P, and find out how much storage each strategy needs, with drain water heat recovery implemented.

### Q10.1 Uniform charging

1. Take the cumulative demand curve with drain water heat recovery, from Q9.2, and plot the uniform charging curve and find the approx. tank size needed.

**Deliverable:** cumulative demand and charging curve over 24h

### Q10.2 Night charging

1. Move all charging to the night (00–06) and draw the new charging curve on the demand curve. Here we assume that the installed power is sufficient to fully charge the tank in 6 hours.
2. Find the storage needed for night charging with drain water heat recovery and check whether 180 L is enough. If not your tapping profile is probably off.

**Deliverable:** cumulative demand and charging curve over 24h

### Q10.3 Tank resizing

1. Choose the tank size (for C1) that covers night charging, from available tank sizes.
2. Find the price of a tank for C1 and recalculate the standing loss.
3. For C3, keep the 180 L tank.

### Q10.4 Check in the tank simulator

1. Enter your tapping profile, tank size, charging hours and heat source in the app.
2. Run uniform and night charging, with and without drain water heat recovery.
3. Report the lowest tap temperature and the time it occurs.
4. Compare with the hand calculation and explain the differences.

**Note S3:** the Compact P tank stays 180 L. In winter the heat pump gives space heating first, so a charge shift is limited by its spare power.

1. Choose a design day and check that a 180 L tank at 55 °C covers it.
2. Calculate the standing loss of the 180 L tank and the yearly heat to the tank.

## H11 LCC of combined heating, ventilation and DHW solutions

Space heating, ventilation and hot water are bought and run as one system, and a cheap installation can be expensive to run. In H11 you bring the results from H9 and H10 together with space heating and fan energy, and compare the three scenarios on life-cycle cost and primary energy.

### Q11.1 Energy use, cost and primary energy

For C1, C2 and C3, with shower drain heat recovery for each DHW case from H10 (uniform or night charging, with or without drain water heat recovery).

1. Split the yearly charging energy on the four tariff periods.
2. Calculate the electricity use for DHW: element (S1), heat pump (S2) and Compact P (S3).
3. Calculate the yearly electricity use for space heating and fans.
4. Calculate the yearly energy cost and primary energy.

### Q11.2 LCC and comparison

Space heating, ventilation and DHW together, as in the scenario table.

1. Collect investment prices (capex) for each scenario: heating system, ventilation unit, DHW tank or heat pump, and drain water heat recovery. Note lifetimes and reinvestments.
2. Add investments, reinvestments and energy costs into an LCC over 100 years.
3. Collect LCC and primary energy for S1, S2 and S3, base and improved, in one table.
4. Show the effect of each improvement step for each scenario.
5. Write a short conclusion.

| LCC | C1 All electric | C2 Floor heating + heat pump | C3 Nilan Compact P |
| --- | --- | --- | --- |
| Space heating LCC | | | |
| DHW LCC | | | |
| Ventilation LCC | | | Built in |
| LCC 100y | | | |

## H12 (may be omitted) Floor heating with supply water close to room temperature

Floor heating can run with supply water only a few degrees above the room temperature. The floor then gives less heat as soon as the room warms up, from the sun or from people, so it partly regulates itself. In H12 you use the floor heating control app to see how far the supply temperature can be lowered, and whether this keeps the room closer to the setpoint.

### Q12.1 Self-regulating floor heating (S2)

Use the floor heating control app in the book chapter Floor heating. The aim is a more self-regulating floor: the on/off (orange) and PI (blue) room temperatures as close as possible to the ideal heater (grey).

1. Choose the floor (light or heavy) closest to the row house, and set the heat loss coefficient and gains to match the row house.
2. Run the default settings. Note heating energy, heat vented, total deviation and return temperature for the ideal heater, on/off and PI.
3. Set a constant supply temperature (heating curve slope 0) and lower the max supply temperature step by step towards the room temperature. Adjust the design flow so the room still reaches the setpoint on the cloudy day.
4. Find the lowest supply temperature that still covers the heat demand.
5. Tune the room control (hysteresis, proportional band, integral time, PWM cycle) at that supply temperature.
6. Collect the results of each step in one table, and show room temperatures for the default and your best case.

## Expected deliverables

| Part | Tables | Figures | Key numbers |
| --- | --- | --- | --- |
| **H9** Drain water heat recovery | Tapping profile (time, volume, flow, temperature, kWh). Showers with preheated cold water temperature and heat saved. | Hourly hot water profile. | DHW kWh/day. Chosen unit, ε₈ and connection. Saving in kWh/year and % of DHW. Investment in the unit. |
| **H10** Uniform vs night charging | Storage needed and tank size for each case: uniform and night, with and without drain water heat recovery. | Cumulative demand curve with uniform and night charging curves. Simulator tap temperature for each case. | Storage needed (kWh and L). Design day check of 180 L. Chosen tank size and price for S1 and S2. Standing loss. Lowest tap temperature in the simulator. |
| **H11** LCC of combined solutions | Energy use per tariff period. Capex, lifetimes and reinvestments. LCC and primary energy for S1, S2 and S3, base and improved. | Effect of each improvement step on LCC and primary energy. | Yearly energy cost (DKK) and primary energy (kWh) per scenario. LCC over 100 years (DKK). Short conclusion with a recommended solution. |
| **H12** Floor heating (may be omitted) | Results of each step: supply temperature, design flow, heating energy, heat vented, total deviation, return temperature. | Room temperatures for the default and your best case. | Lowest supply temperature that covers the demand. Your control settings. |
