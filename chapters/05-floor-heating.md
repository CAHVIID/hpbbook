# Floor heating

## Learning objectives

After this chapter you can:

- estimate the heat output of a heated floor from its surface temperature, and explain why the output regulates itself
- compare light and heavy floor heating constructions by heat capacity and time constant
- estimate the time constant of a floor and the heat it keeps delivering after the loop closes
- describe the parts of a hydronic floor heating installation and what each one controls
- explain why floor heating is a poor match for low-energy houses, where heating demand at night turns into cooling demand during the day

## Introduction

Floor heating is the standard heat emitter in new Danish dwellings. It is invisible, it frees wall space, and it works with low supply temperatures, which suits heat pumps and district heating. In an older house with a large heat demand it also gives good comfort, with warm feet and a small vertical temperature gradient.

A low-energy house is a different case. Its heat loss is small, typically 10–20 W per m² of floor at design conditions and much less on an ordinary spring or autumn day. Its solar and internal gains are large in comparison. On a clear day in April the heating demand at night can turn into a cooling demand by noon. The heat emitter must therefore stop delivering heat within a few hours of being asked to.

A floor cannot do that, because heat is stored in the floor before it reaches the room. Water put into the floor at 4 am keeps warming the room after the sun has come out. The heavier the floor, the longer the delay. This chapter shows how large that delay is for a light floor and for a heavy floor, and why it makes floor heating a risky choice in a low-energy house. Control of floor heating, and what it can and cannot fix, is the topic of the later sections.

## Heat transfer from a heated floor

A heated floor gives off heat to the room by radiation to the other surfaces and by natural convection to the air. Together they give a heat transfer coefficient of about 11 W/(m²·K). EN 1264 gives the heat flux $q$ from the mean floor surface temperature $\theta_F$ and the room temperature $\theta_i$ {cite:p}`en1264`:

$$
q = 8.92\,(\theta_F - \theta_i)^{1.1} \quad \text{W/m}^2
$$ (eq-floor-flux)

For comfort, the mean floor surface temperature is limited to 29 °C in occupied zones, 33 °C in bathrooms and 35 °C in perimeter zones. At 29 °C and a room at 20 °C, equation {eq}`eq-floor-flux` gives about 100 W/m², which is far more than a low-energy house needs.

Two consequences matter for the rest of the chapter:

- **The floor is barely warm.** A heat demand of 15 W/m² needs a floor surface only 1.6 K above the room temperature. The occupants will not feel a "warm floor".
- **The output regulates itself, but slowly.** Because the temperature difference is small, a small rise in room temperature removes much of the output. If the floor is at 23 °C, the output falls from 30 W/m² to 9 W/m² when the room rises from 20 °C to 22 °C. This self-regulation is real, but it only acts after the room has already become warmer.

A floor covering adds thermal resistance between the pipes and the room. Tiles add little, while wood and carpet add a lot, so a wooden floor needs a higher water temperature for the same output. EN 1264 limits the covering resistance to 0.15 m²·K/W.

## Light and heavy floor constructions

Floor heating constructions are often grouped by how the pipes are embedded. For this chapter the useful distinction is how much heat capacity sits between the pipes and the room ({numref}`fig-floor-sections`).

:::{figure} figures/ch05/floor-sections.*
:label: fig-floor-sections
:alt: Two cross-sections drawn to the same scale. Left, a light floor: 22 mm floor boards resting on aluminium plates that wrap around the pipes, which sit in grooves in a 30 mm EPS panel on an 18 mm plywood board above insulation and joists. Right, a heavy floor: 14 mm parquet on a 100 mm concrete slab with the pipes in the middle of the slab, above EPS insulation.
:width: 100%

Light and heavy floor heating constructions, drawn to the same scale. The heat capacity above the pipes is about seven times larger in the heavy floor. Response times are from the model in {numref}`fig-floor-step-response`.
:::

### Light floors

In a light (dry) floor the pipes lie in grooves in an insulation panel, usually EPS. Aluminium heat-diffusion plates wrap around the pipes and spread the heat sideways under the floor covering. The EPS panels rest on a plywood board on the joists, and the covering is laid directly on the plates, typically 22 mm floor boards, a floating wooden floor or gypsum fibre boards. Pipe spacing is 150–300 mm.

