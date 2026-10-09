# Floor heating


<!-- ## Learning objectives

After this chapter you can:

- estimate the heat output of a heated floor from its surface temperature, and explain why the output regulates itself
- compare light and heavy floor heating constructions by heat capacity and time constant
- estimate the time constant of a floor and the heat it keeps delivering after the loop closes
- describe the parts of a hydronic floor heating installation and what each one controls
- explain why floor heating is a poor match for low-energy houses, where heating demand at night turns into cooling demand during the day 

%+++
%edwdds
%#dwd 
%sdas
%+++
-->


<!-- possible classes:

 note, important, seealso: blue 
 tip, hint: green
 warning, caution, attention: orange
 danger, error: red
 
 :::{Tip} This is the tip of the day
 And here goes the tip
 :::

 :::{admonition} Tips of the day
 class: dropdown
 This is the tip
 :::
 
  -->

## Introduction

Floor heating is the standard heat emitter in newer Danish dwellings. It is invisible, it frees wall space, and it potentially works with very low supply temperatures, which suits heat pumps and district heating very well.

Warm water from a manifold runs through a pipe loop in the floor of each room and returns a few kelvin cooler. The heat first warms the floor, and the floor surface then gives it to the room by radiation and convection ({numref}`fig-floor-principle`).

:::{figure} figures/ch03/floor-heating-principle.*
:label: fig-floor-principle
:alt: Two panels. Left, a plan view of a room with a serpentine pipe loop: water leaves a manifold at about 30 °C, runs back and forth across the floor with legs 150–300 mm apart, changing colour from red to blue, and returns at about 25 °C. Right, a section of the same room: pipes cast in a concrete slab on insulation, under a floor covering. Wavy arrows show radiation and dashed arrows show convection from the floor to the room, and sunlight enters through a window onto the floor.
:width: 100%

Principle of hydronic floor heating. (a) One pipe loop per room, fed from a manifold. (b) Heat passes from the water into the slab, and from the floor surface to the room by radiation and convection. In a low-energy house the floor is only 1–3 K warmer than the room air.
:::

In older house with a large heat demand it gives good comfort, with warm feet and a small vertical temperature gradient.

A low-energy house is a different case. Heat loss is small, **only 10 W per m² of floor** at design conditions and much less on an ordinary spring or autumn day. Solar and internal gains are large in comparison. On a clear day in April the heating demand at night can easily turn into a cooling demand by noon. The floor system must therefore stop delivering heat hours before being asked to.

Heavy floors cannot do that, because heat is stored in the floor before it reaches the room. Water put into the floor at 4:00 keeps warming the room after the sun has come out and heat demand has long gone. The heavier the floor, the longer the delay.

<!-- This chapter shows how large that delay is for a light floor and for a heavy floor, and why it makes floor heating a risky choice in a low-energy house. Control of floor heating, and what it can and cannot fix, is the topic of the later sections.
 -->

## Heat transfer of floors

A heated floor gives off heat to the room by radiation to the other surfaces and by natural convection to the air. Added together they give a heat transfer coefficient of about 11 W/(m²·K) {cite:p}`rehva2007`:.

:::{admonition} Extra
:class: dropdown
- **Radiation** Between surfaces in a thermal enclosure, radiative exchange is approx. 5.0 W/(m²·K), and is pretty much fixed.
- **Convection** Convective heat transfer from a heated floor depends strongly on surface type, air speed, and forced or natural convection, but can be assumed to be approx. 6.0 W/(m²·K)
- **Total** Convective and radiative heat transfers sums to 11 W/(m²·K). Source: {cite:p}`rehva2007`
:::

EN 1264 gives the heat flux $q$ from the mean floor surface temperature $\theta_F$ and the room temperature $\theta_i$ {cite:p}`en1264`:

$$
q = 8.92\,(\theta_F - \theta_i)^{1.1} \quad \text{W/m}^2
$$ (eq-floor-flux)

For comfort, the mean floor surface temperature is limited to:
- 29 °C in occupied zones
- 33 °C in bathrooms
- 35 °C in perimeter zones

At 29 °C and a room at 20 °C, equation {eq}`eq-floor-flux` gives about 100 W/m², which is far more than a low-energy house needs ({numref}`fig-en1264-curve`).

