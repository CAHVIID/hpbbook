# Appendix B: Room CFD model

:::{warning} Under revision
This appendix was not verified, needs rework and will change substantially.
:::

This appendix documents a small 2D computational fluid dynamics (CFD) model of a room section. It is used in Part D to show how the placement of an opening, the supply temperature and the airflow decide whether ventilative cooling gives draught at the feet. The model is made for comparing cases and seeing the physics. It does not give design values.

The model exists in two versions that give the same results:


- {download}`room_cfd.py <code/room_cfd.py>` is the reference version in Python, with plotting functions in {download}`room_cfd_plots.py <code/room_cfd_plots.py>` and the figures of this appendix in {download}`cfd_examples.py <code/cfd_examples.py>`.
- {download}`room-cfd.mjs <code/room-cfd.mjs>` is the same solver in JavaScript, which runs as the app.

## The app

**[Open the room CFD app in a new tab](code/room-cfd.html)**. It runs in your browser and needs no installation. {numref}`fig-room-cfd-app` shows it after a run with the default inputs.

:::{figure} figures/appendix-cfd/room-cfd-app.*
:label: fig-room-cfd-app
:alt: Screenshot of the room CFD app. Inputs for the room depth, ceiling height and heat source position, the supply opening, supply temperature, air change rate, room temperature, mesh, advection scheme and turbulence model on the left. On the right, the temperature field and velocity arrows in the room section, an isoline slider beside the colour bar, key results for floor speed, ISO 7730 draught rate, PMV, ankle draught and exhaust temperature, and charts of the conditions at ankle height and of the convergence.
:width: 100%

The room CFD app after a run with the default inputs: a window from 0.9 to 2.1 m, 16 °C supply air and 6 air changes per hour. Open the app to change the inputs.
:::

The app starts a run when it opens. A run simulates 30 minutes of real time and takes under a minute in a browser. The section view shows the instantaneous field while the simulation runs and the time-averaged field when it finishes. Changing a setting starts a new run.

Under Room you can change the depth of the room from the facade (3–10 m) and the ceiling height (2.4–4 m). A third slider moves the 0.4 m wide block of heat gains along the floor. The exhaust slot stays 0.1–0.2 m below the ceiling, and the cells keep the size set under Mesh. The slider beside the colour bar draws one isoline on the section, for example the 0.15 m/s air speed or the 20 % draught rate. Each of the three views keeps its own value.

The app is a single HTML file, {download}`room-cfd.html <code/room-cfd.html>`. Save it anywhere and double-click it to use it offline.

## The room and the cases

The model is a vertical section through a room 5 m deep and 2.5 m high. The room is 4 m wide, which is only used to turn the airflow and the heat gains into values per metre of width. The supply opening sits in the facade at x = 0 and the exhaust is a 0.1 m slot high in the back wall, at 2.3–2.4 m.

The heat gains (people, equipment and sun-heated surfaces lumped together) are a heat source in a block 0.4 m wide and 1.2 m high in the middle of the room. Their size is set so that the well-mixed room temperature is the same in every case:

$$
\Phi = \rho \, c_p \, q_v \, (T_{room} - T_{supply})
$$

A colder supply then means more cooling, which is what a designer compares. If the gains were kept fixed instead, a colder supply would only lower the whole temperature field and the flow pattern would not change, because buoyancy depends on temperature differences and not on the temperature level.

## Equations

The air is treated as incompressible, with buoyancy from the Boussinesq approximation: the density is constant except in the gravity term, where it varies with temperature through the thermal expansion coefficient $\beta = 1/T_{ref}$ (ideal gas, $T_{ref}$ in kelvin). For the velocity $\mathbf{u} = (u, v)$, the pressure $p$ and the temperature $T$:

$$
\nabla \cdot \mathbf{u} = 0
$$

$$
\frac{\partial \mathbf{u}}{\partial t} + (\mathbf{u} \cdot \nabla)\mathbf{u} = -\frac{1}{\rho}\nabla p + \nabla \cdot \left[ (\nu + \nu_t) \nabla \mathbf{u} \right] + g \beta (T - T_{ref}) \, \mathbf{e}_y
$$

$$
\frac{\partial T}{\partial t} + \nabla \cdot (\mathbf{u} T) = \nabla \cdot \left[ \frac{\nu_t}{Pr_t} \nabla T \right] + \frac{S}{\rho c_p}
$$