Light floors are used on timber joists and battens, in renovation, and wherever build height and weight must be kept low. The whole construction above the insulation is 25–50 mm thick and weighs 10–30 kg/m². Its heat capacity above the pipes is about 15–30 kJ/(m²·K), so there is little heat to store.

### Heavy floors

In a heavy floor the pipes are cast into cement screed or concrete. A typical screed system has 45–65 mm of screed above the pipes. In Danish slab-on-ground houses the pipes are often tied to the reinforcement in the middle of a 100 mm concrete slab, with the floor covering laid directly on the slab. The slab weighs around 230 kg/m² and has a heat capacity of 100–250 kJ/(m²·K), and all of it is heated by the pipes.

Heavy floors are cheap to build in new houses, robust, and good at evening out short peaks in demand. That is a strength in an old, poorly insulated house. In a low-energy house it is the problem.

### The time constant of a floor

When the water flow in a loop starts or stops, the heat output to the room does not change at once. For a first-order system, the output approaches its new value exponentially:

$$
q(t) = q_\infty + (q_0 - q_\infty)\,e^{-t/\tau}
$$ (eq-first-order)

where $\tau$ is the time constant. After one time constant, 63 % of the change has happened. After three time constants, 95 % has. The time constant is the product of a heat capacity and a thermal resistance:

$$
\tau = R\,C
$$ (eq-tau)

When the loop closes, the stored heat can only leave through the floor surface. The resistance is then the floor covering plus the surface resistance, about $1/11 \approx 0.09$ m²·K/W, and the heat capacity is that of the whole floor above the insulation. For the two floors in {numref}`fig-floor-sections`:

- **Light floor:** $C \approx 20$ kJ/(m²·K) for the boards and plates, $R \approx 0.09 + 0.08 = 0.17$ m²·K/W, so $\tau \approx 3400$ s, or about 1 hour. The plywood board under the EPS also stores heat, but the EPS separates it from the pipes, so it only adds a slow tail.
- **Heavy floor:** $C \approx 230$ kJ/(m²·K), $R \approx 0.09 + 0.08 + 0.03 = 0.20$ m²·K/W, so $\tau \approx 46\,000$ s, or about 13 hours.

When the loop opens, the water forces the pipe plane to its own temperature. Only the layers above the pipes have to warm up, and they are heated from below as well as losing heat at the top. Switching on is therefore faster than switching off.

{numref}`fig-floor-step-response` shows a more detailed calculation with a one-dimensional heat conduction model of both floors. The water is at 30 °C and the room at 20 °C.

:::{figure} figures/ch05/floor-step-response.*
:label: fig-floor-step-response
:alt: Two line charts of heat output to the room in percent of steady state over 24 hours. Left, after the wax thermostat opens, the light floor reaches 63 % in about half an hour and the heavy floor in about 2 hours. Right, after the wax thermostat closes, the light floor falls to 37 % in about 1 hour, while the heavy floor takes about 12 hours and still delivers about 10 % after 24 hours.
:width: 100%

Heat output of the two floors in {numref}`fig-floor-sections` after a) the wax thermostat opens and b) the wax thermostat closes. The dashed lines mark 63 % of the change. One-dimensional conduction model, water at 30 °C, room at 20 °C. Wax thermostat delay and the response of the room itself are not included.
:::

```{list-table} Response of the light and heavy floor in {numref}`fig-floor-sections` (one-dimensional model, water at 30 °C, room at 20 °C)
:header-rows: 1
:label: tab-floor-response

* -
  - Light floor
  - Heavy floor
* - Heat capacity above pipes
  - 18 kJ/(m²·K)
  - 120 kJ/(m²·K)
* - Heat capacity, whole floor
  - 40 kJ/(m²·K)
  - 230 kJ/(m²·K)
* - Steady-state output
  - 27 W/m²
  - 43 W/m²
* - 63 % response, loop opens
  - 0.5 h
  - 2 h
* - 63 % response, loop closes
  - 1 h
  - 12 h
* - Heat delivered after the loop closes
  - 50 Wh/m²
  - 500 Wh/m²
* - Same, in hours of full output
  - 2 h
  - 12 h
```

