# Room CFD model

:::{warning} Under revision
This appendix is being reworked and may change substantially.
:::

This appendix documents a small 2D computational fluid dynamics (CFD) model of a room section. It is used in Part D to show how the placement of an opening, the supply temperature and the airflow decide whether ventilative cooling gives draught at the feet. The model is made for comparing cases and seeing the physics. It does not give design values.

The model exists in two versions that give the same results:

- {download}`room_cfd.py <code/room_cfd.py>` is the reference version in Python, with plotting functions in {download}`room_cfd_plots.py <code/room_cfd_plots.py>` and the figures of this appendix in {download}`cfd_examples.py <code/cfd_examples.py>`.
- {download}`room-cfd.mjs <code/room-cfd.mjs>` is the same solver in JavaScript, which runs as the app below.

## The app

```{anywidget} code/room-cfd.mjs
{}
```

Press *Run* to start. A run simulates 30 minutes of real time and takes about half a minute in a browser. The section view shows the instantaneous field while the simulation runs and the time-averaged field when it finishes. Changing a setting starts a new run.

The app also runs on its own as a single HTML file: {download}`room-cfd.html <code/room-cfd.html>`. Save it anywhere and double-click it. It opens in a web browser, needs no installation and works offline.

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

The flow in a ventilated room is turbulent, and the model does not resolve the eddies. Instead it adds an eddy viscosity $\nu_t$ that represents the mixing they cause. Two options are available.

**Chen & Xu (default).** A zero-equation model developed for indoor air {cite:p}`chen1998`:

$$
\nu_t = 0.03874 \, V \, \ell
$$

with $V$ the local mean speed and $\ell$ the distance to the nearest wall. It gives little mixing near walls and in still air, and more mixing in the jet.

**Constant.** One eddy viscosity everywhere, by default $\nu_t = 0.002$ m²/s, which is about 130 times the molecular value. It is useful for showing students what the turbulence model does.

## Numerical method

**Grid.** The section is divided into equal rectangular cells, 100 × 50 by default in Python (cells of 5 cm) and 60 × 30 in the app. The grid is staggered (a MAC grid, {cite:t}`harlow1965`): the pressure and the temperature sit in the cell centres, $u$ on the vertical cell faces and $v$ on the horizontal faces. This arrangement couples pressure and velocity tightly and avoids the checkerboard pressure oscillations that a collocated grid suffers from.

**Time stepping.** The model marches in time with the projection method of {cite:t}`chorin1968`. Each time step has three parts:

1. Advance the velocity without the pressure gradient, using the advection, diffusion and buoyancy terms. This gives an intermediate velocity $\mathbf{u}^*$ that does not yet satisfy continuity.
2. Solve a Poisson equation for the pressure, $\nabla^2 p = \rho \, \nabla \cdot \mathbf{u}^* / \Delta t$. The matrix depends only on the grid and the boundary types, so it is factorised once before the run (sparse LU in Python, banded Cholesky in JavaScript), and each step only needs a back-substitution.
3. Correct the velocity with the pressure gradient, $\mathbf{u}^{n+1} = \mathbf{u}^* - \Delta t \, \nabla p / \rho$. The corrected field satisfies continuity to machine precision.

The temperature is then advanced with the new velocity. The time step is set at every step from the stability limits of the explicit scheme:

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

| Boundary | Velocity | Pressure | Temperature |
|---|---|---|---|
| Walls, floor, ceiling | No slip, $u = v = 0$ | Zero gradient | Adiabatic |
| Supply opening | Velocity inlet, $U = q_v / (W \, h_{open})$ normal to the wall | Zero gradient | $T_{supply}$ |
| Exhaust | Zero gradient | Pressure outlet, $p = 0$ | Zero gradient |

The inlet speed follows from the airflow, the room width and the opening height. A large opening therefore gives a low inlet speed: at 6 air changes per hour a 1.2 m high window gives only 0.02 m/s, and the flow into the room is then driven by buoyancy alone.

## Comfort at the feet

Draught is evaluated in a simplified occupied zone that starts 0.6 m from the facade and the back wall and reaches 1.8 m up. The model reports the highest mean air speed at ankle height (0.1 m) and two draught indices at that point.

**ISO 7730 draught rate** {cite:p}`iso7730`, from {cite:t}`fanger1988`, with the turbulence intensity set to $Tu = 40$ %:

$$
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37 \, v \, Tu + 3.14)
$$

The model was derived from sensations at the back of the neck, so it is conservative at the feet. No correction factor is applied. A "feet factor" of 0.82 is found in some sources, but in {cite:t}`fanger1988` 0.82 is the correlation coefficient between predicted and measured dissatisfaction at the feet, not a scaling factor.

**ASHRAE 55 ankle draught** {cite:p}`ashrae55`, from {cite:t}`liu2017`, which also depends on how warm the person feels overall:

$$
PPD_{AD} = \frac{e^{z}}{1 + e^{z}} \cdot 100, \qquad z = -2.58 + 3.05 \, v_{ankle} - 1.06 \, TS
$$

$TS$ is the whole-body thermal sensation, taken as the PMV of the occupied zone (mean air temperature and speed, $t_r = t_a$, 1.2 met, 0.5 clo, 50 % RH). Both limits are 20 %. For ASHRAE 55 this is the same as $v_{ankle} < 0.35 \, TS + 0.39$ m/s: a room that feels slightly warm tolerates more air at the feet, and a room that feels cool tolerates less.

## Verification

**Energy balance.** At steady state the heat leaving through the exhaust must equal the gains. In all runs the exhaust temperature is within 0.15 K of the well-mixed value.

**Continuity.** After the projection, the largest divergence in any cell stays at about $10^{-15}$ s⁻¹, which is rounding error.

**Python and JavaScript.** On the same case the two versions agree to 12 significant digits.

**Grid dependence.** The highest floor speed for a 0.1 m slot at 2.3–2.4 m (16 °C supply, 6 ACH) on four grids:

| Grid | Cell size | Upwind | TVD |
|---|---|---|---|
| 60 × 30 | 8.3 cm | 0.27 m/s | 0.31 m/s |
| 100 × 50 | 5.0 cm | 0.31 m/s | 0.35 m/s |
| 150 × 75 | 3.3 cm | 0.35 m/s | 0.38 m/s |
| 200 × 100 | 2.5 cm | | 0.39 m/s |

With TVD the speed converges towards about 0.40 m/s, and the default grid is within about 10 % of that. With upwind it keeps rising, because the numerical diffusion shrinks with the cell size. The app uses a coarser grid than Python to keep runs short, so its floor speeds are somewhat lower.

**Convergence history.** The run records the rate of change of $u$, $v$ and $T$, the continuity residual, the energy imbalance and two monitor points ({numref}`fig-cfd-convergence`). With `run(case, live=True)` the same four panels are drawn in a window while the run goes on.

:::{figure} figures/appendix-cfd/convergence-example.*
:label: fig-cfd-convergence
:width: 100%

Convergence of the window case at 16 °C supply. The flow flaps for the first minutes and then settles. Temperature settles last, because the room air takes about two time constants ($2/n$ = 20 minutes at 6 ACH) to reach its final temperature, which is why the average is taken over the last 10 minutes.
:::

## Example: window or balcony door

{numref}`fig-cfd-window-door` compares a normal window (sill at 0.9 m, head at 2.1 m) with a balcony door (floor to 2.1 m), both fully open, at 6 air changes per hour and with gains set for a well-mixed 26 °C.

:::{figure} figures/appendix-cfd/window-vs-door.*
:label: fig-cfd-window-door
:width: 100%

Time-averaged temperature and streamlines for a window and a balcony door at 16 °C and 22 °C supply. Yellow and orange contours mark 0.15 and 0.25 m/s. The dotted box holds the heat gains.
:::

In both cases the cold air falls along the facade and runs along the floor. From the window it falls 0.9 m before it reaches the floor and gains speed on the way, so the floor speed is higher. Through the door it enters at floor level and spreads as a cold layer that is slower but 1.5–2 K colder and reaches further into the room ({numref}`fig-cfd-floor-line`). The draught is worst within 1 m of the facade, where neither the window nor the door meets ISO 7730 at 16 °C supply.

:::{figure} figures/appendix-cfd/window-vs-door-floor-line.*
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
| `turbulence` | `"chen-xu"` | or `"constant"` with `nu_t` |
| `advection` | `"tvd"` | or `"upwind"` |
| `t_end`, `t_avg` | 900 s, 300 s | Simulated time and averaging window at the end |

`run` returns a dictionary with the grid (`x`, `y`), the averaged fields (`u`, `v`, `T`, `speed`, `nu_t`), the inlet speed, the energy check (`T_out` against `T_out_expected`) and the convergence `history`. The plotting module has four functions: `profiles` (vertical profiles at chosen distances), `floor_line` (the line at ankle height), `dr_map` (draught rate over the section) and `convergence`. Each takes one result or a dictionary of labelled results.

## Limitations

- **2D.** The opening runs the full width of the room. A jet from a slot decays as $1/\sqrt{x}$, slower than a jet from a real window, which decays as $1/x$, so speeds far from the opening are overestimated.
- **Inlet only.** The supply opening only lets air in. A real wide-open window also lets warm air out at the top, and that two-way flow is not modelled.
- **Turbulence.** The zero-equation model is calibrated for typical room flows. It is not reliable for the details of a separating jet or for the turbulence intensity, so ISO 7730 uses a fixed $Tu = 40$ %.
- **No radiation and adiabatic walls.** Surfaces do not exchange heat with the air or with each other, and there is no cold downdraught from glazing.

Use the model to compare openings, temperatures and airflows, and to see why they behave as they do. For design values, use a validated 3D CFD code or measurements.
