(app-thermal-bridge-lab)=
# Appendix G: Thermal Bridge Lab

:::{warning} Under revision
This appendix is being reworked and may change substantially.
:::

The Thermal Bridge Lab calculates two-dimensional, steady-state heat conduction through a construction detail. The detail is drawn as rectangles of material, and boundary conditions are drawn as edges on its surfaces. The app solves the temperature field with the finite difference method and gives the thermal coupling coefficient $L_{2D}$ and the temperature factor $f_{Rsi}$, from which the linear thermal transmittance $\psi$ follows. The method, the modelling rules of ISO 10211 and a worked example are given in the section *Thermal bridges* of chapter A1 The building envelope.

## The app

**[Open the Thermal Bridge Lab in a new tab](code/thermal-bridge-lab.html)**. It runs in your browser, updates the results while you draw and needs no installation. It opens with an external wall corner: 200 mm concrete with 200 mm mineral wool on the outside, seen in plan ({numref}`fig-thermal-bridge-lab-appendix`).

:::{figure} figures/a1/thermal-bridge-lab-app.*
:label: fig-thermal-bridge-lab-appendix
:alt: Screenshot of the Thermal Bridge Lab. On the left, the drawing board with an L-shaped external wall corner coloured by temperature from blue outside to red inside, with isotherms and labelled inside and outside boundary edges. On the right, the results panel with heat flow, L2D, minimum inside surface temperature and fRsi, followed by the lists of boundary conditions, boundary edges and materials.
:width: 100%

The Thermal Bridge Lab with the external wall corner example, showing the temperature field. Open the app to draw your own detail.
:::

## How to use the app

1. **Drawing.** Pick a material in the *Materials* list, or add one from the library, and edit its name and $\lambda$ in the list. Choose *Draw* (key **D**) and drag on the board to draw a rectangle. Edges snap to existing edges and to the snap grid. A rectangle drawn later covers the ones below it, so a steel profile can be drawn on top of an insulation layer; the order is changed under *Layers*. With *Select* (key **V**), a rectangle is moved or resized, or its coordinates are typed in millimetres under *Selected rectangle*.
2. **Boundary conditions.** Each boundary condition has a name, a type and its values: convective (air temperature and surface resistance), fixed surface temperature, heat flux, or adiabatic. Use $R_{si} = 0.13$ m²K/W for heat loss through walls and add a second inside condition with $R_{si} = 0.25$ m²K/W for the surface temperature. Pick a condition, choose *Boundary* (key **B**) and click on a surface to assign it to the whole face up to the next corner, or drag along the surface to assign part of it. Surfaces without a boundary edge are adiabatic and shown dashed, which is the condition at the cut-off planes.
3. **Mesh.** *Default* sets the cell size from the geometry. Set a smaller minimum cell size and check that $L_{2D}$ does not change in the third digit.
4. **Results.** Switch between *Geometry*, *Mesh*, *Temperature* and *Heat flux*, and hover over the board to read the temperature and heat flux at a point. The results panel gives the heat flow through each boundary, the energy balance, which should be close to zero, and
   - $L_{2D} = \Phi / (\theta_i - \theta_e)$ in W/(m·K), the heat flow per metre length of the detail per kelvin between the warmest and the coldest boundary condition. Subtract $\sum U_j l_j$ of the flanking elements to get $\psi$, with the lengths measured as inside or outside dimensions, consistent with the heat loss calculation.
   - $f_{Rsi} = (\theta_{si,min} - \theta_e)/(\theta_i - \theta_e)$, from the lowest surface temperature on the warmest boundary condition. Read it with $R_{si} = 0.25$ m²K/W on the inside when it is used to assess the risk of mould growth.
5. **Saving.** *Save case file* downloads the model as a JSON file and *Open case file* loads it again. The app does not keep the model when the window is closed.

## Download

The app is a single HTML file, {download}`thermal-bridge-lab.html <code/thermal-bridge-lab.html>`. Save it anywhere and double-click it to use it offline. The two examples, the external wall corner and a steel stud in a light frame wall, are available as case files: {download}`thermal-bridge-corner.json <code/thermal-bridge-corner.json>` and {download}`thermal-bridge-stud.json <code/thermal-bridge-stud.json>`.

The same calculation in Python, with comments on every step, is {download}`thermal_bridge.py <code/thermal_bridge.py>`. It reads the same case files and needs numpy, scipy and matplotlib.
