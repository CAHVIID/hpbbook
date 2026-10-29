# Appendix C: 3D room CFD model

:::{warning} Under revision
This appendix was not verified, needs rework and will change substantially.
:::

This appendix documents the 3D version of the room CFD model in [](appendix-room-cfd.md). The physics, the turbulence models, the advection schemes and the comfort indices are the same, and are only summarised here. The 3D model adds the room width: the side walls are real walls, and an opening can be narrower than the room, for example a window 1.2 m wide in a 4 m wide office. The model is made for comparing cases and seeing the physics. It does not give design values.

The model exists in three versions that give the same results:

- {download}`room_cfd_3d.py <code/room_cfd_3d.py>` is the reference version in Python (NumPy and SciPy).
- {download}`room_cfd_3d_numba.py <code/room_cfd_3d_numba.py>` is the same code with the time step compiled by Numba. It needs the `numba` package and runs about twice as fast.
- {download}`room_cfd_3d_gpu.mjs <code/room_cfd_3d_gpu.mjs>` is the same solver as WebGPU compute shaders, which runs as the app on the graphics card.

## The app

**[Open the 3D room CFD app in a new tab](code/room-cfd-3d.html)**. It runs in the browser on the graphics card and needs a browser with WebGPU: Chrome or Edge on Windows, macOS or ChromeOS, Safari 26 or later, or Firefox 141 or later on Windows. {numref}`fig-room-cfd-3d-app` shows it while a run is going.

:::{figure} figures/appendix-cfd-3d/room-cfd-3d-app.*
:label: fig-room-cfd-3d-app
:alt: Screenshot of the 3D room CFD app. Inputs for the room size, the window type, width, position and height, the heat source position and size, supply temperature, air change rate, room temperature, mesh, advection scheme and turbulence model on the left. On the right, a vertical section and a plan at ankle height with temperature, velocity arrows and an isoline set by a slider beside the colour bar, key results for floor speed, ISO 7730 draught rate, PMV, ankle draught, exhaust temperature and energy balance, and charts of the conditions at ankle height and of the convergence.
:width: 100%

The 3D room CFD app with a window 1.2 m wide, 0.9–2.1 m high, 16 °C supply air and 6 air changes per hour, on the coarse mesh a few seconds into a run. The heat source stands in the middle of the room.
:::

A run simulates 30 minutes and averages the last 10. Before a run the section and the plan show the empty room with the window, the exhaust and the heat source. During a run they show the instantaneous field while the simulation runs and the time-averaged field when it finishes. Three sliders move the long section across the width, the plan up through the room and the cross section (parallel to the facade) back through the room; a dashed line in each view shows where the other two cut, and two checkboxes hide these lines and the occupied zone. The slider beside the colour bar draws one isoline on all three views, for example the 0.15 m/s air speed or the 20 % draught rate; each of the three views keeps its own value. The draught panel shows the key results with two charts of the air speed, the ISO 7730 draught rate and the ASHRAE 55 ankle draught at ankle height: along x in the long section and along y in the cross section. The occupied zone (by default 0.6 m from all walls and 1.8 m high) can be resized, and a button draws the mesh on the three views. A convergence chart at the bottom, next to the exhaust temperature and the energy imbalance, shows the rates of change of velocity and temperature and the floor speed 1 m from the facade at the centre of the window.

The app is a single HTML file, {download}`room-cfd-3d.html <code/room-cfd-3d.html>`, with the solver inlined. Save it anywhere and double-click it to use it offline.

## The room and the cases

The room is by default 5 m deep (x), 4 m wide (y) and 2.5 m high (z), with the facade at x = 0. In the app the depth, width and height can be changed; the mesh is then set by the cell size (20, 10 or 5 cm), and the exhaust stays 0.1–0.2 m below the ceiling. The supply opening sits in the facade or the back wall and can have any width; it is centred unless `y0` and `y1` are given. The app offers the same opening types as the 2D app (a window, a balcony door, a top hatch and a low slot, plus a window across the full width), and the opening can be slid along the facade. The exhaust is in the back wall or the ceiling; in the app it sits in the back wall 0.1–0.2 m below the ceiling. A layout file can place inlets and exhausts anywhere on any wall (see below). The heat gains are a box standing on the floor. In the app it is by default 0.6 m deep, 0.8 m wide and 1.2 m high in the middle of the room, and it can be moved and resized, or placed by clicking in the plan; the Python examples use a box 0.4 m deep and 1.2 m high across the full width at x = 2.3–2.7 m. With a height of 0 it becomes a heated patch of floor (`FloorFlux`), which heats the air through the floor surface, as a sun patch does. The power is sized as in the 2D model so that the well-mixed room temperature is the same in every case:

$$
\Phi = \rho \, c_p \, q_v \, (T_{room} - T_{supply})
$$

## Layout file: several heat sources and furniture

Instead of the single heat source, a room can be furnished from a layout file, a plain text file with one box per line (see {download}`room-layout-office.csv <code/room-layout-office.csv>`):

```text
type, x0, x1, y0, y1, z0, z1, power_W
furniture, 1.0, 1.8, 0.4, 1.8, 0.72, 0.72, 0   # desk (thin table top)
heat, 2.0, 2.4, 0.9, 1.3, 0, 1.2, 100          # person, seated
furniture, 4.4, 4.8, 0.0, 1.2, 0, 2.0, 0       # bookshelf (solid box)
floor, 0.2, 1.6, 0.8, 3.2, 0, 0, 300           # sun patch on the floor
inlet, 0, 0, 1.4, 2.6, 0.9, 2.1, 0             # inlet in the facade (x = 0)
exhaust, 2.3, 2.7, 1.8, 2.2, 2.5, 2.5, 0       # exhaust in the ceiling (z = H)
```

The type is `heat` (a `HeatBlock`), `floor` (a `FloorFlux`; z is ignored), `furniture`, `inlet` or `exhaust`. An inlet or exhaust (a `Vent`) is a rectangle on any of the six walls, with zero size along the axis normal to that wall, at 0 or at the room size. Inlets in the file replace the window and exhausts replace the back-wall exhaust; with several inlets the airflow is shared in proportion to their area, at the same speed. Lines starting with `#` and the header are skipped. The same file is read by `read_layout` in Python and by the app, under Layout, which also has six examples: one heat source, a two-person office, a classroom, a meeting room, an open office with screens, and the two-person office of the MIT displacement ventilation experiment (Chen et al., 1998, Detailed experimental data of room airflow with displacement ventilation, Roomvent 98). The experiment is set up as in the paper: a 3.65 × 5.16 × 2.43 m room, a diffuser 0.5 m wide and 1.1 m high at the floor, 4 h⁻¹ at 17 °C and a 0.43 × 0.43 m exhaust in the ceiling centre; the diffuser and the exhaust are inlet and exhaust lines in the layout. The sizes and powers of the occupants, computers and lights are from the paper, but their positions and the furniture are approximate, because the paper shows them only in a figure. The warm window and walls of the test room are not modelled. With a layout the heat gains are the sum of the powers in the file, and the well-mixed room temperature follows from them.

Furniture is solid and adiabatic. A box takes the cells whose centres lie inside it: the faces of those cells are closed, so no air or heat passes, and the cells stay at the start temperature (grey in the app). A box must therefore be at least one cell thick. Furniture with zero size along one axis is a thin plate, such as a table top or a partition. It sits on the grid plane nearest to it and closes the cell faces in that plane, so it blocks the flow without taking up cells. On both sides of a plate, and on the faces of a box, the velocity parallel to the surface has no slip, with the log-law wall shear when k-ε is used.

## Equations and turbulence

The equations are those of [](appendix-room-cfd.md) with the third velocity component: continuity, momentum with Boussinesq buoyancy along z, and the energy equation in conservative form, for $\mathbf{u} = (u, v, w)$. The turbulence options are the same: standard k-ε with log-law wall functions on all six walls (default), Chen & Xu, or a constant eddy viscosity. In 3D the shear production of $k$ contains all nine velocity gradients:

$$
P_k = \nu_t \left[ 2 \sum_i \left(\frac{\partial u_i}{\partial x_i}\right)^2 + \sum_{i<j} \left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)^2 \right]
$$

## Numerical method

**Grid and time stepping.** As in 2D: a staggered (MAC) grid with $u$, $v$ and $w$ on the cell faces, the projection method with an explicit time step, and TVD (van Leer) or upwind advection. The default grid is 50 × 40 × 25 cells (10 cm), which is 50,000 cells against 5,000 in the 2D section.

**Pressure.** The pressure equation is the costly part in 3D. A direct solver, as used in 2D, does not scale: on 50,000 cells the LU factor has about 27 million entries. The 3D model therefore solves the pressure equation iteratively, with conjugate gradients preconditioned by one multigrid V-cycle {cite:p}`trottenberg2001`. The cells are grouped 2 × 2 × 2 into coarser grids until fewer than a few hundred cells are left, the error is smoothed by weighted Jacobi sweeps on each grid, and the coarsest grid is solved directly. Each time step starts from the pressure of the previous step and stops when the residual has fallen by a factor $10^6$, which changes the temperatures by less than $10^{-4}$ K compared with $10^{-8}$. The number of iterations hardly grows with the number of cells, typically 3–10 per time step.