Here $\nu = 1.5 \cdot 10^{-5}$ m²/s is the molecular viscosity of air, $\nu_t$ the eddy viscosity from the turbulence model, $Pr_t = 0.85$ the turbulent Prandtl number and $S$ the heat source in W/m³. The temperature equation is in conservative (flux) form, so the energy balance of the room closes exactly.

## Turbulence

The flow in a ventilated room is turbulent, and the model does not resolve the eddies. Instead it adds an eddy viscosity $\nu_t$ that represents the mixing they cause. Three options are available.

**k-ε (default).** The standard two-equation model of {cite:t}`launder1974`. Two extra transport equations carry the turbulent kinetic energy $k$ and its dissipation rate $\varepsilon$ through the room, and the eddy viscosity follows from them:

$$
\nu_t = C_\mu \frac{k^2}{\varepsilon}, \qquad
\frac{Dk}{Dt} = \nabla \cdot \left[ \left(\nu + \frac{\nu_t}{\sigma_k}\right) \nabla k \right] + P_k + G_b - \varepsilon, \qquad
\frac{D\varepsilon}{Dt} = \nabla \cdot \left[ \left(\nu + \frac{\nu_t}{\sigma_\varepsilon}\right) \nabla \varepsilon \right] + C_1 \frac{\varepsilon}{k} \left(P_k + G_b^+\right) - C_2 \frac{\varepsilon^2}{k}
$$

$P_k = \nu_t \left[ 2 (\partial u / \partial x)^2 + 2 (\partial v / \partial y)^2 + (\partial u / \partial y + \partial v / \partial x)^2 \right]$ is the production by shear and $G_b = -g \beta (\nu_t / Pr_t) \, \partial T / \partial y$ the production by buoyancy, which is negative in a stable layer and damps the turbulence there. The constants are the standard ones: $C_\mu = 0.09$, $C_1 = 1.44$, $C_2 = 1.92$, $\sigma_k = 1.0$ and $\sigma_\varepsilon = 1.3$. The grid is too coarse to resolve the thin layer next to a wall, so the first cell uses wall functions: the wall shear stress follows the logarithmic law of the wall, and $\varepsilon$ in that cell is set from the local equilibrium $\varepsilon = C_\mu^{3/4} k^{3/2} / (\kappa \, y_p)$. The supply air carries $k = 1.5 (Tu_{in} U)^2$ with $Tu_{in} = 4$ % and $\varepsilon = k^{3/2} / (0.1 \, h_{open})$, as in the IEA Annex 20 test case {cite:p}`nielsen1990`. This turbulence model is the only one of the three implemented models that passes that test (see *Verification*).

**Chen & Xu.** A zero-equation model developed for indoor air {cite:p}`chen1998`:

$$
\nu_t = 0.03874 \, V \, \ell
$$

with $V$ the local mean speed and $\ell$ the distance to the nearest wall. It gives little mixing near walls and in still air, and more mixing in the jet.

**Constant.** One eddy viscosity everywhere, by default $\nu_t = 0.002$ m²/s, which is about 130 times the molecular value.

Chen & Xu and the constant viscosity models are implemented for comparison, because they show what a turbulence model do.

## Numerical method

**Grid.** The section is divided into equal rectangular cells, 100 × 50 by default in Python (cells of 5 cm) and 60 × 30 in the app. The grid is staggered (a MAC grid, {cite:t}`harlow1965`): the pressure and the temperature sit in the cell centres, $u$ on the vertical cell faces and $v$ on the horizontal faces. This arrangement couples pressure and velocity tightly and avoids the checkerboard pressure oscillations that a collocated grid suffers from.

**Time stepping.** The model marches in time with the projection method of {cite:t}`chorin1968`. Each time step has three parts:

1. Advance the velocity without the pressure gradient, using the advection, diffusion and buoyancy terms. This gives an intermediate velocity $\mathbf{u}^*$ that does not yet satisfy continuity.
2. Solve a Poisson equation for the pressure, $\nabla^2 p = \rho \, \nabla \cdot \mathbf{u}^* / \Delta t$. The matrix depends only on the grid and the boundary types, so it is factorised once before the run (sparse LU in Python, banded Cholesky in JavaScript), and each step only needs a back-substitution.
3. Correct the velocity with the pressure gradient, $\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t \, \nabla p / \rho$. The corrected field satisfies continuity to machine precision.

The temperature, and with k-ε model also $k$ and $\varepsilon$, are then advanced with the new velocity. The sink terms of $k$ and $\varepsilon$ are treated implicitly so that both stay positive, and $k$ and $\varepsilon$ use upwind advection. The time step is set at every step from the stability limits of the explicit scheme:

$$
\Delta t = \min \left( C \frac{\Delta x}{|u|_{max}}, \; 0.2 \frac{\Delta x^2}{\nu_{max}}, \; 0.5 \text{ s} \right)
$$

with the Courant number $C = 0.25$ for the TVD scheme and $0.4$ for upwind. With 5 cm cells and 0.4 m/s jets this gives time steps of about 0.03 s, so a 30-minute run takes about 50,000 steps.

**Why march in time.** A steady solver (like SIMPLE in commercial codes) would be faster when the flow has a steady state, but cold air from a window falling into a warm room often flaps and wanders and has none. A time-marching solver handles both cases: it settles if the flow is steady, and it averages if it is not. The fields used for comfort are averaged over the last 10 minutes of the run.

**Advection.** The advection terms decide how much the solution is smeared out. Two schemes are available.

- *Upwind* takes each face value from the cell the flow comes from. It is first order and never oscillates, but it adds numerical diffusion of about $|u| \Delta x / 2$. In a 0.3 m/s jet on a 5 cm grid that is 0.0075 m²/s, which is larger than the eddy viscosity itself. The results then depend on the grid.
- *TVD* (total variation diminishing, the default) adds a limited correction to the upwind value, using the van Leer limiter {cite:p}`vanleer1974`. Where the field is smooth the scheme is second order, and at peaks and steps it falls back to upwind, so it does not create wiggles. For a face between cells $i$ and $i+1$ with flow in the positive direction:

$$
\phi_{i+1/2} = \phi_i + \tfrac{1}{2} \, \psi(r) \, (\phi_{i+1} - \phi_i), \qquad r = \frac{\phi_i - \phi_{i-1}}{\phi_{i+1} - \phi_i}, \qquad \psi(r) = \frac{r + |r|}{1 + |r|}
$$

## Boundary conditions

| Boundary | Velocity | Pressure | Temp. | $k$, $\varepsilon$ (k-ε) |
|---|---|---|---|---|
| Walls, floor, ceiling | No slip, $u = v = 0$, wall functions with k-ε | Zero gradient | Adiabatic | Zero flux for $k$, $\varepsilon$ from the wall function |
| Supply opening | Velocity inlet, $U = q_v / (W \, h_{open})$ normal to the wall | Zero gradient | $T_{supply}$ | $Tu_{in} = 4$ %, length scale $0.1 \, h_{open}$ |
| Exhaust | Zero gradient | Pressure outlet, $p = 0$ | Zero gradient | Zero gradient |

The inlet speed follows from the airflow, the room width and the opening height. A large opening therefore gives a low inlet speed: at 6 air changes per hour a 1.2 m high window gives only 0.02 m/s, and the flow into the room is then driven by buoyancy alone.

## Comfort at the feet

Draught is evaluated in a simplified occupied zone that starts 0.6 m from the facade and the back wall and reaches 1.8 m up. The model reports the highest mean air speed at ankle height (0.1 m) and two draught indices at that point.

**ISO 7730 draught rate** {cite:p}`iso7730`, from {cite:t}`fanger1988`, with the turbulence intensity set to $Tu = 40$ %:

$$
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37 \, v \, Tu + 3.14)
$$

The model was derived from sensations at the back of the neck, so it is conservative at the feet.

**ASHRAE 55 ankle draught** {cite:p}`ashrae55`, from {cite:t}`liu2017`, which also depends on how warm the person feels overall:

$$
PPD_{AD} = \frac{e^{z}}{1 + e^{z}} \cdot 100, \qquad z = -2.58 + 3.05 \, v_{ankle} - 1.06 \, TS
$$

$TS$ is the whole-body thermal sensation, taken as the PMV of the occupied zone (mean air temperature and speed, $t_r = t_a$, 1.2 met, 0.5 clo, 50 % RH). Both limits are 20 %. For ASHRAE 55 this is the same as $v_{ankle} < 0.35 \, TS + 0.39$ m/s: a room that feels slightly warm tolerates more air at the feet, and a room that feels cool tolerates less.

## Verification

**Energy balance.** At steady state the heat leaving through the exhaust must equal the gains. In all runs the exhaust temperature is within 0.15 K of the well-mixed value.

**Continuity.** After the projection, the largest divergence in any cell stays at about $10^{-15}$ s⁻¹, which is rounding error.

**Python and JavaScript.** On the same case the two versions agree to 12 significant digits or better, with all three turbulence models.

