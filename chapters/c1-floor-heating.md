# Floor heating

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

:::{admonition} Learning outcomes
:class: note

After this chapter you should be able to:

1. **Explain** why a low-energy house needs a modulating heat emitter that closely follows the heating demand.
2. **Calculate** the time constant of a light and a heavy floor from the build-up, and the heat the floor stores and still delivers after the loop closes.
3. **Judge** from the time constant whether a floor can follow a heating demand that changes over 24 hours (amplitude ratio and time lag).
4. **Describe** the control chain: heating curve, room temperature sensor, wax thermostat, on/off and PI control with PWM.
5. **Compare** light and heavy floors under on/off and PI control with PWM and different supply temperatures, on return temperature and deviation from the setpoint, using the control model.
6. **Explain** self-regulation and how a low supply temperature makes use of it, and **use** the control model to demonstrate self-regulation.
7. **Calculate** the required pre-settings for hydronic balancing, and **explain** why balancing matters for a low return temperature and what a high supply temperature does to the return temperature.
:::

# Introduction

Floor heating is the standard heat emitter in newer Danish dwellings. It is invisible, it frees wall space, and it potentially works with very low supply temperatures, which suits heat pumps and district heating very well.

Warm water from a manifold runs through a pipe loop in the floor of each room and returns a few kelvin cooler. The heat first warms the floor, and the floor surface then gives it to the room by radiation and convection ({numref}`fig-floor-principle-improved`).

:::{figure} figures/c1/floor-heating-principle.*
:label: fig-floor-principle-improved
:alt: Two panels. Left, a plan view of a room with a serpentine pipe loop: water leaves a manifold at about 30 °C, runs back and forth across the floor with legs 150–300 mm apart, changing colour from red to blue, and returns at about 25 °C. Right, a section of the same room: pipes cast in a concrete slab on insulation, under a floor covering. Wavy arrows show radiation and dashed arrows show convection from the floor to the room, and sunlight enters through a window onto the floor.
:width: 100%

Principle of hydronic floor heating. (a) One pipe loop per room, fed from a manifold. (b) Heat passes from the water into the slab, and from the floor surface to the room by radiation and convection. In a low-energy house the floor is only 1–3 K warmer than the room air.
:::

In an older house with a large heat demand it gives good comfort, with warm feet and a small vertical temperature gradient.

A low-energy house is a different case. The heat loss is small, **only 10 W per m² of floor** at design conditions, and much less on an ordinary spring or autumn day. Solar and internal gains are large in comparison, and the heat that must be supplied is so small that it has to be delivered precisely. On a clear day in April a heating demand at night can turn into a surplus by noon. The heat emitter must therefore **modulate**: it must follow the demand closely, give less as soon as the gains rise, and nothing when they cover the loss.

A floor stores heat before it reaches the room, so its output follows the water with a delay. Water put into a heavy floor at 04:00 keeps warming the room after the sun has come out and the demand has gone. The heavier the floor, the longer the delay, and the harder it is to make the floor follow the demand.

This chapter judges how well, and when, floor heating suits low-energy houses. It uses four measures that apply to any heat emitter:

- **Heating energy.** The heat delivered to the room. Heat that leaves through an open window must be paid for twice: once as heating energy, and again as discomfort.
- **Deviation from the setpoint.** The time integral of the difference between the room temperature and the setpoint, in K·h. Time below the setpoint is discomfort. Time above it is heat the room did not need, which usually leaves through an open window.
- **Return temperature.** The return water goes back to the heat source. A low return temperature lets a heat pump run at a lower condensing temperature, and in district heating it reduces the heat loss of the return pipes. It is weighted by the mass flow, because the heat source sees the mixed return of all loops.
- **Peak-to-average ratio.** The peak hourly heat output divided by the mean output over the day. The heat source and the grid must be sized for the peak, and a heat pump runs most efficiently at a steady, low output. A ratio close to 1 means the emitter draws heat evenly.

The question for the designer is whether floor heating can meet these measures as well as a fast emitter, such as an electric panel radiator or air heating, which responds within minutes. The sections on build-up, time constant, hydronics and control explain the mechanisms. {ref}`sec-floor-performance-improved` puts them together and compares a light and a heavy floor under different controls and supply temperatures with a fast emitter.

# Heat transfer of floors

A heated floor gives off heat to the room by radiation to the other surfaces and by natural convection to the air. Added together they give a heat transfer coefficient of about 11 W/(m²·K):

- **Radiation** Between surfaces in a thermal enclosure, radiative exchange is about 5 W/(m²·K) and nearly constant.
- **Convection** Convective heat transfer from a heated floor depends strongly on surface type, air speed, and forced or natural convection, but is about 6 W/(m²·K) for a heated floor.
- **Total** Convection and radiation together give about 11 W/(m²·K). Source: {cite:p}`rehva2007`

EN 1264 gives the heat flux $q$ from the mean floor surface temperature $\theta_F$ and the room temperature $\theta_i$ {cite:p}`en1264`:

$$
q = 8.92\,(\theta_F - \theta_i)^{1.1} \quad \text{W/m}^2
$$ (eq-floor-flux-improved)

For comfort, the mean floor surface temperature is limited to:
- 29 °C in occupied zones
- 33 °C in bathrooms
- 35 °C in perimeter zones

At 29 °C and a room at 20 °C, equation {eq}`eq-floor-flux-improved` gives about 100 W/m², which is far more than a low-energy house needs ({numref}`fig-en1264-curve-improved`).

:::{figure} figures/c1/en1264-curve.*
:label: fig-en1264-curve-improved
:alt: Line chart of heat flux against the difference between floor surface and room temperature, from 0 to 16 K. The curve rises almost linearly. Marked points: 1.1 K gives 10 W/m² for a low-energy house, 9 K gives 100 W/m² at the limit for occupied zones (29 °C floor, 20 °C room, or 33 °C floor and 24 °C room in bathrooms), and 15 K gives 175 W/m² at the limit for perimeter zones (35 °C floor, 20 °C room).
:width: 80%

Basic characteristic curve of a heated floor, equation {eq}`eq-floor-flux-improved`, with the floor surface temperature limits. After EN 1264 {cite:p}`en1264`. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_small_figures.py)
:::

Floor covering adds thermal resistance between the pipes and the room. Tiles add little, while wood and carpet add a lot, so a wooden floor needs a higher water temperature for the same output.


# Build-up

Floor heating constructions are often grouped by how the pipes are embedded, i.e. how much heat capacity sits between the pipes and the room ({numref}`fig-floor-sections-improved`).

:::{figure} figures/c1/floor-sections.*
:label: fig-floor-sections-improved
:alt: Two cross-sections drawn to the same scale. Left, a light floor: 22 mm floor boards resting on aluminium plates that wrap around the pipes, which sit in grooves in a 30 mm EPS panel on an 18 mm plywood board above insulation and joists. Right, a heavy floor: 14 mm parquet on a 100 mm concrete slab with the pipes in the middle of the slab, above EPS insulation.
:width: 100%

Light and heavy floor heating constructions, drawn to the same scale. The heat capacity above the pipes is about seven times larger in the heavy floor. Response times are from the model in {numref}`fig-floor-step-response-improved`.
:::

%:::{admonition} Details
%:class: dropdown

## Light floors

In a light (dry) floor the pipes lie in grooves in an insulation panel, usually EPS. Aluminium heat-diffusion plates wrap around the pipes and spread the heat sideways under the floor covering. The EPS panels rest on a plywood board on the joists, and the covering is laid directly on the plates, typically 22 mm floor boards, a floating wooden floor or gypsum fibre boards. Pipe spacing is anything between 150–300 mm, depending on pipe diameter and system.

Light floors are used on timber joists and battens, in renovation, and wherever build height and weight must be kept low. The whole construction above the insulation is 25–50 mm thick and weighs 10–30 kg/m². Its heat capacity above the pipes is **about 15–30 kJ/(m²·K)**, so there is little heat to store.

:::{figure} figures/c1/photo-light-floor.jpg
:label: fig-photo-light-floor-improved
:alt: Photo of a room under construction. The floor is covered with grooved boards and shiny aluminium heat-diffusion plates. Pink PEX pipes run in parallel straight lines in the grooves and turn in U-bends at the near end of the room. A large window is at the far end.
:width: 90%

A light floor before the floor boards are laid. The pipes lie in grooved boards under aluminium plates that spread the heat sideways. Photo: C. A. Hviid.
:::

## Heavy floors

