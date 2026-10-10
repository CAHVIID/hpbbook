# Assignment: Passive cooling of the row house

*Draft 2026-10-10. Replaces "Assignment 04 – improved". Teacher notes are in [square brackets] and will be removed.*

:::{note} Files for this assignment
All files are in the folder `assignments/cooling/` of the book repository:
- `weather/5A_Copenhagen_HW_MostSevere_2054_clean.epw`: the heat-wave weather file for part 4.
- `code/fan_comfort.py`: comfort, fan energy, cooling fan efficiency and cooling COP from IDA ICE results (part 3 and 4).
- `code/feet_draught.py`: peak draught rate at feet level from an exported air-velocity field (part 2).
- `code/clean_epw.py`: the script that repaired the weather file.
:::

State who was responsible for which part in your submission.

## Aim

The row house from assignments 1–3 has a very low heating demand. In summer the same airtight, well-insulated envelope keeps the heat in, and the future Copenhagen climate brings warmer summers and longer heat waves. In this assignment you design the passive cooling of the house, step by step, following the cooling strategy from the course:

| Part | Step in the cooling strategy | Main tool |
|---|---|---|
| 1 | Reduce solar gains: window size | IDA ICE AutoMOO optimisation |
| 2 | Remove heat: ventilative cooling through a hatch, without draught | Jet theory + IDA ICE |
| 3 | Cool the people: ceiling fans in peak periods | Fan data, cooling effect, IDA ICE |
| 4 | Survive the heat wave: shutters (+ fans) | IDA ICE heat-wave run |

Each part builds on the model from the previous part. Keep one IDA ICE file per part, so you can go back.

## Common settings

- **Weather, parts 1–3:** `5A_Copenhagen_TMY_2041-2060.epw` (Annex 80, typical year around 2050). The 2050 climate is more critical than 2090, because 2050 has more solar radiation.
- **Weather, part 4:** `weather/5A_Copenhagen_HW_MostSevere_2054_clean.epw` (Annex 80, Qian 2021). The heat wave runs from 9 July to 5 August 2054: four weeks, outdoor maximum 32.0 °C, 14 days above 28 °C, but nights down to 11 °C. The original file had six hours with diffuse and global radiation of 0.9–5.6 million W/m². These are repaired: the direct beam is kept and the diffuse radiation is taken as the mean of the hours before and after. [HW_Longest_2045 is not used: it has no solar radiation on 1–14 August.]
- **Comfort criterion:** EN 16798-1 adaptive model, category II, in occupied hours, May–September (part 4: the heat-wave period). Report hours above the category II upper limit, θ_c + 3 °C with θ_c = 0.33 θ_rm + 18.8.
- Do not judge your results against the BR18 limits (100 h > 27 °C, 25 h > 28 °C). Those limits belong to the BR18 compliance model with its fixed assumptions, not to a detailed IDA ICE model.
- Supply: the IDA ICE files `row_house_assign_4_room_heating.idm` (whole house, return-temperature-controlled ventilation down to 10 °C supply from assignment 3) and the single-zone model for part 1.

---

## Part 1: Optimise the window size with AutoMOO

Large windows give daylight and view, but also solar gain. Since BR18, daylight can be documented with climate-based simulation to EN 17037 (sDA300,50% ≥ 50 %), so the window size can be optimised for the lowest cooling and heating demand that still meets the daylight requirement.

Use the single-zone model: the critical centre zone of the row house, 4 × 4 m, 2.5 m room height, U = 0.1 W/m²K, facing north or south.

**Q1.1 Reference.** Simulate the zone with the reference window and your best glazing from assignment 1. Report sDA300, cooling demand and heating demand (kWh/m²) for north and south.

| | sDA300 (%) | Cooling (kWh/m²) | Heating (kWh/m²) | Hours > adaptive cat. II |
|---|---|---|---|---|
| North | | | | |
| South | | | | |

**Q1.2 AutoMOO study.** Set up a multi-objective optimisation in IDA ICE:
- Variables: window height (sill at 0.9 m) and window width. Optional: glazing type (add one or two solar-control glazings, keep U ≤ 0.6 W/m²K and high selectivity LT/g), overhang depth.
- Objectives: minimise cooling demand and heating demand.
- Constraint: sDA300 ≥ 50 %.
- Make sure the whole range is physically possible (the window must fit in the wall).

Upload the Pareto front (cooling against heating demand), with your chosen design marked.

**Q1.3 Choose a design** for north and south and fill in the table from Q1.1 again. How much did the cooling demand and the overheating hours drop?