:::{figure} figures/ch03/en1264-curve.*
:label: fig-en1264-curve
:alt: Line chart of heat flux against the difference between floor surface and room temperature, from 0 to 16 K. The curve rises almost linearly. Marked points: 1.1 K gives 10 W/m² for a low-energy house, 9 K gives 100 W/m² at the limit for occupied zones (29 °C floor, 20 °C room, or 33 °C floor and 24 °C room in bathrooms), and 15 K gives 175 W/m² at the limit for perimeter zones (35 °C floor, 20 °C room).
:width: 80%

Basic characteristic curve of a heated floor, equation {eq}`eq-floor-flux`, with the floor surface temperature limits. After EN 1264 {cite:p}`en1264`.
:::

Floor covering adds thermal resistance between the pipes and the room. Tiles add little, while wood and carpet add a lot, so a wooden floor needs a higher water temperature for the same output.

%EN 1264 limits the covering resistance to 0.15 m²·K/W.

:::{admonition} Extra
:class: dropdown
- **Barely warm** A heat demand of 10 W/m² needs a floor surface **only 1.1 K above** the room temperature. In low energy houses, the occupants will never feel a "warm floor".
- **Self-regulation** The small temperature difference between floor surface and room means that a small rise in room temperature removes much of the output. If the floor is at 23 °C, the output falls from 30 W/m² to 9 W/m² when the room rises from 20 °C to 22 °C.
- **TABS** Self-regulation is real and exploitable, potentially removing the need for control systems. In practice, it is often seen in thermo-active building systems, where the pipes are deeply embedded into the core of concrete slabs, making them act as heating or cooling "batteries" for basic loads.
:::


## Build-up

Floor heating constructions are often grouped by how the pipes are embedded, i.e. how much heat capacity sits between the pipes and the room ({numref}`fig-floor-sections`).

:::{figure} figures/ch03/floor-sections.*
:label: fig-floor-sections
:alt: Two cross-sections drawn to the same scale. Left, a light floor: 22 mm floor boards resting on aluminium plates that wrap around the pipes, which sit in grooves in a 30 mm EPS panel on an 18 mm plywood board above insulation and joists. Right, a heavy floor: 14 mm parquet on a 100 mm concrete slab with the pipes in the middle of the slab, above EPS insulation.
:width: 100%

Light and heavy floor heating constructions, drawn to the same scale. The heat capacity above the pipes is about seven times larger in the heavy floor. Response times are from the model in {numref}`fig-floor-step-response`.
:::

:::{admonition} Details
:class: dropdown
### Light floors

In a light (dry) floor the pipes lie in grooves in an insulation panel, usually EPS. Aluminium heat-diffusion plates wrap around the pipes and spread the heat sideways under the floor covering. The EPS panels rest on a plywood board on the joists, and the covering is laid directly on the plates, typically 22 mm floor boards, a floating wooden floor or gypsum fibre boards. Pipe spacing is anything between 150–300 mm, depending on pipe diameter and system.

Light floors are used on timber joists and battens, in renovation, and wherever build height and weight must be kept low. The whole construction above the insulation is 25–50 mm thick and weighs 10–30 kg/m². Its heat capacity above the pipes is about 15–30 kJ/(m²·K), so there is little heat to store.

### Heavy floors

In a heavy floor the pipes are cast into cement screed or concrete. A typical screed system has 45–65 mm of screed above the pipes. In Danish slab-on-ground houses the pipes are often tied to the reinforcement in the middle of a 100 mm concrete slab, with the floor covering laid directly on the slab. The slab weighs around 230 kg/m² and has a heat capacity of 100–250 kJ/(m²·K), and all of it is heated by the pipes.

%Heavy floors are cheap to build in new houses, robust, and good at evening out short peaks in demand. That is a strength in an old, poorly insulated house. In a low-energy house it is the problem.
:::

## Hydronic installation

{numref}`fig-hydronic-schematic` shows a typical installation. The parts are the same for light and heavy floors.

:::{figure} figures/ch03/hydronic-schematic.*
:label: fig-hydronic-schematic
:alt: Schematic of a hydronic floor heating system. A heat pump or district heating unit supplies water through a three-way mixing valve and a circulation pump to a manifold. The controller sets the mixing valve from an outdoor sensor and a supply temperature sensor. From the manifold, one loop runs to each of three rooms. The controller drives a motorized mixing valve. Each loop has a flow meter on the supply side and a wax thermostat on the return side, switched by a temperature sensor in its room.
:width: 100%

A hydronic floor heating installation. The controller sets the supply temperature from the outdoor temperature (heating curve). The room temperature sensor in each room opens and closes the wax thermostat on its own loop.
:::

