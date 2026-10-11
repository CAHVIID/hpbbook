# D2 Cooling strategy

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D2.1 Why homes overheat

New Danish houses are insulated and airtight to keep heat in during winter. In summer the same envelope keeps the solar and internal gains in. Large glazed areas add to the gains, and a warmer future climate with longer heat waves ([](d1-weather-files.md)) makes it worse. High indoor temperatures are now one of the most common indoor climate complaints in new Danish dwellings, and not only in summer. On a sunny day in April or September, solar and internal gains can lift the temperature well above comfort levels in a home that hardly needs heating.

A study of Finnish apartment buildings found that openable windows were the most effective passive measure against overheating in the new building, though not enough in the old one {cite:p}`farahani2021`.

In steady state, with all heat removed by transmission and ventilation, the indoor temperature rises above the outdoor temperature by

```{math}
:label: eq-overtemperature
\theta_i - \theta_e = \frac{\Phi_{sol} + \Phi_{int}}{H_{tr} + \rho c_p q_v}
```

where $\Phi_{sol}$ and $\Phi_{int}$ are the solar and internal gains (W), $H_{tr}$ the transmission heat loss coefficient (W/K), and $\rho c_p q_v$ the ventilation heat loss coefficient (W/K), about 0.34 W/K per m³/h of airflow. In a low-energy house $H_{tr}$ is small, so the ventilation term dominates. With heat recovery running, only the unrecovered fraction of $q_v$ counts. To remove 1,000 W of solar gain with only 3 K between inside and outside takes about 1,000 m³/h. That is about six times the BR18 minimum ventilation rate of a 150 m² house (0.3 L/s per m², about 160 m³/h).

The equation shows the levers. Reduce the gains in the numerator, increase the airflow in the denominator, and only then deal with what is left.

## D2.2 Judging overheating

:::{note} BR18 overheating limits
BR18 limits overheating in dwellings to 100 hours above 27 °C and 25 hours above 28 °C operative temperature in a year. These limits are tailored to the thermal model used for BR18 compliance, with its fixed assumptions on weather, internal gains, occupancy and venting. Use them only with that model. Hours from a detailed dynamic simulation, another weather file or measurements in a real house are not directly comparable, and should not be judged against 100 and 25 hours as if they were.
:::

For a detailed simulation of a dwelling without mechanical cooling, use the adaptive comfort model of EN 16798-1 {cite:p}`en16798`. Occupants who can open windows and change clothing accept higher temperatures after a warm spell. The upper limit of the operative temperature for category II is

```{math}
:label: eq-adaptive-upper
\theta_{op,max} = 0.33\,\theta_{rm} + 18.8 + 3
```

where $\theta_{rm}$ is the running mean outdoor temperature (°C), a weighted mean of the daily mean temperatures of the previous days. The model applies for $\theta_{rm}$ between 10 and 30 °C. After a week at 15 °C the limit is 26.8 °C; after a week at 20 °C it is 28.4 °C. Overheating is then reported as the number of occupied hours above the limit in the critical room.

The result depends as much on the weather file as on the building, so check a design against the reference year, a future year and a heat wave ([](d1-weather-files.md)).

## D2.3 The ordered strategy

The measures are applied in the order below. The order is cost-effective: each step is cheaper and uses less energy than the next, and each one reduces what the next has to handle. It also matches how severe the heat is. The first steps handle an ordinary Danish summer, and the later ones are added as warm spells turn into heat waves.

1. **Reduce solar gains, keep daylight and view.** Solar-control glazing with a low g-value, sensible window areas and orientations, and fixed or movable external shading that still lets daylight in and gives a view out ([](a3-glazing.md), [](d3-facade-design.md)). External shading stops the sun outside the glass, while internal blinds release most of the heat they absorb into the room.
2. **Bypass the heat recovery.** Whenever the outdoor air is cooler than the indoor air, the ventilation unit must bypass the heat recovery. Otherwise a recovery unit with 80 to 90% efficiency heats the supply air back up with the warm exhaust air, and the ventilation removes almost no heat. With the bypass open, the airflow can also be boosted, for example at night. It costs nothing but a damper and a control setting.
3. **Ventilative cooling.** Large airflows through windows and hatches, and night cooling of the thermal mass ([](d4-ventilative-cooling.md), [](d5-window-openings.md)).
4. **Ceiling fans.** Fans do not lower the temperature, but they let occupants accept a higher one. About 0.5 m/s gives a cooling effect of roughly 2 °C {cite:p}`raftery2020` ([](d6-ceiling-fans.md)). The energy they save in air-conditioning typically exceeds their own use by a factor of 10 to 100.
5. **Shutters.** In a heat wave, closing external shutters or fully opaque blinds during the day blocks nearly all solar gain. The price is the daylight and the view out, so they are kept for the hottest days, which is why they come after the steps that keep the home usable.
6. **Active cooling.** A reversible heat pump with floor or ceiling cooling, or air-conditioning, for what is left in extreme heat.

Steps 1 to 3 are decided early in design, by the architecture, the openings and the ventilation system, and cost little when planned from the start. In a well-designed Danish house, steps 1 to 5 should be enough to ride out heat waves without active cooling.
