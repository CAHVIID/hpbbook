# D5 Openings for ventilative cooling

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## D5.1 Introduction

Many new Danish homes have bottom-hung (tilt) windows. They are good for airing in winter: the opening is small, safe and rain-proof, and the sash throws the cold air upwards. In summer they are weak, because the opening area is small and the driving temperature difference is only a few Kelvin. Jiang et al. note that bottom-hung windows may not ventilate enough in the warmer months, when the temperature difference is small {cite:p}`jiang2025`.

A side-hung window opens over its full height and, at 60° or more, over its full width. For single-sided ventilation with a small ΔT it gives roughly four to five times the airflow of a tilted sash of the same size. The inflow is slow and drops to the floor, but in summer it is only slightly cooler than the room, so it gives cooling rather than draught.

In short, the bottom-hung window is a winter window and the side-hung window is a summer window.

This chapter gives the equations behind that statement. It covers the free area of the common opening types, the airflow through them at a small temperature difference, where the inflow goes, the draught it can cause, and venting hatches. It builds on the orifice and stack equations in [](d4-ventilative-cooling.md).

## D5.2 Opening types and their free area

The airflow is set by the smallest cross-section the air must pass through, the *free opening area*, not by the glass area.

:::{figure} figures/d5/window-gaps.*
:label: fig-sh-gaps
Free opening of (a) a side-hung window opened 30° and (b) a bottom-hung window tilted 120 mm, for the same 0.8 × 1.3 m sash. Blue: inflow below the neutral plane. Orange: outflow above it. The gaps of the bottom-hung window are exaggerated for clarity.
:::

**Side-hung** (hinge at the side, opening angle α): the free edge leaves a vertical gap over the full sash height h:

```{math}
:label: eq-sh-side
s = 2w\sin(\alpha/2), \qquad A = \min(s, w)\,h
```

where w is the sash width. At α ≥ 60° the gap equals the sash width, and the window is in effect fully open.

**Bottom-hung** (hinge at the bottom, stroke s at the top): the gaps are two triangles at the sides that taper to zero at the hinge, plus a slot at the top:

```{math}
:label: eq-sh-bottom
A = s\,w + 2 \cdot \tfrac{1}{2} s\,h = s\,(w + h)
```

Tilt fittings limit s to about 100–150 mm.

**Top-hung** (hinge at the top, opening outwards at the bottom): the same geometry turned upside down, so A = s(w + h) as well. The widest gap is now at the bottom, where the inflow enters, and the outflow must pass through the narrow slivers at the top.

**Venting hatches** are openings made only for ventilation, usually without glass. They are treated in a section of their own below.

<!-- Photos of the opening types will be added here (Christian). -->

For a 0.8 × 1.3 m sash:

| Window | Opening | Free area A |
|---|---|---|
| Side-hung | 90° | 1.04 m² |
| Side-hung | 30° | 0.54 m² |
| Side-hung | 10° | 0.18 m² |
| Bottom-hung | s = 120 mm | 0.25 m² |
| Top-hung | s = 120 mm | 0.25 m² |

## D5.3 Airflow at small ΔT

### Stack effect: the shape of the gap matters

For a single opening, warm room air leaves through the top and cool outdoor air enters through the bottom. The pressure difference grows linearly with the distance from the neutral plane, so the orifice equation is integrated over the height of the gap. For a gap of constant width, such as the side-hung window, this gives the result already used for a single window in [](d4-ventilative-cooling.md), with the neutral plane at mid-height:

```{math}
:label: eq-sh-stack
Q_{st} = \frac{C_d A}{3}\sqrt{\frac{g\,h\,\Delta T}{T}}
```

For the bottom-hung window the integral must be done numerically, because the gap width varies with height ([script](code/window_flow.py)). Most of the free area sits high up in the top slot and the upper parts of the triangles. The neutral plane moves up to about 1.1 m of the 1.3 m sash, and all the inflow must pass through the narrow lower slivers. The result is less flow per square metre of opening than for the side-hung window.

:::{figure} figures/d5/window-flow-dt.*
:label: fig-sh-flow
Stack-driven airflow through a 0.8 × 1.3 m sash with no wind, for C_d = 0.6. In summer conditions (ΔT < 5 K) the fully open side-hung window delivers 4–5 times more air than the tilted sash.
:::

The discharge coefficient is not a constant. It varies with opening area, window type and temperature difference, and for a side-hung window it falls at large ΔT {cite:p}`heiselberg2000,heiselberg2001`. C_d = 0.6 is a reasonable design value for the summer case.

### Wind