:::{admonition} Details
:class: dropdown
- **Heat source.** A heat pump or district heating. Floor heating needs a low supply temperature, typically 30–35 °C in a low-energy house, with 3–5 K between supply and return.
- **Mixing shunt.** A motorized three-way mixing valve and a circulation pump. The valve mixes return water into the supply to reach the temperature set by the controller. The controller follows a heating curve, which raises the supply temperature as the outdoor temperature falls.
- **Manifold.** Distributes water to one loop per room, or several loops in large rooms. Each loop should be at most 80–100 m long to keep the pressure drop reasonable. Flow meters or balancing valves on the supply side set the design flow in each loop, so that every room gets its share (hydronic balancing).
- **Wax thermostats and room temperature sensors.** Each loop has a valve on the return side, opened and closed by a wax thermostat, an electrically heated wax actuator. The room temperature sensor switches it on and off, either directly or by pulse-width modulation (PWM). The valve only opens or closes the loop. It cannot change the water temperature.
:::


## Control of floor heating

Floor heating has two levels of control ({numref}`fig-hydronic-schematic`). The supply temperature follows a heating curve, set from the outdoor temperature. Each room then switches its own loop with a wax thermostat, driven by its room temperature sensor.

<!-- :::{admonition} Control
:class: Tip
The installation has **two levels of control**.
The supply temperature is set centrally from the outdoor temperature, and each room switches its own loop on or off.
Lower supply temperature will keep the loops more on, and vice versa.
Low supply temperature increases self-regulation.
::: -->

A wax thermostat is an on/off valve ({numref}`fig-wax-thermostat`). A small heater warms a wax capsule, the wax expands and pushes the valve open. It takes 2–3 min before the valve starts to move and another 3–5 min to open fully, and about the same to close.

:::{figure} figures/ch03/wax-thermostat.jpg
:label: fig-wax-thermostat
:alt: Photo of a wax thermostat: a blue cylindrical actuator with a grey threaded base that screws onto the valve on the manifold, and a grey cable for the 24 V supply from the room unit.
:width: 35%

Wax thermostat (telestat) for mounting on the manifold, 24 V, 2 W, normally closed. Photo: Uponor.
:::

The wax thermostat cannot hold positions between fully open, and fully closed, so they are  controlled via pulse-width modulation.

### On/off control.

The loop opens when the room is below the setpoint minus a hysteresis and closes when it is above the setpoint plus the hysteresis. The valve response depends on how narrow or wide the proportional band was set by the user. A narrow proportional band causes the valve to respond "a lot" for even small deviations, a band too wide causes the valve to never quite respond as needed to close the deviation.

{numref}`fig-proportional-band` compares three cases:
- On/off control swings the room between about 20 and 21.3 °C, well outside the ±0.25 K hysteresis, because the floor keeps heating after the valve closes and keeps lagging after it opens
- A narrow band settles close to the setpoint after a few damped oscillations.
- A wide band gives a smooth response, but the room settles about 0.7 K below the setpoint.

<!-- In this example the room needs more than 50 % output, and a proportional controller only gives more than 50 % when the room is below the setpoint. This remaining deviation is the offset. The I part of a PI controller removes it. -->

:::{figure} figures/ch03/proportional-band.*
:label: fig-proportional-band
:alt: Left, controller output in percent against room temperature. On/off control jumps between 0 and 100 % with a ±0.25 K hysteresis around 21 °C. A 0.5 K proportional band gives a steep line and a 4 K band a shallow line, both passing 50 % at the setpoint. Right, room temperature over 12 hours after a cold start at 18 °C. On/off control cycles between about 20 and 21.3 °C. The narrow band overshoots to the setpoint and settles with small damped oscillations just below it. The wide band rises smoothly and settles at about 20.3 °C, an offset of about 0.7 K below the setpoint.
:width: 100%

On/off control compared with a proportional controller with a narrow and a wide proportional band. a) Controller output against room temperature. The dashed line is the switching path when the room cools. b) Room temperature after a cold start. Simple room model with a light floor and a 12 min valve delay. The valve follows the controller output directly, so PWM is averaged out.
:::


### PWM control

The room unit runs a PI controller with a predefined duty cycle. If 40 % output is required and the cycle is 15 min, the valve is only (fully) open for about 6 min of each cycle. On average this behaves like a valve that is 40 % open.


