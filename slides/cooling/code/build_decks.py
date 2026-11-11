"""Build the four starter decks for the cooling assignment. Run: python3 build_decks.py"""
import sys; sys.path.insert(0, "/mnt/project-files/cooling/slides")
from deck_lib import *

F = "/mnt/project-files/cooling/slides/figures/"
D = "/mnt/project-files/cooling/drafts/"
OUT = "/mnt/project-files/cooling/slides/"
COL3 = (W - 2 * Inches(0.3)) // 3
def cx(i, n=3, gap=Inches(0.3)):
    return X0 + i * ((W - gap * (n - 1)) // n + gap)


# ---------------------------------------------------------------- deck 1
def deck1():
    p = new_deck("Passive cooling 1: Window size", "Window size with IDA ICE AutoMOO")
    title_slide(p, "Window size: optimising the facade with AutoMOO", "Passive cooling, lecture 1 of 4  ·  Assignment 4, part 1")
    bullets_slide(p, "Agenda", ["Why window size is a cooling question", "The design summer: Annex 80 Copenhagen 2041–2060",
                                "Daylight as a constraint: EN 17037 sDA", "Multi-objective optimisation and the Pareto front",
                                "Setting up AutoMOO in IDA ICE", "Assignment part 1"])
    where_we_are(p, 0, ["Step 1 of the cooling strategy: reduce solar gains while keeping daylight and view out.",
                        "Each part builds on the model from the previous part. Keep one IDA ICE file per part."])
    section(p, "Why window size is a cooling question", "Part 1")
    fig_slide(p, "The 2050 typical year is the design summer", F + "annex80-typical-years.png",
              bullets=["Parts 1–3 use 5A_Copenhagen_TMY_2041-2060.epw",
                       "82 h above 26 °C outdoors, against 20 h in 2001–2020",
                       "2041–60 has more summer sun than 2081–2100 (686 vs 641 kWh/m²), so it is the more critical file for solar gains"],
              note="Numbers computed from the Annex 80 EPW files in the project folder (make_figures.py). Hours counted over the full year; May–Sep GHI summed from column 14.")
    s = title_only(p, "A window trades daylight and winter sun against summer heat")
    card(s, cx(0), Y0, COL3, Inches(2.6), "Solar gain", ["Scales with window area × g-value × irradiance", "Drives cooling demand and overheating"])
    card(s, cx(1), Y0, COL3, Inches(2.6), "Daylight", ["Scales with window area × light transmittance LT", "Constraint: sDA300,50% ≥ 50 % (EN 17037)"])
    card(s, cx(2), Y0, COL3, Inches(2.6), "Heating", ["A window loses more heat than the wall it replaces", "but collects winter sun on the south facade"])
    text(s, X0, Inches(4.75), W, Inches(0.4), [[("Glazings in the course model", {"bold": True})]], bullets=False)
    table(s, X0, Inches(5.2), W, [["Glazing", "U (W/m²K)", "g", "LT", "Selectivity LT/g"],
                                   ["Pilkington S3 (reference)", "0.6", "0.49", "0.71", "1.4"],
                                   ["Suncool 70/35", "–", "0.34", "0.63", "1.9"],
                                   ["Suncool 66/33", "–", "0.32", "0.59", "1.8"]], col_w=[0.4, 0.15, 0.15, 0.15, 0.15])
    notes(s, "Glazing values from the Assignment 04 solution file and 'Advice for parametric run.pptx'. Fill in the U-values of the Suncool panes from the datasheet (keep U ≤ 0.6 W/m²K).")
    section(p, "Multi-objective optimisation", "Part 1")
    fig_slide(p, "A Pareto front shows the best trade-offs", F + "pareto-schematic.png",
              bullets=["Two objectives: minimise cooling demand and heating demand",
                       "One constraint: sDA300 ≥ 50 %",
                       "A design is dominated if another design is better on both",
                       "The front is the set of non-dominated designs",
                       "You choose on the front, using what the model leaves out: view, glare, cost, the other rooms"], split=0.45)
    s = title_only(p, "Setting up AutoMOO in IDA ICE")
    flow(s, [["Variables", "window height and width"], ["IDA ICE runs", "genetic algorithm"], ["Objectives", "min cooling, min heating"],
             ["Constraint", "sDA300 ≥ 50 %"], ["Pareto front", "pick a design"]], Y0, h=Inches(1.3), size=15)
    card(s, cx(0), Inches(3.5), COL3, Inches(3.1), "Variables", ["Window height, sill at 0.9 m", "Window width", "Optional: glazing type, overhang depth", "Whole range must fit in the wall"], size=14)
    card(s, cx(1), Inches(3.5), COL3, Inches(3.1), "Simulation", ["Type: custom + climate-based daylight", "Keep generated models: yes", "Set each output's role: objective or constraint"], size=14)
    card(s, cx(2), Inches(3.5), COL3, Inches(3.1), "Keep it fast", ["Relax the tolerance, set a max. time step", "Limit the outputs", "Test with a few runs first"], size=14)
    notes(s, "Hints taken from the assignment draft, part 1. See also 'How to - IDA ICE parametric daylight run.pdf' in the course folder.")
    s = title_only(p, "Demo: AutoMOO on the 4 × 4 m centre zone")
    todo(s, X0, Y0, W, Y1 - Y0 - Inches(0.2), ["Screenshots from IDA ICE: parametric run dialog, choosing AutoMOO, setting objective and constraint roles.",
                                               "Pareto plot export and how to read the chosen design back into the model.",
                                               "Single-zone model: 4 × 4 m, 2.5 m high, U = 0.1 W/m²K, facing north or south."])
    s = title_only(p, "Assignment part 1")
    flow(s, [["Q1.1", "reference: sDA, cooling, heating, N and S"], ["Q1.2", "AutoMOO study, Pareto front"], ["Q1.3", "choose a design, repeat table"], ["Q1.4", "reflect"]], Y0, h=Inches(1.4))
    text(s, X0, Inches(3.6), W, Inches(2.8), [[("Hand in", {"bold": True})], "Q1.1/Q1.3 table for north and south",
                                              "Pareto figure with your chosen design marked", "5–10 lines of reflection"], size=16)
    notes(s, "Teacher check only, not for the slides: facade chapter worked example gives south optimum g 0.32, 1.2 m overhang, 1.1 m window height, sDA 53 %, cooling 19.6 kWh/m² (−63 %); north 1.4 m, sDA 59 %, 15.1 kWh/m² (−27 %).")
    s = title_only(p, "Questions to discuss")
    text(s, X0, Y0, W, Y1 - Y0, ["Why is the optimal south window smaller than the north one?",
                                 "What did the optimisation leave out: view out, glare, the other rooms, future weather, cost?",
                                 "Your window was optimised for the 2050 typical year. Would it change for the heat-wave year?"], size=20, space=14)
    p.save(OUT + "lecture-1-window-size-automoo.pptx")


# ---------------------------------------------------------------- deck 2
def deck2():
    p = new_deck("Passive cooling 2: Venting hatches and draught", "Venting hatches without draught")
    title_slide(p, "Venting hatches without draught", "Passive cooling, lecture 2 of 4  ·  Assignment 4, part 2")
    bullets_slide(p, "Agenda", ["Why ventilative cooling needs hatches", "Hatch types and requirements", "Jet theory: ceiling jet and floor flow",
                                "Draught criteria: ISO 7730 DR and ASHRAE 55 ankle draught", "From a draught limit to an ACH limit",
                                "Ventilative cooling in IDA ICE, limited by draught", "Assignment part 2"])
    where_we_are(p, 1, ["Step 3 of the cooling strategy: remove heat with outdoor air, without draught.",
                        "Carry your north and south windows from part 1 into the whole-house model."])
    section(p, "Why hatches", "Part 2")
    fig_slide(p, "Ventilative cooling needs large airflows", D + "ventilation-modes.png",
              bullets=["Cooling P = ṁ · cp · ΔT: a small summer ΔT needs 4–10 ACH",
                       "The risk is not the hot afternoon but the evening, night and shoulder season, when outdoor air is 8–12 K below the room",
                       "Fixed frameless windows need a separate opening: the hatch"], split=0.4,
              note="Figure from the ventilative cooling chapter draft (cooling/drafts/ventilation-modes.png).")
    s = title_only(p, "Hatch types: where does the cold air go?")
    card(s, cx(0), Y0, COL3, Inches(2.5), "High, bottom-hung", ["Air attaches to the ceiling as a wall jet", "Mixes before it reaches people"], size=14)
    card(s, cx(1), Y0, COL3, Inches(2.5), "Low opening", ["Cold air spreads along the floor", "Highest draught risk at the ankles"], size=14)
    card(s, cx(2), Y0, COL3, Inches(2.5), "Side-hung", ["Thermal jet that drops", "Treat as a low opening with a larger K"], size=14)
    text(s, X0, Inches(4.6), W, Inches(0.4), [[("Every hatch must", {"bold": True})]], bullets=False)
    text(s, X0, Inches(5.05), W // 2 - Inches(0.2), Inches(1.8), ["Keep out rain and burglars", "Allow night opening", "Add little heat loss when closed"], size=15)
    text(s, X0 + W // 2, Inches(5.05), W // 2, Inches(1.8), ["Fire escape if it replaces a window: width > 0.5 m, height > 0.6 m, width + height > 1.5 m, sill ≤ 1.2 m (BR18)"], size=15)
    s = title_only(p, "A closed hatch must insulate like a wall")
    stat(s, cx(0), Y0, COL3, "170 mm", "Gas-filled foam (λ 0.020) for U = 0.12 W/m²K, as two panels (120 + 45 mm)")
    stat(s, cx(1), Y0, COL3, "60 mm", "Vacuum panel (λ 0.007) for the same U, at about 25 × the cost")
    stat(s, cx(2), Y0, COL3, "0.07", "W/m²K for a hatch integrated in a prefab facade (2D Comsol), Ψ = 0.005 W/mK")
    text(s, X0, Inches(4.2), W, Inches(2.4), [[("In IDA ICE (Q2.2)", {"bold": True})],
                                              "Model the hatch as a window with frame fraction 0.999 and frame U = hatch U",
                                              "Report the house's mean U-value and heating demand before and after"], size=16)
    notes(s, "Numbers from lecture 16.2 Venting hatches. Two panels because one thick panel blocks the opening and cannot rotate.")
    section(p, "Jet theory", "Part 2")
    s = title_only(p, "High hatch: a ceiling wall jet, if it stays up", note="Svidt, Heiselberg & Nielsen (2000), Table 1: Ka ≈ 7, x0 ≈ −2 m. Only valid well away from the hatch. Heiselberg (2006): the supply acts as a jet for ΔT < 5 K and/or Δp > 4–6 Pa.")
    picture(s, F + "ceiling-jet-decay.png", X0 + int(W * 0.45), Y0, W - int(W * 0.45), Y1 - Y0)
    equation(s, X0, Y0, int(W * 0.45) - Inches(0.3), Inches(1.0), "u_m = K_a · U₀ · √a₀ / (x + x₀)", "Max. jet speed, Ka ≈ 7, x₀ ≈ −2 m")
    text(s, X0, Y0 + Inches(1.25), int(W * 0.45) - Inches(0.3), Inches(3.4),
         ["U₀ = q₀ / a₀: same airflow through a larger opening gives a slower jet",
          "Conservative: take the speed where the jet turns down at the opposite wall",
          "Large ΔT and weak driving force: the cold jet drops off the ceiling",
          "Argue with Ar = g β ΔT h₀ / U₀²"], size=15)
    s = fig_slide(p, "Low opening: cold air spreads along the floor", D + "flow-element/bugenings-floor-flow.png",
                  cap="Bugenings et al. (2025) louvre data, K fitted to 4.4 1/m. Figure from cooling/drafts/flow-element.")
    s = title_only(p, "Low opening: the floor flow element")
    equation(s, X0, Y0, int(W * 0.5), Inches(1.0), "u(x) = K · q₀ / x", "Nielsen et al. (2000), radial floor flow")
    text(s, X0, Y0 + Inches(1.3), int(W * 0.5), Inches(3.3), ["K ≈ 4–5 1/m near isothermal (4.4 fitted to the Bugenings louvre)",
                                                             "K up to about 10 1/m with a large ΔT",
                                                             "Evaluate at 0.1 m above the floor, 1 m from the wall",
                                                             "q₀ in m³/s"], size=16)
    card(s, X0 + int(W * 0.56), Y0, int(W * 0.44), Inches(3.2), "Quick check", ["40 m³ zone at 5 ACH: q₀ = 0.056 m³/s", "K = 4.4 1/m gives u = 0.24 m/s at 1 m", "K = 10 1/m gives 0.56 m/s"], size=15)
    # Heiselberg et al. (1999) and Nielsen et al. (2000): Aalborg window studies
    REF99 = "Heiselberg, Dam, Sørensen, Nielsen & Svidt (1999). Characteristics of air flow through windows. HybVent Forum '99, Sydney. AAU Indoor Env. Eng. No. 103."
    REF00 = "Nielsen, Dam, Sørensen, Svidt & Heiselberg (2000). Characteristics of buoyant flow from open windows in naturally ventilated rooms. ROOMVENT 2000, 825–830."
    fig_slide(p, "Three windows in the Aalborg lab", F + "window-types-heiselberg.png",
              cap="After Heiselberg et al. (1999). Test room 8 × 6 × 3 m; the windows sit in an insulated wall to a cooled room.",
              note=REF99 + " The paper has photos of the three windows (Fig. 3); the drawing here is ours. No window dimensions are given in the paper.")
    s = title_only(p, "Where the cold air lands depends on the window", note=REF99)
    hw = (W - Inches(0.3)) // 2
    card(s, X0, Y0, hw, Inches(3.2), "Single-sided", ["Types 1 and 2: air reaches the floor 0.5–1.5 m from the window and spreads as a stratified layer",
                                                    "Even small openings give high velocities in the occupied zone",
                                                    "Type 3: little air at small angles; it runs down the wall and only reaches the floor at large angles"], size=14)
    card(s, X0 + hw + Inches(0.3), Y0, hw, Inches(3.2), "Cross and stack", ["Types 1 and 2: a thermal jet that reaches the floor",
                                                                         "Type 3, bottom-hung opening in: ceiling jet that separates furthest from the wall, so the lowest velocities",
                                                                         "Type 3, top-hung opening in: free jet into the occupied zone, very high velocities"], size=14)
    text(s, X0, Inches(5.35), W, Inches(1), [[("Design consequence: ", {"bold": True}), ("throw the cold air upwards, above the occupied zone, and let it mix before it falls.", {})]], size=17, bullets=False)
    s = title_only(p, "The discharge coefficient is not a constant", note=REF99 + " Cd measured for type 1 (side-hung) only; the paper gives Cd as plots, not tables. IDA ICE default Cd = 0.65 (lecture 16.1).")
    equation(s, X0, Y0, int(W * 0.5), Inches(1.0), "q = C_d · A · √(2Δp / ρ)", "Orifice equation for an opening")
    text(s, X0, Y0 + Inches(1.35), int(W * 0.55), Inches(3.4), ["Measured for the side-hung window (type 1)",
                                                               "Isothermal: Cd does not depend on Δp, but does depend on the opening area",
                                                               "With a temperature difference: Cd is a function of the Archimedes number and the opening area",
                                                               "Cd above 1 at small angles: the geometric opening area is hard to define"], size=16)
    card(s, X0 + int(W * 0.6), Y0, int(W * 0.4), Inches(3.0), "Why it matters",
         ["A constant Cd, such as IDA ICE's default 0.65, can give serious errors in the predicted airflow", "Check your hatch airflow by hand (Q2.8)"], size=15)
    s = title_only(p, "A side-hung window as a flow element", note=REF00 + " Velocities in the 1999 paper (Fig. 11): ΔT 4.5–8.5 K, 99–389 m³/h, 0–5 m from the wall.")
    stat(s, cx(0), Y0, COL3, "0.81 × 1.38 m", "Side-hung window, sill 1 m above the floor", size=30)
    stat(s, cx(1), Y0, COL3, "0.04 / 0.10 m²", "Opening area a₀ at 5° and 15°", size=30)
    stat(s, cx(2), Y0, COL3, "4–20 1/m", "K_w, rising with Ar′ and a₀", size=30)
    equation(s, X0, Inches(3.75), int(W * 0.5), Inches(1.0), "u_x = K_w · q₀ / (x + x₀)", "Max. floor velocity, measured slope −1.0 in log-log")
    text(s, X0 + int(W * 0.55), Inches(3.75), int(W * 0.45), Inches(2.8),
         ["The cold air drops as a thermal jet, then spreads radially along the floor", "x₀ is negative: the virtual origin lies in front of the window, down to about −3 m",
          "An opening with K ≈ 5 1/m and small x₀ would cut occupied-zone velocities"], size=15)
    fig_slide(p, "Opening height decides where the cold air goes", D + "room-cfd/compare-openings.png",
              cap="Course 2D CFD model (room_cfd.py), 6 ACH, gains set for a well-mixed 26 °C. Teaching model, not mesh-converged.",
              note="From the CFD thread. Low opening keeps cold air on the floor; high opening mixes it but the jet can still drop at the far wall.")
    section(p, "Draught criteria", "Part 2")
    s = title_only(p, "Two ways to judge draught")
    hw = (W - Inches(0.3)) // 2
    equation(s, X0, Y0, hw, Inches(1.1), "DR = (34 − tₐ)(v − 0.05)^0.62 (0.37 v Tu + 3.14)", "ISO 7730 draught rate", size=17)
    text(s, X0, Y0 + Inches(1.35), hw, Inches(2.8), ["Tu = 40 % if unknown", "DR ≤ 20 % is acceptable (category II)", "Local air temperature and speed at the ankle",
                                                    "No 'feet factor': use DR as it stands"], size=15)
    equation(s, X0 + hw + Inches(0.3), Y0, hw, Inches(1.1), "PPD_AD = 100 · eᶻ / (1 + eᶻ),  z = −2.58 + 3.05 v − 1.06 TS", "ASHRAE 55-2020 ankle draught (Liu et al. 2017)", size=15)
    text(s, X0 + hw + Inches(0.3), Y0 + Inches(1.35), hw, Inches(2.8), ["Limit PPD_AD ≤ 20 %", "Equals v_ankle < 0.35 TS + 0.39 m/s", "TS = whole-body thermal sensation: a cool body tolerates less air speed"], size=15)
    notes(s, "Do not apply the 0.82 'feet factor': it was a misread correlation coefficient. Use plain ISO 7730 DR and the ASHRAE 55 ankle model.")
    fig_slide(p, "From a draught limit to an ACH limit", F + "floor-speed-vs-ach.png", split=0.36,
              bullets=["Low opening, 40 m³ zone", "DR 20 % at 26 °C reached at about 5 ACH with K = 4.4, about 2 ACH with K = 10",
                       "Ankle model at TS = 0: about 8 and 3.5 ACH", "Repeat for your hatch and plot max. ACH against ΔT (Q2.4)"],
              note="Computed in make_figures.py: v = K q0 / x at x = 1 m; DR solved for 20 % with Tu = 40 %. Compare with the Roth et al. (2023) chart in lecture 16.2 (CBE/ankle curve).")
    section(p, "Ventilative cooling in IDA ICE", "Part 2")
    s = title_only(p, "Three runs, one limit")
    flow(s, [["Q2.5", "cross-ventilation through hatches"], ["Q2.6", "add stack via roof skylight, PI on critical zone"],
             ["Q2.7", "cap ACH at your draught limit"], ["Q2.8 (optional)", "hand calc. vs IDA ICE airflow"]], Y0, h=Inches(1.4))
    text(s, X0, Inches(3.6), W, Inches(3), [[("IDA ICE hints", {"bold": True})], "Hourly airflow per opening is in the zone results; convert to ACH with the zone volume",
                                            "Limit with the max. opening fraction, or a limiter on the opening signal that depends on outdoor temperature",
                                            "Check afterwards that the peak ACH stays under your limit"], size=16)
    s = title_only(p, "Demo: hatch control and ACH limiter in IDA ICE")
    todo(s, X0, Y0, W, Y1 - Y0 - Inches(0.2), ["Screenshots: hatch as a window object, opening control macro, skylight PI controller on the critical zone.",
                                               "How to read 'Air flow through openings' and convert to ACH.",
                                               "Optional: compare jet theory with the IDA ICE flow element for one evening hour."])
    s = title_only(p, "Assignment part 2")
    text(s, X0, Y0, W, Y1 - Y0, [[("Hand in", {"bold": True})], "Hatch cross section with dimensions, free area and Cd",
                                 "Hatch U-value and heating penalty", "Jet calculation for 2 K and 10 K, with the work shown",
                                 "ACH-limit chart against ΔT", "Hours above adaptive category II for Q2.5–Q2.7"], size=18, space=10)
    p.save(OUT + "lecture-2-venting-hatch-draught.pptx")


# ---------------------------------------------------------------- deck 3
def deck3():
    p = new_deck("Passive cooling 3: Ceiling fans", "Ceiling fans for peak periods")
    title_slide(p, "Ceiling fans for peak periods", "Passive cooling, lecture 3 of 4  ·  Assignment 4, part 3")
    bullets_slide(p, "Agenda", ["How a fan cools people", "Cooling effect from air speed (SET)", "Choosing and placing a fan",
                                "Cooling fan efficiency", "Peak-period operation", "Cooling COP against air-conditioning", "Assignment part 3"])
    where_we_are(p, 2, ["Step 4 of the cooling strategy: ventilative cooling cannot go below the outdoor temperature.",
                        "A fan lets occupants accept a higher temperature, at a fraction of the power of air-conditioning."])
    section(p, "How a fan cools", "Part 3")
    fig_slide(p, "A fan cools people, not the room", D + "ceiling-fan-airflow.png",
              bullets=["Higher air speed raises convective and evaporative heat loss", "The air temperature does not drop",
                       "So the fan only helps when someone is in the room"], split=0.38)
    fig_slide(p, "Cooling effect rises steeply up to about 0.5 m/s", F + "cooling-effect-vs-speed.png", split=0.38,
              bullets=["0.5 m/s gives 2.8 °C at 28 °C, 50 % RH, 1.2 met, 0.5 clo", "Above about 0.8 m/s extra speed buys little",
                       "CBE design guide uses about 2 °C at 0.5 m/s as a design value", "Use pythermalcomfort cooling_effect()"],
              note="Computed with pythermalcomfort 3.x cooling_effect (SET method, ASHRAE 55).")
    fig_slide(p, "The effect is local: sit within one diameter", D + "cooling-effect-distance.png", split=0.38,
              bullets=["Largest within about 0.4 D of the centre", "Drops sharply at the edge of the jet", "Half speed costs about 1 °C under the fan, but saves far more power",
                       "Place the fan over the bed or the sofa"], note="Figure from the ceiling fans chapter (Raftery et al. 2019 air speeds, 1.5 m fan).")
    section(p, "Choosing a fan", "Part 3")
    s = title_only(p, "Choosing and placing a fan")
    card(s, cx(0), Y0, COL3, Inches(2.9), "Size", ["Diameter 0.2–0.4 × √(floor area)", "One fan per roughly square cell", "Aspect ratio up to 1.5:1"], size=14)
    card(s, cx(1), Y0, COL3, Inches(2.9), "Mounting", ["Blades ≥ 2.1 m above floor (CBE); 2.3 m in EN 60335-2-80 [to confirm]", "≈ 0.2 D below the ceiling", "≥ 0.45 m from walls"], size=14)
    card(s, cx(2), Y0, COL3, Inches(2.9), "Datasheet", ["Airflow and power at each speed", "Watch CFM vs m³/h", "DC motors use far less power"], size=14)
    equation(s, X0, Inches(5.0), W, Inches(1.2), "S_F = 4Q / (πD²)      S_O,avg = S_F (0.25 + 0.99 D/R − 0.06 C/D + 0.11 D/1.7 + 0.024)",
             "Room-average air speed for seated occupants (Raftery et al. 2019); D, R, C in m", size=17)
    notes(s, "What does a 2.5 m ceiling mean for blade height and ceiling clearance? Good class discussion. The 2.3 m value in EN 60335-2-80 is still to be confirmed by Christian.")
    fig_slide(p, "Compare fans by cooling per watt", F + "cfe-fans.png", split=0.36,
              bullets=["CFE = cooling effect / fan power (ASHRAE 216)", "Six fans give 3.5–3.9 °C, but CFE differs six-fold",
                       "Choose by power at the speed you need, not by max. airflow"], note="Data from table tab-cfe in the ceiling fans chapter.")
    section(p, "Operation and cooling COP", "Part 3")
    s = title_only(p, "Run the fan only in peak periods")
    flow(s, [["Occupied hour?", ""], ["T_op > cat. II limit?", "or your own threshold"], ["Fan on", "count hour and kWh"], ["Recount hours", "T_op − CE vs limit"]], Y0, h=Inches(1.3), active=2)
    text(s, X0, Inches(3.5), W, Inches(3), ["Fan hours come from your part 2 results", "Fan power counts only in fan hours",
                                            "Recount the hours above category II with CE subtracted, or with the limit raised by CE"], size=17)
    notes(s, "The old PMV script charged 15 W in every hour and gave identical results with and without fans; it is retired until fixed.")
    s = title_only(p, "Cooling COP: what the fan saves an air-conditioner")
    equation(s, X0, Y0, W, Inches(1.2), "COP_fan = [Q_cool(T_sp) − Q_cool(T_sp + CE)] / E_fan", "Ideal cooling demand in IDA ICE at two setpoints, over the fan hours")
    stat(s, cx(0), Inches(3.5), COL3, "5–8", "SEER of a split air-conditioner")
    stat(s, cx(1), Inches(3.5), COL3, "10–100 ×", "HVAC savings over fan energy (CBE guide)")
    text(s, cx(2), Inches(3.5), COL3, Inches(2.8), ["The fan removes no heat", "Compare primary energy", "When do fans run compared with the electricity price?"], size=15)
    s = title_only(p, "Worked example: one fan in a row-house bedroom")
    todo(s, X0, Y0, W, Y1 - Y0 - Inches(0.2), ["Pick a real DC fan, read Q and P per speed from the datasheet.",
                                               "S_F → S_O,avg → CE at 28 °C → CFE per speed; mark the most efficient speed.",
                                               "Show the two-setpoint IDA ICE run for COP_fan on one zone."])
    s = title_only(p, "Assignment part 3")
    flow(s, [["Q3.1", "choose a fan"], ["Q3.2", "air speed and CE"], ["Q3.3", "CFE per speed"], ["Q3.4", "peak-period hours, kWh"], ["Q3.5", "cooling COP"]], Y0, h=Inches(1.3))
    text(s, X0, Inches(3.5), W, Inches(3), [[("Hand in", {"bold": True})], "Table of air speed, CE, power and CFE per speed",
                                            "Fan hours, kWh, and hours above category II with and without fans", "COP_fan with the calculation, 5–10 lines comparing with AC"], size=16)
    p.save(OUT + "lecture-3-ceiling-fans.pptx")


# ---------------------------------------------------------------- deck 4
def deck4():
    p = new_deck("Passive cooling 4: Shutters and fans in a heat wave", "Shutters and fans in a heat wave")
    title_slide(p, "Shutters and fans in a heat wave", "Passive cooling, lecture 4 of 4  ·  Assignment 4, part 4")
    bullets_slide(p, "Agenda", ["Heat waves in future Copenhagen", "The Annex 80 heat-wave files", "External shutters and their control",
                                "Shutters in IDA ICE", "Fans on top", "Assignment part 4 and wrap-up"])
    where_we_are(p, 3, ["Step 5 of the cooling strategy: in a heat wave, close external shutters during the day.",
                        "The hatches keep ventilating while the shutters are closed."])
    section(p, "Heat waves", "Part 4")
    s = fig_slide(p, "The 2054 heat wave: four weeks near the comfort limit", F + "heatwave-2054.png",
                  cap="5A_Copenhagen_HW_Midterm_MostSevere_2054.epw (Annex 80, MPI-REMO RCP8.5). Limit θc + 3 °C with θc = 0.33 θrm + 18.8.")
    s = title_only(p, "Hot days, but the nights still cool")
    stat(s, cx(0, 4), Y0, (W - Inches(0.9)) // 4, "32.0 °C", "Outdoor maximum")
    stat(s, cx(1, 4), Y0, (W - Inches(0.9)) // 4, "14 days", "above 28 °C")
    stat(s, cx(2, 4), Y0, (W - Inches(0.9)) // 4, "11 °C", "Coldest night in the heat wave")
    stat(s, cx(3, 4), Y0, (W - Inches(0.9)) // 4, "28–30 °C", "Adaptive cat. II upper limit")
    picture(s, F + "heatwave-week.png", X0, Inches(3.6), W, Inches(3.2))
    notes(s, "Warmest week 16–22 July 2054: 87 of 168 hours below 24 °C outdoors, so night venting through the hatches still works. Computed in make_figures.py.")
    s = title_only(p, "Which heat-wave file?")
    table(s, X0, Y0, W, [["Annex 80 Copenhagen file", "Use?", "Why"],
                          ["HW_Midterm_MostSevere_2054", "Yes", "9 Jul – 5 Aug, max 32.0 °C. Hand out a cleaned file: a few corrupt GHI/DHI hours"],
                          ["HW_Midterm_MostIntense_2055", "Optional", "For comparison"],
                          ["HW_Midterm_Longest_2045", "No", "No solar radiation on 1–14 August, in the middle of the heat wave"]],
          col_w=[0.32, 0.1, 0.58], size=14, row_h=Inches(0.55))
    text(s, X0, Inches(4.5), W, Inches(2), ["Files are full years: annual results are meaningless", "Extract the heat-wave period only"], size=17)
    s = title_only(p, "What the literature says")
    card(s, X0, Y0, int(W * 0.6), Inches(4.4), "Farahani et al. (2021), Finnish apartments in IDA ICE",
         ["Heat-wave summers: about 10,000 Kh above 27 °C (2018) and 14,000 Kh (synthetic 2050)", "Orientation, blinds and site shading helped little",
          "Openable windows were the most effective passive measure in the new building", "Only a split AC unit removed overheating everywhere"], size=15)
    text(s, X0 + int(W * 0.64), Y0, int(W * 0.36), Inches(4.4), ["Question for the class: what would external shutters and hatches have changed in that study?"], size=15, color=GREY)
    notes(s, "Farahani et al. 2021, Appl. Sci. 11:3972 (doi 10.3390/app11093972), summarised in cooling-background-inventory.md.")
    section(p, "Shutters", "Part 4")
    s = title_only(p, "External shutters block almost all solar gain")
    card(s, cx(0), Y0, COL3, Inches(2.8), "Gain", ["Solar factor multiplier about 0.05–0.1", "Stops the gain before it enters"], size=14)
    card(s, cx(1), Y0, COL3, Inches(2.8), "Cost", ["Daylight and view out", "So keep them for the hottest days"], size=14)
    card(s, cx(2), Y0, COL3, Inches(2.8), "Airflow", ["Shutters close the window as an opening", "The hatch must be a separate opening"], size=14)
    text(s, X0, Inches(5.0), W, Inches(1.5), ["South, east and west windows. Decide about north and argue for it."], size=17)
    s = title_only(p, "A shutter control rule")
    flow(s, [["Incident solar", "> 150–200 W/m² on the window"], ["and room", "above a temperature threshold"], ["Close", "otherwise open"]], Y0, h=Inches(1.4), active=2)
    text(s, X0, Inches(3.7), W, Inches(2.8), [[("Think like an occupant", {"bold": True})], "Would they accept closed shutters in the morning, or at weekends?",
                                              "Who overrides the automation, and when?"], size=17)
    s = title_only(p, "Demo: shutters in IDA ICE")
    todo(s, X0, Y0, W, Y1 - Y0 - Inches(0.2), ["External shading device with low solar factor and its own control (schedule, solar radiation, zone temperature).",
                                               "Check the shutter does not also close the hatch.",
                                               "Extract the heat-wave period; plot outdoor, zone operative and adaptive limit for the warmest week."])
    section(p, "Fans on top", "Part 4")
    s = title_only(p, "Report the heat wave step by step")
    table(s, X0, Y0, W, [["Heat wave, critical zone", "Hours > cat. II", "Max T_op (°C)", "Warmest night (°C)", "Fan kWh"],
                          ["Part 2 hatches only", "", "", "", "–"], ["+ shutters", "", "", "", "–"], ["+ shutters + fans", "", "", "", ""]],
          col_w=[0.32, 0.17, 0.17, 0.19, 0.15], size=15, row_h=Inches(0.6))
    text(s, X0, Inches(4.6), W, Inches(2), ["Warmest night = mean operative temperature 23–07", "Fans: recount the hours with the cooling effect from part 3"], size=16)
    s = title_only(p, "Wrap-up: the whole cooling assignment")
    text(s, X0, Y0, W, Y1 - Y0, ["Which of the four steps gave the largest cut in overheating hours per krone? Which was free?",
                                 "Where in the year does your hatch hit its draught limit, and would occupants close it anyway?",
                                 "A fan with a COP of 50 sounds better than any air-conditioner. What does the comparison leave out?",
                                 "Shutters solve the heat wave but darken the home. How would you hand the decision to the occupants?",
                                 "Is the house safe to live in during the heat wave without active cooling?"], size=18, space=12)
    p.save(OUT + "lecture-4-shutters-heatwave.pptx")


for f in ([deck2] if "--deck2" in sys.argv else (deck1, deck2, deck3, deck4)): f()
print("built")