In a heavy floor the pipes are cast into cement screed or concrete. A typical screed system has 45–65 mm of screed above the pipes. In Danish slab-on-ground houses the pipes are often tied to the reinforcement in the middle of a 100 mm concrete slab, with the floor covering laid directly on the slab. The slab weighs around 230 kg/m² and has a heat capacity of **100–250 kJ/(m²·K)**, and all of it is heated by the pipes.

:::{figure} figures/c1/photo-heavy-floor.jpg
:label: fig-photo-heavy-floor-improved
:alt: Photo of a slab on ground before casting. White EPS insulation is covered by a reinforcement mesh. Pink PEX pipes are tied to the mesh in spiral loops, with supply and return running side by side. A black membrane lines the edge of the slab.
:width: 90%

A heavy floor before the concrete is cast. The pipes are tied to the reinforcement mesh on top of the EPS insulation and end up in the middle of the slab. Photo: C. A. Hviid.
:::


# Time constant of floor heating

Several elements delay the floor's response when the heat demand of the room changes:

- **Room temperature sensor and controller.** The room must first deviate from the setpoint before the controller reacts.
- **Wax thermostat.** The wax must warm up or cool down before the valve moves. This gives a dead time of a few minutes and a stroke of a few minutes more.
- **Water flow.** At the low flow rates of floor heating the water takes several minutes to pass through a 100 m loop.
- **Heat capacity of the floor.** The floor must be charged or discharged before its surface temperature changes. This is by far the longest delay, from about an hour in a light floor to many hours in a heavy floor.

The first three add minutes to tens of minutes. Only the heat capacity of the floor is large enough to matter over a day, and the rest of this section is about that.

A floor stores heat between the pipes and the room, so its output follows the water with a delay. The delay is measured by the floor's time constant, $\tau = RC$: the heat capacity of the floor times the resistance from the floor to the room. It is the time the floor takes to complete 63 % of a change in output after the loop opens or closes. The number 63 % comes from the exponential response of a single heat store: after one time constant the remaining change has fallen to $e^{-1} = 37\,\%$. After three time constants 95 % of the change is complete. The time constant is also the time it would take to empty the store if the floor kept giving off heat at its initial rate. The derivation is in the dropdown at the end of this section. What matters here is the result, and whether a floor can deliver the heat when the room needs it.

{numref}`fig-floor-step-response-improved` and {numref}`tab-floor-response-improved` show the result of a one-dimensional heat conduction model of the two floors in {numref}`fig-floor-sections-improved`, with the water at 30 °C and the room at 20 °C.

:::{figure} figures/c1/floor-step-response.*
:label: fig-floor-step-response-improved
:alt: Two line charts of heat output to the room in percent of steady state over 24 hours. Left, after the wax thermostat opens, the light floor reaches 63 % in about half an hour and the heavy floor in about 2 hours. Right, after the wax thermostat closes, the light floor falls to 37 % in about 1 hour, while the heavy floor takes about 12 hours and still delivers about 12 % after 24 hours.
:width: 100%

Heat output of the two floors in {numref}`fig-floor-sections-improved` after a) the wax thermostat opens and b) the wax thermostat closes. The dashed lines mark 63 % of the change. One-dimensional conduction model, water at 30 °C, room at 20 °C. Wax thermostat delay and the response of the room itself are not included. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/floor_step_response.py)
:::


```{list-table} Response of the light and heavy floor (one-dimensional model, water at 30 °C, room at 20 °C)
:header-rows: 1
:label: tab-floor-response-improved

* - 
  - Light floor
  - Heavy floor
* - Heat capacity above pipes
  - 18 kJ/(m²·K)
  - 120 kJ/(m²·K)
* - Heat capacity, whole floor above insulation
  - 33 kJ/(m²·K)
  - 230 kJ/(m²·K)
* - Output after a long time with the loop open
  - 27 W/m²
  - 43 W/m²
* - Loop opens, 63 % response
  - 0.5 h
  - 2 h
* - Loop closes, 63 % response
  - 1 h
  - 12 h
* - Heat delivered after the loop closes
  - 70 Wh/m²
  - 500 Wh/m²
```

The two floors give different outputs with the same water temperature, because the resistance from the water to the room is smaller in the heavy floor (pipes cast in concrete, thin parquet) than in the light floor (pipes under 22 mm boards). To give the same output, the light floor needs warmer water.

The last two rows are the ones that matter in a low-energy house. When the heavy floor's loop closes, the slab still holds about 500 Wh/m² more heat than at room temperature, and it hands this heat to the room over the next day. If the house needs 5 W/m² on average on a spring day, that is about four days' heating stored in the floor. The room overheats, and the heat must be removed again by opening windows or by cooling.


**A light floor holds 70 Wh/m², 14 % of that heat, and most of it is released within the first hour.** It follows the demand much better, but it still lags behind it, and the control loop adds more delay.

## What the time constant means over a day

The heating demand of a low-energy house in early spring swings over the day, roughly as a sine with a 24-hour period, from a demand at night to a surplus when the sun shines. A floor with a time constant delivers only part of that swing, and delivers it delayed ({numref}`tab-floor-daily-improved`).

:::{figure} figures/c1/floor-daily-swing.*
:label: fig-floor-daily-swing-improved
:alt: Line chart over two days of the deviation from the daily mean, in percent of the demand swing. The heating demand is a sine peaking at 04:00 at plus 100 % and bottoming at 16:00 at minus 100 %. The light floor, time constant 1 hour, follows almost the same curve, 97 % of the swing and 1 hour late. The heavy floor, time constant 12 hours, swings only plus/minus 30 % and peaks 4.8 hours late, around 09:00.
:width: 100%

A first-order floor following a heating demand that swings over 24 hours, equation {eq}`eq-sine-response-improved`. The arrows mark the lag behind the demand peak at 04:00. Only the swing is shown; the daily mean is delivered in full. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_small_figures.py)
:::

The light floor follows the daily swing almost fully, one hour late ({numref}`fig-floor-daily-swing-improved`). The heavy floor flattens it to a third and shifts it by nearly five hours. Heat asked for at 04:00, the coldest hour, is delivered around 09:00, just as the sun takes over.

The figure shows only the swing around the daily mean. The heavy floor delivers the daily mean in full, but at 04:00 it delivers the mean plus only 30 % of the swing, so the room gets less than it needs and actually cools below the setpoint. To compensate, the room thermostat charges the slab further. The heavy floor therefore misses the setpoint in both directions: too cold at night and too warm in the afternoon. A lag of a quarter of the period, 6 h, is the worst case, because the floor then heats hardest when the demand is changing from heating to cooling.

::::{admonition} Extra: what would it take for the floor to follow the demand?
:class: dropdown

{numref}`fig-floor-required-input-improved` turns the question around: how much heat must the water give for the floor to deliver exactly the demand? The light floor needs almost the demand itself, one hour early. The heavy floor needs a swing 3.3 times larger, nearly 5 hours early: 21 W/m² around 23:00, and −11 W/m² around 11:00. The water would have to cool the slab during the day, which a heating system cannot do, and the control would have to know the demand 5 hours ahead, for example from a weather forecast.

:::{figure} figures/c1/floor-required-input.*
:label: fig-floor-required-input-improved
:alt: Line chart over two days of heat flux in W/m². The heating demand, black, swings as a sine between 10 W/m² at 04:00 and 0 at 16:00. The heat the water must give to a light floor, blue dashed, follows almost the same curve one hour earlier, from 0 to 10 W/m². The heat the water must give to a heavy floor, orange dashed, swings from 21 W/m² around 23:00 to minus 11 W/m² around 11:00, 4.8 hours ahead of the demand. The area below zero is shaded and labelled: the water would have to cool the floor.
:width: 100%

Heat the water must give for the floor output to follow a heating demand of 0–10 W/m² exactly, for a first-order floor with τ = 1 h and τ = 12 h. Below zero the water would have to cool the floor. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_required_input.py)
:::
::::

The lag is for the floor alone. The wax thermostat's dead time and stroke, the room's own heat capacity and the controller all add to it.

Several strategies reduce the problem, but none of them removes it:

- **Low supply temperature and self-regulation.** With the supply only a few kelvin above the room, the floor delivers less when the room warms up, even with the valve open.
- **Heating stop and a broad deadband.** Stop heating above an outdoor temperature limit, for example 12–15 °C, and use a broad deadband between the heating and cooling setpoints, so the room temperature can float more.
- **Anticipating the sun.** Lower the setpoint in the morning on sunny days, using a weather forecast or model predictive control.
- **Shading and ventilative cooling.** Remove the solar gain or the surplus heat (see Part D).
- **Floor cooling.** The same pipes can cool by 20–40 W/m², limited by the dew point and a minimum floor surface temperature of about 19–20 °C. But the floor is just as slow when cooling.