<!-- > - **On/off control.** The loop opens when the room is below the setpoint minus a hysteresis and closes when it is above the setpoint plus the hysteresis. Not used anymore
> - **PWM control.** The room unit runs a PI controller and turns its output into a duty cycle. With a 15–20 min cycle and 40 % output, the valve is open for about 6–8 min of each cycle. On average this behaves like a valve that is 40 % open. -->



{numref}`fig-pwm-principle` shows how PWM works. The room unit compares the measured room temperature with a triangular signal that sweeps the proportional band once per cycle. The valve is open while the room is colder than the triangle. Below the band the valve stays open the whole cycle, and above the band it stays closed. Inside the band, the colder the room, the longer the valve is open in each cycle.

:::{figure} figures/ch03/pwm-principle.*
:label: fig-pwm-principle
:alt: Top, a room temperature curve wanders around a 21 °C setpoint inside a 1 K proportional band, crossed by a triangular signal with a 20 min period. Above the band the valve is always closed, below it always open. Bottom, the resulting valve signal is a series of open pulses whose length in each 20 min cycle varies from 18 % to 77 %, longest when the room is coldest.
:width: 100%

PWM control of a wax thermostat. The valve is open while the measured room temperature lies below the triangular signal. The dotted lines link one open pulse to the two crossings that start and end it. The percentages give the share of each cycle that the valve is open. Illustration with a 20 min cycle and a 1 K proportional band.
:::

PWM smooths the room temperature, but it does not remove the delay: the sensor measures the room, the valve acts on the water, but the thermal mass of the floor lies in between. Whatever the controller decides, the floor delivers it over the next 0.5–1 h (light floor) or many hours (heavy floor). When the room warms, the controller sees that and closes the valve, but it cannot take back the heat already stored in the floor.

