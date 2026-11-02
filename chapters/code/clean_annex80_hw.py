"""Repair the corrupt hours in the three Annex 80 Copenhagen heat-wave EPW files.

1. Radiation spikes. Each file has 4-6 hours where diffuse (DHI) and global (GHI)
   horizontal radiation are inflated by the same offset of 0.9e6 to 9.1e6 W/m2. The
   direct normal radiation (DNI) is intact: GHI - DHI still equals DNI * cos(zenith).
   The fix keeps the beam part (GHI - DHI) and replaces DHI by the mean of the hours
   before and after (the method of assignments/cooling/code/clean_epw.py).
2. One hour in MostSevere_2054, 27 July 18:00: dry-bulb 20.8 C, dew point -23.1 C and
   RH 3 % between 29.9 C and 27.2 C. Dry-bulb, dew point and horizontal infrared
   radiation are interpolated from the hours before and after, and RH is recomputed.

The missing solar radiation of 1-14 August in Longest_2045 cannot be repaired.

Usage: python clean_annex80_hw.py [weather folder]
Writes <name>_clean.epw next to each original.
"""
import math
import sys
from pathlib import Path

TDB, TDP, RH, IR, GHI, DNI, DHI = 6, 7, 8, 12, 13, 14, 15   # EPW column indices (0-based)
LIMIT = 1500                   # W/m2, above any physical value
FILES = ["5A_Copenhagen_HW_Midterm_Longest_2045.epw",
         "5A_Copenhagen_HW_Midterm_MostIntense_2055.epw",
         "5A_Copenhagen_HW_Midterm_MostSevere_2054.epw"]
BAD_HOURS = {"5A_Copenhagen_HW_Midterm_MostSevere_2054.epw": [("7", "27", "18")]}


def p_sat(t):
    """Saturation vapour pressure (hPa), Magnus formula."""
    return 6.112 * math.exp(17.62 * t / (243.12 + t))


def mean(a, b, col, nd=1):
    return round((float(a[col]) + float(b[col])) / 2, nd)


def clean(src, dst):
    lines = src.read_text(encoding="latin-1").splitlines()
    head, data = lines[:8], [line.split(",") for line in lines[8:]]
    log = []
    for i, r in enumerate(data):
        ghi, dhi = float(r[GHI]), float(r[DHI])
        if dhi > LIMIT or ghi > LIMIT:
            beam = ghi - dhi
            dhi_new = round((float(data[i - 1][DHI]) + float(data[i + 1][DHI])) / 2)
            r[DHI], r[GHI] = str(dhi_new), str(round(dhi_new + beam))
            log.append(f"{r[1]:>2}/{r[2]:<2} h{r[3]:>2}: GHI {ghi:>9.0f} -> {r[GHI]:>4}, "
                       f"DHI {dhi:>9.0f} -> {r[DHI]:>4} W/m2")
        if tuple(r[1:4]) in BAD_HOURS.get(src.name, []):
            a, b = data[i - 1], data[i + 1]
            old = (r[TDB], r[TDP], r[RH])
            r[TDB], r[TDP] = str(mean(a, b, TDB)), str(mean(a, b, TDP))
            r[IR] = str(round(mean(a, b, IR, 0)))
            r[RH] = str(round(100 * p_sat(float(r[TDP])) / p_sat(float(r[TDB]))))
            log.append(f"{r[1]:>2}/{r[2]:<2} h{r[3]:>2}: Tdb/Tdp/RH {'/'.join(old)} -> "
                       f"{r[TDB]}/{r[TDP]}/{r[RH]}")
    head[6] += f" Cleaned: {len(log)} corrupt hours repaired with clean_annex80_hw.py."
    dst.write_text("\n".join(head + [",".join(r) for r in data]) + "\n", encoding="latin-1")
    return log


if __name__ == "__main__":
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "weather"
    for name in FILES:
        src = folder / name
        print(name)
        for line in clean(src, src.with_name(src.stem + "_clean.epw")):
            print("  " + line)
