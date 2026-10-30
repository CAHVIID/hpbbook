# Training exercise: Energy analysis using IDA ICE

Heating demand and cooling demand are influenced by several factors, e.g. climate conditions and heating/cooling setpoints.

This exercise serves as a first methodological step into energy analyses, and as a way for students to familiarize themselves with the multi-faceted and integrated domains of *thermal simulations*, *building service systems* and *controls* in IDA ICE.

The learning objectives are to:

- quantify the impact of future climatic conditions on residential heating and cooling demand
- quantify the impact of an overhang on daylight and residential heating and cooling demand.

Please upload your results using the provided link.

## Part 1: Install IDA ICE

- Download IDA ICE 5.2 from Equa; the download link and the licence key are on DTU Learn.
- Do **not** save your IDA ICE project files in a OneDrive or Dropbox folder. Constant syncing can make IDA ICE run slower.
- The weather files are on DTU Learn.

## Part 2: Useful resources

Official documentation and guides:

- **IDA ICE Help**, built into the software (press F1)
- Equa AB official tutorials: <https://www.equaonline.com/iceuser/new_documentation.html>
- *Getting Started with IDA ICE*: <https://equa.cloud.xwiki.com/xwiki/bin/view/IDA_ICE/ICE_Gettingstarted/ICE_GS/>

Video tutorials:

- Equa's official YouTube playlist: <https://www.youtube.com/playlist?list=PLiyWmurrMD11Rr5bhe1JhrQsdZKz27Ht2>

## Part 3: Exercise questions

:::{important} Instructions
For each question, create a simulation in IDA ICE and document your process. **Document the results: save screenshots of your model setup, graphs and result tables.**

If in doubt about anything, take a decision yourself. The task is not to report accurate numbers, but to familiarize yourself with IDA ICE and quantify differences.

- Dimensions in IDA ICE are always internal dimensions.
- IDA ICE can run different types of simulations: *heating design*, *cooling design*, *overheating*, etc. **In this course, we only run "Custom" simulations.**
- **Use the default input: do not change anything unless it is explicitly stated in the exercise text.**
:::

### Reference

1. Create *one* zone with *one* external façade: 4 m × 4 m, room height 2.6 m.
2. Place a window in the external façade, size w × h = 2.8 m × 1.2 m, with the lower edge 0.8 m from the floor. **Rotate the zone towards south.**

   ```{image} figures/model.png
   :width: 45%
   ```

3. Change the location to *Copenhagen Airport* (look for the *Download* feature).

   ```{image} figures/location-download.png
   :width: 60%
   ```

4. Look for the *Import climate file* feature and load the weather file *DRY_2011-2023_epw.epw*. It represents a typical meteorological year around 2020.

   ```{image} figures/climate-import.png
   :width: 60%
   ```

5. Press *Custom* simulation and wait for the simulation to finish.

   ```{image} figures/custom-simulation.png
   :width: 40%
   ```

6. Go to the *Summary* tab and look for the *Systems energy* window (bottom left). Note the kWh of *Cooling* and *Heating* (blue print). This is the total annual heating and cooling energy supplied to your zone.

   ```{image} figures/systems-energy.png
   :width: 30%
   ```

7. Look above for *Energy balance* (blue print). Click on it and save the report.

   ```{image} figures/energy-balance.png
   :width: 45%
   ```

### Q1. Reference demand

Report the reference results:

1. heating demand in kWh
2. cooling demand in kWh.

### Q2. Reduced heat losses

- Increase the insulation level to improve the U-value of the *façade* to below 0.15 W/m²K.
- Replace the glazing with a triple-layer low-energy glazing. Choose an existing product from the database; the key words are low U-value and high g-value. Improve the U-value of the *glazing* to below 0.8 W/m²K.

  ```{image} figures/glazing-database.png
  :width: 60%
  ```

- Change the internal gains by setting *Equipment* to 5 W/m². Set occupants and lighting to 0 W/m².
- Change the mechanical ventilation rate to 0.3 L/s per m².

Report:

1. heating demand in kWh (**set to index 100**)
2. cooling demand in kWh (**set to index 100**)
3. a screenshot of the energy balance report
4. Inspect the report and comment on the heating versus the cooling demand.

### Q3. Future climate

Simulate the Q2 model with three climate files:

- *DRY_2011-2023_epw.epw* (~2020). This was also done in Q2.
- *DRY_rcp45_2045-2064_epw.epw* (~2050)
- *DRY_rcp45_2080-2099_epw.epw* (~2090)

Report:

1. the heating index for 2050 and 2090
2. the cooling index for 2050 and 2090.

### Q4. Setpoint temperatures

- Change the cooling setpoint from 25 °C to 26 °C.
- **Deliverable:** calculate the percentage reduction in cooling energy.

### Q5. Daylight

Using the **reference from Q1**, run a *Climate-based daylight (Radiance)* simulation for a horizontal surface inside the room at 0.8 m above the floor. Choose low precision.

1. Report *sDA300, % of plane*.

### Q9. Shading device

- Select a shading device (**Integrated window shading**): *External blind (BRIS)* from the database.

  ```{image} figures/shading-device.png
  :width: 60%
  ```

- Choose the climate file *DRY_rcp45_2045-2064.epw* (~2050).

Then:

1. Select *Shading control* as requested output.
2. Run a custom thermal simulation.
3. Run a daylight simulation where the shading device is controlled according to the custom control signal.

```{image} figures/output-shading-control.png
:width: 60%
```

Report:

1. *sDA300, % of plane* with the shading activated
2. the heating demand index
3. the cooling demand index
4. How is the shading controlled (what causes it to activate and deactivate)? Find this in the manual and describe it in your own words.

## Part 4: Reflection task

Write a short paragraph answering: *Which change in the building parameters had the biggest effect on energy demand, and why? What surprised you the most?*

Discuss with your preferred AI tool and write a one-page summary of how to renovate the European building stock. You can for instance ask:

- Which are the barriers?
- Which are the solutions?
- What are the key recommendations?

Remember: the summary should be outstanding given the allowed use of AI, and you should be 100 % ready to defend the text.
