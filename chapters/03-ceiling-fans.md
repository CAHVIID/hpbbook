# Ceiling fans

# Purpose

Chapter 3 should teach students to size and control a ceiling fan as the first cooling stage. The fan raises air speed so occupants accept higher temperatures, and it uses far less energy than air-conditioning. The chapter turns the 17.1 lecture, the 17.2 adaptive comfort material and the CBE Ceiling Fan Design Guide (2020) into one readable text, and it feeds directly into Assignment 04 Q11.
After the chapter, students can:
• explain how elevated air speed offsets operative temperature, using PMV/SET and the adaptive model;
• size and place a fan for a room from a datasheet;
• set a temperature-stepped control strategy that puts the fan before AC;
• estimate the change in PMV and the fan energy for a room, and compare it with AC.

# Proposed outline
1. Why fans? Fans as an alternative to AC in a warming Danish climate, and the course row house in 2050. Fan types: ceiling, standing, tower, desk and personal fans.
2. Air speed and comfort. How the body loses heat, and the cooling effect of air speed. Operative temperature versus PMV versus the adaptive model, and why the adaptive model suits residences. Key number: 0.5 m/s gives about 2 °C cooling effect (SET, ASHRAE 55 Appendix D). Elevated air speed in EN 16798, ASHRAE 55 and ISO 7730, with the CBE comfort tool as a hands-on aid.
3. How a ceiling fan moves air. The impinging jet (core, expansion and radial floor spread). The highest speeds are under the fan, and a larger diameter relative to the room gives more uniform speeds. Draught from above: mean velocity and turbulence intensity.
4. Fan performance and energy. Fan laws: airflow is proportional to speed and power to speed cubed, so efficacy falls at high speed (median 165 cfm/W at low speed vs 79 cfm/W at high). Compare fans only at equal diameter and airflow. HVAC savings typically exceed fan energy 10 to 100 times. Watch for CFM vs m³/h on datasheets.
5. Sizing and placement. Diameter of 0.2 to 0.4 times √(floor area). One centred fan serves aspect ratios up to 1.5:1, and larger rooms are split into square fan cells. Clearances: blades at least 2.1 m above the floor, at least 0.2–0.3 m below the ceiling and at least 0.45 m from walls. Coordinate with lighting and sprinklers.
6. Control. The fan is the first cooling stage: the fan starts around 23–24 °C and AC only around 25.5–26.5 °C. Minimum speed should stay below about 0.4 m/s for seated occupants. Occupant control versus automation, and reverse mode for winter destratification.
7. Modelling fans. IDA ICE fixes air speed at 0.1 m/s in its comfort output, so fan effects must be post-processed. The course PMV script, with its stepped control (0.1/0.5/0.9 m/s at 25/27/29 °C), is the method.
8. Rules of thumb and guiding questions in the style of chapter 1.

# Worked example and assignment link
The chapter would follow one bedroom or living room in the course row house, using the steps from the 17.1 lecture:
1. Pick a fan datasheet and read its diameter, rated airflow and rated power.
2. Check the diameter against the room using the sizing rule and the clearances.
3. Calculate the rated specific fan figure, then air speed and power at low, medium and high, assuming both scale with airflow.
4. Apply the stepped control and compute PMV with and without the fan, plus annual fan energy.
5. Compare with AC using primary energy as a proxy for carbon.
The chapter would end with the three questions from Assignment 04 Q11. How much cooling does a fan give? Is it enough in future Danish summers, including the Annex 80 heat waves? How much energy does a fan in every habitable room use? The text gives the method, and students answer these for their own model.

# Open points in the source material
These should be settled before the worked example uses real numbers:
• In the PMV script output, the stored With_fans.csv and Without_fans.csv are identical, so they show no fan effect.
• The script charges the 15 W low-speed fan power in every hour, even when the fan is off at 0.1 m/s.
• The paths in input_files.py still point to the E25 folder.
• In the stored results, T_op exceeds 25 °C for only 23–38 h per zone, so the fan rarely runs. The heat-wave weather files should give a clearer example.
• The slide 25 fan energy table (kWh/m²) has ambiguous column alignment in the extract.

# Sources
• 17.1 Ceiling fans (lecture, 41463, Nov 2025)
• 17.2 Adaptive thermal comfort (lecture, 41463)
• Raftery & Douglass-Jaimes, CBE Ceiling Fan Design Guide, UC Berkeley, 2020
• Course PMV script and Assignment 04 (2026 version), Q11