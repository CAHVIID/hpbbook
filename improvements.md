# Improvements

:::{warning} Loose development thoughts
This page collects loose ideas for future versions of the course and the book. The entries are unfinished, unchecked and may never be implemented.
:::

## Melanopic EDI-tailored design

Next year the façade design part may include circadian light. Melanopic EDI (equivalent daylight illuminance, CIE S 026:2018) weights light by its effect on the body clock and is measured vertically at eye level. The consensus target is at least 250 lx in the daytime {cite:p}`brown2022`. Students would size windows and choose glazing so the occupied zone reaches this target, alongside sDA300 and cooling demand. Solar-control glazing that shifts the colour of the light lowers melanopic EDI more than its light transmittance suggests.


## Danish heat-wave years with the Annex 80 method

Chapter D1 uses the Annex 80 heat-wave years for Copenhagen, which are RCP8.5, and DMI publishes no heat-wave years. DMI Rapport 25-14 says its reference years are not suited for extreme events and recommends long time series instead. Next year it could be interesting to create heat-wave years for RCP4.5, the scenario of the DMI reference years, with the published Annex 80 code (github.com/LBNL-ETA/annex80-heat-wave-epw, BSD-3). The steps:
- EURO-CORDEX MPI-ESM-LR/REMO data for Copenhagen, bias-adjusted against DMI observations 2001–2020.
- Typical years by the Finkelstein–Schafer method.
- Heat waves by the Ouzeau et al. (2016) thresholds.

The model data must come from ESGF or the Copernicus Climate Data Store, which need an account.

## Heat island against city size: more European cities and a check of Oke

The figure of the heat island against urban area in D1.5 (fig-uhi-map, panel b) is fitted to four Danish cities only, with the intensities of Sørup et al. (2026): the mean night-time heat island on the 3 % warmest days. Two improvements for next year:

**Check the Oke relation against the original paper.** The reference is Oke (1973), "City size and the urban heat island", Atmospheric Environment 7, 769–779 (not 1970). Under calm, clear skies, Oke found the maximum heat island to grow with the logarithm of the population, with separate lines for North American and European settlements. He also gave a form with wind speed, ΔT = P^0.25 / (4.04 u^0.56), from settlements in Quebec. Secondary sources quote different coefficients for the log lines, and none of these is checked against the paper yet:
- North America: 2.96 log P − 6.41, or 3.06 log P − 6.79 (attributed to Oke 1976)
- Europe: 2.01 log P − 4.06 (attributed to Oke 1973 and to Landsberg 1981)

Oke's values are maxima on ideal nights. The European line gives about 8 K for Copenhagen, against 1.5–2 K for the warm-night mean. The D1 fit therefore borrows only the log form of Oke's relation, and it uses urban area instead of population. The text and caption should say this clearly.

**Add more European cities from one consistent dataset.** Candidates are Stockholm, Oslo, Helsinki, Hamburg, Amsterdam, Berlin, Paris and London. The most consistent source is the UrbClim model run for 100 European cities, 2008–2017, at 100 m resolution (Lauwaet et al. 2024, Urban Climate 54, 101850). It finds heat island indicators of 0.57–2.54 K, with a mean of 1.43 K. City values are in the Copernicus Climate Data Store dataset "Climate variables for cities in Europe" and in the EEA Urban Adaptation Map Viewer. The Data Store needs an account.

The UrbClim metric (the spatial 90th percentile of the summer mean, minus the rural 10th percentile) differs from that of Sørup et al., so the Danish cities should be taken from UrbClim too. ΔT could then be plotted against both population (Eurostat functional urban areas) and urban area, with Oke's European line for comparison.


# D7 Improvements: ideas for cooling

:::{note} Ideas
This chapter collects ideas that may grow into real chapters and sections later. Each section says what it would cover. Draft text, where it exists, is kept out of view until the section is written.
:::

## D7.1 Cooling potential against draught risk

A figure showing how the cooling power of ventilative cooling grows linearly with the airflow and the temperature difference, while the draught risk grows faster with the air speed and with colder inflow. Belongs in chapter D4.

{numref}`fig-cooling-vs-draught` is a first version. The cooling power is proportional to the airflow times the temperature difference, so the lines in (a) are straight. The air speed at the ankles is also proportional to the airflow ({eq}`eq-sh-floor`), but the draught rate grows with the speed to a power of about 1.6 ({eq}`eq-draught`), and colder air raises it further. In this example the draught limit is passed at 1 to 2.5 air changes per hour, long before the cooling power is of any use at small ΔT.

