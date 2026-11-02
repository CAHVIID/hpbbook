# Assignment 4: Passive cooling

:::{important}
Remember to state who was responsible for which part in your submission.
:::

## Aim

In face of climate change, residential cooling has become increasingly important. The aim of assignment 4 is to investigate and combine passive cooling solutions that can mitigate overheating and avoid the necessity of active cooling.

## Motivation

The row house has been optimized to a very low level of heating demand. However, low-energy houses suffer from cooling demand, and this will only be worsened in face of changing climates, especially the severity and longevity of heat waves.

Structure:

- Façade designs to balance daylight and solar gains
- Ventilative cooling
- Ceiling fans

:::{note}
So far we have used the newest official weather files from the Danish Meteorological Institute. However, in this assignment we will use a different set of weather files from Annex 80, because it has heat wave files.
:::

## Façade designs to minimize cooling demand

From the Building Code 2018, it became possible to document daylight according to EN 17037 using climate-based daylight simulation. This means that façade designs can be optimized to meet daylight requirements and minimize solar gains. In this task you will use the parametric features of IDA ICE to simulate the best combination of façade elements that still meets the daylight requirement, while minimizing the need for additional cooling.

The proposed inputs are the following, but if you think there are others, please discuss their relevance and impact internally in the team:

- Window size, specifically the height of the window, assuming that the lower edge of the window is 0.9 m from the floor
- Glazing types, specifically new types with reduced g-value and high selectivity
- Overhang depth, e.g. balconies or ribbed fins that reduce incident radiation from high sun elevations
- Side fins on one side or both sides that reduce incident radiation from low sun elevations
- Orientation, specifically towards North and South

:::{figure} figures/explore-example.png
:label: fig-a4-explore
:alt: Parallel-coordinates plot from the IDA ICE Explore view, with axes for glazing height, glazing type, orientation, overhang depth, sDA300, heating, cooling, hours above 25 °C and hours above 27 °C. A few highlighted runs with sDA300 between 55 and 65 % have the lowest cooling demand.

Example of the Explore view of a parametric study in IDA ICE.
:::

The output to gauge the performance is:

- Spatial Daylight Autonomy, specifically it is important to comply with the Building Code requirement of at least 300 lux for 50 % of the daylight hours in at least 50 % of the daylight plane: sDA300,50% > 50 %. Plane 0.5 m from the floor.
- Annual zone cooling demand, specifically to gauge the impact on cooling demand
- Annual zone heating demand, specifically to gauge the impact on heating demand when solar radiation is minimized

For fastest simulation, we simplify the row house and focus on the most critical centre zone: a 4 × 4 m zone with 2.5 m room height. Prefab constructions with U-values of 0.1 W/m²K. The simulation is sped up additionally by relaxing the tolerance, and setting the maximal time step and the output time step as shown in {numref}`fig-a4-simdata`.

:::{figure} figures/simulation-settings.png
:label: fig-a4-simdata
:alt: IDA ICE Simulation data dialog, Advanced tab: tolerance 0.2, maximal time step 1 h, maximum number of periods 14, tolerance for periodicity 0.001, time step for output 1 h, time-split parallelization ticked.
:width: 45%

Simulation settings for the parametric study.
:::

### Q1: Reference daylight and cooling demand

This question establishes the reference before you are asked to optimize the façade in Q2.

Make a single thermal zone model, 4 × 4 m, room height 2.5 m, with one window (just like the one in the training exercise from Week 1), and implement three glazing types in the database. Start with your best glazing type from Assignment 01 (or better) and add solar coatings to the outer glass to reduce the g-value (surface 2 from outside). Try to keep the selectivity high (= light transmittance (representing the visible spectrum) divided by g-value (representing the total spectrum)). Keep the U-value below 0.6 and LT above 50 %.

| Glazing | Description/Code | U | LT | g | Selectivity |
|---|---|---|---|---|---|
| Assign. 01 | | | | | |
| Type 2 | | | | | |
| Type 3 | | | | | |

