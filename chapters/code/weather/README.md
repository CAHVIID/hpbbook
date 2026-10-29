# Weather files

EPW files used by the figure scripts of chapter D1 (`plot_dry.py`, `plot_annex80.py`, `plot_cloud_cover.py`, `plot_temperature_boxes.py`, `plot_temperature_ridges.py`, `vc_potential_uhi.py`, `compare_heatwave_files.py`). The scripts read this folder by default.

## Danish design reference years (DMI, Sjælsmark)

| File | Content |
| --- | --- |
| `Denmark_DRY_2001-2010.epw` | DRY 2001–2010, the old reference year. Renamed copy of DMI's `DRY_2001-2010_epw-fil.epw`. |
| `DRY_2011-2023_epw-fil.epw` | DRY 2011–2023, the 2025 reference year. |
| `DRY_rcp45_2035_2054_epw-fil.epw` | Climate-projected reference year, RCP4.5, 2035–2054. |
| `DRY_rcp45_2045_2064_epw-fil.epw` | Same, 2045–2064. |
| `DRY_rcp45_2055_2074_epw-fil.epw` | Same, 2055–2074. |
| `DRY_rcp45_2080_2099_epw-fil.epw` | Same, 2080–2099. |

Source: DMI Rapport 25-14, *Dansk Referenceår 2025*, data in EPW format from <https://www.dmi.dk/publikationer> (`EPW_referenceaar_2025.zip`). The DMI archive also holds the RCP2.6 and RCP8.5 years, which are not used here.

## IEA EBC Annex 80, Copenhagen

| File | Content |
| --- | --- |
| `5A_Copenhagen_TMY_2001-2020.epw` | Typical meteorological year, 2001–2020. |
| `5A_Copenhagen_TMY_2041-2060.epw` | Typical meteorological year, 2041–2060. |
| `5A_Copenhagen_TMY_2081-2100.epw` | Typical meteorological year, 2081–2100. |
| `5A_Copenhagen_HW_Midterm_Longest_2045.epw` | Heat-wave year 2041–2060, longest heat wave. |
| `5A_Copenhagen_HW_Midterm_MostIntense_2055.epw` | Heat-wave year 2041–2060, most intense heat wave. |
| `5A_Copenhagen_HW_Midterm_MostSevere_2054.epw` | Heat-wave year 2041–2060, most severe heat wave. |

Source: Machard et al. (2024), *Typical and extreme weather datasets for studying the resilience of buildings to climate change and heatwaves*, Scientific Data 11, 531, doi:10.1038/s41597-024-03319-8. Data at <https://www.wdc-climate.de/ui/entry?acronym=WDTF_Annex80_build_v1.0>.

The heat-wave files are the original ones. They hold a few corrupt radiation hours, and the "longest" file has no solar radiation from 1 to 14 August (see the note in chapter D1). The scripts remove the corrupt hours when they read the files.

## DRY 2011–2023 with summer 2018

| File | Content |
| --- | --- |
| `DRY_2011-2023_heatwave2018.epw` | DRY 2011–2023 with July and August replaced by DMI observations from Sjælsmark (06188), 2018. Direct and diffuse radiation from global with the Erbs model. Built by `build_dry_heatwave_2018.py`. |
| `dmi_06188_2018_jul_aug.csv` | The hourly DMI observations used (UTC, hour ending), from <https://opendataapi.dmi.dk/v2/metObs>. |
