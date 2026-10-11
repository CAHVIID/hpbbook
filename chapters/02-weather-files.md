# Future climate and weather files

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## 1. Introduction

Future climate changes and given the life span of buildings, they need to be designed for that. This chapter gives an overview of the climate challenges.

## 2. What is in a weather file

*TBA* hourly dry-bulb temperature, humidity, direct normal, diffuse and global horizontal radiation, wind and cloud cover. File formats (EPW, the Danish DRY format, IDA ICE weather files) and where to get them.

## 3. The Danish design reference year

A reference year is one artificial year of hourly weather. It is assembled from twelve real calendar months, each picked from a longer measured record as the most typical month of its kind. DMI selects the months with the Finkelstein–Schafer method of ISO 15927-4. The method compares the distribution of daily values in each candidate month with the distribution for all years, using temperature, global radiation and humidity as primary parameters and wind and precipitation as secondary ones.

Denmark has two generations of design reference year (DRY), both for the DMI station at Sjælsmark north of Copenhagen, with solar radiation measured at DTU in Lyngby:

- **DRY 2001–2010**, the reference used in building regulations until now.
- **DRY 2011–2023**, the 2025 reference year (DMI Report 25-14). Its twelve months come from 2014–2023.

### Future reference years

DMI has also published *climate-projected* reference years for three emission scenarios:
- RCP2.6
- RCP4.5
- RCP8.5

RCP is Representative Concentration Pathway and reflect future greenhouse gas concentrations in the atmosphere: https://en.wikipedia.org/wiki/Representative_Concentration_Pathway

Each RCP scenario was projected for four periods:
- 2035–2054
- 2045–2064
- 2055–2074
- 2080–2099

**DMI considers RCP4.5 the most likely scenario**, as it corresponds to about 2.7 °C of global warming by the end of the century (DMI Report 25-14).

:::{admonition} Extra
:class: dropdown
Climate models give only daily temperature and precipitation, not the hourly radiation and humidity a simulation needs. So DMI used the projected daily values to *choose* months from the measured 2014–2023 record: for each calendar month the measured month whose temperature distribution best matches the projection, is picked, with precipitation as the tie-breaker. Every hour in a future file is therefore real, measured weather from the last decade.
:::

{numref}`fig-dry-weather` shows the current and future DRY files, and {numref}`tab-dry-summary` summarises them.

```{figure} figures/ch02/dry-air-temperature.png
:name: fig-dry-weather
:width: 100%

Hourly air temperature and daily mean (blue), daily global horizontal radiation (orange, right axis) and relative humidity (green) for the Danish design reference years at Sjælsmark: the old and new present-day files and the four RCP4.5 projections. The dashed line marks 26 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_dry.py)
```

```{list-table} Annual indicators of the Danish design reference years, computed from the EPW files.
:name: tab-dry-summary
:header-rows: 1

* - Weather file
  - Min (°C)
  - Mean (°C)
  - Max (°C)
  - Hours below 0 °C
  - Hours above 26 °C
  - Global radiation (kWh/m²)
  - Mean RH (%)
  - Mean enthalpy (kJ/kg)
  - Hours WBGT ≥ 25 °C (outdoors)
  - Hours UTCI > 26 °C
  - Hours PET > 29 °C
* - DRY 2001–2010
  - −15.0
  - 8.1
  - 27.7
  - 1,386
  - 28
  - 1,038
  - 83
  - 23.1
  - 64
  - 292
  - 136
* - DRY 2011–2023 (2025)
  - −7.6
  - 9.6
  - 30.3
  - 595
  - 37
  - 1,023
  - 81
  - 25.6
  - 59
  - 432
  - 207
* - RCP4.5, 2035–2054
  - −8.1
  - 9.9
  - 29.0
  - 471
  - 48
  - 1,017
  - 82
  - 26.4
  - 128
  - 546
  - 236
* - RCP4.5, 2045–2064
  - −8.1
  - 10.0
  - 31.0
  - 471
  - 80
  - 1,027
  - 82
  - 26.6
  - 151
  - 610
  - 303
* - RCP4.5, 2055–2074
  - −8.1
  - 10.3
  - 31.2
  - 469
  - 90
  - 1,030
  - 81
  - 27.1
  - 162
  - 623
  - 315
* - RCP4.5, 2080–2099
  - −8.1
  - 10.1
  - 31.2
  - 473
  - 90
  - 1,019
  - 81
  - 26.6
  - 162
  - 627
  - 310
```