Simulate "custom" and "climate-based daylight" with the reference glazing, and report sDA300 in % and the cooling demand in kWh for the zone orientations North and South as shown in the table below.

:::{important}
To get correct results, make sure the simulation period covers the full year.
:::

| Orientation | sDA300 [%] | Cooling demand [kWh/m²] | Heating demand [kWh/m²] |
|---|---|---|---|
| North | | | |
| South | | | |

**Deliverables:**

- table with glazing types
- table with simulated results

### Q2: Parametric study in IDA ICE

Set up a parametric study, and add the parameters you want to study (at least window height, glazing type, overhang depth and orientation). Set up range and distribution. Make sure the whole range is physically possible. Select reasonable parameter variation steps, but remember that the total number of simulations quickly explodes.

Add output metrics. Set the role of each metric: constrain sDA between 40 and 60 and ask for minimization of heating demand and cooling demand. This will help IDA ICE concentrate the simulations and increase the result resolution around the most interesting output.

Check simulation type "custom" and "climate-based daylight". Set Keep generated models to: yes, and Clear results from previous runs to: ask.

:::{tip}
Try and test with small studies and simulations before running the whole setup.
:::

When finished, open the "Explore" button and inspect the figure.

**Deliverable:** figure

### Q3.1: Façade design

Given that sDA300 has to be > 50 %, select a reasonable façade design combination that renders a low cooling demand towards North and South, respectively. Fill out the table below.

| | sDA300 [%] | Cooling demand [kWh/m²] | Heating demand [kWh/m²] |
|---|---|---|---|
| North | | | |
| South | | | |

### Q3.2: Evaluate parametric study

How much did the cooling demand change in kWh/m² from the reference to the façade design you chose in Q3 towards North and South, respectively?

### Q3.3

The parametric study has several weaknesses or aspects that were neglected. List as many as possible.

Your window optimisation was done for the 2050 typical year. Would it change for the heat-wave year?

**Deliverables:**

- table

## Ventilative cooling

Ventilative cooling is provided through envelope openings, sometimes automatic but most often manually operated by the occupants. This part implements venting hatches, gauges the cooling potential and analyses any unwanted results like overcooling, high air velocities and draught.

Use the provided IDA ICE model `row_house_assign_4_room_heating_wo_hatches.idm`.

This model already includes return temperature control with supply temperature down to 10 °C from Assignment 03 Part A for maximal cooling by mechanical ventilation.

:::{important}
Please change the façade of the model towards North and South to the optimal design you found in Q3.
:::

### Q5: Design a venting hatch

Design a venting hatch that complies with fire regulations, protects from incoming rain and burglary and introduces minimal extra heat loss through the envelope. Document the hatch design in a drawing showing a cross section with measurements.

### Q6: Hatch heat loss

Calculate and report the centre U-value of the hatch, neglecting the thermal bridges.

### Q7: Impact of hatch on heating demand

Implement your hatch in the provided IDA ICE file using a window with a frame fraction of 0.999. Set the frame U-value to the calculated centre U-value. Implement one hatch in each perimeter zone (6 total).

Report the average U-value before and after (you can get the exact numbers by using the "Input data report"). How much do you expect the heating demand to increase in percentage with your venting hatches?

### Q8: Ventilative cooling using single-sided ventilation

The venting hatch should open when a certain temperature threshold is met.

Decide on a reasonable cooling setpoint which should reflect reasonable human behaviour (for simplicity use the same setpoint for all zones for all year). The window opening setpoint collides with other active cooling devices, which are therefore removed in the provided IDA model.

Restrict the "custom" simulation to the summer months June–July–August, as this will minimize the risk of overcooling. Also, it minimizes "fictive" cooling that will not happen because of imminent draught risk.

Heating devices are also removed, as they should be off during June–August.

Keep the skylight in the roof house closed.