The conclusion is that a low-energy house needs a heat emitter that modulates with the demand: its output must follow a demand that is small and changes within minutes. A light floor with a time constant of about 1 hour nearly does. A heavy floor with a time constant of about 12 hours does not, whatever the control. A fast emitter, such as an electric panel radiator or air heating, follows the demand even more closely.

::::{admonition} Details: calculating the time constant
:class: dropdown

### A simple model of the floor

Think of the floor above the insulation as one lump with heat capacity $C$ [J/(m²·K)] and a single temperature $T_f$. When the loop closes, the only way out for the stored heat is through the floor covering and the floor surface, a total resistance $R$ [m²·K/W], to the room at $T_r$.

Conservation of energy across lump boundaries ({numref}`fig-floor-lump-balance-improved`):

:::{figure} figures/c1/floor-lump-balance.*
:label: fig-floor-lump-balance-improved
:alt: Diagram of the floor above the insulation drawn as one box with heat capacity C and temperature T_f. An arrow from the left brings energy in from the water in the pipes, zero when the loop is closed. An arrow upwards takes energy out to the room at T_r, equal to (T_f minus T_r) divided by R, through the covering and surface. A note on the right says no heat is generated inside the floor. Inside the box, the stored energy rate is C times dT_f/dt. Below the box is adiabatic insulation.
:width: 75%

Energy balance of the floor as one lump. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_small_figures.py)
:::

$$
\dot E_{in} + \dot E_{gen} - \dot E_{out} = \dot E_{stored}
$$ (eq-energybalance-improved)

No heat is generated in the floor, and with the loop closed nothing comes in, so:

$$
\dot E_{stored} = - \dot E_{out} 
$$ (eq-energybalance-closed-improved)

Think of it as a tank with water, slowly losing heat through the insulated surface. Then the stored energy changes as temperature drops over time:

$$
\frac{m c_p\, \Delta T_f}{\Delta t} = - U A\, (T_f - T_r)
$$ (eq-lump-tank-improved)

$$
C\,\frac{\mathrm{d}T_f}{\mathrm{d}t} = -\frac{T_f - T_r}{R}
$$ (eq-lump-improved)

The rate at which the floor cools is proportional to how much warmer it is than the room.

The solution to the equation is an exponential decay:

$$
T_f(t) - T_r = (T_{f,0} - T_r)\,e^{-t/\tau}, \qquad \tau = R\,C
$$ (eq-tau-improved)

<!-- and since the heat output is $q = (T_f - T_r)/R$, the output decays the same way. A system that obeys {eq}`eq-lump-improved` is called first-order: one heat store, one resistance, one time constant. For any step change in the water flow, the output approaches its new value as

$$
q(t) = q_\infty + (q_0 - q_\infty)\,e^{-t/\tau}
$$ (eq-first-order-improved)
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


### Response to a daily swing

A first-order system that is asked to follow a daily swing does two things: it lags behind, and it delivers less of the swing than asked, because demand starts dropping before the full output is reached.

- Time Lag: The output peak lags behind the input peak.
- Attenuation: The output amplitude is reduced.

For a diurnal cycle with a period of $T = 24\text{ hours } (86{,}400\text{ s})$

- Ordinary Frequency ($f$): $f = \frac{1}{T} = 0.0417\text{ cycles/hour}$
- Angular Frequency ($\omega$): $\omega = 2\pi f = \frac{2\pi}{24\text{ h}} \approx 0.262\text{ rad/hour}$

The system's dynamic performance is governed by its amplitude ratio (the attenuation factor) and time lag (the temporal phase shift):

$$
\text{amplitude ratio} = \frac{1}{\sqrt{1 + (\omega\tau)^2}}, \qquad
\text{time lag} = \frac{\arctan(\omega\tau)}{\omega}
$$ (eq-sine-response-improved)

The product $\omega\tau = 2\pi\,\tau/24\,\mathrm{h}$ compares the time constant with the length of the day. If the floor reacts quickly compared with the day ($\omega\tau \ll 1$), it keeps up: the amplitude ratio is close to 1 and the lag close to $\tau$. If it reacts slowly ($\omega\tau \gg 1$), the demand has already turned before the floor has warmed up. It then follows only a small part of the swing, and the lag approaches a quarter of the period, 6 h. For the light floor $\omega\tau = 0.26$; for the heavy floor $\omega\tau = 3.1$. The daily mean is always delivered in full; only the swing around it is damped and delayed.

```{list-table} Response of a first-order floor to a heating demand that swings over 24 hours
:header-rows: 1
:label: tab-floor-daily-improved

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

::::

:::{admonition} Extra: Time constant of a thermal space
:class: dropdown

The same idea applies to the room or the whole house. The heat store is the heat capacity of air, furniture and internal construction, $C$, and the heat leaves through the envelope and the ventilation, with the heat loss coefficient $UA$ [W/K]. The resistance is $R = 1/UA$, so

$$
\tau_\text{room} = \frac{C}{UA}, \qquad T(t) = T_\infty + (T_0 - T_\infty)\,e^{-t/\tau_\text{room}}, \qquad T_\infty = T_\text{out} + \frac{\Phi}{UA}
$$ (eq-tau-room-improved)

where $\Phi$ is a constant heat gain. Without gains the room cools towards the outdoor temperature. With gains it settles $\Phi/UA$ above it.

```{list-table} Time constant of a room and its temperature rise from solar gain (40 W/m² of floor, no venting). Values per m² of floor.
:header-rows: 1
:label: tab-room-tau-improved

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

# Hydronic installation

{numref}`fig-floor-loops-improved` shows a 100 m² single-storey house with one manifold and six loops of 35–95 m. The living room and kitchen need two loops to keep each below 100 m, and the bathroom has a closer pipe spacing for a warm comfort floor.

:::{figure} figures/c1/floor-loops-improved.*
:label: fig-floor-loops-improved
:alt: Floor plan of an 8 by 12.5 m house with five rooms: living and kitchen on the left, hall and bathroom in the middle, bedroom 1 and bedroom 2 on the right. The manifold sits on the hall wall next to the living room. Each room has a serpentine pipe loop drawn to scale, with dashed feed pipes from the manifold. Loop lengths: living and kitchen 95 m each, hall 38 m, bathroom 35 m with closer spacing, bedroom 1 54 m, bedroom 2 70 m.
:width: 100%

Floor heating loops in a 100 m² house, drawn to scale from the manifold. Pipe spacing 300 mm, 150 mm in the bathroom. The loop lengths include the feed pipes and are measured on the drawing. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_loops_presetting_improved.py)
:::

{numref}`fig-shunt-installation-improved` shows a typical shunt installation with manifolds and valves. The parts are the same for light and heavy floors.

:::{figure} figures/c1/hydronic-schematic-improved.*
:label: fig-shunt-installation-improved
:alt: Schematic of a hydronic floor heating system. A heat pump or district heating unit supplies water through a circulation pump to a manifold. Part of the return water goes back to the heat source through a motorized two-way valve on the primary return; the rest flows through a bypass with a check valve into the supply ahead of the pump. The controller sets the two-way valve from an outdoor sensor and a supply temperature sensor. From the manifold, one loop runs to each of three rooms. Each loop has a flow meter on the supply side and a wax thermostat on the return side, switched by a temperature sensor in its room.
:width: 100%

A hydronic floor heating installation. The controller sets the supply temperature from the outdoor temperature (heating curve). The room temperature sensor in each room opens and closes the wax thermostat on its own loop.
:::

- **Heat source.** A heat pump or district heating. Floor heating needs a low supply temperature, typically 30–35 °C in a low-energy house, with 3–5 K between supply and return.
- **Mixing shunt.** A circulation pump, a motorized two-way valve on the primary return and a bypass with a check valve. The more the two-way valve closes, the less water goes back to the heat source, and the more return water the pump draws through the bypass into the supply. This lowers the supply to the temperature set by the controller. The controller follows a heating curve, which raises the supply temperature as the outdoor temperature falls.
- **Manifold.** Distributes water to one loop per room, or several loops in large rooms. Each loop should be at most 80–100 m long to keep the pressure drop reasonable. Flow meters or balancing valves on the supply side set the design flow in each loop, so that every room gets its share (hydronic balancing).
- **Wax thermostats and room temperature sensors.** Each loop has a valve on the return side, opened and closed by a wax thermostat, an electrically heated wax actuator. The room temperature sensor switches it on and off, either directly or by pulse-width modulation (PWM). The valve only opens or closes the loop. It cannot change the water temperature.