Wind on a single opening drives a turbulent, fluctuating exchange. A simple model is that of Warren and Parkins {cite:p}`warren1985`:

```{math}
:label: eq-sh-wind
Q_w = 0.025\,A\,v
```

with v the wind speed at roof height. It scales with the area only, so it also favours the larger side-hung opening. Stack and wind flows are combined as Q = √(Q_st² + Q_w²).

Many models exist for single-sided flow. In a test of twelve of them against tracer-gas measurements on bottom-hung windows, most underestimated the airflow. The EN 16798-7 model was off by −82 % on average {cite:p}`jiang2025`. Treat the numbers in this chapter as estimates good to about a factor of 1.5.

## D5.4 Where the air goes

The airflow rate decides the cooling power. The flow pattern decides whether the air is felt as a pleasant breeze, as draught at the ankles or not at all. Heiselberg, Svidt and Nielsen showed in laboratory tests that the flow from an open window can be described with jet theory and stratified-flow theory. They developed simple *flow-element* models for the velocities in the occupied zone {cite:p}`heiselberg2001`.

The balance between buoyancy and momentum in the inflow is measured by the Archimedes number:

```{math}
:label: eq-sh-ar
Ar = \frac{g\,\Delta T\,\sqrt{a_0}}{T\,U_0^2}
```

where a₀ is the effective inflow area (C_d times the inflow part of A) and U₀ = q₀/a₀ is the inflow velocity. A small Ar gives a jet that keeps its direction. A large Ar gives cold air that falls.

:::{figure} figures/d5/window-jets.*
:label: fig-sh-jets
Flow patterns from the two window types. (a) A side-hung window opens over the full height; the slow inflow in the lower half drops and spreads along the floor. (b) A bottom-hung window placed high throws the air up to the ceiling, where it attaches as a wall jet. (c) At large ΔT or large flow, the ceiling jet separates at the penetration depth x_s and drops to the floor.
:::

**(a) Side-hung: the inflow drops to the floor.** The side-hung window opens over its full height, and the inflow passes slowly through the lower half. A useful consequence of {eq}`eq-sh-stack` is that in purely stack-driven flow, U₀² scales with ΔT, so Ar is about 1 whatever ΔT is. The inflow therefore always falls towards the floor and spreads in a semi-radial layer, in summer as well as in winter. Only the temperature and speed of that layer change. Nielsen et al. measured this for a side-hung window (0.81 × 1.38 m, sill 1.0 m) and found that the maximum velocity near the floor follows the same form as for a displacement diffuser {cite:p}`nielsen2000`:

```{math}
:label: eq-sh-floor
u = K_w\,\frac{q_0}{x + x_0}
```

K_w lies between about 4 and 20 m⁻¹ and depends on Ar' and the opening area. x₀ is a virtual origin of 0 to −3 m. The highest speed is at ankle height. In summer the layer is only a few kelvin below room temperature, so it is a gentle cooling stream. In cold weather the same layer is draught, which is why a side-hung window must be restricted or closed in winter. Strong wind adds momentum and can push the inflow further into the room before it drops.

**(b) Bottom-hung, placed high: a ceiling jet.** A bottom-hung window is normally placed high, as a top light or a hatch. The inward-tilted sash deflects the air upwards, where it attaches to the ceiling as a wall jet {cite:p}`svidt2000`:

```{math}
:label: eq-sh-ceiling
u_m = K_a\,U_0\,\frac{\sqrt{a_0}}{x + x_0}, \qquad K_a \approx 7,\; x_0 \approx -2\ \text{m}
```

The jet entrains warm room air along the ceiling, so it is mixed and warmed before it reaches people. This is why the high bottom-hung window is the right choice for winter airing.

**(c) Bottom-hung, cold: the jet drops.** A cold jet stays attached to the ceiling only up to a penetration depth x_s, which shrinks as Ar grows. Beyond x_s it separates and falls into the occupied zone. With a large ΔT and a small driving pressure (0.2–0.4 Pa), it drops close to the window and runs along the floor {cite:p}`heiselberg2006`. For a slot at the ceiling of a 3 m high room, model tests show that the cold jet leaves the ceiling before it reaches the end wall once Ar = βghΔT₀/u₀² ≥ 0.02, with h the slot height. In that geometry this is a supply temperature only 0.7 K below the return {cite:p}`nielsen1990`. The bottom-hung window therefore needs a small opening in cold weather, so that the flow stays on the ceiling.

## D5.5 Draught at the feet

The floor stream from a low or full-height opening ({numref}`fig-sh-jets`a) arrives at the ankles. Whether it is felt as cooling or as draught depends on its speed, its temperature and how warm the occupant is. Two models are in use.

