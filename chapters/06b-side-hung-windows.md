# Window openings for ventilative cooling 

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

## Introduction

Many new Danish homes have bottom-hung (tilt) windows. They are good for airing in winter: the opening is small, safe and rain-proof, and the sash throws the cold air upwards. In summer they are weak, because the opening area is small and the driving temperature difference is only a few Kelvin. Jiang et al. note that bottom-hung windows may not ventilate enough in the warmer months, when the temperature difference is small {cite:p}`jiang2025`.

A side-hung window opens over its full height and, at 60° or more, over its full width. For single-sided ventilation with a small ΔT it gives roughly four to five times the airflow of a tilted sash of the same size. The inflow is slow and drops to the floor, but in summer it is only slightly cooler than the room, so it gives cooling rather than draught.

In short, the bottom-hung window is a winter window and the side-hung window is a summer window.

This chapter gives the equations behind that statement and the design consequences. It builds on the orifice and stack equations in [](06-ventilative-cooling.md).

%@claude: 

## The free opening area

The airflow is set by the smallest cross-section the air must pass through, the *free opening area*, not by the glass area.

:::{figure} figures/ch06b/window-gaps.*
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

Tilt fittings limit s to about 100–150 mm. For a 0.8 × 1.3 m sash:

| Window | Opening | Free area A |
|---|---|---|
| Side-hung | 90° | 1.04 m² |
| Side-hung | 30° | 0.54 m² |
| Side-hung | 10° | 0.18 m² |
| Bottom-hung | s = 120 mm | 0.25 m² |

## Single-sided airflow

### Stack effect: the shape of the gap matters

For a single opening, warm room air leaves through the top and cool outdoor air enters through the bottom. The pressure difference grows linearly with the distance from the neutral plane, so the orifice equation is integrated over the height of the gap. For a gap of constant width, such as the side-hung window, this gives the familiar result with the neutral plane at mid-height:

```{math}
:label: eq-sh-stack
Q_{st} = \frac{C_d A}{3}\sqrt{\frac{g\,h\,\Delta T}{T}}
```

For the bottom-hung window the integral must be done numerically, because the gap width varies with height ([script](code/window_flow.py)). Most of the free area sits high up in the top slot and the upper parts of the triangles. The neutral plane moves up to about 1.1 m of the 1.3 m sash, and all the inflow must pass through the narrow lower slivers. The result is less flow per square metre of opening than for the side-hung window.

:::{figure} figures/ch06b/window-flow-dt.*
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

## Where the air goes: jets and the Archimedes number

The airflow rate decides the cooling power. The flow pattern decides whether the air is felt as a pleasant breeze, as draught at the ankles or not at all. Heiselberg, Svidt and Nielsen showed in laboratory tests that the flow from an open window can be described with jet theory and stratified-flow theory. They developed simple *flow-element* models for the velocities in the occupied zone {cite:p}`heiselberg2001`.

The balance between buoyancy and momentum in the inflow is measured by the Archimedes number:

```{math}
:label: eq-sh-ar
Ar = \frac{g\,\Delta T\,\sqrt{a_0}}{T\,U_0^2}
```

where a₀ is the effective inflow area (C_d times the inflow part of A) and U₀ = q₀/a₀ is the inflow velocity. A small Ar gives a jet that keeps its direction. A large Ar gives cold air that falls.

:::{figure} figures/ch06b/window-jets.*
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

## Field evidence: tilt windows in a German office

Fitzner and Finke measured winter window ventilation in an 80 m² office in Berlin with six tilted sashes (0.71 × 1.48 m), and compared the results with earlier laboratory studies {cite:p}`fitzner2012`. Four findings bear directly on this chapter.

**The inflow falls to the floor.** Outdoor air enters through the lower part of the tilted sash "with little momentum", falls to the floor and spreads towards the heat sources, which lift it to the ceiling. The room flow is close to displacement ventilation. This is the pattern in {numref}`fig-sh-jets`(a) and (c), and it agrees with Ar ≈ 1 for stack-driven flow.

**The tilt-window flow scales with the height to the power 1.5.** From their own and five other studies they give

```{math}
:label: eq-sh-fitzner
q = 190\,k\,H^{1.5}\sqrt{\Delta T}
```

with q in m³/h, the stroke k and the sash height H in m. For the sash in the worked example (k = 0.12 m, H = 1.3 m, ΔT = 3 K) this gives 58 m³/h. The numerical integration in this chapter gives 57 m³/h. The H^1.5 dependence means the height of the opening matters more than its area. The same argument favours the full-height side-hung opening in summer.

**The comfort limit is set by the floor stream.** With the radiator below the window switched off, the speed at 0.1 m was 0.21–0.27 m/s from 0.6 to 1.8 m from the window, and the draught rate was 27–37 %. With the radiator on, it deflected the falling cold air and the conditions were acceptable. Their design limits for steady window ventilation are a cooling load of at most 30 W/m² (150 W per metre of façade for a 5 m deep room), about 340 W per tilted window, and an outdoor temperature above 6 °C.

**The window types have different jobs.** In winter only tilted windows, with the largest opening at the top, are suitable; side-hung and sliding windows are not. This agrees with Heiselberg et al. {cite:p}`heiselberg2001`. The side-hung window gives a very large opening. It is used for short, full airing in winter, and for continuous ventilation on windless summer days, when the outdoor temperature is in the comfort range. The authors note that natural ventilation is most difficult with no wind and almost no temperature difference, which calls for the largest possible window openings.

