# Assignment: The hot water tank as a thermal battery

*Draft. The notes for the teacher at the end are not for students.*

## Goal

You will design the hot water system for a single-family house in Denmark in two steps:

1. **Reduce the heat demand for domestic hot water**, mainly with drain water heat recovery (DWHR).
2. **Size the storage tank so it works as a thermal battery**: it is charged when electricity is cheap and has a low primary energy factor, and it delivers the hot water when electricity is expensive.

You judge every design on two numbers: its **life cycle cost (LCC)** and its **primary energy use**. The primary energy factor of Danish electricity changes from hour to hour with the mix of wind, solar, thermal plants and imports. In this assignment the hourly non-renewable primary energy factor is the proxy for CO₂ emissions.

You build every input yourself from real data: the tapping profile, the electricity price, the hourly primary energy factor, the heat pump COP and the component costs. Then you compare the options over one typical week and over the lifetime of the system.

The options are:

- **Heater:** electric resistance heater, or air-to-water heat pump.
- **Drain water heat recovery (DWHR):** with or without a shower drain heat exchanger.
- **Charging strategy:** uniform (any hour), night only (00–06), and one strategy of your own (for example night + midday, or the cheapest N hours).
- **Tank size:** from the smallest tank that keeps the comfort to one that can hold a full day of hot water. Find the size that gives the lowest LCC.

The typical week is a week whose mean outdoor temperature equals the Danish annual mean.

Hand in a short report (max. 10 pages plus appendices) and your spreadsheet or scripts.

---

## Part 1. Tapping profile

