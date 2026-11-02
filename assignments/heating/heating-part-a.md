# Assignment 3, Part A: Heating

**When and how.** Part A uses IDA ICE and a few hand calculations. It is issued on Monday 5 October with Lecture 11. Tasks H1 to H6 use section 5 of the text and Lecture 11; tasks H7 and H8 use section 6 and Lecture 12 (Thursday 8 October). The week of 12 to 16 October is the autumn break. Part B follows from the co-teacher in the week of 19 October. You hand in Part A and Part B together, as one report per group, by 23:59 on Sunday 25 October. The groups are the same as in Assignment 2. The assignment is not graded; you receive feedback on it. Part A is about four to five hours of work with the simulations, and is meant for the two exercise sessions of this week. Where a question asks for a written answer, write at most two sentences, unless the task says otherwise.

**What you receive.**

- The class text, sections 5 and 6, and Appendix E (the model and its settings).
- The IDA ICE model of the row house, `Model C - Heating - Assignment 03.idm`.
- The workbook `heat-pump-coverage.xlsx`, used in H7.

**The model in brief.** It is the row house of Assignment 2 Part B with the Enthalpy wheel AHU connected to every ventilated zone and its control switch at 1 (constant air volume, 60 L/s). Three things are new.

1. **The household.** The people are in the occupant object of each room on daily schedules: two adults and two children, the adults in the master bedroom at night, a child in each of the other bedrooms, the family in the living room in the evening, one adult in the kitchen at breakfast and at dinner. The appliances are in the equipment object of each room, placed where the appliances stand (the kitchen 105 W, the living room 98 W, the first-floor bathroom 47 W, each bedroom 32 W, the other rooms 5 W; 360 W in all), on the daily profile of household electricity, lowest at night and highest in the evening. The cooking is not in the model: the kitchen hood extracts it. Section 5.1 explains the figures.
2. **Room heating.** Every room has a room unit (*Simple fan coil* under *Room Units* in the zone form) that heats the room to the heating setpoint, 22 °C, and cools it above the cooling setpoint, 25 °C. It stands for the radiator or the floor heating of a conventional house. All nine rooms share one setpoint collection, *Row house setpoints* (open any zone form and click *Controller setpoints*): *Temperature Min* is the heating setpoint and *Max* the cooling setpoint. Do not change *Max*.
3. **Air heating.** The AHU has a heating coil after the heat exchanger. Open the AHU (the *General* tab, *HVAC systems*, double-click *Enthalpy wheel AHU*) and find the box *Setpoints for air heating control* at the top left of the schematic. The field *Constant temp.* is the heating setpoint of the return air: whenever the return air (the mixed air extracted from the kitchen and the bathrooms) is below it, the coil heats the supply air, up to the supply air temperature limit of 30 °C (the field *Max & min heated supply air temperature*). The drop-down *Select method here* chooses whether the setpoint is the constant or a schedule.
    - As received, the heating setpoint of the return air is 10 °C. The return air is never that cold, so the coil never heats and the room units heat the house. This is room heating.
    - For air heating you set it to 22 °C and lower the setpoint collection's *Min* to 15 °C, so that the room units never run (H3). The coil then holds the return air at 22 °C; above 23.5 °C the AHU bypasses the heat exchanger (the free cooling of section 4).

The boiler of the Plant runs from 1 November to 31 March, the heating season of the model; from April to October nothing heats. The simulation period is 1 September to 31 May, which holds the whole heating season; keep it. One schedule is in the model, *Heating setpoint 22->21 in peak periods*: 22 °C, lowered to 21 °C from 07:00 to 09:00 and from 17:00 to 21:00 (H6).

**Where to read what.** Everything Part A asks for is in these places.

| What | Where |
| --- | --- |
| The heating and cooling energy of the period | the *Summary* tab, the table *Systems energy*: *Zone heating* (the room units), *AHU heating* (the coil), *Zone cooling* |
| The appliances' electricity | the *Summary* tab, the table *Delivered energy*, the row *Equipment, tenant* |
| The highest heating power of the period | the same table, the row *Electric heating* (the boiler serves the room units and the coil), the column *Peak demand (kW)*. If your table shows no such column, read the highest point of the heating curve in *Total heating and cooling* in the *Year* view instead |
| A room's temperature over time | the *Details* tab, expand the zone to its list of outputs, the diagram *Main temperatures*, the curve *Operative temperature*; the yellow arrow at the bottom left changes the period shown (*Week*, *Day*), the left and right arrows step through it |
| The heating power over time | the *Details* tab, the diagram *Total heating and cooling*: the curve *Ideal heaters and other local units* (the room units) and *AHU heating coil power* (the coil) |
| The supply air temperature over time | the *Details* tab, the diagram *AHU temperatures*, the curve *Supply air dry-bulb temperature* |
| A room's heat balance over time | the *Details* tab, the zone's outputs, the diagram *Energy*: one curve per source of heat into the room, positive into it, named *Envelope and thermal bridges*, *Internal walls and masses*, *Window and solar*, *Mechanical supply air*, *Infiltration and openings*, *Occupants*, *Equipment* and *Local heating units* |