## Design consequences

- **Summer cooling (ΔT < 5 K):** use side-hung windows that can open 60–90°. The cooling power scales with A√h, so tall sashes help. The inflow drops and spreads along the floor as a slow stream at close to room temperature, which is acceptable or even welcome when the occupants are warm (see [](07-ceiling-fans.md)).
- **Night cooling (ΔT 5–10 K):** the side-hung window still gives the most air, but the floor stream is colder and faster. This matters little in a bedroom with the occupants in bed, but matters at a desk near the window.
- **Winter airing (ΔT > 15 K):** use bottom-hung windows or hatches placed high, so that the cold air attaches to the ceiling and mixes before it reaches people. Keep the opening small, because a large flow or a large ΔT makes the jet drop.
- **Safety and rain:** a side-hung window open 90° is not burglar-proof or rain-proof. It needs a restrictor, a fixed guard rail or a protected position (balcony, deep reveal) so it can stay open when it is needed.

:::{admonition} Rules of thumb
:class: tip
- A side-hung window opened 60° or more is in effect fully open: A = w·h.
- A tilted sash gives only s·(w + h), about a quarter of the full area for a normal window.
- At the same ΔT, a fully open side-hung window gives 4–5 times the stack flow of a tilted sash of the same size.
- Inflow through a side-hung window is slow and drops to the floor. The floor speed is u ≈ K_w q₀/x with K_w ≈ 5–10 m⁻¹.
- A high bottom-hung window gives a ceiling jet as long as Ar is small. Large flow or large ΔT makes it drop.
:::

## Worked example: side-hung against bottom-hung on a summer evening

A bedroom of 4 × 5 m with a ceiling height of 2.6 m (52 m³) has one 0.8 × 1.3 m sash with its sill at 0.9 m. On a summer evening the room is at 27 °C and the outdoor air at 24 °C, so ΔT = 3 K. The wind speed is 2 m/s. Compare the window opened fully side-hung with the same window tilted 120 mm.

**Step 1: Free area.** Side-hung at 90°: s = 2 · 0.8 · sin 45° = 1.13 m > w, so A = 0.8 · 1.3 = 1.04 m². Bottom-hung: A = 0.12 · (0.8 + 1.3) = 0.25 m².

**Step 2: Stack flow, side-hung.** From {eq}`eq-sh-stack` with T = 300 K:

```{math}
Q_{st} = \frac{0.6 \cdot 1.04}{3}\sqrt{\frac{9.81 \cdot 1.3 \cdot 3}{300}} = 0.074\ \text{m}^3\text{/s} = 267\ \text{m}^3\text{/h}
```

**Step 3: Wind flow.** From {eq}`eq-sh-wind`, Q_w = 0.025 · 1.04 · 2 = 0.052 m³/s = 187 m³/h.

**Step 4: Combined flow and cooling power.** Q = √(267² + 187²) = 327 m³/h, or 6.3 air changes per hour. The cooling power is

```{math}
P = \rho\,c_p\,Q\,\Delta T = 1.2 \cdot 1005 \cdot 0.091 \cdot 3 = 330\ \text{W}
```

That is about 16 W/m² of floor area.

**Step 5: Bottom-hung.** The numerical integration gives Q_st = 57 m³/h and the wind 45 m³/h, so Q = 73 m³/h (1.4 h⁻¹) and P = 74 W. The tilted window removes less than a quarter of the heat. As a check, {eq}`eq-sh-fitzner` gives 58 m³/h for the stack part.

**Step 6: Air speed at the floor.** The inflow passes through the lower half of the side-hung opening: a₀ = 0.6 · 0.52 = 0.31 m², so √a₀ = 0.56 m. The mean inflow velocity is U₀ = 0.091 / 0.31 = 0.29 m/s, and from {eq}`eq-sh-ar`

```{math}
Ar = \frac{9.81 \cdot 3 \cdot 0.56}{300 \cdot 0.29^2} = 0.65
```

Buoyancy and momentum are of the same order, so the slow inflow drops to the floor and spreads. From {eq}`eq-sh-floor` with x₀ ≈ 0 and K_w = 5–10 m⁻¹, the speed 2 m from the window is

```{math}
u = (5\text{–}10) \cdot \frac{0.091}{2} = 0.23\text{–}0.45\ \text{m/s}
```

The air is at about 24–25 °C after mixing, and the occupants are warm, so in summer this is a gentle cooling stream at the feet rather than draught. With the same window open on a cold night, the same equation gives the draught risk.

<!-- ## Guiding questions

1. A window supplier offers a "tilt-and-turn" window (bottom-hung and side-hung in one sash). Describe how you would tell the occupants to use it in July and in January, and why.
2. Why does the stack flow through a tilted sash grow less with the sash height than the flow through a side-hung window does? Use {numref}`fig-sh-gaps` in your answer.
3. Show that Ar in purely stack-driven flow is independent of ΔT. What does that mean for draught from a low window on a windless night?
4. A side-hung window must be restricted to 10° for safety. How much of the summer airflow is lost, and what other opening could make up for it?
5. In the worked example the inflow runs along the floor at about 0.2–0.4 m/s. When is this welcome, and when is it draught? -->
