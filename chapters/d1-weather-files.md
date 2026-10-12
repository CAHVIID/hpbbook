# D1 Future climate and weather files

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D1.1 Introduction

Future climate changes and given the life span of buildings, they need to be designed for that. This chapter gives an overview of the climate challenges.

## D1.2 What is in a weather file

A weather file holds one year of hourly outdoor conditions for one location: dry-bulb temperature, humidity, direct normal, diffuse and global horizontal radiation, wind speed and direction, and cloud cover. Three abbreviations recur:

- **TMY**, typical meteorological year: one artificial year assembled from twelve typical months taken from many years of data. It represents average weather, not extremes.
- **DRY**, design reference year: the Danish typical year, published by DMI (section D1.3).
%@claude: constrast DRY more to TMY 

Weather files come in many different file formats. The most know is EPW, EnergyPlus weather file whhich is a text format with 8 header lines followed by 8,760 hourly rows. Most building simulation tools read it.

The DRY files can be downloaded as EPW or CSV from [DMI](https://www.dmi.dk/publikationer).

## D1.3 The Danish design reference year - DMI

A reference year is one artificial year of hourly weather. It is assembled from twelve real calendar months, each picked from a longer measured record as the most typical month of its kind. Danish Meteorological Institute (DMI) selects the months with the Finkelstein–Schafer method of ISO 15927-4. The method compares the distribution of daily values in each candidate month with the distribution for all years, using temperature, global radiation and humidity as primary parameters and wind and precipitation as secondary ones.

Denmark has two generations of design reference year (DRY), both for the DMI station at Sjælsmark north of Copenhagen, with solar radiation measured at DTU in Lyngby:

- **DRY 2001–2010**, the reference used in building regulations until now.
- **DRY 2011–2023**, the 2025 reference year {cite:p}`dmi2025`. Its twelve months come from 2014–2023.

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

**DMI considers RCP4.5 the most likely scenario**, as it corresponds to about 2.7 °C of global warming by the end of the century {cite:p}`dmi2025`.

:::{admonition} Extra
:class: dropdown
Climate models give only daily temperature and precipitation, not the hourly radiation and humidity a simulation needs. So DMI used the projected daily values to *choose* months from the measured 2014–2023 record: for each calendar month the measured month whose temperature distribution best matches the projection, is picked, with precipitation as the tie-breaker.  Every hour in a future file is therefore real, measured weather from the last decade.
:::
%@claude: too popular to use the word tie-breaker. Rephrase 

{numref}`fig-dry-weather` shows the current and future DRY files, and {numref}`tab-dry-summary` summarises them.

```{figure} figures/d1/dry-air-temperature.png
:name: fig-dry-weather
:width: 100%

Hourly air temperature and daily mean (blue), daily global horizontal radiation (orange, right axis) and relative humidity (green) for the Danish design reference years at Sjælsmark: the old and new present-day files and the four RCP4.5 projections. The dashed line marks 26 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_dry.py)
```

%@claude: do a box plot of air temperatures here from DMI data. Separate datasets into winter (oct-mar) and summer (apr-sep) first, so we see how the season progress across climate files. In total 12 boxes.

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
  - Hours UTCI > 26 °C
* - DRY 2001–2010
  - −15.0
  - 8.1
  - 27.7
  - 1,386
  - 28
  - 1,038
  - 83
  - 23.1
  - 292
* - DRY 2011–2023 (2025)
  - −7.6
  - 9.6
  - 30.3
  - 595
  - 37
  - 1,023
  - 81
  - 25.6
  - 432
* - RCP4.5, 2035–2054
  - −8.1
  - 9.9
  - 29.0
  - 471
  - 48
  - 1,017
  - 82
  - 26.4
  - 546
* - RCP4.5, 2045–2064
  - −8.1
  - 10.0
  - 31.0
  - 471
  - 80
  - 1,027
  - 82
  - 26.6
  - 610
* - RCP4.5, 2055–2074
  - −8.1
  - 10.3
  - 31.2
  - 469
  - 90
  - 1,030
  - 81
  - 27.1
  - 623
* - RCP4.5, 2080–2099
  - −8.1
  - 10.1
  - 31.2
  - 473
  - 90
  - 1,019
  - 81
  - 26.6
  - 627
```

Enthalpy is the annual mean total specific enthalpy of the outdoor air per kg dry air, $h = 1.006\,T + x\,(2501 + 1.86\,T)$ in kJ/kg, with the humidity ratio $x$ found from air temperature, relative humidity and pressure.

Enthalpy expresses the total energy content of the atmosphere (latent and sensible heat). In a building context, it indicates the increased work load on a chiller that needs to both cool the air, as well as shed the water content. 

The UTCI column is explained in the section on heat stress indices below.

:::{admonition} Take-aways
:class: dropdown
Four take-aways:

1. **A big step has already happened.** Going from the *2001–2010* to the *2011–2023* reference year raises the mean temperature by about 1.5 °C and cuts the hours below 0 °C by more than half, yet [severe frost still occurs](https://www.berlingske.dk/danmark/over-18-frostgrader-goer-natten-til-soendag-til-koldeste-i-fem-aar).
2. **Summers get warmer, but slowly.** Hours above 26 °C rise from 37 today to 80–90 around mid-century.
3. **Radiation and humidity hardly change.** Global radiation stays at about 1,020–1,040 kWh/m² and mean relative humidity at 81–83 %. Solar gains in the future files are those of today.
4. **The projections flatten out.** The 2080–2099 file is no warmer than 2055–2074; the two differ only in January, May and October. Because every future month must be a measured month from 2014–2023, the files can never be hotter than the hottest month of that decade.
:::

### Heat stress index UTCI

Air temperature alone does not tell how hot it feels outdoors. Sun, wind and humidity matter as much, and a heat stress index combines them into one number.

The Universal Thermal Climate Index (UTCI) {cite:p}`brode2012` is the index used in this chapter. It is the air temperature of a reference environment that gives the same physiological strain as the actual one, for a person walking at 4 km/h. The reference environment has 50 % relative humidity, almost no wind and no radiation beyond that of the air temperature. The inputs are air temperature, humidity, wind speed and mean radiant temperature. Here the mean radiant temperature is that of a person standing in the open, found from the direct and diffuse solar radiation in the weather file (the SolarCal method of ASHRAE 55). The tables count the hours with UTCI above 26 °C, which is where moderate heat stress begins.

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

Two alternatives are common:

- **PET**, the Physiological Equivalent Temperature {cite:p}`hoppe1999`, is built on the same idea as UTCI and uses the same inputs, but with an indoor reference environment and a simpler body model. Moderate heat stress starts at about 29 °C {cite:p}`matzarakis1999`.
- **WBGT**, the wet-bulb globe temperature, is a weighted mean of the natural wet-bulb, globe and air temperatures. It is the index of occupational and sports heat limits. It needs measured wet-bulb and globe temperatures, so from a weather file it can only be estimated {cite:p}`bom_wbgt`.

<!-- :::{admonition} Rules of thumb
:class: tip
- Use the current DRY for energy-frame compliance and for sizing heating.
- Check summer comfort with at least one future file as well, since a 2025 building will meet a 2050 climate.
- A reference year is built from *typical* months. DMI itself says it is not suited for sizing against extreme events such as overheating. Stress-test the design with a heat-wave file (section 5).
::: -->

## D1.4 Future weather files - Annex 80

The IEA EBC Annex 80 project made a set of Copenhagen files from the MPI-REMO regional climate model (EURO-CORDEX): typical meteorological years (TMY) for:

- 2001–2020 (representing 2010)
- 2041–2060 (representing 2050)
- 2081–2100 (representing 2090)

and three heat-wave years picked from 2041–2060 under RCP8.5 and bias-adjusted against observations from 2001–2019. 

Unlike the DRY files, these are model output, not measured months, so they can be hotter than anything seen so far. {numref}`fig-annex80-weather` shows them and {numref}`tab-annex80-summary` summarises them in the same way as the DRY files.

```{figure} figures/d1/annex80-weather.*
:name: fig-annex80-weather
:width: 100%

Hourly air temperature and daily mean (blue), daily global horizontal radiation (orange, right axis) and relative humidity (green) for the Annex 80 Copenhagen files: three typical years and three heat-wave years. The dashed line marks 26 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_annex80.py)
```
%@claude: do a box plot of air temperatures here from Annex 80 data. Separate datasets into winter (oct-mar) and summer (apr-sep) first, so we see how the season progress across climate files. In total 12 boxes.

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

### Future cloud cover and solar irradiation

The two file sets disagree on future cloudiness ({numref}`fig-cloud-cover`). The future DRY files show no trend in summer cloud cover, but they cannot: they are built from measured months chosen to match projected temperatures. The Annex 80 files, which are climate model output, have 6% less summer solar irradiation in 2041–2060 and 12% less in 2081–2100 than in 2001–2020, which means less PV output in the cooling season, when AC demand already peaks after sunset ([](#app-ac-europe)).

```{figure} figures/d1/cloud-cover.*
:name: fig-cloud-cover
:width: 100%