**ISO 7730.** The draught rate predicts the percentage dissatisfied with draught {cite:p}`iso7730`:

```{math}
:label: eq-draught
DR = (34 - t_a)(v - 0.05)^{0.62}(0.37\,v\,T_u + 3.14)
```

with $t_a$ the local air temperature (°C), $v$ the mean air speed (m/s) and $T_u$ the turbulence intensity (%). The usual limit is DR < 20 %. The model was developed for people at a neutral thermal sensation, with air at 20–26 °C and below 0.5 m/s at the neck. At the feet it is therefore conservative, and it does not apply to a warm person who welcomes air movement ([](d6-ceiling-fans.md)).

**ASHRAE 55 ankle draught.** Liu et al. measured the response to air at the ankles and included the whole-body thermal sensation TS (−3 to +3) {cite:p}`liu2017`. The model, adopted in ASHRAE 55, gives

```{math}
:label: eq-ankle-draught
PPD_{AD} = 100\,\frac{e^z}{1 + e^z}, \qquad z = -2.58 + 3.05\,v_{ankle} - 1.06\,TS
```

with $v_{ankle}$ the air speed at 0.1 m. The limit $PPD_{AD}$ < 20 % corresponds to $v_{ankle}$ < 0.39 + 0.35·TS m/s: 0.39 m/s for a neutral occupant and 0.22 m/s for one who is slightly cool (TS = −0.5). A warm occupant accepts more.

**Measurements.** Bugenings et al. measured a full-scale low louvre in a test room with almost no temperature difference: the inflow was 24–25 °C and the room only 0.4–1.9 K warmer {cite:p}`bugenings2025`. The highest speed was always at 0.1 m above the floor, even without buoyancy. Calculated from their published data, the ISO 7730 draught rate in the louvre's path passed 20 % at about 7 air changes per hour (0.31–0.36 m/s), while the ankle model stayed below 20 % in every case. Fitzner and Finke measured 0.21–0.27 m/s at 0.1 m under tilted windows in winter, with DR of 27–37 % when the radiator below the window was off {cite:p}`fitzner2012`.

**Design consequence.** In summer a floor stream of 0.2–0.4 m/s that is only a few kelvin below room temperature passes the ankle model for warm occupants, even though it fails ISO 7730. In cold weather the same stream is draught by both models. Low and full-height openings must therefore be restricted when it is cold, and winter airing should use high openings ({numref}`fig-sh-jets`b).

## D5.6 Venting hatches

A venting hatch is an opening made only for ventilation, usually an insulated panel beside a fixed window. Fixed frameless glazing is cheaper, slimmer and more airtight than an openable window, and the hatch gives an opening that can stay open: secure against burglary, protected from rain, fitted with an insect net and damped against noise. This is what failed in the Nordhavn case ([](d4-ventilative-cooling.md)).

**Escape.** If the hatch is also the escape route from the room, BR18 requires a clear opening at least 0.5 m wide and 0.6 m high, with width plus height at least 1.5 m, a sill no more than 1.2 m above the floor, and opening from the inside without tools.

**Insulation when closed.** A hatch is part of the envelope for most of the year. With gas-filled foam (λ = 0.020 W/m·K), U = 0.12 W/m²K takes about 0.17 m of insulation and U = 0.08 W/m²K about 0.25 m. A single panel that thick cannot rotate in the opening, so the insulation is split into two panels, for example a hatch with an inner panel fitted in the heating season. Vacuum panels (λ = 0.007 W/m·K) reach U = 0.12 W/m²K with about 60 mm, at roughly 25 times the cost. Built into a prefabricated façade element, a well-detailed hatch reaches U = 0.07 W/m²K with a linear thermal bridge of 0.005 W/m·K.

**Airflow.** A tall hatch is better than a wide one, because the stack flow grows with the height of the opening to the power 1.5 ({eq}`eq-sh-stack`). The grille, net and damper can leave a free area of only about a third of the hole (34 % for one product), so use the product's free area and discharge coefficient.

**Layouts.** Three solutions are used:

1. a door used for venting and escape;
2. a hatch beside the window, used for both;
3. an escape hatch beside the window, plus an automatic venting hatch high above it.

The third is the best for ventilative cooling. The high automatic hatch is better for noise, rain, insects and safety, so it can stay open at night. Its cold inflow mixes under the ceiling before it reaches people, and together with the low escape hatch it gives a large height for buoyant flow.

The room CFD model in [](appendix-room-cfd.md) compares a window and a top hatch in the same room on a cool summer night and shows the floor speed and the draught at the feet for each. Its app also has a balcony door and a low slot.
