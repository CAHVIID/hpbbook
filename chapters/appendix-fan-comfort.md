(app-fan-comfort)=
# Appendix F: Ceiling fan comfort app

:::{warning} Under revision
This appendix is being reworked and may change substantially.
:::

IDA ICE treats the occupants as sitting in still air, so a ceiling fan only shows up in a simulation as extra internal gain. The app in this appendix adds the comfort benefit of the fan afterwards, hour by hour, from the temperatures IDA ICE has calculated. It uses the same method as section [D6.6](#d6-fans-in-simulation) and the script `fan_comfort.py`.

For each zone, load `TEMPERATURES.prn` and `IAQ.prn` from the unpacked IDA ICE model, give the room width and ceiling height, and choose when the room is occupied. Enter the fan from its datasheet, with airflow and power for each speed. Drop the EPW file used in the simulation to get the adaptive comfort limits of EN 16798-1. The app then finds the hours where the fan runs and at which speed, and calculates SET in still air and with the fan, the cooling effect, PMV, the cooling fan efficiency and the fan energy. The collapsed section *About this app* at the top of the app summarises the method and the thermal comfort background.

## The app

**[Open the ceiling fan comfort app in a new tab](code/fan-comfort.html)**. It runs in your browser and needs no installation. Without your own files, it opens with synthetic example data for a bedroom and a living room. {numref}`fig-fan-comfort-app` shows it with the example data.

:::{figure} figures/appendix-fan/fan-comfort-app.*
:label: fig-fan-comfort-app
:alt: Screenshot of the ceiling fan comfort app. On the left, inputs for the fan datasheet with airflow and power for each speed, the occupant and the fan control, the period, the weather file and the zones with their .prn files. On the right, a table of the fan at the reference condition, a table of results for each zone, and charts of the operative temperature with and without the fan and of SET in still air and with the fan for one week.
:width: 100%

The ceiling fan comfort app with the synthetic example data and the Fanco Breeze AC 132. Open the app to load your own IDA ICE results.
:::

All hourly results for all zones can be downloaded as a CSV file for further work in Excel or Python.

The app is a single HTML file, {download}`fan-comfort.html <code/fan-comfort.html>`. Save it anywhere and double-click it to use it offline. It needs an internet connection the first time to load the chart library.

## The Python version

The same calculation in Python, which writes the results to an Excel file, can be downloaded here: {download}`fan_comfort.py <code/fan_comfort.py>`. Set the folder of the unpacked IDA ICE model, the zones and the fan at the top of the script. It uses the `pythermalcomfort` package for SET and PMV.
