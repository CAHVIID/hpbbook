# The building envelope

<!--
## Learning objectives

After this chapter you can:

- calculate the transmission heat loss of a building from U-values, areas and line losses
- explain what a thermal bridge is and why it matters more the better the envelope is insulated
- calculate the linear thermal transmittance ψ of a detail from a 2D heat flow calculation
- check a detail for surface condensation and mould risk with the temperature factor fRsi
- set up a 2D thermal bridge model with correct cut-off planes and surface resistances
-->

## Introduction

The envelope is everything that separates the heated inside from the outside: walls, roof, floor, windows and doors, and all the joints between them. Its quality sets the heat loss of the building before any technical system is chosen, and a heat loss that is not there never has to be supplied by a heat pump, a floor heating system or a ventilation unit.

In a well-insulated building, the plane parts of the envelope are rarely the weak spot. Heat finds the joints instead: the foundation, the corners, the window frames and the places where something structural passes through the insulation. This chapter covers the heat loss through the envelope and, in detail, how to calculate the heat loss and surface temperatures at those joints, the thermal bridges.

## Heat loss through the envelope

:::{admonition} To be written
:class: dropdown

Transmission heat loss $H_T = \sum U_i A_i + \sum \psi_j l_j + \sum \chi_k$. U-values of layered constructions with surface resistances {cite:p}`iso6946`. Design heat loss and the share of thermal bridges in a low-energy house.
:::

(sec-thermal-bridges)=
## Thermal bridges

### What a thermal bridge is

A thermal bridge is a part of the envelope where the heat flow is no longer one-dimensional, so that the U-value of the plane construction does not describe it. There are two kinds:

- **Geometrical thermal bridges**, where the shape forces the heat flow to spread out: an external corner, where the outside surface is larger than the inside surface.
- **Constructional (material) thermal bridges**, where a better conducting material passes through the insulation: a steel profile, a concrete balcony slab, a window frame or the foundation under the wall.

Most real details are both. Thermal bridges have two effects, and both get relatively worse the better the rest of the envelope is insulated:

1. **Extra heat loss.** In a low-energy house the line losses at foundations, windows and junctions can be a significant part of the total transmission loss.
2. **Cold inside surfaces.** A local drop in the inside surface temperature raises the relative humidity at the surface, which can lead to mould growth or condensation.

### Linear thermal transmittance

A 2D calculation of a detail gives the heat flow $\Phi$ per metre length of the detail (W/m). Dividing by the temperature difference gives the thermal coupling coefficient

```{math}
:label: eq-tb-l2d
L_{2D} = \frac{\Phi}{\theta_i - \theta_e}
```

in W/(m·K). $L_{2D}$ contains both the plane parts of the detail and the extra loss at the joint. The linear thermal transmittance $\psi$ is the extra part only {cite:p}`iso10211`:

```{math}
:label: eq-tb-psi
\psi = L_{2D} - \sum_j U_j \, l_j
```

where $U_j$ is the U-value of each flanking element and $l_j$ the length over which it applies in the model. A point thermal bridge, such as a fixing through the insulation, is described in the same way by a point thermal transmittance $\chi$ in W/K.

The value of $\psi$ depends on how the lengths $l_j$ are measured. With **inside dimensions** the flanking walls of an external corner are shorter than with **outside dimensions**, so $\sum U_j l_j$ is smaller and $\psi$ is larger. The same corner can therefore have a positive $\psi$ on inside dimensions and a negative $\psi$ on outside dimensions, as the worked example below shows. Both are correct; what matters is that the areas in the heat loss calculation are measured the same way as the $\psi$-values used with them {cite:p}`iso14683`.

### Surface temperature and the temperature factor

The lowest inside surface temperature $\theta_{si,min}$ is made independent of the actual temperatures by the temperature factor

```{math}
:label: eq-tb-frsi
f_{Rsi} = \frac{\theta_{si,min} - \theta_e}{\theta_i - \theta_e}
```

A factor of 1 means the surface is at room temperature; 0 means it is at outdoor temperature. To assess mould risk, $f_{Rsi}$ is compared with the minimum factor needed to keep the relative humidity at the surface below the critical level for the climate and the indoor humidity class. That assessment uses a higher inside surface resistance than the heat loss calculation, $R_{si} = 0.25$ m²K/W, to account for furniture and corners with poor air movement {cite:p}`iso13788`.

### Modelling rules

A 2D model is a cut through the construction. ISO 10211 sets the rules that make the result independent of where the cut is made {cite:p}`iso10211`:

- **Cut-off planes.** The model is cut at least 1 m from the central element, or at three times the thickness of the flanking element if that is more, or at a symmetry plane. The cut planes are adiabatic.
- **Surface resistances.** For heat loss, use the values in {numref}`tab-tb-rs`. For surface temperatures and mould risk, use $R_{si} = 0.25$ m²K/W on the inside.
- **Materials.** Use design values of thermal conductivity. Thin layers with little effect, such as membranes, can be left out.