:::{figure} figures/d4/cooling-vs-draught.*
:label: fig-cooling-vs-draught
:width: 100%

(a) Cooling power and (b) ISO 7730 draught rate at ankle height, 1 m from a low opening, against the air change rate for four outdoor temperatures. Room of 4 × 5 × 2.6 m at 24 °C. Assumptions: floor stream $u = K\,q_0/x$ with $K$ rising from 4.4 m⁻¹ at ΔT = 0 to 10 m⁻¹ at ΔT = 10 K, a stream that has warmed halfway to room temperature, and a turbulence intensity of 40 %. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/cooling_vs_draught.py)
:::

## D7.2 Control of openings

Opening setpoints, heating locked off while venting, closing in rain and strong wind, where the temperature sensor sits (the row-house skylight case from lecture 18.2), and opening schedules for the shoulder seasons. Belongs in chapter D4.

## D7.3 Night cooling of the thermal mass

How much heat a concrete slab or heavy wall stores per kelvin of temperature swing, the night airflow needed to discharge it, and why lightweight timber houses gain little. Belongs in chapter D4.

## D7.4 Field evidence: tilt windows in an office

The measurements of Fitzner and Finke in a Berlin office with tilted windows: the inflow falls to the floor, the tilt-window flow scales with the sash height to the power 1.5, and the floor stream sets the comfort limit. Belongs in chapter D5.

<!--
Fitzner and Finke measured winter window ventilation in an 80 m² office in Berlin with six tilted sashes (0.71 × 1.48 m), and compared the results with earlier laboratory studies {cite:p}`fitzner2012`. Four findings bear directly on this chapter.

**The inflow falls to the floor.** Outdoor air enters through the lower part of the tilted sash "with little momentum", falls to the floor and spreads towards the heat sources, which lift it to the ceiling. The room flow is close to displacement ventilation. This is the pattern in {numref}`fig-sh-jets`(a) and (c), and it agrees with Ar ≈ 1 for stack-driven flow.

**The tilt-window flow scales with the height to the power 1.5.** From their own and five other studies they give

```{math}
:label: eq-sh-fitzner
q = 190\,k\,H^{1.5}\sqrt{\Delta T}
```

with q in m³/h, the stroke k and the sash height H in m. For the sash in the worked example (k = 0.12 m, H = 1.3 m, ΔT = 3 K) this gives 58 m³/h. The numerical integration in this chapter gives 57 m³/h. The H^1.5 dependence means the height of the opening matters more than its area. The same argument favours the full-height side-hung opening in summer.

**The comfort limit is set by the floor stream.** With the radiator below the window switched off, the speed at 0.1 m was 0.21–0.27 m/s from 0.6 to 1.8 m from the window, and the draught rate was 27–37 %. With the radiator on, it deflected the falling cold air and the conditions were acceptable. Their design limits for steady window ventilation are a cooling load of at most 30 W/m² (150 W per metre of façade for a 5 m deep room), about 340 W per tilted window, and an outdoor temperature above 6 °C.

**The window types have different jobs.** In winter only tilted windows, with the largest opening at the top, are suitable; side-hung and sliding windows are not. This agrees with Heiselberg et al. {cite:p}`heiselberg2001`. The side-hung window gives a very large opening. It is used for short, full airing in winter, and for continuous ventilation on windless summer days, when the outdoor temperature is in the comfort range. The authors note that natural ventilation is most difficult with no wind and almost no temperature difference, which calls for the largest possible window openings.
-->

## D7.5 Window openings: design consequences and worked example

Design rules for summer cooling, night cooling and winter airing, rules of thumb, a worked example comparing a side-hung and a bottom-hung window on a summer evening, and guiding questions. Belongs in chapter D5.

<!--
## Design consequences

- **Summer cooling (ΔT < 5 K):** use side-hung windows that can open 60–90°. The cooling power scales with A√h, so tall sashes help. The inflow drops and spreads along the floor as a slow stream at close to room temperature, which is acceptable or even welcome when the occupants are warm (see [](d6-ceiling-fans.md)).
- **Night cooling (ΔT 5–10 K):** the side-hung window still gives the most air, but the floor stream is colder and faster. This matters little in a bedroom with the occupants in bed, but matters at a desk near the window.
- **Winter airing (ΔT > 15 K):** use bottom-hung windows or hatches placed high, so that the cold air attaches to the ceiling and mixes before it reaches people. Keep the opening small, because a large flow or a large ΔT makes the jet drop.
- **Safety and rain:** a side-hung window open 90° is not burglar-proof or rain-proof. It needs a restrictor, a fixed guard rail or a protected position (balcony, deep reveal) so it can stay open when it is needed.