# Hydronic balancing

**What goes wrong without balancing.** A loop that gets too much flow returns water that is almost as warm as the supply. The temperature drop $\Delta\theta$ between supply and return falls, and the return temperature rises. The room with the short loop is heated fast and the room at the end of the long loop too slowly, and the usual response is to raise the supply temperature or the pump setting until the worst room is warm. Both make the other loops worse. A high return temperature lowers the efficiency of a heat pump, and in district heating it increases the heat loss of the return pipes and is often penalised in the tariff.

:::{note} A high supply temperature gives a high return temperature
At a given flow, the difference between return and room temperature is a fixed fraction of the difference between supply and room temperature. A loop designed for 35/30 °C in a 20 °C room starts 15 K above the room and returns 10 K above it, a fraction of two thirds. With 45 °C supply and the same flow, the return is about 20 + 2/3 · 25 ≈ 37 °C: **10 K more on the supply gives about 7 K more on the return**. Raising the supply temperature to make up for poor balancing therefore pushes the return temperature up twice.
:::

The loops on a manifold are connected in parallel, so they all see the same pressure difference $\Delta p$ between the supply and return manifold. The pressure drop in a loop grows with the square of the flow,

$$
\Delta p = \left(\frac{\dot m}{K}\right)^2 \qquad\Rightarrow\qquad \dot m = K\,\sqrt{\Delta p}
$$ (eq-loop-flow-coefficient-improved)

where $K$ is the flow coefficient of the loop: the mass flow at a pressure drop of 1 bar. Manufacturers give the flow coefficient of a valve as $K_v$ in m³/h at 1 bar. $K$ for a whole loop combines the pipe and the valve. With the same $\Delta p$ on all loops, each loop gets a flow proportional to its own $K$.

:::{note} Short loops get too much water
A pipe's resistance grows with its length, so with a constant friction factor $K \propto 1/\sqrt{L}$. A 50 m loop then takes $\sqrt{2} = 1.4$ times the flow of a 100 m loop, although it usually serves a smaller room and needs less.
:::

Each loop has a design flow, set by its design heat output and a design temperature drop of typically 5 K, for example 35/30 °C. How to calculate it is covered in other courses.

**Pre-setting.** The valve on each loop has an adjustable throttle, the pre-setting, which sets its $K_v$. The installer chooses the pre-setting so that every loop gets its design flow at the same manifold pressure: long loops get a high pre-setting (open), short loops a low one (throttled). The pump sets the pressure, the pre-settings divide the flow between the loops, much like the accelerator and the gear in a car. The pre-settings must be set after the system has been filled and vented, because air in the loops changes their resistance.


The pre-setting is made on the valve insert in the manifold, with a ring numbered 1–7 and N ({numref}`fig-valve-insert-improved`a). Each setting gives its own valve characteristic: a straight line in a log–log chart of pressure drop against flow ({numref}`fig-valve-insert-improved`b).

:::{figure} figures/c1/presetting-valve-insert.jpg
:label: fig-valve-insert-improved
:alt: Two pictures side by side. a) Photo of two brass valve inserts for a floor heating manifold, each with a red pre-setting ring numbered 1 to 7 around the valve stem. b) Manufacturer chart of pressure drop, 1 to 100 kPa, against flow, 5 to 2000 l/h, on log-log axes, with eight straight parallel lines for pre-settings 1 to 7 and N. Scales below the chart convert the flow to heat output for temperature differences of 10, 15 and 20 °C.
:width: 100%

a) Valve inserts with a pre-setting ring. b) Pressure drop over the valve for pre-settings 1–7 and N, with the heat output for a temperature difference of 10, 15 and 20 °C. Chart: Danfoss.
:::

{numref}`fig-presetting-valve-improved`a shows the pre-settings for this house. The pump is set so that the loop with the largest pressure drop, one of the two 95 m loops in the living room, gets its design flow with the valve fully open (N), here 2.4 kPa over the manifold. Every other loop then has pressure to spare, and its valve must take up the difference. A short loop that needs little flow needs a low pre-setting and takes most of the 2.4 kPa in the valve.

:::{figure} figures/c1/presetting-improved.png
:label: fig-presetting-valve-improved
:alt: Two charts side by side. a) Log-log chart of pressure drop over the valve, 0.01 to 40 kPa, against flow, 5 to 1000 l/h. Eight parallel straight lines, one per pre-setting from 1 (left, most throttled) to 7 and N (fully open, drawn bold). The operating points of six loops are marked. The two living room loops sit on the N line at about 54 l/h and 0.3 kPa. The hall loop is on setting 1 at about 25 l/h and 2 kPa, the bathroom and bedroom 1 on setting 2 at about 33 l/h and 1.7–1.9 kPa, and bedroom 2 on setting 3 at about 36 l/h and 1.4 kPa. b) Bar chart of flow in kg/h for six loops, each with three bars: design flow, all valves fully open, and with pre-settings. Loops 1 and 2, living and kitchen, 95 m, setting N: all three bars about 54 kg/h. Loop 3, hall, 38 m, setting 1: design 19, open 67, pre-set 25 kg/h. Loop 4, bathroom, 35 m, setting 2: design 34, open 70, pre-set 34 kg/h. Loop 5, bedroom 1, 54 m, setting 2: design 29, open 57, pre-set 32 kg/h. Loop 6, bedroom 2, 70 m, setting 3: design 37, open 57, pre-set 36 kg/h.
:width: 100%

a) Pressure drop over a loop valve for pre-settings 1–7 and N (fully open), with the operating point of each loop in the house. Loops 1 and 2 overlap. Typical $K_v$ values for a small pre-settable valve, not product data. b) Flow in each loop with all valves fully open and with the pre-settings, compared with the design flow (35/30 °C). The manifold pressure difference is 2.4 kPa in both cases. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_loops_presetting_improved.py)
:::

{numref}`fig-presetting-valve-improved`b shows what the pre-settings achieve. With all valves fully open, the four shorter loops take 1.5–3.5 times their design flow, and the hall the most. With the pre-settings, every loop is close to its design flow. The hall still gets too much, because it would need a $K_v$ below the lowest setting. The settings come in steps, so balancing is only ever approximate.



::::{admonition} Example: balancing floor heating with virtual sensors
:class: dropdown

Sarran et al. {cite:p}`sarran2022` studied the floor heating in an 85 m² apartment in a DGNB-Gold multi-family building in Copenhagen, built in 2017 (wall U = 0.12 W/(m²·K), windows 0.95 W/(m²·K)). District heating supplies risers that serve six apartments. In each apartment a mixing shunt with its own pump (Grundfos Alpha2 L 15-60, proportional pressure) lowers the supply to the floors. A motorized valve on the return controls the mixed supply temperature, and a check valve sits in the bypass, as in {numref}`fig-riser-shunts-improved`. The kitchen/living room has two loops, the three bedrooms one each. Each loop has an on/off valve switched by the room thermostat. The floors are 14 mm wood on an 80 mm concrete slab with embedded pipes, over 93 mm insulation.

**Method.** No flows or temperatures were measured in the loops. The apartment had only the data a modern installation already logs: the room temperatures and the valve status from the thermostats (1–5 min), the supply and return temperature and the flow from the apartment's heat meter, and the current drawn by the pump (5 min), see {numref}`fig-sarran-schematic-improved`. The authors built a physical model of the installation in Modelica (Dymola), with the riser, the shunt, the pump curves, the manifold and one floor heating component per loop. Each pipe section and valve follows {eq}`eq-loop-flow-coefficient-improved`. Nine parameters were unknown: the flow coefficient of each room loop, of the bypass and of the return valve, the riser pressure difference, the gain and setpoint of the shunt controller. A genetic algorithm (ModestPy) adjusted them until the model matched the measured return temperature, heat meter flow and pump current, by minimising the sum of their normalised RMS errors. The model was fitted on 14 days and validated on the following 17 days in January 2019.

:::{figure} figures/c1/sarran-schematic.*
:label: fig-sarran-schematic-improved
:alt: Schematic of the apartment installation. District heating risers on the left. The supply branch passes a supply riser temperature sensor, a tee where a bypass with a check valve joins from the return, the mixed supply temperature, the pump and the total flow before the supply manifold. One floor loop is drawn as a serpentine in a room; four more loops are dashed. The return manifold has an on/off valve on each loop. The return branch passes the bypass tee, a motorized valve and a heat meter that measures the flow and return riser temperature. Filled red dots mark measured model inputs (supply riser temperature, room temperature, valve status), filled blue dots measured outputs used to fit the model (metered flow, return riser temperature, pump current), and open teal circles the variables the model estimates (mixed supply temperature, total flow, loop flow, loop return temperature, floor surface temperature, room heat output).
:width: 100%