The last two rows are the ones that matter in a low-energy house. When the heavy floor's loop closes, the slab still holds about 500 Wh/m² more heat than at room temperature, and it hands this heat to the room over the next day. If the house needs 10 W/m² on average on a spring day, that is two days' heating stored in the floor. A thermostat that closes the loop when the sun comes out has no influence on this heat. The room overheats, and the heat must be removed again by opening windows or by cooling.

A light floor holds a tenth of that heat, and most of it is released within the first hour. It follows the daily cycle much better, but it still lags behind the demand. The control loop adds more delay, and that is the subject of the section on control.

:::{admonition} Rules of thumb: floor time constants
:class: tip

- Time constant after the loop closes: $\tau \approx C_\text{floor}\,(R_\text{covering} + 0.09)$.
- Light floor with wooden boards: $\tau \approx 1$ h. Screed or concrete slab: $\tau \approx 6$–$15$ h.
- Switching on is faster than switching off, because the water drives the pipe plane but nothing drives the stored heat out.
- Heat delivered after the loop closes ≈ heat capacity × mean excess temperature of the floor. For a 100 mm slab this is several hundred Wh/m², a day or more of the heating demand of a low-energy house.
- A floor with a time constant longer than a few hours cannot follow a heating demand that changes within the day.
:::

## The hydronic installation

{numref}`fig-hydronic-schematic` shows a typical installation. The parts are the same for light and heavy floors.

:::{figure} figures/ch05/hydronic-schematic.*
:label: fig-hydronic-schematic
:alt: Schematic of a hydronic floor heating system. A heat pump or district heating unit supplies water through a three-way mixing valve and a circulation pump to a manifold. The controller sets the mixing valve from an outdoor sensor and a supply temperature sensor. From the manifold, one loop runs to each of three rooms. The controller drives a motorized mixing valve. Each loop has a flow meter on the supply side and a wax thermostat on the return side, switched by a temperature sensor in its room.
:width: 100%

A hydronic floor heating installation. The controller sets the supply temperature from the outdoor temperature (heating curve). The room temperature sensor in each room opens and closes the wax thermostat on its own loop.
:::

- **Heat source.** A heat pump or district heating. Floor heating needs a low supply temperature, typically 30–35 °C in a low-energy house, with 3–5 K between supply and return.
- **Mixing shunt.** A motorized three-way mixing valve and a circulation pump. The valve mixes return water into the supply to reach the temperature set by the controller. The controller follows a heating curve, which raises the supply temperature as the outdoor temperature falls.
- **Manifold.** Distributes water to one loop per room, or several loops in large rooms. Each loop should be at most 80–100 m long to keep the pressure drop reasonable. Flow meters or balancing valves on the supply side set the design flow in each loop, so that every room gets its share (hydronic balancing).
- **Wax thermostats and room temperature sensors.** Each loop has a valve on the return side, opened and closed by a wax thermostat, an electrically heated wax actuator. The room temperature sensor switches it on and off, either directly or by pulse-width modulation (PWM). The valve only opens or closes the loop. It cannot change the water temperature.

So the installation has two control levels. The supply temperature is set centrally from the outdoor temperature, and each room switches its own loop on or off. Neither level knows about the sun, and both act on the floor, not on the room. Any delay in the floor therefore appears directly as a delay in the room.

### Several manifolds on one riser

In buildings with several floors or apartments, one riser pump often feeds a manifold on each floor, each through its own shunt ({numref}`fig-riser-shunts`). The shunt pump circulates water through the floor loops. A thermostatic valve on the return limits the supply temperature: when the sensor bulb gets too warm, it throttles the water returned to the riser, so less hot water is drawn in and more return water is mixed back through the bypass. The check valve stops riser water from flowing backwards through the bypass into the return.