(a) Mean total sky cover, May to September, in the DMI DRY files. (b) Monthly global horizontal irradiation in the Annex 80 Copenhagen TMY files, which contain no cloud cover data. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_cloud_cover.py)
```

## D1.5 Extremes

### Heat waves

A heat wave is a run of hot days. A simple definition, used here, is a period of days with a maximum temperature above 25 °C. A *tropical night* is a night where the temperature does not fall below 20 °C {cite:p}`farahani2021`.

Heat waves raise mortality, mainly through cardiovascular and respiratory strain, and the old and the sick are most at risk. The hot summer of 2018 caused about 380 additional deaths in Finland, and the heat-related mortality risk in Helsinki was about 2.5 times that of the surrounding rural areas {cite:p}`farahani2021`.
%@claude: can you find similar data from the 2026 summer in France, Spain and UK? Preferable from renowed journal publications, otherwise flag for review by me

A reference year holds typical months, so it has no real heat wave. The Annex 80 heat-wave files fill the gap. They are the three years of 2041–2060 with the longest, the most intense (hottest) and the most severe (longest and hottest combined) heat wave. {numref}`tab-heat-waves` compares them with the typical years.

```{list-table} Hot days and tropical nights in the Copenhagen weather files, computed from the EPW files. A tropical night has a minimum above 20 °C between 21:00 and 09:00.
:name: tab-heat-waves
:header-rows: 1

