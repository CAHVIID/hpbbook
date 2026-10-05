# Weather files and future weather

## Learning objectives

After this chapter you can:

- explain what a weather file contains and how a reference year is assembled from measured months;
- tell a design reference year (DRY) from a typical meteorological year (TMY) and choose the right file for sizing, compliance and overheating studies;
- explain how future weather files are made and what their uncertainty means for design;
- define a heat wave and use heat-wave weather files to stress-test a design;
- read an EPW file and compute simple indicators such as hours above 26 °C, hours below 0 °C and degree-hours;
- judge which design decisions still hold in a 2050 climate.

## 1. Introduction

*Outline:* the weather file is the input that decides whether a building passes or fails summer comfort, and buildings designed today will still stand in 2080. The course row house is the running case.

## 2. What is in a weather file

*Outline:* hourly dry-bulb temperature, humidity, direct normal, diffuse and global horizontal radiation, wind and cloud cover. File formats (EPW, the Danish DRY format, IDA ICE weather files) and where to get them.

## 3. The Danish design reference year

A reference year is one artificial year of hourly weather. It is assembled from twelve real calendar months, each picked from a longer measured record as the most typical month of its kind. DMI selects the months with the Finkelstein–Schafer method of ISO 15927-4. The method compares the distribution of daily values in each candidate month with the distribution for all years, using temperature, global radiation and humidity as primary parameters and wind and precipitation as secondary ones.

Denmark has two generations of design reference year (DRY), both for the DMI station at Sjælsmark north of Copenhagen, with solar radiation measured at DTU in Lyngby:

- **DRY 2001–2010**, the reference used in building regulations until now.
- **DRY 2011–2023**, the 2025 reference year (DMI Report 25-14). Its twelve months come from 2014–2023.

### Future reference years

DMI has also published twelve *climate-projected* reference years: three emission scenarios (RCP2.6, RCP4.5 and RCP8.5) for four periods (2035–2054, 2045–2064, 2055–2074 and 2080–2099). DMI considers RCP4.5 the most likely scenario, as it corresponds to about 2.7 °C of global warming by the end of the century (DMI Report 25-14).

The future files are made in an unusual way. Climate models give only daily temperature and precipitation, not the hourly radiation and humidity a simulation needs. So DMI uses the projected daily values to *choose* months from the measured 2014–2023 record: for each calendar month it picks the measured month whose temperature distribution best matches the projection, with precipitation as the tie-breaker. Every hour in a future file is therefore real, measured weather from the last decade.

{numref}`fig-dry-weather` shows the current and future DRY files, and {numref}`tab-dry-summary` summarises them.

```{figure} figures/ch02/dry-air-temperature.png
:name: fig-dry-weather
:width: 100%

Hourly air temperature and daily mean (blue), daily global horizontal radiation (orange, right axis) and relative humidity (green) for the Danish design reference years at Sjælsmark: the old and new present-day files and the four RCP4.5 projections. The dashed line marks 26 °C.
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
* - DRY 2001–2010
  - −15.0
  - 8.1
  - 27.7
  - 1,386
  - 28
  - 1,038
  - 83
* - DRY 2011–2023 (2025)
  - −7.6
  - 9.6
  - 30.3
  - 595
  - 37
  - 1,023
  - 81
* - RCP4.5, 2035–2054
  - −8.1
  - 9.9
  - 29.0
  - 471
  - 48
  - 1,017
  - 82
* - RCP4.5, 2045–2064
  - −8.1
  - 10.0
  - 31.0
  - 471
  - 80
  - 1,027
  - 82
* - RCP4.5, 2055–2074
  - −8.1
  - 10.3
  - 31.2
  - 469
  - 90
  - 1,030
  - 81
* - RCP4.5, 2080–2099
  - −8.1
  - 10.1
  - 31.2
  - 473
  - 90
  - 1,019
  - 81
```

Four things stand out:

1. **The biggest step has already happened.** Going from the 2001–2010 to the 2011–2023 reference year raises the mean temperature by 1.4 °C and cuts the hours below 0 °C by more than half. Heating plant sized on the old file will tend to be oversized.
2. **Summers get warmer, but slowly.** Hours above 26 °C rise from 37 today to 80–90 around mid-century.
3. **Radiation and humidity hardly change.** Global radiation stays at about 1,020–1,040 kWh/m² and mean relative humidity at 81–83 %. Solar gains in the future files are those of today.
4. **The projections flatten out.** The 2080–2099 file is no warmer than 2055–2074; the two differ only in January, May and October. Because every future month must be a measured month from 2014–2023, the files can never be hotter than the hottest month of that decade.

:::{admonition} Rules of thumb
:class: tip
- Use the current DRY for energy-frame compliance and for sizing heating.
- Check summer comfort with at least one future file as well, since a 2025 building will meet a 2050 climate.
- A reference year is built from *typical* months. DMI itself says it is not suited for sizing against extreme events such as overheating. Stress-test the design with a heat-wave file (section 5).
:::

## 4. Future weather files beyond the DRY

*Outline:* climate models (GCM, RCM), downscaling, emission scenarios (RCP, SSP); morphing a present-day year (CCWorldWeatherGen) versus bias-corrected regional model output; the Annex 80 TMY files for 2001–2020, 2041–2060 and 2081–2100; uncertainty.

## 5. Heat waves

*Outline:* definitions (days above 25 °C, tropical nights above 20 °C); health effects; the three Annex 80 Copenhagen heat-wave files for 2041–2060 (longest, most intense and most severe); why warm nights defeat night ventilation.

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
