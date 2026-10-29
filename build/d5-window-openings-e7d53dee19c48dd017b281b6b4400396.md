# D5 Openings for ventilative cooling

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D5.1 Introduction

Bottom-hung (tilt) windows are common in new Danish dwellings. They are suited to airing in winter: the opening is small, secure and protected from rain, and the sash directs the cold inflow upwards. In summer the small opening area and a driving temperature difference of only a few kelvin limit the airflow. Jiang et al. report that bottom-hung windows may not provide sufficient ventilation in the warmer months for this reason {cite:p}`jiang2025`.

A side-hung window opens over its full height and, at an opening angle of 60° or more, over its full width. For single-sided ventilation at a small ΔT, the airflow is four to five times that of a tilted sash of the same size. The inflow is slow and drops to the floor, but in summer it is only slightly cooler than the room air and therefore provides cooling rather than draught. The bottom-hung window is thus suited to winter airing and the side-hung window to summer cooling.

This chapter covers the free area of the common opening types, the airflow through them at a small temperature difference, the flow pattern of the inflow, the resulting draught at the feet, and venting hatches. It builds on the orifice and stack equations in [](d4-ventilative-cooling.md).

## D5.2 Opening types and their free area

The airflow is determined by the smallest cross-section the air passes through, the *free opening area*, and not by the glass area.

:::{figure} figures/d5/window-gaps.*
:label: fig-sh-gaps
Free opening of (a) a side-hung window opened 30° and (b) a bottom-hung window tilted 120 mm, for the same 0.8 × 1.3 m sash. Blue: inflow below the neutral plane. Orange: outflow above it. The gaps of the bottom-hung window are exaggerated for clarity.
:::

**Side-hung** (hinge at the side, opening angle α): the free edge leaves a vertical gap over the full sash height h:

```{math}
:label: eq-sh-side
s = 2w\sin(\alpha/2), \qquad A = \min(s, w)\,h
```

where w is the sash width. For α ≥ 60° the gap equals the sash width, and the free area equals the full sash area.

**Bottom-hung** (hinge at the bottom, stroke s at the top): the gaps are two triangles at the sides that taper to zero at the hinge, plus a slot at the top:

```{math}
:label: eq-sh-bottom
A = s\,w + 2 \cdot \tfrac{1}{2} s\,h = s\,(w + h)
```

Tilt fittings limit s to about 100–150 mm.

**Top-hung** (hinge at the top, opening outwards at the bottom): the same geometry turned upside down, so A = s(w + h) as well. The widest gap is at the bottom, where the inflow enters, and the outflow passes through the narrow gaps at the top.

**Venting hatches** are openings made only for ventilation, usually without glass.

<!-- Photos of the opening types will be added here (Christian). -->

For a 0.8 × 1.3 m sash:

| Window | Opening | Free area A |
|---|---|---|
| Side-hung | 90° | 1.04 m² |
| Side-hung | 30° | 0.54 m² |
| Side-hung | 10° | 0.18 m² |
| Bottom-hung | s = 120 mm | 0.25 m² |
| Top-hung | s = 120 mm | 0.25 m² |

## D5.3 Discharge coefficient of windows and louvres

The orifice equation {eq}`eq-vc-orifice` contains the product $C_d A$, and a discharge coefficient is only meaningful together with the area it refers to. For windows, $C_d$ refers to the free opening area of D5.2. For a sharp-edged opening it is about 0.6. The discharge coefficient of a window is not a constant: it varies with opening area, window type and temperature difference, and for a side-hung window it decreases at large ΔT {cite:p}`heiselberg2000,heiselberg2001`. $C_d = 0.6$ is used as design value for windows in summer conditions.

**Louvres.** Weather louvres and ventilation grilles are tested to EN 13030 {cite:p}`en13030`. The discharge coefficient is determined from the measured airflow and pressure drop and refers to the core area, the opening inside the frame with the blades removed. It therefore already includes the obstruction of the blades, and must not be multiplied by the free area between the blades. The product $C_d A_\text{core}$ is called the aerodynamic free area. EN 13030 classifies louvres by the discharge coefficient: class 1 ≥ 0.4, class 2 0.3–0.4, class 3 0.2–0.3 and class 4 < 0.2.

