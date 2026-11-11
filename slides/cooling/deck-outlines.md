# Cooling assignment: outlines for the four lecture decks

*Draft 2026-10-10. Each deck follows one part of `cooling/assignment/cooling-assignment.md` (hpbbook PR #20). Template: DTU master from lecture 13.1. [TO DEVELOP] = a placeholder slide for IDA ICE screenshots or a worked example.*

Every deck opens with: title, agenda, and "Where we are" (a strip of the four parts with this one highlighted).

## Lecture 1: Window size with AutoMOO (12 slides)

1. **Why window size is a cooling question**
   - The 2050 typical year is the design summer: 82 h above 26 °C vs 20 h in 2001–20; more sun than 2081–2100 (chart from the Annex 80 EPWs)
   - A window trades daylight and winter sun against summer heat: 3 cards (solar gain, daylight, heating) + glazing table (S3, Suncool 70/35, 66/33)
2. **Multi-objective optimisation**
   - Pareto front: dominated vs non-dominated designs, choosing on the front (schematic chart)
   - Setting up AutoMOO: variables → runs → objectives → sDA constraint → front; hints for fast runs
   - [TO DEVELOP] Demo on the 4 × 4 m centre zone
3. **Assignment part 1**: Q1.1–Q1.4 and hand-in
4. **Questions to discuss**: south vs north window; what the optimisation leaves out; 2050 vs the heat-wave year

## Lecture 2: Venting hatches without draught (19 slides)

1. **Why hatches**
   - Ventilative cooling needs 4–10 ACH; the risk is evening/night with ΔT 8–12 K (ventilation-modes figure)
   - Hatch types: high bottom-hung, low, side-hung; requirements (rain, burglary, night opening, BR18 fire escape)
   - A closed hatch must insulate: 170 mm foam / 60 mm VIP for U 0.12; prefab U 0.07; modelling it in IDA ICE (Q2.2)
2. **Jet theory**
   - High hatch: ceiling wall jet u_m = K_a U₀ √a₀ / (x + x₀), Archimedes number, when the jet drops (chart)
   - Low opening: floor flow u = K q₀ / x, K 4.4–10 (Bugenings data figure + quick check)
   - Heiselberg et al. (1999) and Nielsen et al. (2000), 4 slides: the three window types in the Aalborg lab; where the cold air lands (single-sided vs cross/stack); Cd is not a constant; the side-hung window as a flow element (K_w 4–20 1/m, x₀ to −3 m)
   - Opening height decides where cold air goes (course 2D CFD figure)
3. **Draught criteria**: ISO 7730 DR and the ASHRAE 55 ankle model side by side (no feet factor)
4. **From draught limit to ACH limit**: floor speed vs ACH with the DR and ankle limits (chart: about 5 ACH at K 4.4, 2 ACH at K 10)
5. **Ventilative cooling in IDA ICE**: Q2.5 cross → Q2.6 stack → Q2.7 ACH cap → Q2.8 hand vs IDA; [TO DEVELOP] demo
6. **Assignment part 2**: hand-in list

## Lecture 3: Ceiling fans for peak periods (15 slides)

1. **How a fan cools**
   - Cools people, not the room (fan airflow figure)
   - Cooling effect vs air speed: 2.8 °C at 0.5 m/s, 28 °C (SET chart)
   - The effect is local: sit within one diameter (CE vs distance figure)
2. **Choosing a fan**
   - Size, mounting (2.1 m CBE vs 2.3 m EN 60335-2-80, to confirm), datasheet; Raftery S_F and S_O,avg
   - Compare fans by CFE = CE / P_fan: six fans, CFE differs six-fold; which speed is most efficient (chart from the chapter table)
3. **Peak-period operation**
   - Peak-period rule: occupied + above cat. II → fan on, recount hours with CE
   - Running `code/fan_comfort.py` on the unpacked IDA ICE results: fan hours, kWh, hours above cat. II with and without fans
   - Fan COP as an equivalent-comfort yardstick: COP_fan = q_fan · ρ · cp · CE / P_fan (the fan's own airflow, delivered CE cooler); about 280–430 for the Fanco 132, against SEER 5–8 for a split AC. Caveat: not heat actually removed
   - [TO DEVELOP] Worked example: one fan in a bedroom, CE, CFE and COP_fan per speed
4. **Assignment part 3**: questions and hand-in

## Lecture 4: Shutters and fans in a heat wave (15 slides)

1. **Heat waves**
   - The 2054 heat wave: daily outdoor range vs adaptive cat. II limit (chart)
   - Hot days, cool nights: 32.0 °C max, 14 days > 28 °C, nights to 11 °C; warmest week hourly (chart)
   - Which file: MostSevere 2054 yes (cleaned), Longest 2045 no (radiation gap)
   - What the literature says: Farahani et al. 2021
2. **Shutters**
   - External shutters block almost all gain: g multiplier 0.05–0.1, cost in daylight, hatch must stay a separate opening
   - A control rule: solar > 150–200 W/m² and room warm → close; occupant acceptance
   - [TO DEVELOP] Demo: shutters in IDA ICE
3. **Fans on top**: the Q4.4 results table (hatches / + shutters / + fans)
4. **Wrap-up of the whole assignment**: the guiding questions, including what the fan COP comparison leaves out