The apartment installation with the measured and the virtually sensed variables. Redrawn from {cite:t}`sarran2022`, Fig. 3, CC BY 4.0. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/sarran_schematic.py)
:::

This is a grey-box model: physics with parameters fitted to data. Once calibrated, it works as a virtual heat meter on every loop. It gives the flow, return temperature and heat output of each room, which nobody had measured.

**Fit.** The model matched the pump current and heat meter flow well (NRMSE 0.05 and 0.04). The return temperature was the hardest, with a systematic error of −1.4 K on the energy-weighted mean.

**Findings.** The virtual sensors showed an installation running far from its design ({numref}`tab-sarran-diagnosis-improved`).

:::{list-table} Virtually sensed values in the apartment, January 2019, compared with design {cite:p}`sarran2022`
:header-rows: 1
:label: tab-sarran-diagnosis-improved
* -
  - Found
  - Design or guideline
* - Mixed supply temperature setpoint
  - 45.6 °C
  - 35 °C
* - Flow in each bedroom loop
  - 0.08–0.13 kg/s (290–470 kg/h)
  - 0.01–0.03 kg/s (36–110 kg/h)
* - Cooling of the water in the bedroom loops
  - about 2 K
  - 5 K
* - Peak output per bedroom loop
  - 400–600 W
  - 250–350 W
* - Floor surface temperature
  - 26–29 °C
  - at most 27 °C for wooden floors
:::

The loop flows were 4–10 times the design flow, so the water cooled only about 2 K in the bedrooms and the return to the riser was 38–40 °C. With 45.6 °C supply the floors heated the rooms 1 K in 6–12 hours, then switched off for 1–2 days while the slab discharged. One bedroom kept its loop open for days and probably heated the living room through the wall, since the living room's own loop did not open in that period.

**Improvements.** The calibrated model was then used to test changes before anyone touched the installation ({numref}`fig-sarran-return-temps-improved`):

1. **Lower mixed supply temperature, no balancing.** With all loops open, the model found the lowest setpoint that still covered the measured heat demand of the apartment. 35 °C was enough when the demand of the rooms was added up, which matches the design.
2. **Lower pump curve.** Switching the pump to its lower proportional-pressure curve changed the return temperature only a little, because the loops stayed unbalanced.
3. **Balancing.** The flow coefficients of the loops were reduced, in the model, until each loop got its design flow from a dimensioning tool: 0.022 kg/s in each living room loop, 0.017 kg/s in bedroom 1 and 0.012 kg/s in bedrooms 2 and 3. In the installation this corresponds to new pre-settings on the loop valves.

{numref}`fig-sarran-pump-curves-improved` shows why the lower pump curve alone did little. The loops were so open that the system curve was flat, and the pump ran at high flow on either curve (points 1 and 2). Only the smaller flow coefficients after balancing make the system curve steep, so the flow falls to about a sixth (point 3).

:::{figure} figures/c1/sarran-pump-curves.*
:label: fig-sarran-pump-curves-improved
:alt: Pump diagram with water flow from 0 to 0.8 kg/s and pump head from 0 to 45 kPa. Two proportional-pressure pump curves, high and low, and two parabolic system curves. Point 1, as found, is on the high pump curve at about 0.54 kg/s and 32 kPa. Point 2, low pump curve, is at about 0.41 kg/s and 18 kPa. Point 3, low pump curve with balanced loops, is on a much steeper system curve at about 0.09 kg/s and 13 kPa.
:width: 90%

Pump curves and operating points with all loops open: 1 as found, 2 low pump curve, 3 low pump curve and balanced loops. Values read from {cite:t}`sarran2022`, Fig. 11, CC BY 4.0. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/sarran_pump_curves.py)
:::


{numref}`fig-sarran-return-temps-improved` shows the return temperature for each scenario at decreasing supply setpoints. The lower pump curve alone lowered the return by 0.2–0.6 K. Balancing lowered it by 1.5–3.5 K at the same setpoint, most at the highest setpoints. With balanced loops, 37 °C was the lowest setpoint the model found sufficient, which gives 8.6 K lower supply and 6.5 K lower return than the installation as found. The balanced loops also cut the pump power to about a third.

:::{figure} figures/c1/sarran-return-temps.*
:label: fig-sarran-return-temps-improved
:alt: Grouped bar chart of the energy-weighted mean return temperature to the riser against the mixed supply temperature setpoint, 45.6, 43, 40, 37, 35 and 33 °C. Three bars per setpoint: as found 37.5, 36.4, 34.4, 32.5, 31.3, 30.2 °C; lower pump curve 36.9, 35.9, 34.1, 32.2, 31.1, 30.0 °C; lower pump curve with balancing 34.0, 33.1, 32.0, 31.0, 30.4, 29.9 °C. The balanced case at 35 °C and all three cases at 33 °C are hatched, meaning that the heat demand of the apartment was not covered.
:width: 90%

Energy-weighted mean return temperature to the riser for the improvement scenarios, with all loops open. Hatched bars: the heat demand of the apartment was not covered. Redrawn from {cite:t}`sarran2022`, Fig. 12, CC BY 4.0; the as-found values are from their Table 7, the others read from the figure. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/sarran_return_temps.py)
:::

Two limits should be kept in mind. The model's return temperature was biased by −1.4 K, and the model did not reproduce the shunt well at low setpoints: a setpoint of 35 °C gave at most 32.5 °C, which is why balancing plus 35 °C did not cover the demand.
::::

# Control of floor heating

Floor heating has two levels of control ({numref}`fig-shunt-installation-improved`). The supply temperature follows a heating curve, set from the outdoor temperature. Each room then switches its own loop with a wax thermostat, driven by its room temperature sensor.

A wax thermostat is an on/off valve ({numref}`fig-wax-thermostat-improved`). A small heater warms a wax capsule, the wax expands and pushes the valve open. It takes 2–3 min before the valve starts to move and another 3–5 min to open fully, and about the same to close.

:::{figure} figures/c1/wax-actuators-manifold.jpg
:label: fig-wax-thermostat-improved
:alt: Photo of six wax thermostats from different makers, side by side on the valve connections of a brass floor heating manifold. They are small cylindrical or box-shaped actuators, mostly white, one dark grey with a blue top, each screwed onto a valve with a knurled ring, and each with a cable to the room unit.
:width: 90%

Wax thermostats (thermoelectric actuators) from different makers, mounted on the valves of a floor heating manifold. Each one opens or closes one loop. Photo: Harold2013, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Thermische_Stellantriebe,_Thermische_Antriebe,_Fussbodenheizung,_thermal_actuator,_actuateur_thermique.jpg), CC0.
:::

:::{note} A wax thermostat is either open or closed
The wax thermostat cannot hold positions between fully open and fully closed. It is therefore controlled either on/off or with pulse-width modulation (PWM).
:::

## On/off

The loop opens when the room is below the setpoint minus a hysteresis and closes when it is above the setpoint plus the hysteresis. On/off control swings the room between about 20 and 21.3 °C, well outside the ±0.25 K hysteresis, because the floor keeps heating after the valve closes and keeps lagging after it opens ({numref}`fig-proportional-band-improved`).

:::{figure} figures/c1/proportional-band.*
:label: fig-proportional-band-improved
:alt: Left, controller output in percent against room temperature. On/off control jumps between 0 and 100 % with a ±0.25 K hysteresis around 21 °C. A 0.5 K proportional band gives a steep line and a 4 K band a shallow line, both passing 50 % at the setpoint. Right, room temperature over 12 hours after a cold start at 18 °C. On/off control cycles between about 20 and 21.3 °C. The narrow band overshoots to the setpoint and settles with small damped oscillations just below it. The wide band rises smoothly and settles at about 20.3 °C, an offset of about 0.7 K below the setpoint.
:width: 100%

On/off control compared with proportional control with a narrow and a wide proportional band, as achieved on average with PWM. a) Controller output against room temperature. The dashed line is the switching path when the room cools. b) Room temperature after a cold start. Simple room model with a light floor and a 12 min valve delay. The valve follows the controller output directly, so PWM is averaged out. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/pband_figure.py)
:::

<!-- In this example the room needs more than 50 % output, and a proportional controller only gives more than 50 % when the room is below the setpoint. This remaining deviation is the offset. The I part of a PI controller removes it. -->


## Pulse-width-modulation (PWM)

