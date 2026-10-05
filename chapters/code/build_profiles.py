"""Writes the tapping profiles and their references into dhw_tank.py and dhw-tank.mjs, so the
Python reference model and the browser app use exactly the same numbers.
The literature profiles are defined in tapping_profiles_candidates.py.
Run:  python build_profiles.py
"""
import json, re
import tapping_profiles_candidates as c

EN_REF = ("Commission Regulation (EU) No 814/2013, Annex III, Table 1 (load profiles used for "
          "ecodesign and energy labelling; the same profiles are used in EN 16147 for heat pump water heaters).")
EN_URL = "https://eur-lex.europa.eu/eli/reg/2013/814/oj"
EN_NOTE = ("Times, energies and flows as in the regulation. Energies are converted to litres at the use "
           "temperature: Tp where the table gives one (bath and floor cleaning 40 °C, dishwashing 55 °C), "
           "otherwise Tm (small tappings 25 °C, shower and cleaning 40 °C). Cold water 10 °C.")
T26_REF = ("Jordan, U., Vajen, K. (2001). Realistic domestic hot-water profiles in different time scales. "
           "IEA SHC Task 26, Universität Marburg.")
T26_URL = "https://sel.me.wisc.edu/trnsys/trnlib/iea-shc-task26/iea-shc-task26-load-profiles-description-jordan.pdf"
T26_NOTE = ("200 L/day at 45 °C on average. Draw-off categories: short 1 L/min × 1 min (28/day), medium "
            "6 L/min × 1 min (12/day), shower 8 L/min × 5 min (2/day), bath 14 L/min × 10 min (once a week). "
            "The original profile has random times; here short and medium draws are spread evenly from 05:00 "
            "to 23:00 and the showers are placed in the morning and evening peaks.")
DK_REF = ("Marszal-Pomianowska, A. et al. (2021). Comfort of domestic water in residential buildings: flow, "
          "temperature and energy in draw-off points. Field study in two Danish detached houses. "
          "Energies 14(11), 3314.")
DK_URL = "https://doi.org/10.3390/en14113314"
DK4_NOTE = ("House 1 in the study: 4 occupants, 92 L/day of hot water, 1.6 showers/day of 7–8 min at "
            "35.5–40.4 °C, about 33 short kitchen draws/day (mostly under 20 s, 24.5 °C), hand washing about "
            "23 °C, peaks 06:30–07:00 and 18:00–20:00 on weekdays. Representative weekday built from these "
            "statistics; the shower flow of 7 L/min is assumed.")
DK2_NOTE = ("House 2 in the study: 2 occupants, about 43 L/day of hot water, 0.8 showers/day, about 11 kitchen "
            "draws/day at 35.5 °C. Representative weekday built from these statistics; the shower flow of "
            "7 L/min is assumed.")
OWN_REF = "Illustrative profile written for this book, not taken from the literature."

OWN = {
    "Family of 4, morning and evening": [
        (6.50, "shower", 42, 7, 40), (6.75, "shower", 42, 7, 40), (7.00, "washbasin", 3, 5, 35),
        (7.10, "washbasin", 3, 5, 35), (7.25, "kitchen tap", 2, 6, 45), (7.50, "washbasin", 3, 5, 35),
        (12.00, "kitchen tap", 3, 6, 45), (17.50, "kitchen tap", 4, 6, 45), (18.00, "washbasin", 3, 5, 35),
        (19.00, "washing up", 10, 6, 45), (20.00, "shower", 42, 7, 40),
        (21.50, "washbasin", 3, 5, 35), (21.60, "washbasin", 3, 5, 35), (22.00, "kitchen tap", 2, 6, 45)],
    "Family of 4, all showers in the evening": [
        (7.00, "washbasin", 3, 5, 35), (7.10, "washbasin", 3, 5, 35), (7.25, "kitchen tap", 2, 6, 45),
        (7.50, "washbasin", 3, 5, 35), (12.00, "kitchen tap", 3, 6, 45), (17.50, "kitchen tap", 4, 6, 45),
        (18.00, "washbasin", 3, 5, 35), (19.00, "washing up", 10, 6, 45), (19.50, "shower", 42, 7, 40),
        (19.75, "shower", 42, 7, 40), (20.00, "shower", 42, 7, 40),
        (21.50, "washbasin", 3, 5, 35), (21.60, "washbasin", 3, 5, 35), (22.00, "kitchen tap", 2, 6, 45)],
    "Couple, morning showers": [
        (6.50, "shower", 42, 7, 40), (6.80, "shower", 42, 7, 40), (7.10, "washbasin", 3, 5, 35),
        (7.25, "kitchen tap", 2, 6, 45), (17.50, "kitchen tap", 3, 6, 45), (19.00, "washing up", 8, 6, 45),
        (22.00, "washbasin", 3, 5, 35), (22.10, "washbasin", 3, 5, 35)],
}