Read the temperatures by eye in the *Week* view, to the nearest half degree. The coldest week of the period is 7 to 14 February; use it wherever a task says "the coldest week". To simulate: the *Simulation* tab, *Run* beside *Custom*; a simulation takes a few minutes, and ticking *Time-split parallelization* in the *Setup* beside it makes it faster. Save a copy of the model for each task, named after the task, and never overwrite the model you received. For every simulated number in the report, name the copy it comes from.

## H1. The house as received

*What it shows:* how much heating a low-energy house needs, and how it compares with the free heat. Section 5.1.

1. Simulate the model as received (room heating, constant air volume).
2. Record the four readings of table H1.

| Table H1: room heating, 1 September to 31 May | Value |
| --- | --- |
| Zone heating, kWh | |
| AHU heating, kWh (expect 0) | |
| Equipment, tenant, kWh | |
| Peak demand of Electric heating, kW | |

**Q1.1** The appliances' electricity is heat given off in the house. How many times larger is it than the heating, and what does that say about how much of the year the house needs heating at all?

**Q1.2** In the coldest week, read the operative temperature of the master bedroom and of the living room (*Main temperatures*, the *Week* view): their lowest and highest values. Which room is warmer, and why?

*Hand in:* table H1; the four temperatures of Q1.2; the answers.

## H2. The household: 60 % and 150 % of the appliances

*What it shows:* how much the heating of the same house depends on who lives in it. Section 5.1.

The 360 W of appliances are a typical family's. A family with class-A appliances, LED lighting and a heat-pump dryer gives off about 60 % of it; a family with old refrigerators, a condenser dryer and more screens about 150 %. IDA ICE scales the appliances in the *Energy (whole year)* simulation.

1. Save a copy of the model as received. In the *Simulation* tab, click *Setup* to the right of *Energy (whole year)*. In the box *Percentage of internal gains*, enter 60 in *Equipment* (leave *Occupants* and *Light* at 100). Click *Run*.
2. Record *Zone heating* and the peak demand (the same two places as in H1). This simulation covers the whole year; the heating is zero from April to October, so it compares directly with H1.
3. Repeat with *Equipment* at 150. Set it back to 100 afterwards.

| Table H2: the household | Equipment 60 % | 100 % (H1) | 150 % |
| --- | --- | --- | --- |
| Zone heating, kWh | | | |
| Peak demand of Electric heating, kW | | | |

**Q2.1** By what factor does the heating differ between the two households?

**Q2.2** Which household should the heating system be sized for, and why?

**Q2.3** Open the living room's *Main temperatures* in the 150 % case and step through the weeks of January and February: on some afternoons the room reaches 25 °C and stops there. What holds it at 25 °C, and what does that say about a house whose household gives off a lot of heat?

*Hand in:* table H2; the answers.

## H3. Air heating against room heating

*What it shows:* whether one coil in the AHU heats the house as well as a heater in every room. Sections 5.3 and 5.4.

1. Save a copy of the model as received. Open the AHU and set the heating setpoint of the return air (*Constant temp.*) to 22. Open the setpoint collection *Row house setpoints* and set *Temperature Min* to 15. Simulate.
2. Record *Zone heating* (expect 0) and *AHU heating*, and the peak demand.
3. In both models, read in the coldest week the lowest and the highest operative temperature of three rooms: the master bedroom, the living room and the kitchen.

| Table H3: 1 September to 31 May | Room heating (H1) | Air heating |
| --- | --- | --- |
| Zone heating, kWh | | |
| AHU heating, kWh | | |
| Peak demand of Electric heating, kW | | |
| Master bedroom, coldest week, lowest and highest °C | | |
| Living room, coldest week, lowest and highest °C | | |
| Kitchen, coldest week, lowest and highest °C | | |

**Q3.1** The kitchen and the bathrooms receive no supply air. Why are they still close to 22 °C with air heating? Section 5.4 gives two reasons.

**Q3.2** Compare the two systems in energy and in the rooms' temperatures: does the house with room heating buy anything in comfort for its heater, valve and thermostat in every room?

**Q3.3** *By hand.* A 9 m² bathroom at 25 °C loses about 90 W. A heated floor gives the room about 10 W/m² for every kelvin its surface is above the room air. How warm is the floor that delivers the 90 W, and does it feel warm? Section 5.2.