With PWM the room unit runs a P or PI controller and turns its output into a duty cycle for the wax thermostat. If 40 % output is required and the cycle is 15 min, the valve is only (fully) open for about 6 min of each cycle. On average this behaves like a valve that is 40 % open.


<!-- > - **On/off control.** The loop opens when the room is below the setpoint minus a hysteresis and closes when it is above the setpoint plus the hysteresis. Not used anymore
> - **PWM control.** The room unit runs a PI controller and turns its output into a duty cycle. With a 15–20 min cycle and 40 % output, the valve is open for about 6–8 min of each cycle. On average this behaves like a valve that is 40 % open. -->



{numref}`fig-pwm-principle-improved` shows how PWM works. The room unit compares the measured room temperature with a triangular signal that sweeps the proportional band once per cycle. The valve is open while the room is colder than the triangle. Below the band the valve stays open the whole cycle, and above the band it stays closed. Inside the band, the colder the room, the longer the valve is open in each cycle. The triangular signal plays the same role as the proportional band of a proportional controller: it sets how far the room must deviate before the valve is fully open or fully closed.

:::{figure} figures/c1/pwm-principle-improved.*
:label: fig-pwm-principle-improved
:alt: Top, a room temperature curve wanders around a 21 °C setpoint inside a 1 K proportional band, crossed by a triangular signal with a 20 min period. Above the band the valve is always closed, below it always open. Bottom, the resulting valve signal is a series of open pulses whose length in each 20 min cycle varies from 18 % to 77 %, longest when the room is coldest.
:width: 100%

PWM control of a wax thermostat. The valve is open while the measured room temperature lies below the triangular signal. The dotted lines link one open pulse to the two crossings that start and end it. The percentages give the share of each cycle that the valve is open. Illustration with a 20 min cycle and a 1 K proportional band. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/pwm_figure_improved.py)
:::


Averaged over a cycle, PWM makes the on/off valve act like a valve controlled by a proportional controller. {numref}`fig-proportional-band-improved` compares this average behaviour with plain on/off control. The width of the proportional band is set in the room unit:

- A narrow band settles close to the setpoint after a few damped oscillations.
- A wide band gives a smooth response, but the room settles about 0.7 K below the setpoint. The I part of a PI controller removes this offset.



## Self-regulation
In low-energy houses with very small heating demands, floor heating shows strong self-regulation. The floor surface is only a little warmer than the room, so a small rise in room temperature removes much of the output, without any controller ({numref}`fig-floor-self-regulation-improved`a). If the room becomes warmer than the floor, the floor cools the room, though less effectively than it heats, because warm air above a cool floor is stable {cite:p}`en1264`.

Over a sunny day the same slab therefore heats the room at night and cools it in the afternoon, without anything switching ({numref}`fig-floor-self-regulation-improved`b).

:::{figure} figures/c1/floor-self-regulation-low.*
:label: fig-floor-self-regulation-improved
:alt: Two charts. Left, heat flux from the floor against room temperature from 19 to 26 °C for a floor surface at 22 °C. The line falls through 19 W/m² at 20 °C and 9 W/m² at 21 °C to zero at 22 °C, shaded orange and labelled floor heats. Above 22 °C it continues down, less steeply, through minus 7 W/m² at 23 °C, shaded blue and labelled floor cools. Right, over 24 hours the room temperature swings as a sine between 21 °C at 03:00 and 23 °C at 15:00, around a constant floor surface temperature of 22 °C. The heat flux is positive, up to 9 W/m² at 03:00, until about 09:00, then negative, down to minus 7 W/m² at 15:00, until about 21:00, then positive again.
:width: 100%

Self-regulation of a floor with its surface at 22 °C. a) Heat flux against room temperature; EN 1264 characteristic for heating, 7 W/(m²·K) for cooling. b) The same floor over a sunny day with the room swinging ±1 K around the floor temperature. Illustration: the floor surface is held constant, which a heavy floor with a low, constant supply temperature roughly does. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_self_regulation_low.py)
:::

Self-regulation works best when the floor surface temperature is close to the room temperature, which requires a low supply temperature. With a high supply temperature the floor never cools, and a warmer room only trims its output a little. Self-regulation is also no substitute for control: in {numref}`fig-floor-self-regulation-improved`b the room still swings by 2 K, and the heat delivered at night adds to the afternoon overheating.







# Interactive control model

The model below simulates one room in a low-energy house with a light and a heavy floor ({numref}`fig-floor-sections-improved`) over a cloudy spring day followed by a sunny one. The floor is controlled in three ways: an on/off room thermostat, a PI controller whose output is a PWM signal to the wax thermostat, and, for reference, an ideal heater that delivers exactly the heat needed without any delay. The ideal heater stands for a fast emitter, such as an electric panel radiator or air heating. Windows are opened when the room gets too warm, and the heat removed this way is counted as heat vented.

**[Open the control model in a new tab](code/floor-control_improved.html)**. It runs in your browser and needs no installation. {numref}`fig-floor-control-app-improved` shows it with the default inputs.

:::{figure} figures/c1/floor-control-app-improved.*
:label: fig-floor-control-app-improved
:alt: Screenshot of the control model. Sliders for room and climate, supply water, room control and wax thermostat in a column on the left. In the middle, four charts over 48 hours for the light floor: room temperature, heat flux at the floor surface, supply, return and floor surface temperature, and mass flow in the loop, each comparing the ideal heater, the on/off thermostat and the PI controller with PWM. A table on the right lists heating energy, heat vented, degree hours below and above the setpoint and the return temperature for the three controls.
:width: 100%

The control model with the default inputs, light floor. Open the model to change the inputs and to see the heavy floor.
:::

The same model in Python, with comments on every assumption, can be downloaded here: {download}`floor_control_improved.py <code/floor_control_improved.py>`. Running it prints the table for the default inputs. The equations are given in the dropdown below.

(sec-floor-model-theory-improved)=
::::{admonition} Control model equations
:class: dropdown

## Theory behind the interactive model

:::{caution}
Needs review
:::

The model is an RC network ({numref}`fig-rc-network-improved`). The room is one node, and the floor is split into thin layers of about 2 mm, each a node with its own heat capacity. The water reaches the floor at the pipe plane.

:::{figure} figures/c1/rc-network.*
:label: fig-rc-network-improved
:alt: RC network of the model. The room node is connected to the outdoor temperature through the resistance one over H loss, has the heat capacity C r, receives solar and internal gains and loses vented heat. Below it, a chain of resistances and capacitances represents the floor layers from the surface to an adiabatic underside. The two nodes either side of the pipe plane are connected to the supply water temperature through the water conductance g w, which the wax thermostat switches.
:width: 75%

RC network behind the interactive model. Each floor layer is split into nodes of about 2 mm. The wax thermostat sets the mass flow and so the conductance $g_\mathrm{w}$ between the supply water and the pipe plane.
:::

**Room node.** The heat balance of the room is

$$
C_\mathrm{r}\frac{\mathrm{d}T_\mathrm{r}}{\mathrm{d}t} = H_\mathrm{loss}(T_\mathrm{out}-T_\mathrm{r}) + G_\mathrm{s}(T_1-T_\mathrm{r}) + \Phi_\mathrm{sol} + \Phi_\mathrm{int} + \Phi_\mathrm{ideal} - \Phi_\mathrm{vent}
$$ (eq-room-node-improved)

where $G_\mathrm{s} = 1/(1/h_\mathrm{s} + \Delta z_1/2\lambda_1)$ links the room to the top floor node through the surface coefficient $h_\mathrm{s} = 10.8$ W/(m²·K). The term $G_\mathrm{s}(T_1-T_\mathrm{r})$ is the heat flux from the floor surface shown in the app. $\Phi_\mathrm{ideal}$ is only used for the ideal heater.

**Floor nodes.** Each floor node $i$ exchanges heat with its neighbours by conduction:

$$
C_i\frac{\mathrm{d}T_i}{\mathrm{d}t} = G_{i-1,i}(T_{i-1}-T_i) + G_{i,i+1}(T_{i+1}-T_i) + g_\mathrm{w}(T_\mathrm{sup}-T_i)
$$ (eq-floor-node-improved)

with $C_i = \rho_i c_i \Delta z_i$ and $G_{i,i+1} = 1/(\Delta z_i/2\lambda_i + \Delta z_{i+1}/2\lambda_{i+1})$. The last term only applies to the two nodes either side of the pipe plane. The bottom node has no neighbour below, so the underside is adiabatic. The heat loss of the room is all in $H_\mathrm{loss}$.