```{admonition} Modeling time constant of floor heating
:class: dropdown

When the water flow in a loop starts or stops, the heat output to the room does not change at once. This section explains why, and what the delay means for a low-energy house.

Think of the floor above the insulation as one lump with heat capacity $C$ [J/(m²·K)] and a single temperature $T_f$. When the loop closes, the only way out for the stored heat is through the floor covering and the floor surface, a total resistance $R$ [m²·K/W], to the room at $T_r$.

Conservation of energy across lump boundaries ({numref}`fig-floor-lump-balance`):

:::{figure} figures/ch03/floor-lump-balance.*
:label: fig-floor-lump-balance
:alt: Diagram of the floor above the insulation drawn as one box with heat capacity C and temperature T_f. An arrow from the left brings energy in from the water in the pipes, zero when the loop is closed. An arrow upwards takes energy out to the room at T_r, equal to (T_f minus T_r) divided by R, through the covering and surface. A note on the right says no heat is generated inside the floor. Inside the box, the stored energy rate is C times dT_f/dt. Below the box is adiabatic insulation.
:width: 75%

Energy balance of the floor as one lump.
:::

$$
\dot E_{in} + \dot E_{gen} - \dot E_{out} = \dot E_{stored}
$$ (eq-energybalance)

When $E_{gen}$ was stoppped and $E_{in}$ is zero, it simplies to:

$$
\dot E_{stored} = - \dot E_{out} 
$$ (eq-energybalance-closed)

Think of it as a tank with water, slowly losing heat through the insulated surface. Then the stored energy changes as temperature drops over time:

$$
\frac{m c_p\, \Delta T_f}{\Delta t} = - U A\, (T_f - T_r)
$$ (eq-lump-tank)

$$
C\,\frac{\mathrm{d}T_f}{\mathrm{d}t} = -\frac{T_f - T_r}{R}
$$ (eq-lump)

The rate at which the floor cools is proportional to how much warmer it is than the room.

The solution to the equation is an exponential decay:

$$
T_f(t) - T_r = (T_{f,0} - T_r)\,e^{-t/\tau}, \qquad \tau = R\,C
$$ (eq-tau)

<!-- and since the heat output is $q = (T_f - T_r)/R$, the output decays the same way. A system that obeys {eq}`eq-lump` is called first-order: one heat store, one resistance, one time constant. For any step change in the water flow, the output approaches its new value as

$$
q(t) = q_\infty + (q_0 - q_\infty)\,e^{-t/\tau}
$$ (eq-first-order)
 -->

The time constant $\tau$ has two useful meanings:

- At $t = \tau$ the factor $e^{-1} = 0.37$ remains, so 63 % of the change has happened. After $3\tau$, 95 % has.
- If the floor kept losing heat at its initial rate, it would be empty after exactly $\tau$. The initial slope of the curve points at $t = \tau$.

%The units confirm it: J/(m²·K) × m²·K/W = J/W = s.

% ### Switching off: the whole floor discharges through the surface

When the loop closes, all the heat stored above the insulation has to leave through the flooring and the surface. $C$ is the heat capacity of the whole floor above the insulation, and $R$ is the flooring plus the surface resistance $1/h_s \approx 0.09$ m²·K/W.

We calculate when 63% of the change has happened, i.e. when the floor temperature has dropped 63% of the way from initial $T_f$ to ambient $T_r$:

- **Light floor:** $C \approx 18$ kJ/(m²·K) for the boards and plates, $R \approx 0.09 + 0.17 = 0.26$ m²·K/W (22 mm boards, λ = 0.13 W/(m·K)), so $\tau \approx 4700$ s, or about **1.3 hours**.
- **Heavy floor:** $C \approx 230$ kJ/(m²·K) for the slab, $R \approx 0.09 + 0.08 + 0.03 = 0.20$ m²·K/W (surface, parquet, upper half of the slab), so $\tau \approx 46\,000$ s, or about **13 hours**.

The flooring matters. A rug raises $R$, which lowers the output and slows the discharging of the floor.

Because $\tau = R C$, and $R$ between pipes and floor is much smaller than between floor and ambient air, the time to heat up is much lower than to cool off.


<!-- 
### Switching on: the water holds the pipe plane

When the loop opens, the water forces the pipe plane towards the water temperature. Only the layers above the pipes have to warm up, and they are fed from below through the resistance $R_\text{up}$ between the pipes and the surface, while they lose heat at the top through $1/h_s$. Seen from the stored heat, the two resistances act in parallel, and the time constant becomes

$$
\tau_\text{on} \approx C_\text{above}\,\frac{R_\text{up}\cdot(1/h_s)}{R_\text{up} + 1/h_s}
$$ (eq-tau-on)

- **Light floor:** $C_\text{above} \approx 18$ kJ/(m²·K), $R_\text{up} \approx 0.17$ m²·K/W, so $\tau_\text{on} \approx 0.3$ h.
- **Heavy floor:** $C_\text{above} \approx 120$ kJ/(m²·K), $R_\text{up} \approx 0.11$ m²·K/W, so $\tau_\text{on} \approx 1.7$ h.

Switching on is therefore much faster than switching off, by a factor of 4–8. The water drives the floor when the loop is open, but nothing drives the heat out when it closes. This asymmetry is the core of the problem: a floor heats up willingly and cools down reluctantly.

### Why one time constant is only an approximation

The lumped model assumes the floor has one temperature. That is reasonable when the resistance inside the floor is small compared with the resistance at its surface, measured by the Biot number $Bi = h\,L/\lambda$. For the concrete slab $Bi \approx 0.35$, so the slab is close to uniform, and one time constant describes it well. For the light floor the boards themselves are the main resistance ($Bi \approx 2$), but they hold little heat, so the floor still behaves almost as one lump.

In reality a floor has many layers and therefore many time constants.  -->
```









<!-- {numref}`fig-floor-step-response` shows this: the output drops quickly at first while the layers near the surface empty, then follows a long tail as heat comes up from deeper layers. The heavy floor still delivers about 12 % of its output a full day after the loop closed. The single time constant is a good summary, not the whole story.
 -->
{numref}`fig-floor-step-response` shows the temperature progression of a one-dimensional heat conduction model. The water is at 30 °C and the room at 20 °C.

:::{figure} figures/ch03/floor-step-response.*
:label: fig-floor-step-response
:alt: Two line charts of heat output to the room in percent of steady state over 24 hours. Left, after the wax thermostat opens, the light floor reaches 63 % in about half an hour and the heavy floor in about 2 hours. Right, after the wax thermostat closes, the light floor falls to 37 % in about 1 hour, while the heavy floor takes about 12 hours and still delivers about 12 % after 24 hours.
:width: 100%

Heat output of the two floors in {numref}`fig-floor-sections` after a) the wax thermostat opens and b) the wax thermostat closes. The dashed lines mark 63 % of the change. One-dimensional conduction model, water at 30 °C, room at 20 °C. Wax thermostat delay and the response of the room itself are not included.
:::


<!-- The interactive model below shows the consequence. With the default inputs, the choice between on/off and PI changes the result by a few percent. The choice between a light and a heavy floor changes it much more. -->