**Deliverables:**

- Report the selected cooling setpoint.
- Report the number of hours above 25 °C from all perimeter zones.
- When the hatch is controlled on individual zone control, the chance of cross ventilation is not great. Can you visualize when air is actually flowing through the building (IDA feature)?

### Q9: Ventilative cooling using stack ventilation

Repeat Q8, but this time exploiting the stack ventilation using the skylight in the roof house. Make the skylight open automatically using a PI controller.

Report the number of hours above 25 °C from all perimeter zones with the PI controller.

The skylight controller acts on the temperature in the roof house. Is that a problem, i.e. does it constrain the stack ventilation by being closed when there is need for ventilative cooling? Assess this by comparing the temperature of the roof house to the temperature of the perimeter zones. Upload a figure showing the temperature curves.

Repeat the simulation, but now give the skylight its own control based on the temperature in the most critical zone, with its own setpoint. Assess the number of hours above 25 °C and below 21 °C, and adjust the skylight activation setpoint a bit down for maximum cooling without overcooling.

**Deliverables:**

- Report the number of hours above 25 °C from all perimeter zones with the improved skylight controller.
- Report the number of hours in category II or better (adaptive thermal comfort model).
- Can you visualize how air is actually flowing through the building (IDA feature)?

### Q10: Risk of draught

Using ventilative cooling can easily create draught. Assess the risk of draught by inspecting the magnitude of airflow into each perimeter zone. Identify the peak airflow through the hatch.

Assess the risk of draught using the air velocity theory of displacement jets. Check with the 2D CFD simulator. Are there differences between CFD and jet theory?

**Deliverable:** worked-through draught documentation example, comparing jet theory with CFD results

## Ceiling fans

Facing more severe and longer heat waves, ventilative cooling may not provide enough cooling to the occupants.

Ceiling fans are well-known cooling devices, especially in warmer regions than Denmark. They come in many different shapes and designs, but over the years minimalistic designs, sometimes integrated with a ceiling lamp, have made their way into the market.

Ceiling fans are used to increase the overall air velocity in the space, which according to Fanger and the thermal sensation method (predicted mean vote, PMV) increases the heat transfer of the skin and the evaporation rate, in effect cooling the body.

An alternative to PMV is the American Standard Effective Temperature (SET), which is more relevant for elevated air velocities.

The questions that arise are:

- How much cooling can be provided by a ceiling fan? E.g. how much is SET reduced, or what is the equivalent operative temperature that would provide the same (reduced) PMV?
- Is the cooling enough considering the future Danish summer climate, also during extreme heat waves?
- What is the cooling fan efficiency?
- How much energy is used if there needs to be a ceiling fan in every habitable space?

### Q11: Impact of ceiling fans on thermal comfort, and energy use

Use the refined IDA ICE file with improved façade design and ventilative cooling. Change the climate file to the most severe heat wave year from Annex 80 (`5A_Copenhagen_HW_MostSevere_2054_clean.epw`).

Select a ceiling fan online, use the provided script, and report SET before and after implementation of ceiling fans.

Report the total energy used by the fans.

The alternative to ceiling fans is probably air-conditioning. Given the results of the analysis, write a summarizing section that tells the reader what the mitigating measures are in the row house preventing overheating in a "normal" 2050 climate and in heat wave years.

:::{note} Files for this assignment
The folder `assignments/cooling/` of the book repository holds:
- `weather/5A_Copenhagen_HW_MostSevere_2054_clean.epw`: the Annex 80 heat-wave year (9 July to 5 August 2054), with six corrupt radiation hours repaired.
- `code/fan_comfort.py`: the provided script for Q11. It reads the IDA ICE `TEMPERATURES.prn` files and calculates SET, the cooling effect, PMV, fan energy and the cooling fan efficiency.
- `code/feet_draught.py`: peak draught rate at feet level from an exported air-velocity field (Q10).
:::