**Grid dependence.** The highest floor speed for a 0.1 m slot at 2.3–2.4 m (16 °C supply, 6 ACH, k-ε) on four grids, from {download}`cfd_grid.py <code/cfd_grid.py>`:

| Grid | Cell size | Upwind | TVD |
|---|---|---|---|
| 60 × 30 | 8.3 cm | 0.27 m/s | 0.36 m/s |
| 100 × 50 | 5.0 cm | 0.31 m/s | 0.39 m/s |
| 150 × 75 | 3.3 cm | 0.34 m/s | 0.41 m/s |
| 200 × 100 | 2.5 cm | 0.36 m/s | 0.42 m/s |

With TVD the speed converges towards about 0.42 m/s, and the default grid is within about 7 % of that. With upwind it keeps rising, because the numerical diffusion shrinks with the cell size. The app uses a coarser grid than Python to keep runs short, so its floor speeds are somewhat lower.

**Validation against measurements.** The IEA Annex 20 two-dimensional test case {cite:p}`nielsen1990` is an isothermal room 9 m long and 3 m high. Air enters through a 0.168 m slot under the ceiling at 0.455 m/s (a Reynolds number of 5000 based on the slot height) and leaves through a 0.48 m opening at the floor of the opposite wall. Laser-Doppler measurements of the mean velocity are given on two vertical lines (x = H and x = 2H) and two horizontal lines, h/2 below the ceiling and h/2 above the floor. The report and the data are in the book's `background/airflow` folder, and {download}`cfd_annex20.py <code/cfd_annex20.py>` runs the case on a 321 × 107 grid.

The measured flow is one large eddy that fills the room: the supply air stays on the ceiling as a wall jet almost to the far wall, turns down, and returns along the floor ({numref}`fig-cfd-annex20-fields`). With k-ε the model reproduces this pattern and the measured profiles ({numref}`fig-cfd-annex20`). The root-mean-square difference is 0.05–0.06 $u_0$ on three of the lines and 0.12 $u_0$ on the line under the ceiling, where the model lets the jet turn down slightly early. With Chen & Xu the jet leaves the ceiling about halfway into the room and splits the room into three eddies, and the difference is 0.11–0.41 $u_0$. The measured flow is not perfectly two-dimensional: the net flow through the line at x = 2H is about 37 % below the supply flow, so a difference of a few per cent of $u_0$ is as close as a 2D model can get.

:::{figure} figures/appendix-cfd/annex20-fields.*
:label: fig-cfd-annex20-fields
:width: 85%

Annex 20 test room: time-averaged speed and streamlines with k-ε (top) and Chen & Xu (bottom).
:::

:::{figure} figures/appendix-cfd/annex20-profiles.*
:label: fig-cfd-annex20
:width: 100%

Annex 20 test room: horizontal velocity $u/u_0$ on the four measuring lines, model against the laser-Doppler measurements reported by {cite:t}`nielsen1990`.
:::

**Convergence history.** The run records the rate of change of $u$, $v$ and $T$, the continuity residual, the energy imbalance and two monitor points ({numref}`fig-cfd-convergence`). With `run(case, live=True)` the same four panels are drawn in a window while the run goes on.

:::{figure} figures/appendix-cfd/convergence-example.*
:label: fig-cfd-convergence
:width: 100%

Convergence of the window case at 16 °C supply with k-ε. The flow never becomes steady: the cold stream along the floor pulses with a period of about one minute, so the rates of change level off instead of falling. The exhaust temperature settles after about 20 minutes, two time constants of the room air ($2/n$ at 6 ACH), which is why the comfort values are averaged over the last 10 minutes.
:::

## Example: window or top hatch

{numref}`fig-cfd-window-hatch` compares a normal window (sill at 0.9 m, head at 2.1 m) with a top hatch (2.2–2.4 m), both fully open, at 6 air changes per hour. The gains are set for a well-mixed room at 26 °C, and the supply air is 10 K colder, at 16 °C, as on a summer night.

:::{figure} figures/appendix-cfd/window-vs-hatch.*
:label: fig-cfd-window-hatch
:width: 100%

Time-averaged temperature and streamlines for a window and a top hatch at 16 °C supply and 6 air changes per hour, with gains for a well-mixed 26 °C. Yellow and orange contours mark 0.15 and 0.25 m/s. The dotted box holds the heat gains.
:::

From the window the cold air falls 0.9 m along the facade and runs along the floor. It slows down about 1 m into the room but leaves a cool layer of about 22 °C over the floor ({numref}`fig-cfd-floor-line`).