%{numref}`fig-floor-sections`
```{list-table} Response of the light and heavy floor (one-dimensional model, water at 30 °C, room at 20 °C)
:header-rows: 1
:label: tab-floor-response

* - 
  - Light floor
  - Heavy floor
* - Heat capacity above pipes
  - 18 kJ/(m²·K)
  - 120 kJ/(m²·K)
* - Heat capacity, whole floor above insulation
  - 33 kJ/(m²·K)
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
  - 70 Wh/m²
  - 500 Wh/m²
* - Same, in hours of full output
  - 2.5 h
  - 12 h
```

The last two rows are the ones that matter in a low-energy house. When the heavy floor's loop closes, the slab still holds about 500 Wh/m² more heat than at room temperature, and it hands this heat to the room over the next day. If the house needs 10 W/m² on average on a spring day, that is two days' heating stored in the floor. A thermostat that closes the loop when the sun comes out has no influence on this heat. The room overheats, and the heat must be removed again by opening windows or by cooling.

A light floor holds about an eighth of that heat, and most of it is released within the first hour. It follows the daily cycle much better, but it still lags behind the demand. The control loop adds more delay, and that is the subject of the section on control.


<!-- :::{admonition} Rules of thumb: floor time constants
:class: tip

- Time constant after the loop closes: $\tau \approx C_\text{floor}\,(R_\text{covering} + 0.09)$.
- Light floor with wooden boards: $\tau \approx 1$ h. Screed or concrete slab: $\tau \approx 6$–$15$ h.
- Switching on is faster than switching off, because the water drives the pipe plane but nothing drives the stored heat out.
- Heat delivered after the loop closes ≈ heat capacity × mean excess temperature of the floor. For a 100 mm slab this is several hundred Wh/m², a day or more of the heating demand of a low-energy house.
- A floor with a time constant longer than a few hours cannot follow a heating demand that changes within the day.
::: -->


### What the time constant means over a day

The heating demand of a low-energy house in early spring swings over the day, roughly as a sine with a 24-hour period, from a demand at night to a surplus when the sun shines.
A first-order system that is asked to follow such a swing does two things: it lags behind, and it delivers less of the swing than asked, because demand starts dropping before the full output is reached.

- Time Lag: The output peak lags behind the input peak.
- Attenuation: The output amplitude is reduced.

For a diurnal cycle with a period of $T = 24\text{ hours } (86{,}400\text{ s})$

- Ordinary Frequency ($f$): $f = \frac{1}{T} = 0.0417\text{ cycles/hour}$
- Angular Frequency ($\omega$): $\omega = 2\pi f = \frac{2\pi}{24\text{ h}} \approx 0.262\text{ rad/hour}$

The system's dynamic performance is governed by its amplitude ratio (the attenuation factor) and time lag (the temporal phase shift):

$$
\text{amplitude ratio} = \frac{1}{\sqrt{1 + (\omega\tau)^2}}, \qquad
\text{time lag} = \frac{\arctan(\omega\tau)}{\omega}
$$ (eq-sine-response)

The product $\omega\tau = 2\pi\,\tau/24\,\mathrm{h}$ compares the time constant with the length of the day. If the floor reacts quickly compared with the day ($\omega\tau \ll 1$), it keeps up: the amplitude ratio is close to 1 and the lag close to $\tau$. If it reacts slowly ($\omega\tau \gg 1$), the demand has already turned before the floor has warmed up. It then follows only a small part of the swing, and the lag approaches a quarter of the period, 6 h. For the light floor $\omega\tau = 0.26$; for the heavy floor $\omega\tau = 3.1$. The daily mean is always delivered in full; only the swing around it is damped and delayed.

```{list-table} Response of a first-order floor to a heating demand that swings over 24 hours
:header-rows: 1
:label: tab-floor-daily

* - Time constant $\tau$
  - Share of the swing delivered
  - Time lag
* - 1 h (light floor)
  - 97 %
  - 1.0 h
* - 2 h
  - 89 %
  - 1.8 h
* - 6 h
  - 54 %
  - 3.8 h
* - 12 h (heavy floor)
  - 30 %
  - 4.8 h
```

:::{figure} figures/ch03/floor-daily-swing.*
:label: fig-floor-daily-swing
:alt: Line chart over two days of the deviation from the daily mean, in percent of the demand swing. The heating demand is a sine peaking at 04:00 at plus 100 % and bottoming at 16:00 at minus 100 %. The light floor, time constant 1 hour, follows almost the same curve, 97 % of the swing and 1 hour late. The heavy floor, time constant 12 hours, swings only plus/minus 30 % and peaks 4.8 hours late, around 09:00.
:width: 100%