* - Weather file
  - Days above 25 °C
  - Longest run of days above 25 °C
  - Tropical nights
  - Warmest night, minimum (°C)
* - DRY 2011–2023 (2025)
  - 12
  - 4
  - 0
  - 18.6
* - DRY RCP4.5, 2080–2099
  - 21
  - 4
  - 0
  - 19.8
* - Annex 80 TMY 2041–2060
  - 16
  - 7
  - 0
  - 18.9
* - Heat wave longest (2045)
  - 27
  - 10
  - 1
  - 21.1
* - Heat wave most intense (2055)
  - 25
  - 5
  - 2
  - 24.0
* - Heat wave most severe (2054)
  - 42
  - 14
  - 1
  - 20.4
```

Warm nights are the real problem. Night ventilation removes heat in proportion to the airflow times the temperature difference between indoor and outdoor air ([](d4-ventilative-cooling.md)). When the night stays above 20 °C, that difference is only a few kelvin, so the thermal mass is not emptied and the next day starts warmer. After a few such days the building has no reserve left.

Simulations of Finnish apartment buildings without cooling show the result {cite:p}`farahani2021`. The heat wave of 2018 had 24 days above 25 °C and 5 tropical nights, and gave about 10,000 degree-hours above 27 °C indoors.

The same heat wave moved to the climate of 2050 has 15 tropical nights and gives about 14,000 degree-hours above 27 °C, and the degree-hours above 32 °C, a health risk threshold, triple from about 1,000 to 3,000. Openable windows were the most effective passive measure, but only a cooling unit removed the overheating completely.

### Urban heat island

The urban heat island intensity is the air temperature difference $\Delta T_\mathrm{UHI} = T_\mathrm{urban} - T_\mathrm{rural}$. It is mainly a night-time effect and peaks a few hours before sunrise on calm, clear summer nights. The causes:

- **Heat storage:** brick, concrete and asphalt store solar heat during the day and release it at night.
- **Low sky view factor:** street canyons see little of the cold night sky, so long-wave cooling is reduced.
- **Little evaporation:** sealed surfaces drain rain away instead of evaporating it.
- **Low wind speed:** buildings reduce convective cooling and mixing.
- **Waste heat:** traffic, buildings and air-conditioning condensers.

In Denmark the effect is modest but not negligible. {numref}`fig-uhi-denmark` shows it for the four largest Danish cities. On the 3 % warmest days of the year, Copenhagen is on average 1.5–2 K warmer than its rural surroundings at night, and on some nights close to 3 K. The difference almost disappears around 09:00. The other three cities stay at about 1 K {cite:p}`sorup2026`. In four Finnish cities the mean intensity is 0.5–1.2 K, peaking at about 1.5 K around 05:00 in Helsinki {cite:p}`taylor2025`.
%@claude: add a reference to Lauwaet et al. (2024), Urban Climate 54, 101850 (100 European cities), which is valuable for European context.

```{figure} figures/d1/urbansci-10-00171-g003.png
:name: fig-uhi-denmark
:width: 100%

Urban heat island intensity (°C) over the day in Copenhagen, Odense, Aarhus and Aalborg, for the 3 % warmest days, summer, winter and the 3 % coldest days. Lines are the average and bands the spread, for a machine-learning downscaled temperature product (C4C, blue) and the DANRA reanalysis (orange). Reproduced unchanged from Figure 3 of Sørup et al. {cite:p}`sorup2026`, © the authors, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
```


%Wang et al. (2023), Urban Climate 49, 101531 (Stockholm) is a model sensitivity study and adds little here.

The heat island acts exactly when night ventilation works. {numref}`fig-vc-uhi` colours every hour by the temperature difference available for ventilative cooling, $\Delta T = T_\mathrm{in} - T_\mathrm{out}$, with $T_\mathrm{in} = 24$ °C. The heat island is set to 2 K at night, the upper end of the Copenhagen averages.

The effect of urban heat islands is more pronounced with future climate, but the magnitude will probably remain the same or even decrease a little as global radiation drops, and mitigating actions are implemented like more green areas in the built environment.

```{figure} figures/d1/vc-potential-uhi.*
:name: fig-vc-uhi
:width: 100%

Hourly ventilative cooling potential $\Delta T = T_\mathrm{in} - T_\mathrm{out}$ for the present reference year and RCP4.5 2080–2099 at Sjælsmark, each without and with a 2 K night-time urban heat island (tapering to 0 K in the afternoon). Grey: heating days, with a daily mean below 12 °C. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/vc_potential_uhi.py)
```