| Opening | Rain protection | $C_d$ | Area basis |
|---|---|---|---|
| Window, sharp-edged opening | none | 0.6 | free opening area |
| Single-bank weather louvre (Colt 1UL) {cite:p}`colt_louvres` | low | 0.43 | core area |
| Triple-bank weather louvre (Colt 3UL) {cite:p}`colt_louvres` | high | 0.28 | core area |
| Louvre in door, class A to 3 m/s (CS RSH-5700) {cite:p}`bugenings2025` | high | 0.28 | core area |
| Venting grille, 34 % physical free area (DucoGrille NightVent) {cite:p}`duco_nightvent` | high, burglar-resistant | 0.20 | total area |
| Weather louvre with bird mesh (Renson L.066V) {cite:p}`renson_l066v` | high | 0.12 | louvre area |

EN 13030 gives an entry coefficient for intake and a discharge coefficient for exhaust. They differ little, and the table gives the entry value where the product data state it. Products with better rain protection have more blade banks or deeper blades and a lower $C_d$. Insect and bird screens reduce it further. The DucoGrille value can be checked against the product's flow rating of 369 L/s per m² at 2 Pa: $0.369 / \sqrt{2 \cdot 2/1.2} = 0.20$.

**Consequence for design.** For the same airflow, an opening with $C_d = 0.2$ requires three times the area of an open window with $C_d = 0.6$. A venting hatch of 0.5 m² behind a grille of $C_d = 0.2$ is equivalent to an open window of only 0.17 m². When a louvre and a window act in series, they are combined with the general form of {eq}`eq-vc-aeff`, and the louvre dominates.

## D5.4 Airflow at small ΔT

For a single opening, warm room air leaves through the upper part and cool outdoor air enters through the lower part. The pressure difference increases linearly with the distance from the neutral plane, so the orifice equation is integrated over the height of the gap. For a gap of constant width, such as that of the side-hung window, the neutral plane is at mid-height and the integration gives the single-opening equation of [](d4-ventilative-cooling.md):

```{math}
:label: eq-sh-stack
Q_{st} = \frac{C_d A}{3}\sqrt{\frac{g\,h\,\Delta T}{T}}
```

For the bottom-hung window the gap width varies with height, and the integral is evaluated numerically ([script](code/window_flow.py)). Most of the free area is in the top slot and the upper parts of the side triangles. The neutral plane is therefore at about 1.1 m of the 1.3 m sash height, and the inflow passes through the narrow lower parts of the triangles. The airflow per square metre of free area is lower than for the side-hung window.

:::{figure} figures/d5/window-flow-dt.*
:label: fig-sh-flow
Stack-driven airflow through a 0.8 × 1.3 m sash without wind, C_d = 0.6, and through a hatch of the same size behind a venting grille with C_d = 0.2 (DucoGrille NightVent, D5.3). [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/plot_window_flow.py)
:::

## D5.5 Flow pattern of the inflow

The airflow rate determines the cooling power, while the flow pattern determines whether the inflow is perceived as air movement, as draught at the ankles, or not at all. Heiselberg, Svidt and Nielsen showed in laboratory tests that the flow from an open window can be described by jet theory and stratified-flow theory, and developed simple *flow-element* models for the velocities in the occupied zone {cite:p}`heiselberg2001`.

The balance between buoyancy and momentum in the inflow is measured by the Archimedes number:

```{math}
:label: eq-sh-ar
Ar = \frac{g\,\Delta T\,\sqrt{a_0}}{T\,U_0^2}
```

where a₀ is the effective inflow area (C_d times the inflow part of A) and U₀ = q₀/a₀ is the inflow velocity. At small Ar the inflow behaves as a jet and keeps its direction; at large Ar it is governed by buoyancy and falls.

:::{figure} figures/d5/window-jets.*
:label: fig-sh-jets
Flow patterns from the two window types. (a) A side-hung window opens over the full height; the slow inflow in the lower half drops and spreads along the floor. (b) A bottom-hung window placed high throws the air up to the ceiling, where it attaches as a wall jet. (c) At large ΔT or large flow, the ceiling jet separates at the penetration depth x_s and drops to the floor.
:::

**(a) Side-hung window: floor flow.** The side-hung window opens over its full height, and the inflow passes slowly through the lower half. It follows from {eq}`eq-sh-stack` that U₀² is proportional to ΔT in purely stack-driven flow, so Ar is about 1 independent of ΔT. The inflow therefore falls towards the floor and spreads in a semi-radial layer in summer as well as in winter; only the temperature and velocity of the layer change. Nielsen et al. measured this for a side-hung window (0.81 × 1.38 m, sill 1.0 m) and found that the maximum velocity near the floor follows the same form as for a displacement diffuser {cite:p}`nielsen2000`:

```{math}
:label: eq-sh-floor
u = K_w\,\frac{q_0}{x + x_0}
```