**Water to floor.** The mass flow is proportional to the wax thermostat position $y$ (0 closed, 1 open), $\dot m = y\,\dot m_\mathrm{design}$. The heat transfer from the water uses an effectiveness model with $UA = 1/R_\mathrm{pipe}$, split equally on the two pipe nodes:

$$
g_\mathrm{w} = \tfrac{1}{2}\,\dot m c_p\left(1-e^{-UA/\dot m c_p}\right), \qquad
T_\mathrm{ret} = T_\mathrm{sup} - \frac{\Phi_\mathrm{w}}{\dot m c_p}
$$ (eq-water-improved)

where $\Phi_\mathrm{w} = \sum g_\mathrm{w}(T_\mathrm{sup}-T_p)$ is the heat delivered to the floor. As the flow falls, the water cools more on its way through the loop, so the return temperature drops.

$R_\mathrm{pipe}$ is the thermal resistance per m² floor between the bulk water and the pipe plane. It is the resistance per metre of pipe, $R'$ in m·K/W, times the pipe spacing $s$:

$$
R_\mathrm{pipe} = s\left(\frac{1}{h_\mathrm{i}\,\pi d_\mathrm{i}} + \frac{\ln(d_\mathrm{o}/d_\mathrm{i})}{2\pi\lambda_\mathrm{pipe}}\right)
$$ (eq-r-pipe-improved)

For a PEX pipe 16 × 2 mm ($\lambda_\mathrm{pipe}$ = 0.35 W/(m·K)) with turbulent flow ($h_\mathrm{i} \approx$ 1600 W/(m²·K)), the convection term is 0.017 m·K/W and the pipe wall 0.13 m·K/W. The wall dominates.

- **Heavy floor**, spacing 200 mm: $R_\mathrm{pipe}$ = 0.2 × 0.15 ≈ 0.03 m²·K/W, the value used in the model. The model leaves out the spreading resistance in the concrete from the round pipe to the mean temperature of the pipe plane, which is about as large again ($R' \approx \ln(s/\pi d_\mathrm{o})/2\pi\lambda_\mathrm{c} \approx$ 0.13 m·K/W).
- **Light floor**, spacing 300 mm: convection and wall give 0.3 × 0.15 ≈ 0.045 m²·K/W. The contact between the pipe and the aluminium plate and the spreading along the plate to the space between the pipes add to this. The model uses an estimated 0.10 m²·K/W.

$R_\mathrm{pipe}$ mostly sets how much the water cools in the loop. Doubling it for the heavy floor raises the return temperature by about 0.5 K and changes the heating energy and the deviation by a few per cent. The time constant is set by the heat capacity of the floor, not by $R_\mathrm{pipe}$.

**Supply temperature and climate.** The heating curve and the boundary conditions are

$$
T_\mathrm{sup} = \min\!\left(T_\mathrm{sup,max},\; 20 + s\,(20-T_\mathrm{out})\right), \quad
T_\mathrm{out} = 7 - 5\cos\frac{2\pi(t-3)}{24}, \quad
\Phi_\mathrm{sol} = \hat\Phi_\mathrm{sol}\max\!\left(0, \sin\frac{\pi(t-7)}{12}\right)
$$ (eq-boundary-improved)

with $t$ in hours and $s$ the heating curve slope. With $s = 0$ the supply is constant at $T_\mathrm{sup,max}$. The outdoor temperature is 2 °C at 03:00 and 12 °C at 15:00. The sun shines from 07:00 to 19:00 with the peak $\hat\Phi_\mathrm{sol}$ at 13:00.

**Control.** The on/off controller opens the loop below $T_\mathrm{set} - \Delta T_\mathrm{hyst}$ and closes it above $T_\mathrm{set} + \Delta T_\mathrm{hyst}$. The PI controller computes, at the start of each PWM cycle,

$$
u = K_p e + \frac{K_p}{T_i}\int e\,\mathrm{d}t, \qquad e = T_\mathrm{set}-T_\mathrm{r}, \qquad K_p = 1/X_p
$$ (eq-pi-improved)

where $X_p$ is the proportional band. The output $u$ (0–1, with anti-windup) is the duty cycle: the loop is open for the first $u\,t_\mathrm{cycle}$ of each cycle. The wax thermostat follows the signal after a dead time and then moves at the rate $1/t_\mathrm{stroke}$, separately for opening and closing.

The ideal heater supplies what the room needs to stay at the setpoint, with the room correcting itself in 10 min:

$$
\Phi_\mathrm{ideal} = \max\!\left(0,\; H_\mathrm{loss}(T_\mathrm{set}-T_\mathrm{out}) - \Phi_\mathrm{sol} - \Phi_\mathrm{int} + C_\mathrm{r}\frac{T_\mathrm{set}-T_\mathrm{r}}{600\ \mathrm{s}}\right)
$$ (eq-ideal-improved)

**Venting.** When the room exceeds $T_\mathrm{vent}$, the windows remove the excess at once: $T_\mathrm{r}$ is reset to $T_\mathrm{vent}$ and the heat removed, $C_\mathrm{r}(T_\mathrm{r}-T_\mathrm{vent})$, is counted as heat vented.

**Solution.** The equations are solved with implicit Euler time steps of 60 s. Each step is a tridiagonal linear system, solved directly. The results in the table are sums over the two days shown: the heating energy $\int\Phi_\mathrm{w}\,\mathrm{d}t$, the heat vented, and the deviation from the setpoint, $\int\max(0, T_\mathrm{set}-T_\mathrm{r})\,\mathrm{d}t$ below and $\int\max(0, T_\mathrm{r}-T_\mathrm{set})\,\mathrm{d}t$ above, in K·h.
::::

:::{admonition} Model assumptions
:class: note

- One-dimensional heat conduction in the floor; the underside is adiabatic.
- The room is one node with the heat capacity of air, furniture and light internal parts (40 kJ/(m²·K)). All solar gain heats this node.
- Outdoor temperature varies between 2 °C at 03:00 and 12 °C at 15:00 on both days. The supply temperature follows a heating curve, or is constant if the slope is set to 0.
- The loop mass flow is proportional to the valve position, 6 kg/(h·m²) fully open by default. That is a conventional design flow, about 35 W/m² at a 5 K drop, and about 3.5 times what this low-energy room needs at design conditions (1.7 kg/(h·m²) for 10 W/m²). Heat transfer from the water to the pipe plane uses an effectiveness (NTU) model, which gives the return temperature.
- The wax thermostat opens after a dead time and then moves linearly to fully open; it closes after 2 min and over 5 min.
- Four cloudy days are simulated before the two days shown, so the floors start in a realistic state.
:::

(sec-floor-performance-improved)=
# Control comparison

{numref}`fig-floor-performance-improved` compares the light and the heavy floor with on/off and PI control for two supply strategies:

- a constant supply of 40 °C,
- the default heating curve (24.8–30.8 °C).

Both are compared with a self-regulation strategy: a fixed supply temperature of 23 °C and a fixed flow, with the loop always open and no room control. The dashed lines show the ideal heater.

:::{figure} figures/c1/floor-performance.*
:label: fig-floor-performance-improved
:alt: Four bar charts in a 2 by 2 grid, each with two blocks, light floor and heavy floor. In each block, on/off and PI with PWM have two bars, for 40 °C constant supply and for the heating curve, and a third, blue bar shows self-regulation with 23 °C fixed supply and the loop always open. a) Heating energy over both days in Wh/m². Light: on/off 172 and 146, PI 145 and 148, self-regulation 113. Heavy: on/off 192 and 164, PI 149 and 165, self-regulation 121. Dashed lines mark the ideal heater at 130 and 122 Wh/m². b) Deviation from the setpoint over the cloudy day in K·h. Light: on/off 36 and 19, PI 15 and 16, self-regulation 24. Heavy: on/off 42 and 34, PI 32 and 33, self-regulation 21. Dashed lines mark the ideal heater at 10 and 6 K·h. c) Flow-weighted return temperature on the cloudy day. Light: on/off 30.8 and 26.2, PI 25.7 and 24.3, self-regulation 22.5 °C. Heavy: on/off 24.2 and 23.3, PI 23.3 and 23.1, self-regulation 22.5 °C. d) Peak-to-average ratio of the hourly heat input on the cloudy day. Light: on/off 11.4 and 7.4, PI 7.1 and 5.4, self-regulation 1.9. Heavy: on/off 13.5 and 8.1, PI 9.3 and 6.5, self-regulation 1.5. Dashed lines mark the ideal heater at 2.6 and 2.4.
:width: 100%