:::{table} Surface resistances for heat loss calculations {cite:p}`iso6946`.
:label: tab-tb-rs

| Surface | Direction of heat flow | $R_s$ [m²K/W] |
|---|---|---|
| Inside, $R_{si}$ | horizontal (walls) | 0.13 |
| Inside, $R_{si}$ | upwards (ceilings, roofs) | 0.10 |
| Inside, $R_{si}$ | downwards (floors) | 0.17 |
| Outside, $R_{se}$ | any | 0.04 |
:::

### How the calculation works

The app and the Python script below solve two-dimensional, steady-state heat conduction with the finite difference method on a structured grid. The steps are:

1. **Geometry.** The construction is drawn as rectangles of material. Rectangles can overlap; the one drawn last is on top. A wall can be drawn as one large rectangle of insulation with a thin steel profile drawn on top of it.
2. **Mesh.** Every rectangle edge becomes a grid line across the whole model. Each gap between two lines is divided into cells that are small next to the lines and grow towards the middle of the gap. This puts fine cells at the material interfaces, where the temperature gradients are steepest, and coarse cells in the bulk of each layer. A 1 mm steel web gets its own row of cells without making the whole model fine.
3. **Materials.** Each cell takes the conductivity $\lambda$ of the top-most rectangle that covers its centre. Cells that no rectangle covers are empty space, which is how L-shapes and voids are modelled.
4. **Energy balance.** For each cell the heat flows to its four neighbours add up to zero. The flow between two cells is a conductance times their temperature difference, with the conductance of two half cells in series:

   ```{math}
   :label: eq-tb-conductance
   G = \frac{A}{\dfrac{\Delta x_1}{2 \lambda_1} + \dfrac{\Delta x_2}{2 \lambda_2}}
   ```

   where $A$ is the face area per metre length (the cell height, in m²/m).
5. **Boundaries.** Every cell face between material and empty space is a surface. A convective surface connects the cell to the air temperature through half a cell plus the surface resistance, $G = A / (\Delta x / 2\lambda + R_s)$. A fixed surface temperature is the same with $R_s = 0$, a heat flux adds a known heat flow, and an adiabatic surface adds nothing. Surfaces without a boundary are adiabatic, which is exactly what the cut-off planes need.
6. **Solution.** The balances form a linear system $\mathbf{A}\,\mathbf{T} = \mathbf{b}$ with one unknown temperature per cell, solved directly. The heat flow through each boundary, the surface temperatures and the heat flux field follow from the temperatures.

For a plane wall the method gives exactly the 1D result $U = 1/(R_{si} + \sum d/\lambda + R_{se})$ on any mesh, which is the first check of the code.

### Thermal Bridge Lab

The app below runs the calculation in your browser and updates the results while you draw. It opens with the external wall corner from the worked example.

```{anywidget} code/thermal-bridge.mjs
{}
```

#### How to use the app

1. **Materials.** Pick a material in the *Materials* list or add one from the library. Edit the name and $\lambda$ directly in the list.
2. **Draw rectangles.** Choose *Draw* (key **D**) and drag on the board. Edges snap to existing edges and to the snap grid. Later rectangles cover earlier ones; change the order in *Layers*. With *Select* (key **V**), drag a rectangle to move it or a corner to resize it, or type exact coordinates in millimetres under *Selected rectangle*.
3. **Boundary conditions.** Each boundary condition has a name, a type and its values: convective (air temperature and surface resistance), surface temperature, heat flux into the construction, or adiabatic. Add as many as the detail needs, for example a separate inside condition with $R_{si} = 0.25$ m²K/W.
4. **Draw boundary edges.** Pick a boundary condition and choose *Boundary* (key **B**). Click on a surface to assign the whole straight face up to the next corner, or drag along a surface to assign part of it. Surfaces without an edge are shown dashed and are adiabatic. An edge that does not lie on a surface is marked *Not on a surface: no effect*.
5. **Mesh.** Set the minimum cell size next to the grid lines, the maximum cell size and the growth ratio. Refine until the results stop changing.
6. **Read the results.** Switch between *Geometry*, *Mesh*, *Temperature* and *Heat flux*, and hover over the board to read the temperature and heat flux at any point. The results panel gives the heat flow through each boundary, $L_{2D}$ and $f_{Rsi}$, taken from the warmest boundary condition, and an energy balance that should be close to zero.
7. **Save your work.** *Save case file* downloads the model as a JSON file and *Open case file* loads one again. The Python script reads the same files.

Use the mouse wheel to zoom and drag on empty space to pan. *Delete* removes the selected rectangle or edge. If the app becomes slow on a fine mesh, untick *Live* and press *Solve* after each change.

### The stand-alone app

