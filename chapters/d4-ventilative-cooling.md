# D4 Ventilative cooling

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

Ventilative cooling or venting (udluftning) means using outdoor air to remove heat from a building whenever the outdoor air is cooler than the indoor air.

It is the third step in the cooling strategy ([](d2-cooling-strategy.md)), after reducing the solar gains and bypassing the heat recovery, and before ceiling fans ([](d6-ceiling-fans.md)), shutters and active cooling. This chapter deals with the building as a whole: how much air is needed and how wind and buoyancy drive it through the house. The openings themselves, and where the air goes once it is inside, are the subject of [](d5-window-openings.md).

## D4.1 Cooling needs large airflows

Outdoor air that enters a room at temperature $T_o$ and leaves at the room temperature $T_i$ removes heat at the rate

```{math}
:label: eq-vc-cooling
P = \rho \, c_p \, q_V \, (T_i - T_o)
```

where $P$ is the cooling power (W), $\rho \approx 1.2$ kg/m³ the air density, $c_p \approx 1005$ J/(kg·K) the specific heat capacity of air and $q_V$ the airflow (m³/s).

In the context of ventilative cooling, the temperature difference is the weak point. On a warm afternoon the outdoor air may be only 2 to 4 K cooler than the room. To remove 1 kW of solar and internal gains from a 30 m² living room $(33.3 W/m^2)$ with a 3 K temperature difference, {eq}`eq-vc-cooling` gives

```{math}
q_V = \frac{1000}{1.2 \cdot 1005 \cdot 3} = 0.28 \text{ m}^3\text{/s} = 280 \text{ L/s}
```

That is about 13 air changes per hour, or 30 times the 9 L/s that the mechanical ventilation supplies to the same room for air quality (0.3 L/s per m²).

Airflows like this are only possible through large openings. They also explain why ventilative cooling works best at night, when the outdoor air is cooler and the temperature difference is larger.

## D4.2 Three ways to move the air

The air can be moved in three ways:

- **Natural ventilation**: openings only, such as windows, roof windows and venting hatches, driven by wind and stack effect.

- **Mechanical ventilation**: fans only, for example by bypassing the heat recovery unit and boosting the airflow.

- **Hybrid (mixed-mode) ventilation**: a combination of the two. This is the normal solution in Danish dwellings, with mechanical ventilation with heat recovery in winter and openings for cooling in summer.

Ventilative cooling is cheap and uses little or no energy, but it is easy to overestimate. The temperature difference between indoors and outdoors is small exactly when cooling is needed, so large airflows are required. The openings must also actually be open.

## D4.3 The driving forces

### Airflow through an opening

The airflow through an opening is driven by the pressure difference across it. For a large opening the flow follows the orifice equation

```{math}
:label: eq-vc-orifice
Q = C_d \, A \, \sqrt{\frac{2 \, \Delta p}{\rho}}
```

where $C_d$ is the discharge coefficient (–), $A$ the free opening area (m²) and $\Delta p$ the pressure difference (Pa). The discharge coefficient accounts for the contraction of the air jet through the opening. It is about 0.6 to 0.65 for a sharp-edged opening; IDA ICE uses 0.65. Grilles, insect nets and louvres lower it considerably, so always use the free area and the discharge coefficient of the actual product. As an example, the rain-defence louvre tested by Bugenings et al. has a discharge coefficient of only 0.29, rated according to EN 13030 {cite:p}`bugenings2025`.

Because the airflow only grows with the square root of the pressure difference, doubling the driving pressure gives just 40 % more airflow. Doubling the opening area doubles it.

When air flows through two openings in series, for example in through a window and out through a roof window, the openings can be combined into one effective area:

```{math}
:label: eq-vc-aeff
\frac{1}{A_\text{eff}^2} = \frac{1}{A_1^2} + \frac{1}{A_2^2}
```

The smaller opening dominates. Two openings of 0.5 m² each give an effective area of only 0.35 m², and a large window does not help much if the outlet is small.

The pressure difference has two sources: buoyancy (the stack effect) and wind. Together with the placement of the openings they give the three modes of natural ventilative cooling in {numref}`fig-vc-modes`.