**Numba.** {download}`room_cfd_3d_numba.py <code/room_cfd_3d_numba.py>` turns each stage of the time step into one compiled loop over the cells, run in parallel on all processor cores. The pressure solve still takes about 80 % of the run time, so the gain is a factor of about 2 (see the run times below).

**WebGPU.** {download}`room_cfd_3d_gpu.mjs <code/room_cfd_3d_gpu.mjs>` runs the whole time loop on the graphics card, including the time step and the dot products of the pressure solver, so data only comes back to the page for plotting. The differences from the Python version are:

- Single precision, because WGSL has no double precision. Temperature is stored as the deviation from the start value to keep the small changes per time step.
- The multigrid uses plain aggregation with 7-point coarse operators (half the Galerkin product), so every grid level is a simple stencil that runs well on a GPU, and an exact solve on the coarsest grid of at most 128 cells.

## Boundary conditions

| Boundary | Velocity | Pressure | Temp. | $k$, $\varepsilon$ (k-ε) |
|---|---|---|---|---|
| Walls, side walls, floor, ceiling | No slip, wall functions with k-ε | Zero gradient | Adiabatic | Zero flux for $k$, $\varepsilon$ from the wall function |
| Supply opening (any wall) | Velocity inlet, $U = q_v / A_{open}$ | Zero gradient | $T_{supply}$ | $Tu_{in} = 4$ %, length scale $0.1 \, h_{open}$ |
| Exhaust (any wall) | Zero gradient | $p = 0$ | Zero gradient | Zero gradient |
| Furniture (boxes and thin plates) | No slip, log-law shear with k-ε | Zero gradient | Adiabatic | Zero flux |

The opening area $A_{open}$ counts the cell faces whose centres lie inside the opening, so an opening must cover at least one cell face in both directions.

## Verification

**Python, Numba and WebGPU.** On the same case room_cfd_3d.py and room_cfd_3d_numba.py agree to about $10^{-13}$. The WebGPU version agrees with the Numba version to about $10^{-6}$ of the range of each field after 30 s of simulated time, which is the precision of single-precision arithmetic. The same holds with furniture: on a case with two heat sources, two thin plates and a box, Numba agrees with Python to $10^{-13}$ and WebGPU to about $10^{-5}$ of the range.

**2D and 3D.** With a window across the full width the 3D flow is close to two-dimensional, and the 3D model gives the same highest floor speed as the 2D model on the same x-z grid (0.235 m/s for both).

**Energy balance.** The time-averaged exhaust temperature is within 0.11 K of the well-mixed value, and the energy imbalance at the end of the runs is below 1 %.

**Validation against measurements.** The IEA Annex 20 room {cite:p}`nielsen1990` was run in 3D with the slot across the full width ($W = H$ = 3 m assumed) on 72 × 18 × 36 cells. The flow is not two-dimensional: the net flow through the line x = H is 0.13 of the supply flow at mid-width and up to 1.6 near the side walls, so the return flow is pushed to the sides. On this coarse grid the errors are 0.07–0.15 $u_0$ on three of the four measuring lines and 0.30 $u_0$ on the line under the ceiling, close to the 2D model on the same x-z grid (0.05–0.30 $u_0$). The accuracy is limited by the grid, not by the third dimension. The fine grid that gives 0.05–0.12 $u_0$ in 2D (321 × 107) would need about 3 million cells in 3D.

:::{figure} figures/appendix-cfd-3d/annex20-3d-profiles.*
:label: fig-cfd-3d-annex20
:width: 100%

Annex 20 test room in 3D: horizontal velocity $u/u_0$ on the four measuring lines at mid-width and at a quarter of the width, the 2D model on the same x-z grid, and the laser-Doppler measurements reported by {cite:t}`nielsen1990`. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/cfd3d_annex20.py)
:::

## Example: window width

{numref}`fig-cfd-3d-window-width` compares a window across the full 4 m width with a window 1.2 m wide, both 0.9–2.1 m high, at 16 °C supply and 6 air changes per hour, with gains for a well-mixed 26 °C. The airflow is the same, so the narrow window has 3.3 times the inlet speed (0.058 against 0.017 m/s).

:::{figure} figures/appendix-cfd-3d/window-width-ankle.*
:label: fig-cfd-3d-window-width
:width: 100%

Mean air speed and streamlines at 0.1 m above the floor for a full-width window and a window 1.2 m wide, 16 °C supply and 6 air changes per hour. Yellow and orange contours mark 0.15 and 0.25 m/s; dashed: the occupied zone. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/cfd3d_window.py)
:::

