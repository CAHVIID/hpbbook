"""Candidate tapping profiles from the literature, for review before they go into the tank simulator.

Each tapping: (start time h, name, volume at the tap L, flow at the tap L/min, use temperature C).
Volumes for the EN profiles are converted from the tabulated energy with cold water at 10 C and
mean water properties (rho 994 kg/m3, cp 4.182 kJ/kgK, i.e. 1.1547 Wh per L per K).
Writes tapping-profiles-candidates.png/.svg (hourly heat per profile) and prints daily totals.
"""
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

WH_PER_LK = 994 * 4.182 / 3600          # 1.1547 Wh/(L K)
T_COLD = 10.0


def en(t, name, q_kwh, flow, t_use):
    """EN 16147 / Reg. 814/2013 tapping given as energy -> litres at the use temperature."""
    h, m = t
    return (h + m / 60, name, round(q_kwh * 1000 / (WH_PER_LK * (t_use - T_COLD)), 1), flow, t_use)


# Use temperature for EN tappings: Tp where the table gives one, otherwise Tm.
# Small (0.105 kWh, 3 L/min, Tm 25), shower (6 L/min, Tm 40), bath (10 L/min, Tp 40),
# dishwashing (4 L/min, Tp 55), floor cleaning (3 L/min, Tp 40), cleaning (3 L/min, Tm 40).
SMALL = ("small", 0.105, 3, 25)
def small(h, m): return en((h, m), *SMALL)

EN_M = [small(7, 0), en((7, 5), "shower", 1.4, 6, 40), small(7, 30), small(8, 1), small(8, 15), small(8, 30),
        small(8, 45), small(9, 0), small(9, 30), en((10, 30), "floor cleaning", 0.105, 3, 40), small(11, 30),
        small(11, 45), en((12, 45), "dishwashing", 0.315, 4, 55), small(14, 30), small(15, 30), small(16, 30),
        small(18, 0), en((18, 15), "cleaning", 0.105, 3, 40), en((18, 30), "cleaning", 0.105, 3, 40), small(19, 0),
        en((20, 30), "dishwashing", 0.735, 4, 55), small(21, 15), en((21, 30), "shower", 1.4, 6, 40)]

EN_L = [small(7, 0), en((7, 5), "shower", 1.4, 6, 40), small(7, 30), small(7, 45), en((8, 5), "bath", 3.605, 10, 40),
        small(8, 25), small(8, 30), small(8, 45), small(9, 0), small(9, 30), en((10, 30), "floor cleaning", 0.105, 3, 40),
        small(11, 30), small(11, 45), en((12, 45), "dishwashing", 0.315, 4, 55), small(14, 30), small(15, 30),
        small(16, 30), small(18, 0), en((18, 15), "cleaning", 0.105, 3, 40), en((18, 30), "cleaning", 0.105, 3, 40),
        small(19, 0), en((20, 30), "dishwashing", 0.735, 4, 55), en((20, 46), "bath", 3.605, 10, 40), small(21, 30)]

EN_XL = [small(7, 0), en((7, 15), "shower", 1.82, 6, 40), small(7, 26), en((7, 45), "bath", 4.42, 10, 40),
         small(8, 1), small(8, 15), small(8, 30), small(8, 45), small(9, 0), small(9, 30), small(10, 0),
         en((10, 30), "floor cleaning", 0.105, 3, 40), small(11, 0), small(11, 30), small(11, 45),
         en((12, 45), "dishwashing", 0.735, 4, 55), small(14, 30), small(15, 0), small(15, 30), small(16, 0),
         small(16, 30), small(17, 0), small(18, 0), en((18, 15), "cleaning", 0.105, 3, 40),
         en((18, 30), "cleaning", 0.105, 3, 40), small(19, 0), en((20, 30), "dishwashing", 0.735, 4, 55),
         en((20, 46), "bath", 4.42, 10, 40), small(21, 15), en((21, 30), "bath", 4.42, 10, 40)]