:::{figure} figures/ch05/riser-shunts.*
:label: fig-riser-shunts
:alt: Schematic of a riser fed by a heat pump and a riser pump. On each of two floors, a branch from the riser supply passes a bypass junction, a shunt pump and a sensor bulb before reaching a supply manifold with three connections. The return manifold has a wax thermostat on each connection. The return passes the bypass junction and a 2-way thermostatic valve, connected to the sensor bulb by a capillary, before rejoining the riser return. The bypass between return and supply has a check valve. One floor loop is drawn in full.
:width: 100%

A riser with a riser pump feeding two floor heating manifolds, each through a shunt with its own pump, a 2-way thermostatic valve on the return and a check valve in the bypass. Three pumps in total. Only one floor loop per manifold is drawn.
:::

## Control of floor heating

Floor heating is controlled on two levels ({numref}`fig-hydronic-schematic`). The supply temperature follows a heating curve, set from the outdoor temperature. Each room then switches its own loop with a wax thermostat, driven by its room temperature sensor.

A wax thermostat is an on/off valve. A small heater warms a wax capsule, the wax expands and pushes the valve open. It takes 2–3 min before the valve starts to move and another 3–5 min to open fully, and about the same to close. It cannot hold an intermediate position for long, so the room unit controls it in one of two ways:

- **On/off control.** The loop opens when the room is below the setpoint minus a hysteresis and closes when it is above the setpoint plus the hysteresis.
- **PWM control.** The room unit runs a PI controller and turns its output into a duty cycle. With a 15–20 min cycle and 40 % output, the valve is open for about 6–8 min of each cycle. On average this behaves like a valve that is 40 % open.

PWM smooths the room temperature, but it does not remove the delay. The sensor measures the room, the valve acts on the water, and the floor lies in between. Whatever the controller decides, the floor delivers it over the next 0.5–1 h (light floor) or many hours (heavy floor). A controller that sees the room warming can close the valve, but it cannot take back the heat already stored in the floor.

The interactive model below shows the consequence. With the default inputs, the choice between on/off and PI changes the result by a few percent. The choice between a light and a heavy floor changes it much more.

### Interactive model: control and solar gains

The model below simulates one room in a low-energy house with a light and a heavy floor ({numref}`fig-floor-sections`) over a cloudy spring day followed by a sunny one. The floor is controlled in three ways: an on/off room thermostat, a PI controller whose output is a PWM signal to the wax thermostat, and, for reference, an ideal heater that delivers exactly the heat needed without any delay. Windows are opened when the room gets too warm, and the heat removed this way is counted as heat vented.

Use the toggle to switch between the light and the heavy floor, and change the inputs to see how the floor, the controller and the weather interact. Hover over an input name for an explanation. The four graphs show the room temperature, the heat flux from the floor surface to the room, the supply, return and floor surface temperatures, and the mass flow in the loop. The table gives the heating energy and heat vented over the two days, the summed deviation below and above the setpoint in K·h, and the mass-flow-weighted return temperature. The tab *Extra: floor materials* lets you change the layers of both floors.

```{anywidget} code/floor-control.mjs
{}
```

The app runs in your browser. The same model in Python, with comments on every assumption, can be downloaded here: {download}`floor_control.py <code/floor_control.py>`. Running it prints the table for the default inputs. The equations are given at the end of the chapter, in {ref}`sec-floor-model-theory`.

:::{admonition} Model assumptions
:class: note

- One-dimensional heat conduction in the floor; the underside is adiabatic.
- The room is one node with the heat capacity of air, furniture and light internal parts (40 kJ/(m²·K)). All solar gain heats this node.
- Outdoor temperature varies between 2 °C at 03:00 and 12 °C at 15:00 on both days. The supply temperature follows a heating curve.
- The loop mass flow is proportional to the valve position, 6 kg/(h·m²) fully open by default. Heat transfer from the water to the pipe plane uses an effectiveness (NTU) model, which gives the return temperature.
- The wax thermostat opens after a dead time and then moves linearly to fully open; it closes after 2 min and over 5 min.
- Four cloudy days are simulated before the two days shown, so the floors start in a realistic state.
:::

## Heating and cooling within the same 24 hours