| Window | Mesh | Highest floor speed | ISO 7730 DR | ASHRAE 55 $PPD_{AD}$ |
|---|---|---|---|---|
| Full width, 4 m | 25 × 20 × 25 | 0.22 m/s | 23 % | 12 % |
| 1.2 m wide | 25 × 20 × 25 | 0.29 m/s | 41 % | 18 % |
| 1.2 m wide | 50 × 40 × 25 | 0.30 m/s | 42 % | 20 % |

A 2D model cannot show this case: it treats every opening as running the full width.

**Run times** for the 1.2 m window, 30 minutes simulated, on a 4-core 2.1 GHz Xeon processor:

| Mesh | NumPy | Numba |
|---|---|---|
| 25 × 20 × 25 | 14 min | 6 min |
| 50 × 40 × 25 | about 55 min | 25 min |

## Using the Python code

The interface follows the 2D model. A case is a `Case` object, and every field has a default:

```python
from room_cfd_3d_numba import Case, Opening, HeatBlock, run, occupied_zone, plot_slices
# or: from room_cfd_3d import ...  (same interface, no Numba needed)

c = Case(inlet=Opening("left", 0.9, 2.1, 1.4, 2.6), outlet=Opening("right", 2.3, 2.4),
         T_in=16.0, ach=6, t_end=1800, t_avg=600)
c.heat = [HeatBlock(2.3, 2.7, 0.0, c.W, 0.0, 1.2, 1.2 * 1005 * c.q * (26 - c.T_in))]
res = run(c, verbose=True)
print(occupied_zone(res))        # floor speed and where, DR, TS, PPD_AD and the ankle speed limit
plot_slices(res, y=2.0, z=0.1, path="slices.png")

from room_cfd_3d import read_layout
lay = read_layout("room-layout-office.csv")   # dict with heat, floor_flux and furniture
c.heat, c.floor_flux, c.furniture = lay["heat"], lay["floor_flux"], lay["furniture"]
```

| `Case` field | Default | Meaning |
|---|---|---|
| `L`, `W`, `H` | 5, 4, 2.5 m | Room depth, width and height |
| `nx`, `ny`, `nz` | 50, 40, 25 | Number of cells |
| `ach` | 6 h⁻¹ | Air change rate |
| `T_in`, `T_room0` | 18 °C, well-mixed value | Supply and initial room temperature |
| `inlet`, `outlet` | 0.1–0.3 m left, 2.2–2.4 m right | `Opening(side, start, end, y0, y1)`, side `"left"`, `"right"` or `"top"`; `y0`, `y1` = None for the full width |
| `heat` | none | List of `HeatBlock(x0, x1, y0, y1, z0, z1, power)`, power in W |
| `floor_flux` | none | List of `FloorFlux(x0, x1, y0, y1, power)`, power in W |
| `furniture` | none | List of `Furniture(x0, x1, y0, y1, z0, z1)`; zero size along one axis = a thin plate |
| `turbulence` | `"k-epsilon"` | or `"chen-xu"`, or `"constant"` with `nu_t` |
| `advection` | `"tvd"` | or `"upwind"` |
| `pressure`, `p_tol` | `"multigrid"`, $10^{-6}$ | or `"direct"` (small grids only) |
| `t_end`, `t_avg` | 900 s, 300 s | Simulated time and averaging window at the end |

`run` returns the grid (`x`, `y`, `z`), the averaged fields (`u`, `v`, `w` on the faces; `T`, `speed`, `nu_t`, `k` in the cells), the energy check (`T_out` against `T_out_expected`), the convergence `history` and the number of pressure iterations. `occupied_zone` uses a zone 0.6 m from the facade, the back wall and both side walls.

## Limitations

- **Grid.** The default grid has 10 cm cells, twice the 2D default, and grids fine enough for grid-independent jets are out of reach on a laptop.
- **Inlet only, no radiation, adiabatic walls, fixed $Tu$ in the comfort indices**, as in the 2D model.
- **Furniture.** Boxes are made of whole cells and plates snap to the nearest grid plane, so furniture is only as accurate as the mesh. The k-ε wall functions for $k$ and $\varepsilon$ are applied at the room walls only, not at the furniture, and furniture neither stores nor conducts heat.
- **Single precision on the GPU.** Enough for the flow, but the time-averaged fields from the app and from Python differ in the last digits, and more where the flow is unsteady.

Use the model to compare openings, temperatures and airflows in a room, and to see where the 2D section is and is not enough. For design values, use a validated CFD code or measurements.
