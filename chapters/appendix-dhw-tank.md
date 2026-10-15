(app-dhw-tank)=
# Appendix D: Stratified tank simulator

:::{warning} Under revision
This appendix is being reworked and may change substantially.
:::

A hot water tank is not simply full or empty. Hot water floats on top of cold water, and a well-designed tank keeps the two apart, with a thin mixing zone, the thermocline, between them. Hot water is drawn from the top while cold mains water flows in at the bottom, so the thermocline moves up as the tank is emptied. The simulator in this appendix follows this hour by hour for one day.

The tank is split into horizontal layers. A heat pump charges it through an external heat exchanger: the charging loop takes water from the bottom of the tank and returns it at mid-height, and there is no circulation loop. A thermostat starts the heat pump when the sensor falls below the setpoint, and it can only run in the hours you allow. The tab *Tapping profiles* shows the predefined days of hot water use, with their sources, and lets you import a profile made with DHWcalc.

## The app

**[Open the tank simulator in a new tab](code/dhw-tank.html)**. It runs in your browser and needs no installation. {numref}`fig-dhw-tank-app` shows it with the default inputs.

:::{figure} figures/appendix-dhw/dhw-tank-app.*
:label: fig-dhw-tank-app
:alt: Screenshot of the tank simulator. Sliders for the tank, the heat pump and heat exchanger, the control and the hours the heat pump may run, and a list of tapping profiles at the top. Below, a drawing of the tank coloured by temperature with the heat exchanger and heat pump, the temperature profile over the tank height, a time slider, and charts over 24 hours of the tank temperature by height, the temperatures at the top, inlet, bottom and tap, and the heat flows.
:width: 100%

The tank simulator with the default inputs: a 200 L tank, a 3 kW heat pump allowed to run in all hours and the profile "Family of 4, morning and evening". Open the simulator to change the inputs.
:::

The simulator is a single HTML file, {download}`dhw-tank.html <code/dhw-tank.html>`. Save it anywhere and double-click it to use it offline.

## The Python version

The same model in Python, with comments on every assumption, can be downloaded here: {download}`dhw_tank.py <code/dhw_tank.py>`. Running it prints the daily heat of each profile and the results for the default inputs.
