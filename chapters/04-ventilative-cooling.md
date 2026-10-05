# Ventilative cooling

## Learning objectives

After this chapter you can:

- explain why well-insulated, airtight Nordic homes overheat, and where ventilative cooling fits in the cooling strategy
- estimate the airflow through an opening driven by wind and by stack effect, and the cooling it delivers
- choose between single-sided, cross and stack ventilation, and mechanical ventilative cooling (bypass, boost and night cooling)
- design a venting hatch that meets the requirements for fire escape, rain, burglary and heat loss
- set up an opening control that cools without overcooling or draught
- interpret overheating results against the BR18 and adaptive comfort criteria

## Introduction

Danish homes are increasingly at risk of overheating. New dwellings are well insulated and airtight, often have large glazed areas, and keep their heat well. That works well in winter, but in summer the same building struggles to get rid of solar and internal gains.

High indoor temperatures are now one of the most common indoor climate complaints in new Danish dwellings, and not only in summer .
Insulation, airtightness and large windows have made new homes very good at keeping heat in.

On a sunny day in April or September, solar and internal gains can lift the temperature well above comfort levels in a home that hardly needs heating. In a warmer climate with longer heat waves the problem grows. A study of Finnish apartment buildings found that openable windows were the most effective passive measure against overheating in the new building, though not enough in the old one {cite:p}`farahani2021`.

## Ventilative cooling

Ventilative cooling or venting (udluftning) means using outdoor air to remove heat from a building whenever the outdoor air is cooler than the indoor air.

It is the second step in the cooling hierarchy, after reducing the heat gains (chapter 1) and before ceiling fans (chapter 5) and active cooling.

The air can be moved in three ways:

- **Natural ventilation**: openings only, such as windows, roof windows and venting hatches, driven by wind and stack effect.

- **Mechanical ventilation**: fans only, for example by bypassing the heat recovery unit and boosting the airflow.

- **Hybrid (mixed-mode) ventilation**: a combination of the two. This is the normal solution in Danish dwellings, with mechanical ventilation with heat recovery in winter and openings for cooling in summer.

Ventilative cooling is cheap and uses little or no energy, but it is easy to overestimate. The temperature difference between indoors and outdoors is small exactly when cooling is needed, so large airflows are required. The openings must also actually be open.

:::{Practical issue}
In a low-energy apartment building in Nordhavn, Copenhagen, the energy calculation assumed a generous venting rate. In practice most of the openings were balcony doors that could only be secured at a 1 cm opening, or were too windy to leave open, and the top-floor flats overheated badly. Openings must be designed so that they can stay open when they are needed: secure, protected from rain, quiet and free of draught.
:::

<!--The chapter first explains the physics of airflow through openings and the ventilative cooling strategies available. It then covers the design of venting hatches, opening control and draught. It ends with how to assess overheating, and a worked example from the course row house.-->

## The physics of airflow through openings

### Cooling needs large airflows

Outdoor air that enters a room at temperature $T_o$ and leaves at the room temperature $T_i$ removes heat at the rate

```{math}
:label: eq-vc-cooling
P = \rho \, c_p \, Q \, (T_i - T_o)
```

where $P$ is the cooling power (W), $\rho \approx 1.2$ kg/m³ the air density, $c_p \approx 1005$ J/(kg·K) the specific heat capacity of air and $Q$ the airflow (m³/s).

The temperature difference is the weak point. On a warm afternoon the outdoor air may be only 2 to 4 K cooler than the room. To remove 1 kW of solar and internal gains from a 30 m² living room with a 3 K temperature difference, {eq}`eq-vc-cooling` gives

```{math}
Q = \frac{1000}{1.2 \cdot 1005 \cdot 3} = 0.28 \text{ m}^3\text{/s} = 280 \text{ L/s}
```

That is about 13 air changes per hour, or 30 times the 9 L/s that the mechanical ventilation supplies to the same room for air quality (0.3 L/s per m²). Airflows like this are only possible through large openings. They also explain why ventilative cooling works much better at night, when the outdoor air is cooler and the temperature difference is larger.

### Airflow through an opening

The airflow through an opening is driven by the pressure difference across it. For a large opening the flow follows the orifice equation

```{math}
:label: eq-vc-orifice
Q = C_d \, A \, \sqrt{\frac{2 \, \Delta p}{\rho}}
```

where $C_d$ is the discharge coefficient (–), $A$ the free opening area (m²) and $\Delta p$ the pressure difference (Pa). The discharge coefficient accounts for the contraction of the air jet through the opening. It is about 0.6 to 0.65 for a sharp-edged opening; IDA ICE uses 0.65. Grilles, insect nets and louvres lower it considerably, so always use the free area and the discharge coefficient of the actual product.

Because the airflow only grows with the square root of the pressure difference, doubling the driving pressure gives just 40 % more airflow. Doubling the opening area doubles it.

When air flows through two openings in series, for example in through a window and out through a roof window, the openings can be combined into one effective area:

```{math}
:label: eq-vc-aeff
\frac{1}{A_\text{eff}^2} = \frac{1}{A_1^2} + \frac{1}{A_2^2}
```

The smaller opening dominates. Two openings of 0.5 m² each give an effective area of only 0.35 m², and a large window does not help much if the outlet is small.

The pressure difference has two sources: buoyancy (the stack effect) and wind. Together with the placement of the openings they give the three modes of natural ventilative cooling in {numref}`fig-vc-modes`.

:::{figure} figures/ch04/ventilation-modes.*
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

In reality wind and buoyancy act together. They can reinforce each other or work against each other, depending on where the openings are. Building simulation tools such as IDA ICE solve this as an airflow network, where every opening is a flow element and the pressures are balanced in each zone and every time step. Hand calculations with {eq}`eq-vc-stackflow` and {eq}`eq-vc-cross` are still useful to check the order of magnitude of the simulated airflows.

:::{admonition} Rules of thumb
:class: tip

- **Cooling power**: every 100 L/s of outdoor air removes about 120 W per kelvin of temperature difference.
- **Single-sided ventilation** is effective up to a room depth of about 2.5 times the ceiling height.
- **Cross-ventilation** is effective up to a building depth of about 5 times the ceiling height.
- **Stack ventilation** works best with a large height difference between inlet and outlet, and with openings of similar size.
- **Calm days**: design for the stack effect alone; wind is a bonus.
:::