**Q1.4 Reflect.** Why is the optimal south window smaller than the north one? What did the optimisation leave out (view out, glare, the other rooms, future weather, cost)?

*IDA ICE hints*
- Parametric runs → choose the optimisation (AutoMOO) rather than a full grid. Set the role of each output: objective (minimise) or constraint.
- Simulation type: "custom" plus "climate-based daylight". Keep generated models: yes. Clear results from previous runs: ask.
- Relax the tolerance, set a max time step and limit the outputs to keep the runs fast. Test with a few runs first.
- [Facade chapter worked example: south optimum g 0.32, 1.2 m overhang, 1.1 m window height, sDA 53 %, cooling 19.6 kWh/m² (−63 %); north 1.4 m, sDA 59 %, 15.1 kWh/m² (−27 %). Use as a check, not in the hand-out.]

**Deliverables:** Q1.1/Q1.3 table, Pareto figure, chosen design for north and south, 5–10 lines of reflection.

---

## Part 2: Design a venting hatch without draught

Carry the north and south window designs from part 1 into the whole-house model. Ventilative cooling needs large airflows (4–10 ACH), and large airflows of cool outdoor air can cause draught. In summer the problem is not the hot afternoon, when the air is welcome, but the evening, night and shoulder season, when the outdoor air is 8–12 K below the room.

### 2A Hatch design

**Q2.1** Design a venting hatch for the perimeter rooms. Choose the type and position:
- high bottom-hung (air attaches to the ceiling as a wall jet),
- low (air spreads along the floor),
- side-hung (thermal jet),
- or another type you can argue for.

The hatch must protect against rain and burglary, allow night opening, and add little heat loss. If it replaces a window opening, check the fire escape rule (width > 0.5 m, height > 0.6 m, width + height > 1.5 m, sill ≤ 1.2 m above the floor). Draw a cross section with dimensions, and give the free opening area and discharge coefficient C_d.

**Q2.2** Calculate the centre U-value of the closed hatch (neglect thermal bridges). Implement one hatch per perimeter zone in IDA ICE as a window with frame fraction 0.999 and frame U-value = the hatch U-value. Report the house's mean U-value before and after (Input data report) and the change in heating demand.

### 2B Draught risk from jet theory

**Q2.3** For your hatch, calculate the maximum air speed in the occupied zone as a function of the airflow, for two cases:

| Case | Indoor | Outdoor | ΔT |
|---|---|---|---|
| Summer afternoon | 26 °C | 24 °C | 2 K (near isothermal) |
| Summer night | 25 °C | 15 °C | 10 K |

Use the flow element that fits your hatch:
- **High bottom-hung hatch, ceiling wall jet** (Svidt, Heiselberg & Nielsen 2000):
  u_m(x) = K_a · U_0 · √a_0 / (x + x_0), with K_a ≈ 7 and x_0 ≈ −2 m,
  where U_0 = q_0/a_0 is the speed in the free opening area a_0 and x the distance from the hatch. Conservatively, take the speed where the jet turns down at the opposite wall as the speed entering the occupied zone.
  Check whether the jet stays on the ceiling: Heiselberg (2006) says the supply acts as a jet for ΔT < 5 K and/or Δp > 4–6 Pa; for small driving forces and large ΔT the cold air drops along the wall to the floor. Use the Archimedes number Ar = g β ΔT h_0 / U_0² to argue for your case.
- **Low opening, floor flow** (Nielsen et al. 2000): u(x) = K · q_0 / x, with K ≈ 4–5 m⁻¹ near isothermal (4.4 m⁻¹ fitted to the Bugenings et al. 2025 louvre data) and up to about 10 m⁻¹ with a large ΔT. Evaluate at 0.1 m above the floor, 1 m from the wall.
- **Side-hung window:** treat as a low opening with the larger K.

Then judge the draught two ways:
- ISO 7730 draught rate, DR = (34 − t_a)(v − 0.05)^0.62 (0.37 v Tu + 3.14), with Tu = 40 % if unknown. DR ≤ 20 % is acceptable (category II). Do not apply any "feet factor" to DR.
- ASHRAE 55-2020 ankle draught (Liu et al. 2017): PPD_AD = 100 · e^z / (1 + e^z), z = −2.58 + 3.05 v_ankle − 1.06 TS, limit 20 %. This equals v_ankle < 0.35 TS + 0.39 m/s.

**Q2.4** From Q2.3, draw the maximum allowed airflow, in ACH, against ΔT (indoor − outdoor) for your hatch. This is your hatch's draught limit. Compare it with the Roth et al. (2023) chart in lecture 16.2 (use the CBE/ankle curve).

### 2C Ventilative cooling in IDA ICE, limited by draught

