"""plots.py: standard output plots for room_cfd.run() results.

  profiles(res, xs)      vertical profiles of speed and temperature at chosen x positions
                         (heights as in ISO 7730 / the Bugenings columns are marked)
  floor_line(res, h)     speed, temperature and draught rate along the room at height h
  dr_map(res)            draught rate over the whole section, occupied zone outlined
  convergence(res)       rate of change, continuity, energy imbalance and monitor points vs time

Each function takes one result or a dict {label: result} and returns the figure.
Draught: ISO 7730 draught rate DR (Tu = 40 %, limit 20 %) and, at ankle height, the ASHRAE 55-2020
ankle draft model PPD_AD (Liu et al. 2017, limit 20 %). No feet factor is applied to DR.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator
from room_cfd import draught_rate, ankle_draft_ppd, occupied_zone, draw_convergence

ISO_H = [0.1, 0.6, 1.1, 1.7]            # ankle, seated waist, seated head, standing head (ISO 7730)
COLORS = ["#2a78d6", "#eb6834", "#1b9e77", "#7a1f4f"]


def _as_dict(res):
    return res if isinstance(res, dict) and "case" not in res else {"": res}


def _at_x(r, x):
    i = int(np.clip(np.searchsorted(r["x"], x), 0, len(r["x"]) - 1))
    return i, r["x"][i]


def profiles(res, xs=(1.0, 2.0, 3.0), tu=40.0):
    """Speed and temperature against height at the given x positions (m from the inlet wall)."""
    runs = _as_dict(res)
    fig, ax = plt.subplots(2, len(xs), figsize=(2.6 * len(xs) + 1, 6.2), sharex="row", sharey=True, squeeze=False)
    for k, (lab, r) in enumerate(runs.items()):
        for j, x in enumerate(xs):
            i, xi = _at_x(r, x)
            kw = dict(color=COLORS[k % 4], lw=1.8, label=lab or None)
            ax[0, j].plot(r["speed"][i], r["y"], **kw)
            ax[1, j].plot(r["T"][i], r["y"], **kw)
            ax[0, j].set_title(f"x = {xi:.2f} m", fontsize=10)
    for a in ax.flat:
        for h in ISO_H: a.axhline(h, color="0.85", lw=0.8, zorder=0)
        a.spines[["top", "right"]].set_visible(False); a.grid(alpha=0.25)
    for a in ax[0]:
        a.axvline(0.15, color="0.5", ls="--", lw=0.8); a.set_xlabel("Mean air speed (m/s)"); a.set_xlim(left=0)
    for a in ax[1]:
        a.set_xlabel("Air temperature (°C)")
        a.xaxis.set_major_locator(MaxNLocator(integer=True))       # labels on whole degrees
        a.xaxis.set_minor_locator(MultipleLocator(1))              # grid every 1 °C
        a.grid(which="minor", alpha=0.25)
    ax[0, 0].set_ylabel("Height (m)"); ax[1, 0].set_ylabel("Height (m)")
    if len(runs) > 1: ax[0, -1].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def floor_line(res, h=0.1, x_min=0.6, tu=40.0, rh=50.0, met=1.2, clo=0.5):
    """Speed, temperature and draught against x at height h. Shaded: outside the occupied zone.
    At ankle height (h <= 0.2 m) a fourth panel shows the ASHRAE 55 ankle draft PPD_AD, with the
    thermal sensation TS taken as the occupied-zone PMV (see room_cfd.occupied_zone)."""
    runs = _as_dict(res)
    ankle = h <= 0.2
    fig, ax = plt.subplots(4 if ankle else 3, 1, figsize=(7, 8.4 if ankle else 6.5), sharex=True)
    for k, (lab, r) in enumerate(runs.items()):
        j = min(int(h / r["dy"]), len(r["y"]) - 1)
        s, t = r["speed"][:, j], r["T"][:, j]
        kw = dict(color=COLORS[k % 4], lw=1.8, label=lab or None)
        ax[0].plot(r["x"], s, **kw); ax[1].plot(r["x"], t, **kw); ax[2].plot(r["x"], draught_rate(t, s, tu), **kw)
        if ankle:
            ts = occupied_zone(r, x_min=x_min, h=h, rh=rh, met=met, clo=clo)["TS"]
            kw["label"] = f"{lab}{', ' if lab else ''}TS (PMV) = {ts:+.2f}"
            ax[3].plot(r["x"], ankle_draft_ppd(s, ts), **kw)
        L = r["case"].L
    for a in ax:
        a.axvspan(0, x_min, color="0.92", zorder=0); a.axvspan(L - x_min, L, color="0.92", zorder=0)
        a.spines[["top", "right"]].set_visible(False); a.grid(alpha=0.25)
    ax[0].set_ylabel("Air speed (m/s)"); ax[0].set_ylim(bottom=0)
    ax[1].set_ylabel("Temperature (°C)")
    ax[2].set_ylabel("ISO 7730 DR (%)"); ax[2].set_ylim(0, max(25, ax[2].get_ylim()[1]))
    ax[2].axhline(20, color="k", ls="--", lw=0.8); ax[2].text(0.05, 21, "20 % (category II)", fontsize=8)
    if ankle:
        ax[3].set_ylabel("ASHRAE 55\nankle PPD$_{AD}$ (%)"); ax[3].set_ylim(0, max(32, 1.4 * ax[3].get_ylim()[1]))
        ax[3].axhline(20, color="k", ls="--", lw=0.8); ax[3].text(0.05, 21, "20 % (ASHRAE 55 limit)", fontsize=8)
        ax[3].legend(frameon=False, fontsize=8, loc="upper right")
    ax[-1].set_xlabel("Distance from the inlet wall x (m)"); ax[-1].set_xlim(0, L)
    ax[0].set_title(f"At {h:.2f} m above the floor (grey: outside the occupied zone)", fontsize=10)
    if len(runs) > 1: ax[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def dr_map(res, tu=40.0, x_min=0.6, h_max=1.8, vmax=40):
    """ISO 7730 draught rate over the section, occupied zone outlined."""
    runs = _as_dict(res)
    n = len(runs)
    fig, axs = plt.subplots(n, 1, figsize=(7, 2.9 * n + 0.4), squeeze=False)
    for a, (lab, r) in zip(axs[:, 0], runs.items()):
        c = r["case"]; X, Y = np.meshgrid(r["x"], r["y"], indexing="ij")
        dr = draught_rate(r["T"], r["speed"], tu)
        im = a.pcolormesh(X, Y, dr, cmap="magma_r", vmin=0, vmax=vmax, shading="auto")
        a.contour(X, Y, dr, levels=[20], colors="w", linewidths=1.2)
        a.add_patch(plt.Rectangle((x_min, 0), c.L - 2 * x_min, h_max, fill=False, ec="#2a78d6", lw=1.5, ls="--"))
        for op, col in ((c.inlet, "#2a78d6"), (c.outlet, "0.3")):
            if op.side == "top": a.plot([op.start, op.end], [c.H, c.H], color=col, lw=5)
            else: a.plot([0 if op.side == "left" else c.L] * 2, [op.start, op.end], color=col, lw=5)
        oz = (X > x_min) & (X < c.L - x_min) & (Y < h_max)
        share = 100 * (dr[oz] > 20).mean()
        a.set_title(f"{lab}{': ' if lab else ''}DR > 20 % in {share:.0f} % of the occupied zone", fontsize=9)
        a.set_aspect("equal"); a.set_ylabel("Height (m)")
        fig.colorbar(im, ax=a, shrink=0.9, label="DR (%)")
    axs[-1, 0].set_xlabel("x (m)")
    fig.tight_layout()
    return fig


def convergence(res):
    """Convergence history of one run (same panels as the live window, run(case, live=True))."""
    fig, ax = plt.subplots(2, 2, figsize=(10, 6))
    draw_convergence(res["history"], res["case"], fig, ax)
    return fig