:::{figure} figures/d4/ventilation-modes.*
:label: fig-vc-modes
:alt: Three building sections side by side. (a) A room with one tall window: cool air enters at the bottom of the window and warm air leaves at the top, with the neutral pressure plane halfway up the opening. (b) A room with windows on opposite façades: wind pushes cool air in on the windward side, marked plus, and out on the leeward side, marked minus. (c) A two-storey section with a low window and a roof opening: cool air enters low, rises through the house and leaves through the roof, with the neutral pressure plane between the openings and the height h marked.
:width: 100%

The three modes of natural ventilative cooling. (a) Single-sided ventilation through one opening. (b) Cross-ventilation driven by the wind pressure difference between two façades. (c) Stack ventilation between a low inlet and a high outlet, separated by the height $h$.
:::

### Stack effect

Warm indoor air is lighter than cooler outdoor air. The pressure difference between two openings at a height difference $h$ is

```{math}
:label: eq-vc-stack
\Delta p = \rho_o \, g \, h \, \frac{T_i - T_o}{T_i}
```

where $g = 9.81$ m/s², $\rho_o$ is the outdoor air density and the temperatures are in kelvin. Air flows in through the lower opening and out through the upper one. Somewhere between them is the neutral pressure plane, where the indoor and outdoor pressures are equal. With two equal openings it sits halfway between them; a larger opening pulls the neutral plane towards itself.

Inserting {eq}`eq-vc-stack` in {eq}`eq-vc-orifice` gives the stack-driven airflow

```{math}
:label: eq-vc-stackflow
Q = C_d \, A_\text{eff} \, \sqrt{2 \, g \, h \, \frac{T_i - T_o}{T_i}}
```

The stack effect is weak in summer, because the temperature difference is small. A window and a roof window, each 0.5 m² and 5 m apart in height, with a 3 K temperature difference, give a pressure difference of only 0.6 Pa. The airflow is still useful: $Q = 0.65 \cdot 0.35 \cdot 0.99 = 0.23$ m³/s, or about 830 W of cooling. Height is what makes the stack effect work, which is why roof windows, skylights and stairwells are so effective.

A single opening also has a stack effect: cool air enters at the bottom of the opening and warm air leaves at the top. The airflow is

```{math}
:label: eq-vc-single
Q = \frac{C_d \, A}{3} \sqrt{g \, H \, \frac{T_i - T_o}{T_i}}
```

where $H$ is the height of the opening. A 0.6 m² window that is 1.2 m tall gives only 45 L/s, or 160 W of cooling, at a 3 K temperature difference. Single-sided ventilation is weak, and tall openings are better than wide ones.

### Wind

Wind creates an overpressure on the windward façade and an underpressure on the leeward façade and the roof. The pressure on a surface is

```{math}
:label: eq-vc-wind
p_w = C_p \, \tfrac{1}{2} \, \rho \, v^2
```

where $v$ is the wind speed at building height (m/s) and $C_p$ the pressure coefficient (–). $C_p$ is typically positive (+0.4 to +0.8) on the windward façade and negative (−0.2 to −0.5) on the leeward façade and the roof. It depends strongly on the wind direction and on how sheltered the building is by its surroundings. A dense urban site can reduce the wind-driven airflow to a fraction of that on an open site.

For cross-ventilation, the driving pressure is the difference between the two façades:

```{math}
:label: eq-vc-cross
\Delta p = (C_{p,1} - C_{p,2}) \, \tfrac{1}{2} \, \rho \, v^2
```

With the same two 0.5 m² openings on opposite façades, a wind speed of 3 m/s and a $C_p$ difference of 0.8, the pressure difference is 4.3 Pa. The airflow is 0.62 m³/s, almost three times the stack-driven airflow, and gives 2.2 kW of cooling at a 3 K temperature difference.

Cross-ventilation therefore gives much more airflow than single-sided ventilation, but wind is unreliable. It varies in speed and direction, and the warmest days are often calm. Design for the stack effect on a calm day, and treat the wind as a bonus. Strong wind also causes its own problems: draught, slamming doors and papers flying, which make occupants close the openings.

### Combined wind and stack effect

In reality wind and buoyancy act at the same time. For two openings, the hand calculation follows directly from the equations above, because the two pressure differences add up across the openings:

1. **Stack pressure.** Find the height difference $h$ between the openings and calculate $\Delta p_\text{stack}$ with {eq}`eq-vc-stack`.
2. **Wind pressure.** Look up $C_p$ for the façade or roof surface of each opening and calculate $\Delta p_\text{wind}$ with {eq}`eq-vc-cross`.
3. **Assisting or opposing?** The stack effect always pushes air in at the bottom and out at the top. If the wind pushes in the same direction (the lower opening has the higher $C_p$), the pressures add. If not, they work against each other:

   ```{math}
   :label: eq-vc-combined
   \Delta p = \Delta p_\text{stack} \pm \Delta p_\text{wind}
   ```

4. **Effective area.** Combine the openings with {eq}`eq-vc-aeff`.
5. **Airflow.** Insert $\Delta p$ and $A_\text{eff}$ in the orifice equation {eq}`eq-vc-orifice`.
6. **Cooling.** Calculate the cooling power with {eq}`eq-vc-cooling`.

When the pressures assist each other, step 5 is the same as adding the two airflows in quadrature, $Q = \sqrt{Q_\text{stack}^2 + Q_\text{wind}^2}$. The combined airflow is therefore always smaller than the sum of the two airflows calculated separately.

Take the house from the stack example: a 0.5 m² window low on the windward façade ($C_p = +0.5$) and a 0.5 m² roof window 5 m higher on the roof ($C_p = -0.3$), with a 3 K temperature difference and a wind speed of 3 m/s.

- Stack pressure: $\Delta p_\text{stack} = 1.2 \cdot 9.81 \cdot 5 \cdot 3/298 = 0.59$ Pa.
- Wind pressure: $\Delta p_\text{wind} = (0.5 - (-0.3)) \cdot \tfrac{1}{2} \cdot 1.2 \cdot 3^2 = 4.32$ Pa.
- The windward window is the lower opening, and the roof has suction, so the pressures assist: $\Delta p = 0.59 + 4.32 = 4.91$ Pa.
- Effective area: $A_\text{eff} = 0.35$ m².
- Airflow: $Q = 0.65 \cdot 0.35 \cdot \sqrt{2 \cdot 4.91/1.2} = 0.66$ m³/s.
- Cooling: $P = 1.2 \cdot 1005 \cdot 0.66 \cdot 3 \approx 2.4$ kW.

At 3 m/s the wind dominates, and the combined airflow is only 7 % higher than with wind alone. On a calm day with 1 m/s wind, $\Delta p_\text{wind}$ falls to 0.48 Pa. The two pressures are then about equal, and the airflow is 0.31 m³/s, or 1.1 kW of cooling.

Now turn the wind around so that the roof window is on the windward side and the low window on the leeward side. The wind then pushes air in at the top and the stack effect pushes it out at the top. The pressures cancel at a wind speed of only

```{math}
v = \sqrt{\frac{\Delta p_\text{stack}}{(C_{p,1} - C_{p,2}) \, \tfrac{1}{2} \, \rho}} = \sqrt{\frac{0.59}{0.8 \cdot 0.6}} = 1.1 \text{ m/s}
```

At that wind speed the airflow almost stops, and the room is not cooled even though both openings are wide open. At higher wind speeds the flow reverses, and the warm air from the room is pushed down through the house. Place inlets low on the façade facing the prevailing summer wind, and outlets high where there is suction: on the roof or on the leeward façade.

Building simulation tools such as IDA ICE solve the same problem as an airflow network, where every opening is a flow element and the pressures are balanced in each zone and every time step. Hand calculations like the one above are still essential for checking whether the simulated airflows have the right order of magnitude.

## D4.4 Ventilation strategies

The three modes in {numref}`fig-vc-modes` are compared here with one worked example each, using the equations above.

### Single-sided ventilation

**Worked example.**

A 30 m² room with a ceiling height of 2.5 m (75 m³) has one openable window on a single façade. The free opening area is $A = 0.6$ m² and the opening is $H = 1.2$ m tall. The wind speed is $v = 2$ m/s, the room is at 25 °C and the outdoor air at 20 °C, so $\Delta T = 5$ K. What is the airflow through the window?

**Stack effect alone.** With {eq}`eq-vc-single`:

