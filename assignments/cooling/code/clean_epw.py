"""Clean the corrupt diffuse radiation hours in an Annex 80 heat-wave EPW file.

In 5A_Copenhagen_HW_Midterm_MostSevere_2054.epw, six hours have diffuse horizontal
radiation (DHI) and global horizontal radiation (GHI) inflated by the same offset of
0.9e6 to 5.6e6 W/m2. The direct normal radiation (DNI) is intact: GHI - DHI still
equals DNI * cos(zenith). The fix keeps the beam part (GHI - DHI) and replaces DHI by
the mean of the hours before and after.

Usage: python clean_epw.py input.epw output.epw
"""
import sys

GHI, DNI, DHI = 13, 14, 15     # EPW column indices (0-based)
LIMIT = 1500                   # W/m2, above any physical value


def clean(src, dst):
    with open(src, newline="") as f:
        lines = f.read().splitlines()
    head, data = lines[:8], [line.split(",") for line in lines[8:]]
    fixed = []
    for i, r in enumerate(data):
        ghi, dhi = float(r[GHI]), float(r[DHI])
        if dhi > LIMIT or ghi > LIMIT:
            beam = ghi - dhi
            dhi_new = round((float(data[i - 1][DHI]) + float(data[i + 1][DHI])) / 2)
            r[DHI], r[GHI] = str(dhi_new), str(round(dhi_new + beam))
            fixed.append((r[1], r[2], r[3], ghi, r[GHI], dhi, r[DHI]))
    # Note the repair in the COMMENTS 2 header line
    head[6] += f" Cleaned: DHI and GHI repaired in {len(fixed)} corrupt hours with clean_epw.py."
    with open(dst, "w", newline="") as f:
        f.write("\r\n".join(head + [",".join(r) for r in data]) + "\r\n")
    return fixed


if __name__ == "__main__":
    for m, d, h, g0, g1, d0, d1 in clean(sys.argv[1], sys.argv[2]):
        print(f"{m:>2}/{d:<2} h{h:>2}: GHI {g0:>9.0f} -> {g1:>4}, DHI {d0:>9.0f} -> {d1:>4} W/m2")