The app also runs on its own, outside the book, as a single HTML file: {download}`thermal-bridge-lab.html <code/thermal-bridge-lab.html>`. Save it anywhere and double-click it. It opens in your web browser with the whole window for the app, needs no installation and works offline. The button *Download stand-alone app* in the app above saves the same file with your current model in it, so you can carry on working outside the book. Save your work with *Save case file*; the stand-alone app does not remember it when you close the window.

### The Python version

The same calculation is written out in Python with comments on every step: {download}`thermal_bridge.py <code/thermal_bridge.py>`. It needs numpy, scipy and matplotlib.

```bash
python thermal_bridge.py                       # the two examples, with plots
python thermal_bridge.py my-detail.json        # a case file saved from the app
python thermal_bridge.py --validate            # 1D check against the hand calculation
```

The two examples are also available as case files to open in the app: {download}`thermal-bridge-corner.json <code/thermal-bridge-corner.json>` and {download}`thermal-bridge-stud.json <code/thermal-bridge-stud.json>`. A case file holds the materials with their $\lambda$, the rectangles in drawing order, the named boundary conditions, the boundary edges and the mesh settings, with all coordinates in metres.

### Worked example: an external wall corner

The corner in the app is a 200 mm concrete wall with 200 mm mineral wool on the outside, seen in plan. The room is in the inner corner. The flanking walls are cut 1.0 m from the inside corner and the cut planes are adiabatic. Inside 20 °C with $R_{si} = 0.13$ m²K/W, outside 0 °C with $R_{se} = 0.04$ m²K/W.

The U-value of the flanking walls is

```{math}
U = \frac{1}{0.13 + \frac{0.2}{1.7} + \frac{0.2}{0.037} + 0.04} = 0.176 \text{ W/(m}^2\text{K)}
```

The 2D calculation gives $\Phi = 8.68$ W/m, so $L_{2D} = 8.68 / 20 = 0.434$ W/(m·K). Refining the mesh from 2 mm to 0.5 mm next to the interfaces changes the result by less than 0.001 W/(m·K).

- With **inside dimensions** each flanking wall is 1.0 m long: $\psi_i = 0.434 - 2 \cdot 1.0 \cdot 0.176 = +0.083$ W/(m·K).
- With **outside dimensions** each flanking wall is 1.4 m long: $\psi_e = 0.434 - 2 \cdot 1.4 \cdot 0.176 = -0.058$ W/(m·K).

The negative value on outside dimensions does not mean that the corner gains heat. It means that the outside areas already count more heat loss than the corner really has.

The lowest inside surface temperature, in the corner, is 19.05 °C with $R_{si} = 0.13$ m²K/W. For the mould assessment with $R_{si} = 0.25$ m²K/W it is 18.47 °C, so $f_{Rsi} = 0.92$. With the insulation on the outside, the corner is warm.

The second example, *Steel stud in wall*, is a light steel-frame wall with a 1 mm steel C-profile through 200 mm of mineral wool. The stud adds $\psi = 0.074$ W/(m·K) per stud, which with a stud every 0.6 m is 0.12 W/(m²K) on top of the U-value of 0.165 W/(m²K) of the insulated wall between the studs. The lowest inside surface temperature over the stud gives $f_{Rsi} = 0.79$ with $R_{si} = 0.25$ m²K/W. The same profile in a material with $\lambda = 0.13$ W/(m·K), as timber, gives $\psi \approx 0$.

### Exercises

1. Open the corner example. Move the insulation to the inside of the concrete: draw the mineral wool on the room side and the concrete outside it, and draw the boundary edges again. Compare $\psi_i$, $\psi_e$ and $f_{Rsi}$ with the outside-insulated corner. Which one would you build, and why?
2. Add a second inside boundary condition with $R_{si} = 0.25$ m²K/W and draw it only in the corner, 0.2 m along each wall. How much does the corner surface temperature drop?
3. Open the steel stud example. Find how thick an external insulation layer outside the studs must be before the stud's $\psi$ is halved.
4. Make the mesh coarser and finer for one of your models. How small must the cells next to the interfaces be before $L_{2D}$ is stable to three digits?
5. Draw a concrete balcony slab through an insulated wall, with and without a thermal break, and compare $\psi$ and $f_{Rsi}$.

### Limitations

The app and the script are teaching tools, and their results must be checked before they are used for design. The geometry is made of rectangles only, the calculation is steady-state and two-dimensional, and point thermal bridges are not included. Air cavities, which need an equivalent conductivity, have to be entered as a material. Validated thermal bridge programs follow ISO 10211, which includes reference cases for checking the software {cite:p}`iso10211`.

## Airtightness

:::{admonition} To be written
:class: dropdown

Infiltration heat loss, the airtight layer and its continuity at joints, blower door test and $q_{50}$, and what the Danish Building Regulations require.
:::

## Moisture in the envelope

:::{admonition} To be written
:class: dropdown

Vapour diffusion and the position of the vapour barrier, surface condensation and mould risk with $f_{Rsi}$ {cite:p}`iso13788`, and drying out of built-in moisture.
:::