In a low-energy house, a spring or autumn day often needs both heating and cooling. The night is cold and the room needs heat in the early morning. From late morning the sun through the windows covers the heat loss, and by the afternoon the room overheats. The heating demand is small and short, and it is followed within a few hours by a cooling demand.

A floor cannot follow this. The heat the controller asks for at 05:00 is still leaving the floor at 10:00, when the sun has taken over. The floor then works as a heater during the hours when the room needs cooling. The room temperature sensor closes the loop as soon as the room is warm, but the stored heat keeps flowing. The heavier the floor, the more heat it stores and the longer it keeps delivering.

The model shows this for the two days. Compared with the ideal heater, the light floor needs about 15 Wh/m² more heat and gives about 10 K·h more overheating. The heavy floor needs about 40 Wh/m² more heat and gives about 30 K·h more overheating. The extra heat is not useful heat. It is heat that ends up being removed again, through open windows or by a cooling system.

Several strategies reduce the problem, but none of them removes it:

- **Low supply temperature and self-regulation.** With the supply only a few kelvin above the room, the floor delivers less when the room warms up, even with the valve open.
- **Heating stop.** Stop heating above an outdoor temperature limit, for example 12–15 °C, and use a deadband between the heating and cooling setpoints.
- **Anticipating the sun.** Lower the setpoint in the morning on sunny days, using a weather forecast or model predictive control.
- **Shading and ventilative cooling.** Remove the solar gain or the surplus heat (see chapter 2).
- **Floor cooling.** The same pipes can cool by 20–40 W/m², limited by the dew point and a minimum floor surface temperature of about 19–20 °C. But the floor is just as slow when cooling.

The conclusion is that a heat emitter with a long time lag is a poor match for a house whose heating demand is small and changes within hours. A fast emitter, such as heating through the ventilation air or a small convector, can switch off at the moment the sun starts to heat the room.

(sec-floor-model-theory)=
## Theory behind the interactive model

::::{admonition} Show the equations
:class: dropdown

The model is an RC network ({numref}`fig-rc-network`). The room is one node, and the floor is split into thin layers of about 2 mm, each a node with its own heat capacity. The water reaches the floor at the pipe plane.

:::{figure} figures/ch05/rc-network.*
:label: fig-rc-network
:alt: RC network of the model. The room node is connected to the outdoor temperature through the resistance one over H loss, has the heat capacity C r, receives solar and internal gains and loses vented heat. Below it, a chain of resistances and capacitances represents the floor layers from the surface to an adiabatic underside. The two nodes either side of the pipe plane are connected to the supply water temperature through the water conductance g w, which the wax thermostat switches.
:width: 75%

RC network behind the interactive model. Each floor layer is split into nodes of about 2 mm. The wax thermostat sets the mass flow and so the conductance $g_\mathrm{w}$ between the supply water and the pipe plane.
:::

**Room node.** The heat balance of the room is

$$
C_\mathrm{r}\frac{\mathrm{d}T_\mathrm{r}}{\mathrm{d}t} = H_\mathrm{loss}(T_\mathrm{out}-T_\mathrm{r}) + G_\mathrm{s}(T_1-T_\mathrm{r}) + \Phi_\mathrm{sol} + \Phi_\mathrm{int} + \Phi_\mathrm{ideal} - \Phi_\mathrm{vent}
$$ (eq-room-node)

where $G_\mathrm{s} = 1/(1/h_\mathrm{s} + \Delta z_1/2\lambda_1)$ links the room to the top floor node through the surface coefficient $h_\mathrm{s} = 10.8$ W/(m²·K). The term $G_\mathrm{s}(T_1-T_\mathrm{r})$ is the heat flux from the floor surface shown in the app. $\Phi_\mathrm{ideal}$ is only used for the ideal heater.

**Floor nodes.** Each floor node $i$ exchanges heat with its neighbours by conduction:

$$
C_i\frac{\mathrm{d}T_i}{\mathrm{d}t} = G_{i-1,i}(T_{i-1}-T_i) + G_{i,i+1}(T_{i+1}-T_i) + g_\mathrm{w}(T_\mathrm{sup}-T_i)
$$ (eq-floor-node)