A first-order floor following a heating demand that swings over 24 hours, equation {eq}`eq-sine-response`. The arrows mark the lag behind the demand peak at 04:00. Only the swing is shown; the daily mean is delivered in full.
:::

The light floor follows the daily swing almost fully, one hour late ({numref}`fig-floor-daily-swing`). The heavy floor flattens it to a third and shifts it by nearly five hours. Heat asked for at 04:00, the coldest hour, is delivered around 09:00, just as the sun takes over. A lag of a quarter of the period is the worst case: the floor then heats hardest when the demand is changing from heating to cooling. This is why heating demand at night turns into overheating during the day.

The lag in {numref}`tab-floor-daily` is for the floor alone. The wax thermostat's dead time and stroke, the room's own heat capacity and the controller all add to it, as the section on control shows.

:::{admonition} Extra: Time constant of a thermal space
:class: dropdown
### The room has a time constant too

The same idea applies to the room or the whole house. The heat store is the heat capacity of air, furniture and internal construction, $C$, and the heat leaves through the envelope and the ventilation, with the heat loss coefficient $UA$ [W/K]. The resistance is $R = 1/UA$, so

$$
\tau_\text{room} = \frac{C}{UA}, \qquad T(t) = T_\infty + (T_0 - T_\infty)\,e^{-t/\tau_\text{room}}, \qquad T_\infty = T_\text{out} + \frac{\Phi}{UA}
$$ (eq-tau-room)

where $\Phi$ is a constant heat gain. Without gains the room cools towards the outdoor temperature. With gains it settles $\Phi/UA$ above it.

```{list-table} Time constant of a room and its temperature rise from solar gain (40 W/m² of floor, no venting). Values per m² of floor.
:header-rows: 1
:label: tab-room-tau

* - House
  - $UA$
  - $C$
  - $\tau_\text{room}$
  - Steady rise, $\Phi_\text{sol}/UA$
  - Rise after 6 h of sun
* - Older house, heavy
  - 2.5 W/(m²·K)
  - 150 kJ/(m²·K)
  - 17 h
  - 16 K
  - 5 K
* - Low-energy house, light
  - 0.6 W/(m²·K)
  - 40 kJ/(m²·K)
  - 19 h
  - 67 K
  - 18 K
* - Low-energy house, heavy
  - 0.6 W/(m²·K)
  - 150 kJ/(m²·K)
  - 69 h
  - 67 K
  - 6 K
```

The older heavy house and the light low-energy house have almost the same time constant, 17 and 19 hours. The low-energy house gets its long time constant from a small $UA$, not from mass. Insulation alone makes a light house as slow as an old heavy one. The difference is the steady temperature rise: with a small $UA$ the same gain lifts the room four times as much. The sun would heat the room 67 K above the outdoor temperature if nothing removed the heat. The room is protected only because the sun sets before that happens, and by its heat capacity, which slows the rise. Any heat from the floor comes on top of the solar gain and has nowhere to go but out of the windows.

The app below shows how fast a room cools after the heating stops. Change $UA$ and $\tau$ and compare with the three reference rooms of 20 m² floor.

```{anywidget} code/room-cooldown.mjs
{}
```

The same model in Python: {download}`room_cooldown.py <code/room_cooldown.py>`. Run it with `python room_cooldown.py --UA 12 --tau 18` to simulate one room, or without arguments to compare the reference rooms.
:::


### Control model

The model below simulates one room in a low-energy house with a light and a heavy floor ({numref}`fig-floor-sections`) over a cloudy spring day followed by a sunny one. The floor is controlled in three ways: an on/off room thermostat, a PI controller whose output is a PWM signal to the wax thermostat, and, for reference, an ideal heater that delivers exactly the heat needed without any delay. Windows are opened when the room gets too warm, and the heat removed this way is counted as heat vented.

**[Open the control model in a new tab](code/floor-control.html)**. It runs in your browser and needs no installation. {numref}`fig-floor-control-app` shows it with the default inputs.

:::{figure} figures/ch03/floor-control-app.*
:label: fig-floor-control-app
:alt: Screenshot of the control model. Sliders for room and climate, supply water, room control and wax thermostat at the top. Below, four charts over 48 hours for the light floor: room temperature, heat flux at the floor surface, supply, return and floor surface temperature, and mass flow in the loop, each comparing the ideal heater, the on/off thermostat and the PI controller with PWM. A table at the bottom lists heating energy, heat vented and hours below and above the setpoint for the three controls.
:width: 100%