The flow from the top hatch does not stay on the ceiling. The opening is low and narrow, so the inflow is fast and the Archimedes number is large ({eq}`eq-sh-ar`), and the jet falls along the facade from 2.2 m. It gains more speed on the way down than the window flow and reaches the floor at up to 0.39 m/s against 0.29 m/s. The fast floor stream also reaches further into the room: the ISO 7730 draught rate is above 20 % up to about 1.6 m from the facade, against about 0.9 m for the window. The air at the floor is 1.5–2 K warmer than with the window, because the falling jet mixes with room air on its way down.

Neither opening meets ISO 7730 near the facade at this supply temperature, while both stay below the ASHRAE 55 ankle limit, at 15 % for the window and 17 % for the hatch. The hatch in the model is a plain slot in the wall. A real bottom-hung hatch deflects the inflow upwards, which helps it attach to the ceiling ([](d5-window-openings.md)), so the result is a worst case for the hatch.

:::{figure} figures/appendix-cfd/window-vs-hatch-floor-line.*
:label: fig-cfd-floor-line
:width: 80%

Air speed, temperature, ISO 7730 draught rate and ASHRAE 55 ankle draught at 0.1 m above the floor, 16 °C supply. Grey: outside the occupied zone.
:::

## Using the Python code

A case is a `Case` object. Every field has a default, so only the differences need to be given:

```python
from room_cfd import Case, Opening, HeatBlock, run, occupied_zone
import room_cfd_plots as plots

c = Case(inlet=Opening("left", 0.9, 2.1), T_in=16.0, ach=6)
c.heat = [HeatBlock(2.3, 2.7, 0.0, 1.2, 1.2 * 1005 * c.q * (26 - c.T_in) / c.W)]
res = run(c, live=True)          # live=True draws the convergence monitor while it runs
print(occupied_zone(res))        # floor speed, DR, TS, PPD_AD and the ankle speed limit
plots.floor_line(res).savefig("floor.png")
```

| `Case` field | Default | Meaning |
|---|---|---|
| `L`, `H`, `W` | 5, 2.5, 4 m | Room depth, height and width |
| `nx`, `ny` | 100, 50 | Number of cells |
| `ach` | 6 h⁻¹ | Air change rate |
| `T_in` | 18 °C | Supply temperature |
| `T_room0` | well-mixed value | Initial room temperature |
| `inlet`, `outlet` | 0.1–0.3 m left, 2.2–2.4 m right | `Opening(side, start, end)`, side `"left"`, `"right"` or `"top"` |
| `heat` | none | List of `HeatBlock(x0, x1, y0, y1, power)`, power in W per metre of width |
| `floor_flux` | none | List of `FloorFlux(x0, x1, power)`, for a sun patch on the floor |
| `turbulence` | `"k-epsilon"` | or `"chen-xu"`, or `"constant"` with `nu_t` |
| `Tu_in` | 0.04 | Turbulence intensity of the supply air (k-ε) |
| `advection` | `"tvd"` | or `"upwind"` |
| `t_end`, `t_avg` | 900 s, 300 s | Simulated time and averaging window at the end |

`run` returns a dictionary with the grid (`x`, `y`), the averaged fields (`u`, `v`, `T`, `speed`, `nu_t`), the inlet speed, the energy check (`T_out` against `T_out_expected`) and the convergence `history`. The plotting module has four functions: `profiles` (vertical profiles at chosen distances), `floor_line` (the line at ankle height), `dr_map` (draught rate over the section) and `convergence`. Each takes one result or a dictionary of labelled results.

## Limitations

- **2D.** The opening runs the full width of the room. A jet from a slot decays as $1/\sqrt{x}$, slower than a jet from a real window, which decays as $1/x$, so speeds far from the opening are overestimated.
- **Inlet only.** The supply opening only lets air in. A real wide-open window also lets warm air out at the top, and that two-way flow is not modelled.
- **Turbulence.** The standard k-ε model with wall functions reproduces the main flow pattern of a ventilated room, but it is known to be less accurate for flows that separate or are strongly stratified. The comfort indices use a fixed $Tu = 40$ % rather than the modelled turbulence.
- **No radiation and adiabatic walls.** Surfaces do not exchange heat with the air or with each other, and there is no cold downdraught from glazing.

Use the model to compare openings, temperatures and airflows, and to see why they behave as they do. For design values, use a validated 3D CFD code or measurements.