*Hand in:* table H3 with the two copies named; the answers, with the calculation of Q3.3.

## H4. The cool bedroom: the window open at night

*What it shows:* what a cool bedroom costs in a low-energy house. Section 5.2.

Many people want a cool bedroom at night. Turning the bedroom's thermostat down does little in this house, because the bedroom's heater is already off on most nights (section 5.2). The way people get a cool bedroom is the window. You simulate the parents opening the master bedroom's window at night.

1. Start from a copy of the model as received (room heating). Open the master bedroom's zone form.
2. In the drop-down beside *Controller setpoints*, choose the entry *local for zone* (shown in square brackets), then click *Controller setpoints*: the form opens. Set *Temperature Min* to 10 (the bedroom's room unit never heats) and *Max* to 18 (the temperature the window will hold). Click *OK*.
3. Under *Room Units*, open the *Simple fan coil* and set *Design power › Cooling* to 0, so that the window and not the unit cools the room.
4. Click *Windows* in the zone form and open the bedroom's window. In the box *Opening*, set *Control* to *PI temperature control AND schedule* and choose the schedule *Sleeping 23-6 EN15666*: the window now opens between 23:00 and 06:00, as far as needed to hold 18 °C, and is closed by day. The other bedrooms stay as they are.
5. Simulate. Record *Zone heating* and the peak demand, and in the coldest week the master bedroom's lowest and highest operative temperature.
6. In the *Details* tab, open the master bedroom's *Energy* diagram, step to a week of January in the *Week* view, and keep a picture of it for the report.

| Table H4: 1 September to 31 May | Room heating (H1) | The window open at night |
| --- | --- | --- |
| Zone heating, kWh | | |
| Peak demand of Electric heating, kW | | |
| Master bedroom, coldest week, lowest and highest °C | | |

**Q4.1** By how much did the house's heating rise, although the bedroom's own heater never ran? Which rooms' heaters paid for it? Section 5.2 gives the mechanism; to check one room, compare the curve *Local heating units* in the second-floor bathroom's *Energy* diagram in the two models, in the same January week.

**Q4.2** Read your January figure: at night, where does the heat that leaves through the window come from? Look at the curves *Infiltration and openings* and *Internal walls and masses*: which is the loss and which the largest source, and what does the second one do by day?

**Q4.3** With air heating there is no bedroom thermostat; the only setpoint is the AHU's. In two sentences: what would lowering that setpoint at night do to the house and to the bedroom?

*Hand in:* table H4; the January figure; the answers.

## H5. The heating coil and the water it needs

*What it shows:* how much heat the coil must carry, and how warm its water must be. Section 5.4.

Use the air-heating copy of H3.

1. In the *Details* tab, open *Total heating and cooling* and step to the coldest week: read the highest value of *AHU heating coil power*. Check it against the peak demand of table H3.
2. Open *AHU temperatures* in the same week: read the highest *Supply air dry-bulb temperature*.

**Q5.1** *By hand.* On the coldest days the air leaves the heat exchanger at about 17 °C. Compute the heat the coil delivers when it raises 60 L/s from 17 °C to the supply temperature you read, from $P = 1.2 \times q \times (T_\text{supply} - 17\ °\text{C})$ with $q$ in L/s, and compare it with the coil power you read.

**Q5.2** The manufacturer's table in section 5.4 gives, for air entering the coil at 16 °C: water at 40/30 °C makes 28 °C of supply air and 870 W; water at 60/40 °C makes 38 °C and 1 580 W. Which water temperature does the coil need at your peak? Radiators are designed for water at 55 to 70 °C, floor heating for 30 to 40 °C: what does the answer mean for a heat pump supplying the water?

*Hand in:* the two readings; the calculation of Q5.1; the answer to Q5.2.

## H6. Heating in the peak periods

*What it shows:* what a setpoint lowered in the peak hours does to the house and to the two heating systems. Section 5.5.

The electricity grid has its largest loads in the morning and in the early evening. The schedule *Heating setpoint 22->21 in peak periods* lowers the heating setpoint to 21 °C from 07:00 to 09:00 and from 17:00 to 21:00. You test it on both systems.

1. **Room heating with the schedule.** Start from a copy of the model as received. Open the setpoint collection *Row house setpoints*. In the box *Variable Setpoints*, set *Min temperature* to the schedule *Heating setpoint 22->21 in peak periods*. Simulate.
2. **Air heating with the schedule.** Start from the air-heating copy of H3. Open the AHU and, in the box *Setpoints for air heating control*, set *Select method here* to *Schedule*. Simulate.
3. For each, record *Zone heating* or *AHU heating* and the peak demand. Then open *Total heating and cooling* in the *Day* view on 8 February (the coldest evening) and read the highest heating power between 21:00 and 23:00. Open the living room's *Main temperatures* on the same day and read its lowest operative temperature between 17:00 and 21:00. Read the same two values on 8 February in the H1 and the H3 copies, for the first and third columns of the table.

| Table H6: 1 September to 31 May | Room heating, 22 °C (H1) | Room heating, schedule | Air heating, 22 °C (H3) | Air heating, schedule |
| --- | --- | --- | --- | --- |
| Heating of the period (Zone or AHU), kWh | | | | |
| Peak demand of Electric heating, kW | | | | |
| Highest heating power after 21:00 on 8 February, W | | | | |
| Living room, lowest °C from 17:00 to 21:00 on 8 February | | | | |

**Q6.1** *By hand.* The part of the house that warms and cools with the air is about 18 MJ/K (5 kWh/K). If the heating stops for the four evening hours on a day that needs 700 W, how far does the house cool, from $\Delta T = P \times t / C$? Is 21 °C reached?

**Q6.2** What happens in the hour after 21:00 in each system, and why does the coil's answer differ from the room units'? Section 5.5 explains the rebound and the supply air temperature limit.

**Q6.3** Is the house, in your judgement, as comfortable with the schedule as without it? The period's heating is a little lower with the schedule, because the house is cooler for six hours a day; that is not the point of the schedule, so do not judge it by that.

*Hand in:* table H6 with the copies named; the calculation of Q6.1; the answers.

## H7. The heat pump's coverage (after Lecture 12)

*What it shows:* how much of the space heating a small exhaust-air heat pump covers. Section 6.4.

The heat pump of the text delivers to the supply air, by its certificate, 0.61 kW at −4 °C, 0.78 kW at 2 °C and 0.92 kW at 7 °C of outdoor temperature; the hot water needs about 215 W on average.

1. In the air-heating copy of H3, open *AHU heating coil power* alone in its diagram for the whole period (double-click its name in the legend of *Total heating and cooling*) and click the *Export to Excel* icon at the bottom of the diagram window, second from the right. IDA ICE opens Excel with the time and the hourly values.
2. Paste the two columns into the sheet *Hourly* of `heat-pump-coverage.xlsx` as its *Read me* says, and do the same for *Outdoor air dry-bulb temperature* from *AHU temperatures*.
3. Read from the sheet *Summary*: the share of the space heating the heat pump covers, the hours it falls short, the heat from the electric element, and the seasonal COP of the pair.

**Q7.1** How many hours a year need the electric element, and what does the hot water add to them? (The *Summary*'s line on the capacity left for the hot water gives the second number.)

**Q7.2** With demand-controlled ventilation the AHU supplies 22 L/s when nobody is home. What does that do to the heat the coil can carry at the same supply air temperature limit? No simulation.

*Hand in:* the four lines of the *Summary*; the answers.

## H8. The exhaust air and frost (after Lecture 12)

*What it shows:* how cold the exhaust air gets when a heat pump takes its heat from it. Section 6.4.

**Q8.1** *By hand.* With return air at 22 °C, a heat exchanger with a temperature efficiency of 0.85 and balanced airflows of 60 L/s, compute the temperature of the exhaust air leaving the heat exchanger at −4 °C outdoors. Then compute how much further the heat pump cools that air when it delivers 0.61 kW at a COP of 2.65: the heat taken from the air is $P \times (\text{COP} - 1)/\text{COP}$, and $\Delta T = Q / (1.2 \times q)$ with $q$ in L/s.

**Q8.2** Is there a risk of frost on the heat pump's evaporator at this outdoor temperature? Would a heat pump twice as large be a sensible way to cover the hours of H7? Compare the return air of your model in the coldest week (*AHU temperatures*) with the 22 °C assumed.

*Hand in:* the two temperatures with the calculation; the answers.

## The report

One report per group, as a Word or PDF file. For every simulated number, the model copy it comes from. Keep the written answers to two sentences each.

| Task | Deliverables |
| --- | --- |
| H1 | Table H1; the four temperatures of Q1.2; Q1.1, Q1.2 |
| H2 | Table H2; Q2.1 to Q2.3 |
| H3 | Table H3; Q3.1, Q3.2; the calculation of Q3.3 |
| H4 | Table H4; the January figure; Q4.1 to Q4.3 |
| H5 | The two readings; the calculation of Q5.1; Q5.2 |
| H6 | Table H6; the calculation of Q6.1; Q6.2, Q6.3 |
| H7 | The *Summary* lines; Q7.1, Q7.2 |
| H8 | The calculation of Q8.1; Q8.2 |