Light and heavy floor with on/off and PI control with PWM, for two supply strategies, compared with self-regulation (23 °C fixed, loop always open, no room control) and the ideal heater (dashed). a) Heating energy over both days. b) Deviation from the 21 °C setpoint, below plus above, on the cloudy day. c) Return temperature on the cloudy day, weighted by the mass flow. d) Peak-to-average ratio: the highest hourly mean heat input divided by the mean over the cloudy day. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_floor_performance.py)
:::

- **Heating energy.** A light floor uses about as much heat as the ideal heater: 11–14 % more with PI control, and 13 % less with the loop open at 23 °C.
- **Deviation from the setpoint.** Light floors perform closer to the ideal heater than heavy floors.
- **Return temperature.** Across floor types, a low supply temperature carries through to a low return temperature, and especially in light floors self-regulation always gives a low return temperature. There are concerns, however: rooms may need different amounts of heat, because of their orientation and their internal gains.
- **Peak-to-average ratio.** Room control makes the load peaky: the peak hour is 5–14 times the daily mean, against about 2.5 for the ideal heater. PI control and the heating curve lower the ratio. Self-regulation gives the steadiest load, 1.5–1.9, because the floor takes heat whenever the room is cooler than the floor. The ratio is computed from hourly means, since a heat source serving many loops sees a smoother load than the PWM pulses of one loop.

A heavy floor does worse: it uses up to 57 % more heat and deviates up to 36 K·h more than the ideal heater, unless the supply temperature is kept low.


## Self-regulation in the control model

{numref}`fig-floor-self-regulation-setpoint-improved` compares the heavy floor with two strategies. In the first, the supply is a constant 40 °C and a PI controller with PWM switches the loop to hold 21 °C. In the second, the supply is a constant 23 °C and the loop is always open: there is no room control at all, only self-regulation.

The main points:

- **Self-regulation alone holds the room.** With the loop always open, the room stays between 20.9 and 23.0 °C on the cloudy day, closer to 21 °C than with PI control at 40 °C (20.6–23.6 °C). The water gives at most 5 W/m², more when the room is cool and less when it is warm.
- **Less heat, less overheating.** The open loop uses about a fifth less heat than PI control at 40 °C.
- **A low and steady return temperature.** At 23 °C the return stays at 22.3–23.3 °C. At 40 °C it rises from 22 to 24 °C each time the slab is charged.

:::{figure} figures/c1/floor-self-regulation-setpoint.*
:label: fig-floor-self-regulation-setpoint-improved
:alt: Four stacked line charts over 48 hours, a cloudy day followed by a sunny day, for the heavy floor with a 21 °C setpoint. Two cases: constant supply 40 °C with PI control and PWM, and constant supply 23 °C with the loop always open. a) Room temperature: with 40 °C and PI the room dips to 20.6 °C at night and peaks at 23.6 °C on the cloudy day; with 23 °C and the loop open it stays between 20.9 and 23.0 °C. Both reach 24 °C on the sunny afternoon. b) Heat from the water to the floor: with 40 °C short PWM pulses up to about 120 W/m² between 01:00 and 05:00 on the cloudy day only; with 23 °C a smooth 2 to 5 W/m², highest in the morning, falling slightly below zero on the sunny afternoon. c) Heat flux at the floor surface: peaks of about 13 W/m² with 40 °C and 7.5 W/m² with 23 °C in the early morning, slightly negative from noon to 18:00 on the cloudy day, and down to minus 9 to minus 11 W/m² on the sunny afternoon. d) Return temperature: with 40 °C rising from 22 to about 24 °C during charging; with 23 °C a smooth 22.3 to 23.3 °C. Thin lines mark the flow-weighted means over the cloudy day, 23.3 and 22.5 °C.
:width: 100%

Self-regulation of the heavy floor in the control model, setpoint 21 °C. Constant supply of 40 °C with PI control and PWM, and constant supply of 23 °C with the loop always open (no room control). a) Room temperature. b) Heat from the water to the floor, cut at 40 W/m². c) Heat flux at the floor surface; negative values mean that the floor takes heat from the room. d) Return temperature while the valve is open, with the flow-weighted mean over the cloudy day as thin lines. Default inputs otherwise. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/c1_self_regulation_setpoint.py)
:::

:::{admonition} Try it in the control model
:class: seealso

Open the [control model](code/floor-control_improved.html), select the heavy floor and set the heating curve slope to 0, so the supply temperature is constant.

1. Set the max supply temperature to 35 °C and then to 25 °C. How do the heat flux at the floor surface and the room temperature change on the cloudy day?
2. Lower the supply temperature further, to 23 °C and 22 °C. When does the room start to fall below the setpoint at night? What happens to the return temperature?
3. Repeat with the light floor. Why does a low supply temperature help the light floor less?
:::

:::{admonition} Take-aways for low-energy houses
:class: tip

- **Heating energy.** A light floor with PI control uses only 11–14 % more heat than an ideal heater. A heavy floor uses 22–35 % more, because heat stored at night comes out when the sun already heats the room.
- **Deviation from the setpoint.** In a heavy floor, keep the supply temperature low. The floor then limits its own output, and the room overheats less.
- **Return temperature.** With PI control and the heating curve, floor heating returns the water 2–3.5 K above the setpoint, and with self-regulation only about 1.5 K, which suits a heat pump or district heating. On/off control at 40 °C supply loses this advantage in a light floor, with a return near 31 °C.
- **Peak-to-average ratio.** Room control makes the load peaky, 5–14 times the daily mean. A low, steady supply temperature without room control gives the steadiest load, below 2.
:::

# Several manifolds on one riser (needs revision)

In buildings with several floors or apartments, one riser pump often feeds a manifold on each floor, each through its own shunt ({numref}`fig-riser-shunts-improved`). The shunt pump circulates water through the floor loops. A thermostatic valve on the return limits the supply temperature: when the sensor bulb gets too warm, it throttles the water returned to the riser, so less hot water is drawn in and more return water is mixed back through the bypass. The check valve stops riser water from flowing backwards through the bypass into the return.

:::{figure} figures/c1/riser-shunts.*
:label: fig-riser-shunts-improved
:alt: Schematic of a riser fed by a heat pump and a riser pump. On each of two floors, a branch from the riser supply passes a bypass junction, a shunt pump and a sensor bulb before reaching a supply manifold with three connections. The return manifold has a wax thermostat on each connection. The return passes the bypass junction and a 2-way thermostatic valve, connected to the sensor bulb by a capillary, before rejoining the riser return. The bypass between return and supply has a check valve. One floor loop is drawn in full.
:width: 100%

A riser with a riser pump feeding two floor heating manifolds, each through a shunt with its own pump, a 2-way thermostatic valve on the return and a check valve in the bypass. Three pumps in total. Only one floor loop per manifold is drawn.
:::

The check valve in the bypass is spring loaded and needs a certain pressure difference to open. This becomes a problem in low-energy apartment buildings, where the floor loops need little heat but the riser pump keeps its pressure up ({numref}`fig-riser-pump-curve-improved`). At design load the shunts draw a large flow from the riser, and the riser pump runs at its design point A. In mild weather the thermostatic valves throttle, the flow drawn from the riser becomes small, and a constant-speed riser pump runs up its curve to almost its shut-off head (point B). The riser pressure then pushes against the bypass. Before any water can flow up through the bypass, the thermostatic valve must absorb both the riser pressure and the opening pressure of the check valve. The valve ends up almost closed with a large pressure across it, so it hunts and can be noisy, and until the check valve opens the floor loops get either too little flow or water that is too hot.

A riser pump in proportional-pressure mode lowers its head as the flow falls (point C), which makes the problem much smaller. A check valve with a low opening pressure also helps.

:::{figure} figures/c1/riser-pump-curve.*
:label: fig-riser-pump-curve-improved
:alt: Pump diagram with the flow drawn from the riser on the horizontal axis and differential pressure on the vertical axis. A constant-speed riser pump curve falls slowly from 45 kPa at zero flow. A proportional-pressure curve rises linearly from about 20 kPa to the same design point at 600 litres per hour and 41 kPa. Two system curves are shown, one for design and a steep one for low load. A dashed line 10 kPa above the constant-speed curve marks the pressure the thermostatic valve must absorb before the check valve opens. Point B at low load on the constant-speed curve is at about 45 kPa, and point C on the proportional-pressure curve is at about 23 kPa.
:width: 90%

Riser pump at design (A) and at low load with constant speed (B) and proportional pressure (C). The shaded band is the opening pressure of the check valve, which the thermostatic valve must absorb on top of the riser pressure before water flows through the bypass. Example values: 45 kPa shut-off head, 600 l/h design flow, 10 kPa opening pressure. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/riser_pump_curve.py)
:::