with $C_i = \rho_i c_i \Delta z_i$ and $G_{i,i+1} = 1/(\Delta z_i/2\lambda_i + \Delta z_{i+1}/2\lambda_{i+1})$. The last term only applies to the two nodes either side of the pipe plane. The bottom node has no neighbour below, so the underside is adiabatic. The heat loss of the room is all in $H_\mathrm{loss}$.

**Water to floor.** The mass flow is proportional to the wax thermostat position $y$ (0 closed, 1 open), $\dot m = y\,\dot m_\mathrm{design}$. The heat transfer from the water uses an effectiveness model with $UA = 1/R_\mathrm{pipe}$, split equally on the two pipe nodes:

$$
g_\mathrm{w} = \tfrac{1}{2}\,\dot m c_p\left(1-e^{-UA/\dot m c_p}\right), \qquad
T_\mathrm{ret} = T_\mathrm{sup} - \frac{\Phi_\mathrm{w}}{\dot m c_p}
$$ (eq-water)

where $\Phi_\mathrm{w} = \sum g_\mathrm{w}(T_\mathrm{sup}-T_p)$ is the heat delivered to the floor. As the flow falls, the water cools more on its way through the loop, so the return temperature drops.

**Supply temperature and climate.** The heating curve and the boundary conditions are

$$
T_\mathrm{sup} = \min\!\left(T_\mathrm{sup,max},\; 20 + s\,(20-T_\mathrm{out})\right), \quad
T_\mathrm{out} = 7 - 5\cos\frac{2\pi(t-3)}{24}, \quad
\Phi_\mathrm{sol} = \hat\Phi_\mathrm{sol}\max\!\left(0, \sin\frac{\pi(t-7)}{12}\right)
$$ (eq-boundary)

with $t$ in hours and $s$ the heating curve slope. The outdoor temperature is 2 °C at 03:00 and 12 °C at 15:00. The sun shines from 07:00 to 19:00 with the peak $\hat\Phi_\mathrm{sol}$ at 13:00.

**Control.** The on/off controller opens the loop below $T_\mathrm{set} - \Delta T_\mathrm{hyst}$ and closes it above $T_\mathrm{set} + \Delta T_\mathrm{hyst}$. The PI controller computes, at the start of each PWM cycle,

$$
u = K_p e + \frac{K_p}{T_i}\int e\,\mathrm{d}t, \qquad e = T_\mathrm{set}-T_\mathrm{r}, \qquad K_p = 1/X_p
$$ (eq-pi)

where $X_p$ is the proportional band. The output $u$ (0–1, with anti-windup) is the duty cycle: the loop is open for the first $u\,t_\mathrm{cycle}$ of each cycle. The wax thermostat follows the signal after a dead time and then moves at the rate $1/t_\mathrm{stroke}$, separately for opening and closing.

The ideal heater supplies what the room needs to stay at the setpoint, with the room correcting itself in 10 min:

$$
\Phi_\mathrm{ideal} = \max\!\left(0,\; H_\mathrm{loss}(T_\mathrm{set}-T_\mathrm{out}) - \Phi_\mathrm{sol} - \Phi_\mathrm{int} + C_\mathrm{r}\frac{T_\mathrm{set}-T_\mathrm{r}}{600\ \mathrm{s}}\right)
$$ (eq-ideal)

**Venting.** When the room exceeds $T_\mathrm{vent}$, the windows remove the excess at once: $T_\mathrm{r}$ is reset to $T_\mathrm{vent}$ and the heat removed, $C_\mathrm{r}(T_\mathrm{r}-T_\mathrm{vent})$, is counted as heat vented.

**Solution.** The equations are solved with implicit Euler time steps of 60 s. Each step is a tridiagonal linear system, solved directly. The results in the table are sums over the two days shown: the heating energy $\int\Phi_\mathrm{w}\,\mathrm{d}t$, the heat vented, and the deviation from the setpoint, $\int\max(0, T_\mathrm{set}-T_\mathrm{r})\,\mathrm{d}t$ below and $\int\max(0, T_\mathrm{r}-T_\mathrm{set})\,\mathrm{d}t$ above, in K·h.
::::