# IEA SHC Task 26 (Jordan & Vajen): 200 L/day at 45 C on average. Categories: short 1 L/min x 1 min (28/day),
# medium 6 L/min x 1 min (12/day), shower 8 L/min x 5 min (2/day), bath 14 L/min x 10 min (once a week).
# Deterministic day: short and medium spread evenly 05:00-23:00, showers in the morning and evening peaks.
def task26(bath):
    prof = [(5 + 18 * (i + 0.5) / 28, "short", 1, 1, 45) for i in range(28)]
    prof += [(5 + 18 * (i + 0.3) / 12, "medium", 6, 6, 45) for i in range(12)]
    prof += [(7.0, "shower", 40, 8, 45), (19.5, "shower", 40, 8, 45)]
    if bath:
        prof += [(20.25, "bath", 140, 14, 45)]
    return sorted(prof)

# Marszal-Pomianowska et al. (2021), two Danish detached houses, high-resolution measurements.
# House 1: 4 occupants, 92 L/day hot water, 1.6 showers/day of 7-8 min, ~33 kitchen draws/day mostly < 20 s,
# kitchen 24.5 C, hand washing ~23 C, showers 35.5-40.4 C. Peaks 06:30-07:00 and 18:00-20:00 on weekdays.
# House 2: 2 occupants, ~43 L/day, 0.8 showers/day, ~11 kitchen draws/day at 35.5 C.
# Representative weekday constructed from those statistics (flows are assumed: shower 7 L/min).
DK4 = sorted([(6.75, "shower", 52, 7, 38), (19.5, "shower", 52, 7, 38)]
             + [(t, "kitchen tap", 1.5, 6, 25) for t in (6.6, 6.9, 7.1, 7.3, 7.5, 8.0, 12.0, 12.2, 15.5, 16.0,
                                                          16.5, 17.0, 17.3, 17.6, 17.9, 18.2, 18.5, 18.8, 19.0,
                                                          19.2, 19.7, 20.0, 20.3, 20.6, 21.0, 21.5)]
             + [(t, "washbasin", 1, 5, 23) for t in (6.65, 7.0, 7.2, 7.4, 21.8, 22.0, 22.2, 22.4)])
DK2 = sorted([(7.0, "shower", 42, 7, 38)]
             + [(t, "kitchen tap", 1.5, 6, 35) for t in (7.2, 7.5, 12.0, 17.5, 18.0, 18.3, 18.6, 19.0, 19.3, 20.0, 21.0)]
             + [(t, "washbasin", 1, 5, 23) for t in (7.1, 7.4, 22.0, 22.2)])

CANDIDATES = {
    "EN 16147 M (Reg. 814/2013)": EN_M,
    "EN 16147 L (Reg. 814/2013)": EN_L,
    "EN 16147 XL (Reg. 814/2013)": EN_XL,
    "IEA SHC Task 26, weekday": task26(False),
    "IEA SHC Task 26, bath day": task26(True),
    "Danish house, 4 persons (measured)": DK4,
    "Danish house, 2 persons (measured)": DK2,
}


def heat_kwh(prof):
    return sum(v * WH_PER_LK * (tu - T_COLD) for _, _, v, _, tu in prof) / 1000


if __name__ == "__main__":
    fig, axs = plt.subplots(len(CANDIDATES), 1, figsize=(8, 1.35 * len(CANDIDATES) + 0.6), sharex=True)
    for ax, (name, prof) in zip(axs, CANDIDATES.items()):
        hourly = [0.0] * 24
        for t, _, v, _, tu in prof:
            hourly[int(t)] += v * WH_PER_LK * (tu - T_COLD) / 1000
        vol = sum(v for _, _, v, _, _ in prof)
        print(f"{name:40s} {len(prof):3d} tappings {vol:6.1f} L at the tap {heat_kwh(prof):6.2f} kWh/day")
        ax.bar([h + 0.5 for h in range(24)], hourly, width=0.85, color="#2a78d6")
        ax.set_ylim(0, 9.5); ax.set_yticks([0, 4, 8])
        ax.text(0.2, 8.3, f"{name}: {heat_kwh(prof):.1f} kWh/day", fontsize=9, va="top")
        for s in ("top", "right"): ax.spines[s].set_visible(False)
        ax.axvspan(17, 21, color="#eb6834", alpha=0.10, lw=0)
    axs[-1].set_xticks(range(0, 25, 3)); axs[-1].set_xlim(0, 24)
    axs[-1].set_xlabel("Hour of day (shaded: 17-21, evening price peak)")
    fig.supylabel("Heat drawn per hour [kWh]", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(f"../tapping-profiles-candidates.{ext}", dpi=160)