**Q2.5** Let the hatches open on room temperature with a cooling setpoint that reflects reasonable occupant behaviour (same setpoint in all zones, all year; active cooling devices are removed in the model). Keep the roof house skylight closed (cross-ventilation only). Simulate June–August. Report the setpoint, the hours above the adaptive category II limit, and the peak airflow (ACH) through each hatch.

**Q2.6** Repeat with stack ventilation through the roof house skylight. Give the skylight its own PI control on the temperature in the most critical zone (not the roof house temperature). Upload a figure of the zone temperatures and the skylight opening for a warm week. Report hours above the category II limit and below 21 °C.

**Q2.7** Now limit the opening so the hourly ACH never exceeds your draught limit from Q2.4 at the actual ΔT. Report the hours above the category II limit again. How much cooling did the draught limit cost?

**Q2.8 Check with the flow element model.** Pick the hour with the highest draught risk from Q2.5–Q2.7 (large hatch airflow and large indoor–outdoor ΔT). Run the IDA ICE flow element model for that hour and export the air-velocity and temperature field. Calculate the peak draught rate at feet level (0.1 m) with `code/feet_draught.py`: set the file and its column names at the top of the script and run it. It reports the peak ISO 7730 DR, the peak ASHRAE 55 ankle draught PPD_AD, where they occur, and the share of the floor area above 20 %, and it plots a DR map.

Compare the peak with your jet calculation in Q2.3. Which is more conservative, and why?

*IDA ICE hints*
- Hourly airflow through each opening is in the zone results ("Air flow through openings" / leaks and openings). Convert to ACH with the zone volume.
- Limit the airflow with the window's maximum opening fraction, or, in the advanced level, add a limiter on the opening signal that depends on outdoor temperature. Check afterwards that the peak ACH really stays under your limit.

**Deliverables:** hatch drawing with dimensions, U-value and heating penalty, jet calculation (show the work), ACH-limit chart, table of hours above the category II limit for Q2.5–Q2.7, feet-level DR map and peak values from Q2.8.

---

## Part 3: Ceiling fans for peak periods

Ventilative cooling cannot cool the room below the outdoor temperature. In warm periods a ceiling fan lets occupants accept a higher temperature, at a fraction of the power of air-conditioning.

**Q3.1 Choose a fan.** Find a ceiling fan on the market for a bedroom or living room in the row house. Report diameter, airflow and power at each speed setting. Check the mounting: the blades should be at least 2.3 m above the floor (EN 60335-2-80) and about 0.2 D below the ceiling. What does that mean for a 2.5 m ceiling? [Christian to confirm the 2.3 m value.]

**Q3.2 Air speed and cooling effect.** Estimate the room-average air speed for a seated occupant with the Raftery et al. (2019) model from the ceiling fan chapter (S_F = 4Q/πD², then S_O,avg). Calculate the cooling effect (CE) with pythermalcomfort `cooling_effect()` (ASHRAE 55 / SET), for example at 28 °C, 50 % RH, 1.2 met, 0.5 clo. For reference: 0.5 m/s gives about 2.8 °C at 28 °C.

**Q3.3 Cooling fan efficiency.** CFE = CE / P_fan (°C per W) for each speed. Which speed is most efficient?

**Q3.4 Peak-period operation.** Save the part 2 model as "unpacked" so each zone gets a folder with `TEMPERATURES.prn` and `IAQ.prn`. Enter the model folder, your fan datasheet, the room sizes and the occupied hours in the input section of `code/fan_comfort.py` and run it. For every occupied hour the script:
- takes the air and operative temperature from IDA ICE and finds the mean radiant temperature (t_r = 2 t_op − t_air);
- starts the fan when PMV at still air exceeds 0.5, and picks the lowest speed that brings PMV back to 0.5;
- calculates the room-average air speed (Raftery), the cooling effect CE (SET), and PMV with the fan (ASHRAE 55 elevated air speed method);
- counts the hours above the adaptive category II limit with t_op and with t_op − CE.

Report the fan hours per speed, the fan electricity (kWh), the PMV distribution with and without fans, and the hours above the category II limit with and without fans.

**Q3.5 Cooling COP.** The fan does not remove heat; it lets the occupant accept a room that is CE warmer. An air-conditioner would instead have to lower the room temperature by CE, which in steady state takes Q_eq = H · CE, with H (W/K) the zone's heat loss coefficient (transmission and ventilation). The script sums Q_eq over the fan hours and reports

COP_fan = Q_eq / E_fan