# name -> (group, tappings, reference, url, note); CITE gives the short citation shown under the dropdown
ALL = {
    "EN 16147 M": ("Standard test cycles", c.EN_M, EN_REF, EN_URL, EN_NOTE + " Typical for 1–2 persons."),
    "EN 16147 L": ("Standard test cycles", c.EN_L, EN_REF, EN_URL, EN_NOTE + " Typical for a family; two baths."),
    "EN 16147 XL": ("Standard test cycles", c.EN_XL, EN_REF, EN_URL, EN_NOTE + " Large family; three baths."),
    "IEA SHC Task 26, weekday": ("Statistical profiles", c.task26(False), T26_REF, T26_URL, T26_NOTE + " Weekday without bath."),
    "IEA SHC Task 26, bath day": ("Statistical profiles", c.task26(True), T26_REF, T26_URL, T26_NOTE + " Day with the weekly bath at 20:15."),
    "Danish house, 4 persons": ("Measured in Danish houses", c.DK4, DK_REF, DK_URL, DK4_NOTE),
    "Danish house, 2 persons": ("Measured in Danish houses", c.DK2, DK_REF, DK_URL, DK2_NOTE),
    **{k: ("Illustrative (this book)", v, OWN_REF, "", "Shows the effect of when the showers are taken.") for k, v in OWN.items()},
}
DEFAULT = "Family of 4, morning and evening"
CITE = {"Standard test cycles": "Reg. (EU) 814/2013 / EN 16147", "Statistical profiles": "Jordan & Vajen (2001), IEA SHC Task 26",
        "Measured in Danish houses": "Marszal-Pomianowska et al. (2021)", "Illustrative (this book)": "illustrative, not from literature"}


def taps_py(taps):
    return "[" + ", ".join(f"({t!r}, {n!r}, {v!r}, {f!r}, {tu!r})" for t, n, v, f, tu in taps) + "]"


def taps_js(taps):
    return "[" + ", ".join(f"[{t!r}, {json.dumps(n)}, {v!r}, {f!r}, {tu!r}]" for t, n, v, f, tu in taps) + "]"


py = ["PROFILES = {"] + [f"    {k!r}: {taps_py(v[1])}," for k, v in ALL.items()] + ["}"]
py += ["PROFILE_INFO = {"] + [f"    {k!r}: dict(group={v[0]!r}, cite={CITE[v[0]]!r}, ref={v[2]!r}, url={v[3]!r}, note={v[4]!r})," for k, v in ALL.items()] + ["}"]
py += [f"DEFAULT_PROFILE = {DEFAULT!r}"]
js = ["export const PROFILES = {"] + [f"  {json.dumps(k)}: {taps_js(v[1])}," for k, v in ALL.items()] + ["};"]
js += ["export const PROFILE_INFO = {"] + [f"  {json.dumps(k)}: {json.dumps(dict(group=v[0], cite=CITE[v[0]], ref=v[2], url=v[3], note=v[4]), ensure_ascii=False)}," for k, v in ALL.items()] + ["};"]
js += [f"export const DEFAULT_PROFILE = {json.dumps(DEFAULT)};"]

for fn, lines, cm in (("dhw_tank.py", py, "#"), ("dhw-tank.mjs", js, "//")):
    s = open(fn).read()
    a, b = f"{cm} --- profiles (generated by build_profiles.py) ---", f"{cm} --- end of profiles ---"
    s = re.sub(re.escape(a) + r".*?" + re.escape(b), lambda m: a + "\n" + "\n".join(lines) + "\n" + b, s, flags=re.S)
    open(fn, "w").write(s)
print("profiles written:", ", ".join(ALL))