:::{admonition} Rules of thumb
:class: tip
- A side-hung window opened 60° or more is in effect fully open: A = w·h.
- A tilted sash gives only s·(w + h), about a quarter of the full area for a normal window.
- At the same ΔT, a fully open side-hung window gives 4–5 times the stack flow of a tilted sash of the same size.
- Inflow through a side-hung window is slow and drops to the floor. The floor speed is u ≈ K_w q₀/x with K_w ≈ 5–10 m⁻¹.
- A high bottom-hung window gives a ceiling jet as long as Ar is small. Large flow or large ΔT makes it drop.
:::

## Worked example: side-hung against bottom-hung on a summer evening

A bedroom of 4 × 5 m with a ceiling height of 2.6 m (52 m³) has one 0.8 × 1.3 m sash with its sill at 0.9 m. On a summer evening the room is at 27 °C and the outdoor air at 24 °C, so ΔT = 3 K. The wind speed is 2 m/s. Compare the window opened fully side-hung with the same window tilted 120 mm.

**Step 1: Free area.** Side-hung at 90°: s = 2 · 0.8 · sin 45° = 1.13 m > w, so A = 0.8 · 1.3 = 1.04 m². Bottom-hung: A = 0.12 · (0.8 + 1.3) = 0.25 m².

**Step 2: Stack flow, side-hung.** From {eq}`eq-sh-stack` with T = 300 K:

```{math}
Q_{st} = \frac{0.6 \cdot 1.04}{3}\sqrt{\frac{9.81 \cdot 1.3 \cdot 3}{300}} = 0.074\ \text{m}^3\text{/s} = 267\ \text{m}^3\text{/h}
```

**Step 3: Wind flow.** From {eq}`eq-sh-wind`, Q_w = 0.025 · 1.04 · 2 = 0.052 m³/s = 187 m³/h.

**Step 4: Combined flow and cooling power.** Q = √(267² + 187²) = 327 m³/h, or 6.3 air changes per hour. The cooling power is

```{math}
P = \rho\,c_p\,Q\,\Delta T = 1.2 \cdot 1005 \cdot 0.091 \cdot 3 = 330\ \text{W}
```

That is about 16 W/m² of floor area.

**Step 5: Bottom-hung.** The numerical integration gives Q_st = 57 m³/h and the wind 45 m³/h, so Q = 73 m³/h (1.4 h⁻¹) and P = 74 W. The tilted window removes less than a quarter of the heat. As a check, {eq}`eq-sh-fitzner` gives 58 m³/h for the stack part.

**Step 6: Air speed at the floor.** The inflow passes through the lower half of the side-hung opening: a₀ = 0.6 · 0.52 = 0.31 m², so √a₀ = 0.56 m. The mean inflow velocity is U₀ = 0.091 / 0.31 = 0.29 m/s, and from {eq}`eq-sh-ar`

```{math}
Ar = \frac{9.81 \cdot 3 \cdot 0.56}{300 \cdot 0.29^2} = 0.65
```

Buoyancy and momentum are of the same order, so the slow inflow drops to the floor and spreads. From {eq}`eq-sh-floor` with x₀ ≈ 0 and K_w = 5–10 m⁻¹, the speed 2 m from the window is

```{math}
u = (5\text{–}10) \cdot \frac{0.091}{2} = 0.23\text{–}0.45\ \text{m/s}
```

The air is at about 24–25 °C after mixing, and the occupants are warm, so in summer this is a gentle cooling stream at the feet rather than draught. With the same window open on a cold night, the same equation gives the draught risk.

## Guiding questions

1. A window supplier offers a "tilt-and-turn" window (bottom-hung and side-hung in one sash). Describe how you would tell the occupants to use it in July and in January, and why.
2. Why does the stack flow through a tilted sash grow less with the sash height than the flow through a side-hung window does? Use {numref}`fig-sh-gaps` in your answer.
3. Show that Ar in purely stack-driven flow is independent of ΔT. What does that mean for draught from a low window on a windless night?
4. A side-hung window must be restricted to 10° for safety. How much of the summer airflow is lost, and what other opening could make up for it?
5. In the worked example the inflow runs along the floor at about 0.2–0.4 m/s. When is this welcome, and when is it draught?
-->



# Use your own heatpump operation as a case for DHW and SH and SCOP