:::{admonition} Take-aways
:class: dropdown
Four take-aways:
1. **A big step has already happened.** Going from the *2001–2010* to the *2011–2023* reference year cuts the hours below 0 °C by more than half, yet [severe freeze temperatures still occurs:](https://www.berlingske.dk/danmark/over-18-frostgrader-goer-natten-til-soendag-til-koldeste-i-fem-aar)
Enthalpy is the annual mean total specific enthalpy of the outdoor air per kg dry air, $h = 1.006\,T + x\,(2501 + 1.86\,T)$ in kJ/kg, with the humidity ratio $x$ found from air temperature, relative humidity and pressure.

The wet-bulb globe temperature (WBGT) is a heat-stress index that combines air temperature, humidity, radiation and wind. The outdoor values in the table use the simplified formula of the Australian Bureau of Meteorology, $\mathrm{WBGT} = 0.567\,T + 0.393\,e + 3.94$, where $T$ is air temperature in °C and $e$ is water vapour pressure in hPa. The formula assumes moderate sun and light wind, so it needs only temperature and humidity from the weather file {cite:p}`bom_wbgt`.

The Universal Thermal Climate Index (UTCI) {cite:p}`brode2012` and the Physiological Equivalent Temperature (PET) {cite:p}`hoppe1999` are European heat-balance indices. Both express the outdoor condition as the air temperature of a reference environment that gives the same physiological strain. They use air temperature, humidity, wind and mean radiant temperature. Here the mean radiant temperature is that of a person standing in the open, found from the direct and diffuse solar radiation in the file (the SolarCal method of ASHRAE 55). The thresholds are the start of moderate heat stress: UTCI above 26 °C {cite:p}`brode2012` and PET above 29 °C {cite:p}`matzarakis1999`. Because they include sun and wind, both count far more hours than the simplified WBGT formula, which uses only temperature and humidity.

:::{admonition} UTCI assessment scale
:class: dropdown
UTCI is an outdoor index. Its ten stress classes {cite:p}`brode2012` are:

| UTCI (°C) | Stress class |
|---|---|
| above 46 | extreme heat stress |
| 38 to 46 | very strong heat stress |
| 32 to 38 | strong heat stress |
| 26 to 32 | moderate heat stress |
| 9 to 26 | no thermal stress |
| 0 to 9 | slight cold stress |
| −13 to 0 | moderate cold stress |
| −27 to −13 | strong cold stress |
| −40 to −27 | very strong cold stress |
| below −40 | extreme cold stress |
:::

Four things stand out:

1. **The biggest step has already happened.** Going from the 2001–2010 to the 2011–2023 reference year raises the mean temperature by 1.4 °C and cuts the hours below 0 °C by more than half. Heating plant sized on the old file will tend to be oversized.
2. **Summers get warmer, but slowly.** Hours above 26 °C rise from 37 today to 80–90 around mid-century.
3. **Radiation and humidity hardly change.** Global radiation stays at about 1,020–1,040 kWh/m² and mean relative humidity at 81–83 %. Solar gains in the future files are those of today.
4. **The projections flatten out.** The 2080–2099 file is no warmer than 2055–2074; the two differ only in January, May and October. Because every future month must be a measured month from 2014–2023, the files can never be hotter than the hottest month of that decade.
:::

<!-- :::{admonition} Rules of thumb
:class: tip
- Use the current DRY for energy-frame compliance and for sizing heating.
- Check summer comfort with at least one future file as well, since a 2025 building will meet a 2050 climate.
- A reference year is built from *typical* months. DMI itself says it is not suited for sizing against extreme events such as overheating. Stress-test the design with a heat-wave file (section 5).
::: -->

## 4. Future weather files beyond the DRY

*TBA:* climate models (GCM, RCM), downscaling, emission scenarios (RCP, SSP); morphing a present-day year (CCWorldWeatherGen) versus bias-corrected regional model output; the Annex 80 TMY files for 2001–2020, 2041–2060 and 2081–2100; uncertainty.

The IEA EBC Annex 80 project made a second set of Copenhagen files from the MPI-REMO regional climate model (EURO-CORDEX): typical meteorological years (TMY) for 2001–2020, 2041–2060 and 2081–2100, and three heat-wave years picked from 2041–2060 under RCP8.5 and bias-adjusted against observations from 2001–2019. Unlike the DRY files, these are model output, not measured months, so they can be hotter than anything seen so far. {numref}`fig-annex80-weather` shows them and {numref}`tab-annex80-summary` summarises them in the same way as the DRY files.

```{figure} figures/ch02/annex80-weather.*
:name: fig-annex80-weather
:width: 100%

Hourly air temperature and daily mean (blue), daily global horizontal radiation (orange, right axis) and relative humidity (green) for the Annex 80 Copenhagen files: three typical years and three heat-wave years. The dashed line marks 26 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_annex80.py)
```

```{list-table} Annual indicators of the IEA EBC Annex 80 weather files for Copenhagen, computed from the EPW files.
:name: tab-annex80-summary
:header-rows: 1

* - Weather file
  - Min (°C)
  - Mean (°C)
  - Max (°C)
  - Hours below 0 °C
  - Hours above 26 °C
  - Global radiation (kWh/m²)
  - Mean RH (%)
  - Mean enthalpy (kJ/kg)
  - Hours UTCI > 26 °C
* - TMY 2001–2020
  - −9.6
  - 9.0
  - 28.3
  - 818
  - 20
  - 1,049
  - 81
  - 24.4
  - 407
* - TMY 2041–2060
  - −6.8
  - 9.7
  - 30.2
  - 577
  - 82
  - 991
  - 83
  - 26.3
  - 464
* - TMY 2081–2100
  - −10.4
  - 11.2
  - 29.7
  - 246
  - 49
  - 941
  - 83
  - 29.5
  - 530
* - Heat wave longest (2045)\*
  - −11.0
  - 10.5
  - 29.8
  - 530
  - 78
  - 1,016\*
  - 79
  - 27.1
  - 537\*
* - Heat wave most intense (2055)
  - −8.9
  - 9.4
  - 32.8
  - 1,006
  - 100
  - 1,041
  - 81
  - 25.5
  - 620
* - Heat wave most severe (2054)
  - −9.4
  - 10.2
  - 32.0
  - 509
  - 192
  - 1,044
  - 81
  - 26.8
  - 683
```

:::{note}
\*The heat-wave file "longest" (2045) has no solar radiation from 1 to 14 August: global, direct and diffuse radiation are zero in all 336 hours, while temperature and humidity run on normally. The gap lies inside the heat wave the file was made for (15 July to 20 August 2045). Its annual global radiation is therefore about 90 kWh/m² too low, and its UTCI hours are underestimated. Use this file for temperature and humidity only, and the "most intense" or "most severe" file where solar gains matter. The three heat-wave files also contain 4–6 corrupt hours of global and diffuse radiation (values far above 1,400 W/m²); these were removed and interpolated before the table was computed.
:::

## 5. Extremes

### Heat waves

*TBA:* definitions (days above 25 °C, tropical nights above 20 °C); health effects; the three Annex 80 Copenhagen heat-wave files for 2041–2060 (longest, most intense and most severe); why warm nights defeat night ventilation.

### Urban heat island

The urban heat island intensity is the air temperature difference $\Delta T_\mathrm{UHI} = T_\mathrm{urban} - T_\mathrm{rural}$. It is mainly a night-time effect and peaks a few hours before sunrise on calm, clear summer nights. The causes:

- **Heat storage:** brick, concrete and asphalt store solar heat during the day and release it at night.
- **Low sky view factor:** street canyons see little of the cold night sky, so long-wave cooling is reduced.
- **Little evaporation:** sealed surfaces drain rain away instead of evaporating it.
- **Low wind speed:** buildings reduce convective cooling and mixing.
- **Waste heat:** traffic, buildings and air-conditioning condensers.

In Denmark the effect is modest but not negligible. On warm nights central Copenhagen is typically about 2 K warmer than the open land around it, and the effect is strongest on the warmest days of the year {cite}`sorup2026`. In four Finnish cities the mean intensity is 0.5–1.2 K, peaking at about 1.5 K around 05:00 in Helsinki {cite}`taylor2025`.

The Danish reference years are measured at Sjælsmark, a rural station, so they contain no heat island. The heat island acts exactly when night ventilation works. {numref}`fig-vc-uhi` colours every hour by the temperature difference available for ventilative cooling, $\Delta T = T_\mathrm{in} - T_\mathrm{out}$, with $T_\mathrm{in} = 24$ °C. Adding a 2 K night-time heat island lowers the mean night-time $\Delta T$ from May to September from 10.7 K to 8.8 K, and the number of night hours with less than 3 K rises from 20 to 77. In the RCP4.5 2080–2099 file with a heat island, the mean drops to 7.9 K and 161 night hours have less than 3 K.

```{figure} figures/ch02/vc-potential-uhi.*
:name: fig-vc-uhi
:width: 100%

Hourly ventilative cooling potential $\Delta T = T_\mathrm{in} - T_\mathrm{out}$ for the rural reference year at Sjælsmark, the same year with a 2 K night-time urban heat island (tapering to 0 K in the afternoon), and RCP4.5 2080–2099 with the heat island. Grey: heating days, with a daily mean below 12 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/vc_potential_uhi.py)
```

## 6. Overheating indicators and design consequences

*Outline:* hours above 26/27/28 °C, degree-hours, adaptive comfort categories; results from Farahani et al. (2021) and Potin (2023); overhangs, g-value and window size today versus in the future.

## 7. Worked example

*Outline:* read the DRY, Annex 80 TMY and heat-wave EPW files with a short Python script and compare peak temperature, hours above 26 °C, tropical nights and the longest heat wave.

## 8. Guiding questions

*Outline:* for example, "Which weather file would you use to size a heat pump, and which to check overheating?" and "Why can a design that passes the building regulations overheat in a heat wave?"

## Sources

- DMI (2025). *Dansk Referenceår 2025*. DMI Rapport 25-14. Danish Meteorological Institute.
- Velashjerdi Farahani, A., et al. (2021). Overheating risk and energy demand of Nordic old and new apartment buildings during average and extreme weather conditions under a changing climate. *Applied Sciences*, 11, 3972. doi:10.3390/app11093972
- Potin, E. (2023). *Methodology to guide designers in conceiving dwellings that reduce overheating risk in the context of climate change*. MSc thesis, DTU / University of Mons.