Find H for each zone from IDA ICE: add an ideal cooler, run with cooling setpoints T_sp and T_sp + 1 K, and divide the difference in cooling energy by 1 K and by the number of hours. Enter H in the script. Compare COP_fan with the SEER of a split air-conditioner (about 5–8). Why is the COP of a fan in a well-insulated house lower than the factor 10–100 often quoted? Comment on primary energy, and on when the fans run compared with the electricity price.

*Hints*
- `pip install pythermalcomfort pandas openpyxl`. The results are written to `fan_results.xlsx` (sheets `fan` and `zones`) and to `hourly_results/<zone>.csv` for your own figures.
- The fan power only counts in fan hours.
- Check the clothing, metabolic rate and the PMV threshold in the input section, and argue for your choice.

**Deliverables:** fan datasheet values, table of air speed, CE, power and CFE per speed, fan hours and kWh, hours above category II with and without fans, COP_fan with the calculation shown, 5–10 lines comparing fans with air-conditioning.

---

## Part 4: Shutters for heat waves

In a four-week heat wave the windows, hatches and fans may not be enough. External shutters, closed during the day, block almost all solar gain, at the cost of daylight and view. The hatches keep ventilating while the shutters are closed.

**Q4.1 Baseline heat wave.** Run your part 2 model (with the draught-limited hatches) on the MostSevere 2054 weather file. Report, for the heat-wave period 9 July–5 August, the hours above the adaptive category II limit, the maximum operative temperature, and the warmest night (mean operative temperature 23–07) for the most critical zone.

**Q4.2 Shutter control.** Add external shutters to the windows facing south, east and west (decide about north). Choose and justify a control rule, for example: closed when the incident solar radiation on the window exceeds about 150–200 W/m² and the room is above a temperature threshold, open otherwise. Think about occupants: would they accept closed shutters in the morning, or at weekends?

**Q4.3 Test the shutters** on the heat-wave run and report the same results as Q4.1. Upload a figure of outdoor, zone operative and adaptive limit temperatures for the warmest week, with and without shutters.

**Q4.4 Fans on top.** If the shutters are not enough, add the ceiling fans from part 3: run `code/fan_comfort.py` on the heat-wave results (set `EPW_FILE` to the heat-wave file and `PERIOD` to 9 July–5 August). Report the final table:

| Heat wave, critical zone | Hours > cat. II | Max T_op (°C) | Warmest night (°C) | Fan kWh |
|---|---|---|---|---|
| Part 2 hatches only | | | | – |
| + shutters | | | | – |
| + shutters + fans | | | | |

**Q4.5 Conclude.** Is the house safe to live in during the heat wave without active cooling? Which step mattered most, and what would you do next?

*IDA ICE hints*
- Model the shutter as an external shading device with a low solar factor (g multiplier about 0.05–0.1) and its own control (schedule, solar radiation and zone temperature).
- Check that the shutter does not also close the hatch: the hatch must be a separate opening.
- Annual results are meaningless for this weather file. Extract the heat-wave period only.

**Deliverables:** shutter description and control rule, heat-wave figure, the final table, 5–10 lines of conclusion.

---

## Guiding questions for the report

1. Which of the four steps gave the largest reduction in overheating hours per krone? Which was free?
2. Your window optimisation was done for the 2050 typical year. Would it change for the heat-wave year?
3. Where in the year does your hatch hit its draught limit, and would occupants close it anyway?
4. A fan with a COP of 50 sounds better than any air-conditioner. What does the comparison leave out?
5. Shutters solve the heat wave but darken the home. How would you hand the shutter decision to the occupants?

## Sources

- EN 16798-1:2019; ISO 7730:2005; ASHRAE 55-2020 (ankle draught, cooling effect).
- Heiselberg, P. (2006). Design of Natural and Hybrid Ventilation. DCE Lecture Notes 5, Aalborg University.
- Nielsen, P.V. et al. (2000); Svidt, K., Heiselberg, P. & Nielsen, P.V. (2000): flow elements for windows and hatches.
- Bugenings, L.A., Kamari, A. & Rong, L. (2025). Experimental investigations of a full-scale louvre element. Aarhus University.
- Liu, S., Schiavon, S. et al. (2017). Predicted percentage dissatisfied with ankle draft. Indoor Air.
- Roth, J., Heiselberg, P. & Zhang, C. (2023). Thermal comfort and risk of draught with natural ventilation. AIVC, Copenhagen.
- Raftery, P. et al. (2019); CBE Ceiling Fan Design Guide (2020).
- Qian, B. (2021), Annex 80 Copenhagen weather files.
- Lectures 16.1, 16.2, 17.1, 17.2; book chapters on cooling strategy, ventilative cooling and ceiling fans.