1. Generate a one-week tapping profile at 1-minute resolution for your household with **OpenDHW** (Python, <https://github.com/RWTH-EBC/OpenDHW>) or **DHWcalc** (Windows, Universität Kassel). State the number of occupants, the mean daily draw-off (L/day at 45 °C) and the settings you used.
2. Plot the hot water flow for one weekday and the weekend days. Find the daily volume, the daily heat demand (cold water 10 °C) and the largest 1-hour and 10-minute heat demand.
3. Compare your daily demand with one literature profile in the simulator's "Tapping profiles" tab (EN 16147 M or L, IEA Task 26, or the Danish measurements). Explain the difference.
4. Import one day of your profile into the simulator (DHWcalc import). Which day did you choose, and why?

**Check:** the daily heat demand should be between about 1 and 2 kWh per person per day (the Danish measurements give about 1, the rule of thumb in section 2 gives 1.5–2). If yours is far off, find out why before moving on.

## Part 2. Electricity price and primary energy factor

Use Energi Data Service (<https://www.energidataservice.dk>, Energinet). All datasets are free and need no login. Choose DK1 or DK2 and use one full year.

1. **Spot price.** Download the day-ahead price (dataset `DayAheadPrices`; 15-minute values from October 2025, the older `Elspotprices` before that).
2. **Network tariff.** Find your network company's time-of-use tariff (dataset `DatahubPricelist`, or the company's own price list). Note the peak period and the season it applies to.
3. **Taxes and other charges.** Find the electricity tax (elafgift), Energinet's system and transmission tariffs and VAT for the same year. Write down your sources.
4. **Production mix.** Download the hourly electricity production by source for the same area and year (dataset `ProductionConsumptionSettlement`, or `ElectricityProdex5MinRealtime` aggregated to hours: offshore and onshore wind, solar, central and local thermal plants, and exchange with neighbouring areas).
5. **Hourly primary energy factor.** Give each source a total and a non-renewable primary energy factor, and justify your values (for example from EN ISO 52000-1 / EN 17423 conventions: wind and solar 1.0 total and 0 non-renewable; thermal plants 1/η, with the fuel split between fossil and biomass; imports a fixed value of your choice). Compute, for every hour,

   $$f_{P,nren}(t) = \frac{\sum_i E_i(t)\, f_{P,nren,i}}{\sum_i E_i(t)}$$

   Compare the annual mean with the fixed factor for electricity in the Danish Building Regulations (BR18). Why does the building code use one fixed number?
6. **Diurnal profiles.** Reduce each time series to a typical 24-hour profile:
   - average per hour of day for the month(s) that match your typical week (see Part 4), and separately for weekdays and weekends;
   - also compute the 10 % and 90 % quantiles per hour, to show the spread.
7. Plot the total consumer price (spot + tariffs + taxes + VAT) and the non-renewable primary energy factor on the same 24-hour axis. Where are the cheapest hours and the hours with the lowest primary energy factor? Are they the same?

**Questions**

- How large a share of the consumer price is the spot price? What does that mean for the value of shifting the load?
- How much does the diurnal profile change between seasons? Would your conclusions change in January or July?

## Part 3. Costs of the components

Find realistic Danish prices (installed, incl. VAT) for:

- hot water tanks in at least two sizes (for example 150 L and 300 L), with their standing loss (from the energy label, in W or kWh/day);
- an electric water heater of the same size;
- an air-to-water heat pump for hot water (a dedicated DHW heat pump or the DHW share of a combined unit; explain your choice);
- a shower drain heat exchanger (DWHR), including installation, and its effectiveness from the product data sheet;
- service life of each component.

Use at least two sources per component (supplier price lists, the Danish Energy Agency's technology catalogue, product data sheets). Give a range where the sources disagree.

## Part 4. Typical week and heat pump COP

1. Use a Danish weather file (DMI Design Reference Year, or one of the EPW files on the course page). Find the annual mean outdoor temperature.
2. Pick the week (Monday to Sunday) whose mean temperature is closest to the annual mean. State the dates, the mean temperature and the daily minimum and maximum.
3. Find a COP curve for your heat pump: from the data sheet (EN 16147 / EN 14511 test points), or from a Carnot-based model with an efficiency you justify. COP depends on the outdoor temperature and on the temperature you charge the tank to.
4. Make an hourly COP profile for the typical week. Plot it next to the price and primary energy factor profiles.

**Question:** the night is colder than the day. How much of the price advantage of night charging does the lower COP take back?

## Part 5. Reduce the demand: drain water heat recovery

1. From the effectiveness of your DWHR unit, calculate the preheated cold water temperature for a shower at 40 °C with 7 L/min (equal flow, cold water 10 °C).
2. Calculate the heat saved per shower, per week and per year with your tapping profile. Only the showers count.
3. In the simulator, model the DWHR as a higher cold water temperature during showers. How does it change the tank size you need?
4. List other ways to cut the hot water heat demand (lower setpoint, water-saving shower heads, tank insulation, shorter pipes). Estimate the saving of one of them and compare it with DWHR. Which ones conflict with using the tank as a thermal battery?

## Part 6. The tank as a thermal battery

### 6a. Size the tank by hand

Size the tank so it can work as a thermal battery for your charging strategies, using the four-step method in the section "Sizing the tank as a thermal battery" of the textbook. Do it for each charging strategy, with and without DWHR:

1. Hourly heat demand from your tapping profile (Part 1), plus the standing loss of the tank (Part 3).
2. Hourly charging: the daily heat spread over the allowed hours. Check that your heat pump can deliver it.
3. Cumulative demand and charge curves (one plot per strategy), and the heat the tank must store.
4. Tank volume, with a usable fraction you justify. Round up to a tank size you found in Part 3.

Hand in the spreadsheet and the plots.

### 6b. Check in the simulator that the tank does not run empty

For each tank from 6a, run the simulator with your tapping profile and charging strategy:

1. Does the tank run empty? Look at the unmet hot water in the summary and at the tank temperatures in the heatmap: when does the hot zone reach the top of the tank, and which tapping gets too cold water?
2. If the tank runs empty, increase the size one step at a time until it does not. Report the smallest tank that keeps the comfort, and compare it with your hand estimate. Explain the difference (thermostat control and sensor position, the thermocline, the standing loss).
3. A strategy that leaves a shower cold is not acceptable, whatever it saves.

**Questions on tank sizing**

- Why does the night-charged tank lose less heat per day than the tank charged all day, even though it is larger?
- What happens to the stored heat $Q_{store}$ if your household moves its evening showers to the morning? Sketch the curves before you calculate.
- Charging at 00–06 and again at 11–15, when solar power makes electricity cheap, splits the day in two. How does that change the tank size?
- Drain water heat recovery cuts the heat drawn by the showers. Which step of the method does it change, and how much smaller can the tank be?

### 6c. Simulate the week

For every combination of heater, DWHR, charging strategy and the tank size from 6b:

1. Run the simulator and read off the electricity use per hour, the heat loss, the number of starts and the mean COP.
2. Multiply the hourly electricity use by your hourly consumer price and by your hourly primary energy factor. Sum over the week. Compare with the primary energy you get from the fixed BR18 factor.

Report the results in one table: tank size (hand estimate and checked), weekly kWh electricity, weekly cost (DKK), weekly primary energy (kWh, total and non-renewable), unmet hot water and standing loss.

## Part 7. Life cycle cost

1. Scale the typical week to a year (52 weeks). Explain why this is a simplification, and in which direction it is likely to be wrong.
2. Calculate the life cycle cost over 20 years with a real discount rate of 3 % (try 1 % and 5 %) and your component lifetimes, including reinvestments.
3. Calculate the annual primary energy use, with the hourly factors and with the fixed BR18 factor.
4. Plot LCC against tank size for each heater, with and without DWHR. Where is the optimum?
5. Plot LCC against annual non-renewable primary energy for all options. Which options are on the front (no other option is better on both)?

## Part 8. Discussion

- Which pays back first: reducing the demand (DWHR) or storing more (a bigger tank)? Answer for each heater.
- Does the strategy with the lowest cost also give the lowest primary energy? If not, why not?
- How good a proxy for CO₂ is the hourly non-renewable primary energy factor? When would it give the wrong answer?
- Why does load shifting save more money with a resistance heater than with a heat pump?
- What happens to the grid if every house charges at 00–06? What happens to the night price?
- Which single input changes your ranking the most? Show it with a sensitivity plot.

---

## Notes for the teacher (not for students)

- **Typical week temperature.** The annual means in the course weather files are about 8.2–9.6 °C, depending on the file and period. A week near the annual mean will fall in April–May or October.
- **Data access.** Energi Data Service has a web UI with CSV download and a REST API (`https://api.energidataservice.dk/dataset/<name>?start=...&end=...`). The day-ahead market moved to 15-minute prices on 1 October 2025, so students who take a year spanning that date must handle two resolutions.
- **Primary energy factors.** `ProductionConsumptionSettlement` gives hourly production by source per price area, which is enough for the hourly factor. The split of thermal production between fossil and biomass is not in that dataset; students can take it from the annual declaration (Energinet) or assume it. Imports are the weak point of the method; a fixed factor is acceptable at this level.
- **Workload.** This is a lot for one assignment. If it must be shorter, give out Part 3 (costs) as a table and keep Parts 1, 2 and 4 as the data work.

### What the simulator needs before this assignment works

The current simulator handles the tank, the stratification, the tapping profile and the charging hours. It is missing:

1. **A week, not a day.** It now repeats one day three times. It needs to run 7 days with a different tapping day each day (the DHWcalc import already holds a full year).
2. **Heater choice.** Resistance heater (COP 1) or heat pump.
3. **Hourly outdoor temperature** feeding the COP, instead of one fixed source temperature.
4. **DWHR switch** with an effectiveness, raising the cold water temperature during showers.
5. **Price and primary energy factor input.** Paste or upload a 24-hour (or 168-hour) profile, and show cost and primary energy in the summary.
6. **CSV export** of the hourly electricity use, so students can do the economics in their own spreadsheet.
7. **"Cheapest N hours" strategy** based on the price profile (optional).

### Sources checked

- Energi Data Service API guide: <https://www.energidataservice.dk/guides/api-guides>
- Energi Data Service data catalogue: <https://www.energidataservice.dk/Data_catalog_EN.pdf>
- Energinet, new declaration datasets: <https://energinet.dk/media/5jmnrole/new-declaration-datasets-on-eds.pdf>
- 15-minute day-ahead prices: <https://github.com/openhab/openhab-addons/pull/18695>