The control model with the default inputs, light floor. Open the model to change the inputs and to see the heavy floor.
:::

The same model in Python, with comments on every assumption, can be downloaded here: {download}`floor_control.py <code/floor_control.py>`. Running it prints the table for the default inputs. The equations are given at the end of the chapter, in {ref}`sec-floor-model-theory`.

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
- **Shading and ventilative cooling.** Remove the solar gain or the surplus heat (see chapter 5).
- **Floor cooling.** The same pipes can cool by 20–40 W/m², limited by the dew point and a minimum floor surface temperature of about 19–20 °C. But the floor is just as slow when cooling.

The conclusion is that a heat emitter with a long time lag is a poor match for a house whose heating demand is small and changes within hours. A fast emitter, such as heating through the ventilation air or a small convector, can switch off at the moment the sun starts to heat the room.

### Several manifolds on one riser

In buildings with several floors or apartments, one riser pump often feeds a manifold on each floor, each through its own shunt ({numref}`fig-riser-shunts`). The shunt pump circulates water through the floor loops. A thermostatic valve on the return limits the supply temperature: when the sensor bulb gets too warm, it throttles the water returned to the riser, so less hot water is drawn in and more return water is mixed back through the bypass. The check valve stops riser water from flowing backwards through the bypass into the return.

:::{figure} figures/ch03/riser-shunts.*
:label: fig-riser-shunts
:alt: Schematic of a riser fed by a heat pump and a riser pump. On each of two floors, a branch from the riser supply passes a bypass junction, a shunt pump and a sensor bulb before reaching a supply manifold with three connections. The return manifold has a wax thermostat on each connection. The return passes the bypass junction and a 2-way thermostatic valve, connected to the sensor bulb by a capillary, before rejoining the riser return. The bypass between return and supply has a check valve. One floor loop is drawn in full.
:width: 100%

A riser with a riser pump feeding two floor heating manifolds, each through a shunt with its own pump, a 2-way thermostatic valve on the return and a check valve in the bypass. Three pumps in total. Only one floor loop per manifold is drawn.
:::

The check valve in the bypass is spring loaded and needs a certain pressure difference to open. This becomes a problem in a low-energy house, where the floor loops need little heat but the riser pump keeps its pressure up ({numref}`fig-riser-pump-curve`). At design load the shunts draw a large flow from the riser, and the riser pump runs at its design point A. In mild weather the thermostatic valves throttle, the flow drawn from the riser becomes small, and a constant-speed riser pump runs up its curve to almost its shut-off head (point B). The riser pressure then pushes against the bypass. Before any water can flow up through the bypass, the thermostatic valve must absorb both the riser pressure and the opening pressure of the check valve. The valve ends up almost closed with a large pressure across it, so it hunts and can be noisy, and until the check valve opens the floor loops get either too little flow or water that is too hot.

A riser pump in proportional-pressure mode lowers its head as the flow falls (point C), which makes the problem much smaller. A check valve with a low opening pressure also helps.

:::{figure} figures/ch03/riser-pump-curve.*
:label: fig-riser-pump-curve
:alt: Pump diagram with the flow drawn from the riser on the horizontal axis and differential pressure on the vertical axis. A constant-speed riser pump curve falls slowly from 45 kPa at zero flow. A proportional-pressure curve rises linearly from about 20 kPa to the same design point at 600 litres per hour and 41 kPa. Two system curves are shown, one for design and a steep one for low load. A dashed line 10 kPa above the constant-speed curve marks the pressure the thermostatic valve must absorb before the check valve opens. Point B at low load on the constant-speed curve is at about 45 kPa, and point C on the proportional-pressure curve is at about 23 kPa.
:width: 90%

Riser pump at design (A) and at low load with constant speed (B) and proportional pressure (C). The shaded band is the opening pressure of the check valve, which the thermostatic valve must absorb on top of the riser pressure before water flows through the bypass. Example values: 45 kPa shut-off head, 600 l/h design flow, 10 kPa opening pressure.
:::

(sec-floor-model-theory)=
## Theory behind the interactive model

::::{admonition} Show the equations
:class: dropdown

The model is an RC network ({numref}`fig-rc-network`). The room is one node, and the floor is split into thin layers of about 2 mm, each a node with its own heat capacity. The water reaches the floor at the pipe plane.

:::{figure} figures/ch03/rc-network.*
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
