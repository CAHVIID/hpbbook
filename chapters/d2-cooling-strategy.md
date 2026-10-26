# D2 Cooling strategy

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D2.1 Why homes overheat

New Danish houses are insulated and airtight to keep heat in during winter. In summer the same envelope keeps the solar and internal gains in. Large glazed areas add to the gains, and a warmer future climate with longer heat waves ([](d1-weather-files.md)) makes it worse. Owners report overheating in 11–17 % of Danish homes built after 2000 (Realdania 2024); for detached houses built after 2000 the share is 13.4 % {cite:p}`lyhne2023`. It is not only a summer problem.

On a sunny day in April or September, solar and internal gains can lift the temperature well above comfort levels in a home that hardly needs heating.

A simulation study of new Finnish apartments in timber blocks completed in 2015–2018 found window opening to be the most effective single passive measure {cite:p}`sukanen2023`. Daytime or temperature-controlled opening kept the degree-hours above 27 °C within the Finnish limit in most climates, and together with external blinds it met the limit in every climate up to the 2050s. A lower g-value or a fixed overhang alone cut the degree-hours by only 26–36 %.

> The solution is *not* to reduce insulation, as we need it to solve the winter situation, but to apply a sound cooling strategy for the summer situation and the shoulder seasons, where heating and cooling demand alternate within the same 24 h cycle.

## D2.2 Overheating in residences

To assess overheating in dwellings without mechanical cooling, use the adaptive comfort model of EN 16798-1 {cite:p}`en16798`, shown in {numref}`fig-adaptive-comfort`. Occupants who can open windows and change clothing accept higher temperatures after a warm spell.

The upper limit of the operative temperature for category II is

```{math}
:label: eq-adaptive-upper
\theta_{op,max} = 0.33\,\theta_{rm} + 18.8 + 3
```

where $\theta_{rm}$ is the running mean outdoor temperature (°C), a weighted mean of the daily mean temperatures of the previous days.

The adaptive limits apply for $\theta_{rm}$ between 10 and 30 °C. Below 10 °C the ordinary limits apply: 21–25.5 °C for category I, 20–26 °C for II and 18–27 °C for III. After a week at 15 °C the limit is 26.8 °C; after a week at 20 °C it is 28.4 °C. Overheating is then reported as the number of occupied hours above the limit in the critical room.

:::{figure} figures/d2/adaptive-comfort.*
:label: fig-adaptive-comfort
:width: 90%

Adaptive comfort limits of the operative temperature for categories I, II and III, drawn from the equations of EN 16798-1. The comfort temperature (dash) is $0.33\,\theta_{rm} + 18.8$. Upper and lower limits as shown. Left of $\theta_{rm}$ = 10 °C: the ordinary limits, I 21–25.5, II 20–26 and III 18–27 °C. The points mark the category II upper limit after a week at 15 °C and at 20 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/adaptive_comfort.py)
:::

:::{note} BR18 overheating limits
BR18 limits overheating in dwellings to

- 100 hours above 27 °C
- 25 hours above 28 °C

operative temperature in a year. These limits are tailored to the thermal model used for BR18 compliance, with its fixed assumptions on weather, internal gains, occupancy and venting. Use these limits only with that model. Hours from a detailed dynamic simulation, another weather file or measurements in a real house should not be judged against 100 and 25 hours.
:::

## D2.3 Cooling strategy

Cooling measures should be applied in the order below as it is cost-effective: each step is cheaper and uses less energy than the next, and each one reduces what the next has to handle. It also matches how severe the overheating problem is. The first steps handle an ordinary Danish summer, and the later ones are added as warm spells turn into heat waves.

1. **Reduce solar gains while keeping daylight and view out.** Solar-control glazing with a low g-value, sensible window areas and orientations, and fixed or movable external shading that still lets daylight in and gives a view out ([](a3-glazing.md), [](d3-facade-design.md)). Potentially an overhang could reduce peak solar gains while keeping a view out. Solar-coated glazings are cheap, without maintenance, but the lowest level of the g-value is constrained by the acceptable light transmittance.
2. **Bypass the heat recovery** and exploit the deep amplitude of the outdoor temperature in temperate climates. When the outdoor air is cooler than the indoor air, the ventilation unit must bypass the heat recovery. Otherwise a recovery unit with 85–90% efficiency heats the supply air back up with the warm exhaust air, and the heat removal drops to almost nothing. With the bypass open, the airflow can also be boosted, for example at night. It costs only a damper and a control setting.
3. **Ventilative cooling.** Large airflows through windows, hatches and skylights, exploiting cross and stack ventilation and night cooling of the thermal mass ([](d4-ventilative-cooling.md), [](d5-window-openings.md)). Louvred openings (hatches) are particularly beneficial as they can stay open independently of the weather and occupancy. The caveat to avoid is draught when the outdoor temperature is low.
4. **Ceiling fans.** Fans let occupants accept a higher temperature. Elevated air speeds of 0.5 m/s give a cooling effect of roughly 2 °C {cite:p}`raftery2020` ([](d6-ceiling-fans.md)). The energy they save in air-conditioning typically exceeds their own use by a factor of 10 to 100.
5. **Shutters.** In a heat wave, closing external shutters or fully opaque blinds during the day blocks nearly all solar gain. The price is the daylight and the view out, so shutters are kept for the hottest days. Shutters block the airflow through the windows, unless hatches/louvred openings are used as openings instead.
6. **Active cooling.** PV covers much of the midday cooling demand, but AC keeps running after sunset: in the 2026 European heat waves the grid strain and price spikes came in the early evening, around 19:00 ([](#app-ac-europe)). Active cooling also forces the manual/automatic window openings to close.

Steps 1 to 4 are decided early in design, by the architecture, the openings and the ventilation system, and cost little when planned from the start.

In a well-designed Danish house, steps 1 to 5 should be enough to ride out heat waves without active cooling.