```{math}
Q_\text{stack} = \frac{0.65 \cdot 0.6}{3} \sqrt{9.81 \cdot 1.2 \cdot \frac{5}{298}} = 0.13 \cdot 0.44 = 0.058 \text{ m}^3\text{/s} = 58 \text{ L/s}
```

**Wind alone.** With a single opening there is no pressure difference across the room, so {eq}`eq-vc-cross` does not apply. The wind still drives some exchange through turbulence and pulsating flow at the opening. A simple empirical estimate by Warren and Parkins is $Q_\text{wind} = 0.025 \, A \, v$:

```{math}
Q_\text{wind} = 0.025 \cdot 0.6 \cdot 2 = 0.030 \text{ m}^3\text{/s} = 30 \text{ L/s}
```

**Wind and stack combined.** The two drivers do not simply add up. EN 16798-7 uses an empirical expression for single-sided ventilation through an open window, based on measurements by de Gids and Phaff, where the larger of the two drivers decides:

```{math}
:label: eq-vc-en16798
Q = 0.5 \, A \sqrt{\max\left(C_\text{wnd} \, v^2 \, ; \; C_\text{st} \, H \, \Delta T\right)}
```

with $C_\text{wnd} = 0.001$ (1/(m/s)) and $C_\text{st} = 0.0035$ ((m/s)/(m·K)). The wind term is $0.001 \cdot 2^2 = 0.004$ and the stack term is $0.0035 \cdot 1.2 \cdot 5 = 0.021$. The stack term is larger, so

```{math}
Q = 0.5 \cdot 0.6 \cdot \sqrt{0.021} = 0.044 \text{ m}^3\text{/s} = 44 \text{ L/s}
```

**Result.** The window gives about 45 to 60 L/s, or 2 to 3 air changes per hour. With {eq}`eq-vc-cooling` this removes

```{math}
P = 1.2 \cdot 1005 \cdot 0.044 \cdot 5 \approx 260 \text{ W}
```

Two lessons follow. At a moderate wind speed of 2 m/s, the stack effect over the height of the window dominates, so a tall window is worth more than a wide one. And even with a 5 K temperature difference, one window removes only about a quarter of the 1 kW of heat gains from the earlier example. Single-sided ventilation can handle a well-shaded room, but a room with large solar gains needs cross or stack ventilation.

### Cross-ventilation

**Worked example.**

Now give the room from the previous example a second, identical window on the opposite façade, so that air can flow straight through. The conditions are the same: $A = 0.6$ m² per window, $v = 2$ m/s and $\Delta T = 5$ K. The windward façade has $C_p = +0.5$ and the leeward façade $C_p = -0.3$. The windows are at the same height, so the stack effect between them is zero and only the wind drives the flow.

**Wind pressure.** With {eq}`eq-vc-cross`:

```{math}
\Delta p = (0.5 - (-0.3)) \cdot \tfrac{1}{2} \cdot 1.2 \cdot 2^2 = 1.92 \text{ Pa}
```

**Effective area.** The two windows are in series, so with {eq}`eq-vc-aeff`:

```{math}
A_\text{eff} = \left( \frac{1}{0.6^2} + \frac{1}{0.6^2} \right)^{-1/2} = 0.42 \text{ m}^2
```

**Airflow.** With the orifice equation {eq}`eq-vc-orifice`:

```{math}
Q = 0.65 \cdot 0.42 \cdot \sqrt{\frac{2 \cdot 1.92}{1.2}} = 0.49 \text{ m}^3\text{/s} = 490 \text{ L/s}
```

**Cooling.** With {eq}`eq-vc-cooling`:

```{math}
P = 1.2 \cdot 1005 \cdot 0.49 \cdot 5 \approx 3.0 \text{ kW}
```

**Result.** Opening a second window on the opposite façade raises the airflow from about 45 L/s to 490 L/s, more than ten times as much. That is about 24 air changes per hour, which removes the 1 kW of heat gains with plenty to spare. In practice the occupants will close the windows partly long before that, because air speeds this high cause draught ([](d5-window-openings.md)).

The result is sensitive to the assumptions:

- **Sheltered site.** In a dense urban area the $C_p$ difference may be only 0.3 instead of 0.8. Since the airflow scales with the square root of the pressure difference, it falls to $490 \cdot \sqrt{0.3/0.8} = 300$ L/s.
- **Internal doors.** In a dwelling the air must usually pass through an internal door on its way across. An open door of 1.6 m² is a third opening in series and hardly matters: the airflow drops to 480 L/s. A closed door with a 2 cm undercut leaves only about 0.02 m², and the airflow drops to 23 L/s, less than single-sided ventilation through one window. Cross-ventilation only works when the path through the building is open.
- **Wind speed.** The wind speed in the equation is the local wind at the building, not the meteorological wind measured at 10 m height in open terrain. In a built-up area the local wind is often only half the meteorological value or less.

### Stack ventilation

**Worked example.** A two-storey house has an open stair. On the ground floor a window with a free area of $A_1 = 1.0$ m² is open, and at the top of the stair a roof window with $A_2 = 0.6$ m² is open. The height between the centres of the two openings is $h = 5.5$ m. There is no wind. The house is at 25 °C (298 K) and the outdoor air at 22 °C, so $\Delta T = 3$ K. What is the airflow and the cooling power, and what happens on the first floor?

**Effective area.** With {eq}`eq-vc-aeff`:

```{math}
A_\text{eff} = \left( \frac{1}{1.0^2} + \frac{1}{0.6^2} \right)^{-1/2} = 0.51 \text{ m}^2
```

**Airflow.** With {eq}`eq-vc-stackflow`:

```{math}
Q = 0.65 \cdot 0.51 \cdot \sqrt{2 \cdot 9.81 \cdot 5.5 \cdot \frac{3}{298}} = 0.35 \text{ m}^3\text{/s} = 350 \text{ L/s}
```

**Cooling.** With {eq}`eq-vc-cooling`:

```{math}
P = 1.2 \cdot 1005 \cdot 0.35 \cdot 3 \approx 1.3 \text{ kW}
```

This is five times the single-sided window above, at a smaller temperature difference and with no wind at all. At night, with the outdoor air at 17 °C ($\Delta T = 8$ K), the airflow rises to 0.57 m³/s and the cooling power to about 5.5 kW.

**Neutral plane.** The same airflow passes both openings, so the pressure difference across each one scales with $1/A^2$. The neutral plane therefore lies at a height above the lower opening of

```{math}
:label: eq-vc-npl
h_n = \frac{h}{1 + (A_1/A_2)^2} = \frac{5.5}{1 + (1.0/0.6)^2} = 1.5 \text{ m}
```

The neutral plane sits low, close to the larger opening. Everything above about 1.5 m is at overpressure, so a bedroom window opened on the first floor lets warm air out instead of letting cool air in. To ventilate the first floor as well, the roof window must be the larger opening. Doubling it to 1.2 m² raises the airflow by 50 % to 0.52 m³/s and lifts the neutral plane to 3.3 m.

### Practical issue: Nordhavn

:::{admonition} Practical issue
:class: warning
In a low-energy apartment building in Nordhavn, Copenhagen, the summer comfort check in Be18 used a simple daytime venting rate based on the openable window area as a share of the floor area:

```{math}
q_\text{vent} = \frac{11\,\%}{1.5\,\%} \cdot 0.9 \ \text{L/s per m}^2 = 6.6 \ \text{L/s per m}^2
```

For the 30 m² room in the worked examples above, that is 200 L/s, or about 9.5 air changes per hour. Compare it with the examples:

| Strategy | Airflow (L/s) | Per floor area (L/s per m²) |
|---|---|---|
| Single-sided, one window, 5 K | 44 | 1.5 |
| Assumed in Be18 | 200 | 6.6 |
| Cross-ventilation, two windows, 2 m/s | 490 | 16 |

The assumed rate is more than four times what one open window delivers. It is only reached with cross or stack ventilation, with the openings actually open and the path through the dwelling open. In the building most openings were balcony doors that could only be secured at a 1 cm opening, or were too windy to leave open. The top-floor flats, with no balcony above to shade them, overheated badly, and solar control films had to be installed afterwards. Openings must be designed so that they can stay open when they are needed: secure, protected from rain, quiet and free of draught ([](d5-window-openings.md)).
:::