K_w lies between about 4 and 20 m⁻¹ and depends on Ar' and the opening area. x₀ is a virtual origin of 0 to −3 m. The maximum velocity occurs at ankle height. In summer the layer is a few kelvin below room temperature and provides cooling. In cold weather the same layer causes draught, and the side-hung window must be restricted or closed. Strong wind adds momentum and can carry the inflow further into the room before it drops.

**(b) Bottom-hung window placed high: ceiling jet.** A bottom-hung window is normally placed high, as a top light or a hatch. The inward-tilted sash deflects the inflow upwards, where it attaches to the ceiling as a wall jet {cite:p}`svidt2000`:

```{math}
:label: eq-sh-ceiling
u_m = K_a\,U_0\,\frac{\sqrt{a_0}}{x + x_0}, \qquad K_a \approx 7,\; x_0 \approx -2\ \text{m}
```

The jet entrains warm room air along the ceiling and is mixed and warmed before it reaches the occupied zone. For this reason the high bottom-hung window is suited to winter airing.

**(c) Bottom-hung window at large ΔT: separation.** A cold jet remains attached to the ceiling only up to a penetration depth x_s, which decreases with increasing Ar. Beyond x_s it separates and falls into the occupied zone. At a large ΔT and a small driving pressure (0.2–0.4 Pa), it drops close to the window and continues along the floor {cite:p}`heiselberg2006`. For a slot at the ceiling of a 3 m high room, model tests show that the cold jet leaves the ceiling before it reaches the end wall once Ar = βghΔT₀/u₀² ≥ 0.02, with h the slot height. In that geometry this is a supply temperature only 0.7 K below the return {cite:p}`nielsen1990`. In cold weather the bottom-hung window must therefore be opened only slightly, so that the jet remains attached to the ceiling.

**Worked example.** A bedroom is cooled at night through a side-hung window of 0.8 × 1.3 m, fully open (A = 1.04 m², {numref}`fig-sh-gaps`a). The room is at 25 °C and the outdoor air at 21 °C, so ΔT = 4 K. There is no wind. Is there draught at the feet?

*Airflow.* With {eq}`eq-sh-stack` and $C_d = 0.6$:

```{math}
Q = \frac{0.6 \cdot 1.04}{3} \sqrt{\frac{9.81 \cdot 1.3 \cdot 4}{298}} = 0.208 \cdot 0.414 = 0.086 \text{ m}^3\text{/s}
```

This is 86 L/s and a cooling power of $1.2 \cdot 1005 \cdot 0.086 \cdot 4 = 0.42$ kW.

*Archimedes number.* The inflow passes the lower half of the opening, $a_0 = 0.6 \cdot 1.04/2 = 0.31$ m², so $U_0 = 0.086/0.31 = 0.28$ m/s. With {eq}`eq-sh-ar`:

```{math}
Ar = \frac{9.81 \cdot 4 \cdot \sqrt{0.31}}{298 \cdot 0.28^2} = 0.97
```

Ar is of order 1, and the inflow falls to the floor.

*Floor velocity.* With {eq}`eq-sh-floor`, $K_w = 5$ m⁻¹ and $x_0 = 0$ (assumed, at the low end of the measured range), the maximum velocity is 0.43 m/s at 1 m from the window and 0.22 m/s at 2 m.

*Draught.* The floor layer is assumed to have warmed halfway, $t_a = 23$ °C, with $T_u = 40$ %. At 1 m, {eq}`eq-draught` gives DR = 57 % and {eq}`eq-ankle-draught` gives $PPD_{AD}$ = 22 % for a neutral occupant (TS = 0). At 2 m the values are 23 % and 13 %.

*Restricted opening.* At an opening angle of 30° the free area is 0.54 m² ({eq}`eq-sh-side`). The airflow and the floor velocity are halved: 45 L/s, 0.22 kW and 0.22 m/s at 1 m, with $PPD_{AD}$ = 13 %.

The fully open window meets the ankle-draught limit from about 1.1 m into the room, which is acceptable for a bed placed away from the window. The ISO 7730 limit is exceeded in both cases, which illustrates the difference between the two models in D5.6.


## D5.6 Draught at the feet

The floor stream from a low or full-height opening ({numref}`fig-sh-jets`a) reaches the occupants at ankle height. Whether it is perceived as cooling or as draught depends on its velocity and temperature and on the thermal sensation of the occupant. Two models are in use.

**ISO 7730.** The draught rate predicts the percentage dissatisfied with draught {cite:p}`iso7730`:

```{math}
:label: eq-draught
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37\,v\,T_u + 3.14)
```

with $t_a$ the local air temperature (°C), $v$ the mean air speed (m/s) and $T_u$ the turbulence intensity (%). The usual limit is DR < 20 %. The model was developed for people at neutral thermal sensation, with air at 20–26 °C and below 0.5 m/s at the neck. At the feet it is conservative, and it does not apply to occupants who are warm and prefer air movement ([](d6-ceiling-fans.md)).

**ASHRAE 55 ankle draught.** Liu et al. measured the response to air movement at the ankles as a function of the whole-body thermal sensation TS (−3 to +3) {cite:p}`liu2017`. The model, adopted in ASHRAE 55, gives

```{math}
:label: eq-ankle-draught
PPD_{AD} = 100\,\frac{e^z}{1 + e^z}, \qquad z = -2.58 + 3.05\,v_{ankle} - 1.06\,TS
```

with $v_{ankle}$ the air speed at 0.1 m. The limit $PPD_{AD}$ < 20 % corresponds to $v_{ankle}$ < 0.39 + 0.35·TS m/s: 0.39 m/s for a neutral occupant and 0.22 m/s for a slightly cool occupant (TS = −0.5). Warm occupants accept higher velocities.

**Measurements.** Bugenings et al. measured the flow from a full-scale low louvre in a test room at a small temperature difference: the inflow was 24–25 °C and the room 0.4–1.9 K warmer {cite:p}`bugenings2025`. The maximum velocity was at 0.1 m above the floor in all cases, also without buoyancy. Calculated from their published data, the ISO 7730 draught rate in the louvre's path passed 20 % at about 7 air changes per hour (0.31–0.36 m/s), while the ankle model stayed below 20 % in every case.

Fitzner and Finke measured the flow from six tilted bottom-hung windows in a 180 m³ office in winter {cite:p}`fitzner2012`. In the hour before the velocity measurements, the airflow was 3.3 air changes per hour at a mean temperature difference of 13.8 K, a cooling power of 2.7 kW. With the radiator below the window switched off, the inflow fell to the floor, and the velocity at 0.1 m was 0.21–0.27 m/s with DR of 27–37 %.

<!-- Hidden until revised (Christian, 2026-10-28)

## D5.7 Venting hatches

A venting hatch is an opening made only for ventilation, usually an insulated panel beside a fixed window. Fixed frameless glazing is cheaper, slimmer and more airtight than an openable window. The hatch provides an opening that can remain open, as it can be made secure against burglary, protected from rain, fitted with an insect screen and attenuated against noise. These requirements were not met in the Nordhavn case ([](d4-ventilative-cooling.md)).

**Escape.** If the hatch is also the escape route from the room, BR18 requires a clear opening at least 0.5 m wide and 0.6 m high, with width plus height at least 1.5 m, a sill no more than 1.2 m above the floor, and opening from the inside without tools.

**Insulation when closed.** A hatch is closed and part of the thermal envelope for most of the year. With gas-filled foam (λ = 0.020 W/m·K), U = 0.12 W/m²K takes about 0.17 m of insulation and U = 0.08 W/m²K about 0.25 m. A panel of that thickness cannot rotate in the opening, so the insulation is divided into two panels, for example a hatch with an inner panel that is fitted in the heating season. Vacuum panels (λ = 0.007 W/m·K) reach U = 0.12 W/m²K with about 60 mm, at roughly 25 times the cost. Built into a prefabricated façade element, a well-detailed hatch reaches U = 0.07 W/m²K with a linear thermal bridge of 0.005 W/m·K.

**Airflow.** For a given area, a tall hatch gives more airflow than a wide one, because the stack-driven flow increases with the opening height to the power 1.5 ({eq}`eq-sh-stack`). The grille, insect screen and damper can reduce the free area to about a third of the hole (34 % for one product), so the free area and discharge coefficient of the product must be used.

**Layouts.** Three solutions are used:

1. a door used for venting and escape;
2. a hatch beside the window, used for both;
3. an escape hatch beside the window, plus an automatic venting hatch high above it.

The third layout is preferable for ventilative cooling. The high automatic hatch is less exposed to noise, rain, insects and intrusion and can therefore remain open at night. Its cold inflow mixes under the ceiling before it reaches the occupied zone, and together with the low escape hatch it provides a large height difference for stack-driven flow.

The room CFD model in [](appendix-room-cfd.md) compares a window and a high hatch in the same room on a cool summer night, with the floor velocity and the draught at the feet for each. The app also includes a balcony door and a low slot.

-->
