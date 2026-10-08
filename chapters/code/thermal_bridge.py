"""
thermal_bridge.py - 2D steady-state heat conduction through building constructions.

Reference version of the Thermal Bridge Lab app (thermal-bridge.mjs) in the chapter
"The building envelope". Both read the same case files.

How it works
  1. Geometry   : a list of rectangles of material. The LAST rectangle in the list is on top,
                  so a thin steel profile can be drawn over a layer of insulation.
  2. Mesh       : grid lines at every rectangle edge and at the ends of every boundary edge.
                  Each gap is split into cells that are h_min next to the lines and grow by
                  `ratio` towards the middle, up to h_max (graded refinement).
  3. Materials  : each cell takes the conductivity of the top-most rectangle covering its centre.
                  Cells covered by no rectangle are empty space and are not part of the model.
  4. Boundaries : every cell face between material and empty space is a surface. A surface takes
                  the condition of the boundary edge drawn on it (the last edge drawn wins);
                  surfaces with no edge are adiabatic. This allows L-shapes, corners and voids.
  5. Assembly   : one energy balance per cell (cell-centred finite differences):
                  sum of G * (T_neighbour - T_cell) + sources = 0, with G the conductance of
                  two half cells in series. Convective surfaces link the cell to the air
                  temperature through the half cell plus the surface resistance R.
  6. Solve      : sparse direct solve of A T = b.
  7. Results    : heat flow through each boundary (W/m, positive into the construction),
                  surface temperatures, L2D, fRsi and the heat flux field.

Units: m, W/(m K), deg C, m2K/W, W/m2. Results are per metre length of the detail.

Usage:
  python thermal_bridge.py                 # both examples: wall corner and steel stud
  python thermal_bridge.py case.json       # run a case file exported from the app
  python thermal_bridge.py --validate      # compare with a 1D hand calculation

Requires numpy, scipy and matplotlib. Written for teaching: verify results before using
them for design.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

KINDS = ("convective", "temperature", "flux", "adiabatic")
TOL = 1e-7


# --------------------------------------------------------------------------- input
@dataclass
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float
    material: str

    def __post_init__(self):
        self.x0, self.x1 = sorted((float(self.x0), float(self.x1)))
        self.y0, self.y1 = sorted((float(self.y0), float(self.y1)))
        if self.x1 - self.x0 <= 0 or self.y1 - self.y0 <= 0:
            raise ValueError(f"Rectangle {self} has zero width or height")


@dataclass
class Boundary:
    """A named boundary condition.

    convective  - air temperature T through surface resistance R (Robin)
    temperature - fixed surface temperature T (Dirichlet)
    flux        - heat flux q INTO the construction, W/m2 (Neumann)
    adiabatic   - no heat flow
    """
    name: str
    kind: str = "convective"
    T: float = 0.0
    R: float = 0.13
    q: float = 0.0

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown boundary kind '{self.kind}'")


@dataclass
class Edge:
    """A horizontal or vertical line where a boundary condition applies."""
    boundary: str
    x0: float
    y0: float
    x1: float
    y1: float

    def __post_init__(self):
        if abs(self.x0 - self.x1) > TOL and abs(self.y0 - self.y1) > TOL:
            raise ValueError("Edges must be horizontal or vertical")

    @property
    def orient(self):  # 'v': x fixed, 'h': y fixed
        return "v" if abs(self.x0 - self.x1) <= TOL else "h"

    @property
    def c(self):
        return self.x0 if self.orient == "v" else self.y0

    @property
    def span(self):
        a = (self.y0, self.y1) if self.orient == "v" else (self.x0, self.x1)
        return min(a), max(a)


@dataclass
class MeshSettings:
    h_min: float = 0.002   # cell size next to grid lines, m
    h_max: float = 0.02    # largest cell size, m
    ratio: float = 1.3     # growth factor from one cell to the next (>= 1)


@dataclass
class Case:
    materials: dict
    rects: list
    boundaries: list
    edges: list
    mesh: MeshSettings = field(default_factory=MeshSettings)


# --------------------------------------------------------------------------- mesh
def graded_split(L, h_min, h_max, ratio):
    """Cells of size h_min at both ends of a gap, growing by `ratio` towards the middle."""
    if L <= 2 * h_min:
        return np.array([L])
    half, acc, h = [], 0.0, h_min
    while acc + h <= L / 2 + 1e-15:
        half.append(h)
        acc += h
        h = min(h * ratio, h_max)
    rest = L - 2 * acc
    if rest > 0.5 * half[-1]:
        return np.array(half + [rest] + half[::-1])
    return np.array(half + half[::-1]) * L / (2 * acc)


def grid_lines(coords, s: MeshSettings):
    base = np.unique(np.round(np.asarray(coords, float), 9))
    lines = [base[0]]
    for a, b in zip(base[:-1], base[1:]):
        lines.extend(a + np.cumsum(graded_split(b - a, s.h_min, max(s.h_max, s.h_min), max(s.ratio, 1.0))))
    lines = np.array(lines)
    lines[-1] = base[-1]
    return lines


def build_mesh(case: Case):
    xs = [v for r in case.rects for v in (r.x0, r.x1)]
    ys = [v for r in case.rects for v in (r.y0, r.y1)]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    inside = lambda v, a, b: a + 1e-9 < v < b - 1e-9
    for e in case.edges:  # edge ends become grid lines so a condition can stop mid-face
        a0, a1 = e.span
        if e.orient == "v":
            xs += [e.c] if inside(e.c, bx0, bx1) else []
            ys += [a for a in (a0, a1) if inside(a, by0, by1)]
        else:
            ys += [e.c] if inside(e.c, by0, by1) else []
            xs += [a for a in (a0, a1) if inside(a, bx0, bx1)]
    return grid_lines(xs, case.mesh), grid_lines(ys, case.mesh)


def assign_materials(xl, yl, case: Case):
    xc, yc = 0.5 * (xl[:-1] + xl[1:]), 0.5 * (yl[:-1] + yl[1:])
    X, Y = np.meshgrid(xc, yc)
    owner = -np.ones(X.shape, int)
    for n, r in enumerate(case.rects):
        if r.material not in case.materials:
            raise KeyError(f"material '{r.material}' has no lambda value")
        owner[(X > r.x0) & (X < r.x1) & (Y > r.y0) & (Y < r.y1)] = n
    lam = np.array([case.materials[r.material] for r in case.rects] + [np.nan], float)
    return lam[owner], owner


# --------------------------------------------------------------------------- solve
@dataclass
class Result:
    xl: np.ndarray
    yl: np.ndarray
    k: np.ndarray
    owner: np.ndarray
    T: np.ndarray
    qx: np.ndarray
    qy: np.ndarray
    faces: dict          # per surface face: geometry, boundary index, heat flow, surface temperature
    flows: dict          # boundary name -> heat flow into the construction, W/m
    surface_T: dict      # boundary name -> (min, max) surface temperature
    case: Case


def exposed_faces(xl, yl, k, case: Case):
    """All faces between material and empty space, with the boundary drawn on them."""
    ny, nx = k.shape
    act = ~np.isnan(k)
    dx, dy = np.diff(xl), np.diff(yl)
    xc, yc = 0.5 * (xl[:-1] + xl[1:]), 0.5 * (yl[:-1] + yl[1:])
    nb = np.zeros_like(act)
    out = {key: [] for key in ("j", "i", "dir", "x0", "y0", "x1", "y1", "area", "d")}
    for direction in ("left", "right", "bottom", "top"):
        nb[:] = False
        if direction == "left":   nb[:, 1:] = act[:, :-1]
        if direction == "right":  nb[:, :-1] = act[:, 1:]
        if direction == "bottom": nb[1:, :] = act[:-1, :]
        if direction == "top":    nb[:-1, :] = act[1:, :]
        J, I = np.nonzero(act & ~nb)
        if direction in ("left", "right"):
            x = xl[I] if direction == "left" else xl[I + 1]
            geo = (x, yl[J], x, yl[J + 1], dy[J], dx[I] / 2)
        else:
            y = yl[J] if direction == "bottom" else yl[J + 1]
            geo = (xl[I], y, xl[I + 1], y, dx[I], dy[J] / 2)
        for key, v in zip(("j", "i"), (J, I)):
            out[key].append(v)
        out["dir"].append(np.full(len(J), direction))
        for key, v in zip(("x0", "y0", "x1", "y1", "area", "d"), geo):
            out[key].append(v)
    f = {key: np.concatenate(v) for key, v in out.items()}

    # which drawn edge lies on each face (last drawn wins)
    names = [b.name for b in case.boundaries]
    f["edge"] = -np.ones(len(f["j"]), int)
    vert = f["x0"] == f["x1"]
    coord = np.where(vert, f["x0"], f["y0"])
    along = np.where(vert, 0.5 * (f["y0"] + f["y1"]), 0.5 * (f["x0"] + f["x1"]))
    for n, e in enumerate(case.edges):
        a0, a1 = e.span
        m = (vert == (e.orient == "v")) & (np.abs(coord - e.c) < TOL) & (along > a0 - TOL) & (along < a1 + TOL)
        f["edge"][m] = n
    f["bc"] = np.array([names.index(case.edges[n].boundary) if n >= 0 else -1 for n in f["edge"]], int)
    return f


def solve(case: Case) -> Result:
    xl, yl = build_mesh(case)
    k, owner = assign_materials(xl, yl, case)
    ny, nx = k.shape
    act = ~np.isnan(k)
    idx = -np.ones((ny, nx), int)
    idx[act] = np.arange(act.sum())
    n = int(act.sum())
    dx, dy = np.diff(xl), np.diff(yl)

    with np.errstate(invalid="ignore"):
        Gx = dy[:, None] / (dx[None, :-1] / (2 * k[:, :-1]) + dx[None, 1:] / (2 * k[:, 1:]))
        Gy = dx[None, :] / (dy[:-1, None] / (2 * k[:-1, :]) + dy[1:, None] / (2 * k[1:, :]))
    Gx = np.where(act[:, :-1] & act[:, 1:], Gx, 0.0)
    Gy = np.where(act[:-1, :] & act[1:, :], Gy, 0.0)

    rows, cols, vals = [], [], []
    diag, b = np.zeros(n), np.zeros(n)
    for G, a, c in ((Gx, idx[:, :-1], idx[:, 1:]), (Gy, idx[:-1, :], idx[1:, :])):
        m = G > 0
        p, q, g = a[m], c[m], G[m]
        rows += [p, q]; cols += [q, p]; vals += [-g, -g]
        np.add.at(diag, p, g)
        np.add.at(diag, q, g)

    f = exposed_faces(xl, yl, k, case)
    kc = k[f["j"], f["i"]]
    p = idx[f["j"], f["i"]]
    f["G"] = np.zeros(len(p))
    f["qsrc"] = np.zeros(len(p))
    for bi, bc in enumerate(case.boundaries):
        m = f["bc"] == bi
        if bc.kind in ("convective", "temperature"):
            R = bc.R if bc.kind == "convective" else 0.0
            f["G"][m] = f["area"][m] / (f["d"][m] / kc[m] + R)
            np.add.at(diag, p[m], f["G"][m])
            np.add.at(b, p[m], f["G"][m] * bc.T)
        elif bc.kind == "flux":
            f["qsrc"][m] = bc.q
            np.add.at(b, p[m], bc.q * f["area"][m])
    if not np.any(f["G"] > 0):
        raise ValueError("No surface has a convective or temperature boundary: "
                         "the temperature level is undefined.")

    rows.append(np.arange(n)); cols.append(np.arange(n)); vals.append(diag)
    A = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n))
    Tv = spla.spsolve(A, b)
    if not np.all(np.isfinite(Tv)):
        raise ValueError("A part of the construction has no convective or temperature surface.")
    T = np.full((ny, nx), np.nan)
    T[act] = Tv[idx[act]]

    # heat flow per face (into the construction) and surface temperature
    Tc = T[f["j"], f["i"]]
    Tref = np.array([case.boundaries[i].T if i >= 0 else 0.0 for i in f["bc"]])
    f["Q"] = np.where(f["G"] > 0, f["G"] * (Tref - Tc), f["qsrc"] * f["area"])
    f["Ts"] = Tc + f["Q"] / f["area"] * f["d"] / kc

    # flux field: face values (positive +x / +y), averaged to cell centres
    Tz = np.nan_to_num(T)
    fx, fy = np.zeros((ny, nx + 1)), np.zeros((ny + 1, nx))
    fx[:, 1:-1] = Gx * (Tz[:, :-1] - Tz[:, 1:]) / dy[:, None]
    fy[1:-1, :] = Gy * (Tz[:-1, :] - Tz[1:, :]) / dx[None, :]
    qn = f["Q"] / f["area"]
    for d, sign in (("left", 1), ("right", -1), ("bottom", 1), ("top", -1)):
        m = f["dir"] == d
        J, I = f["j"][m], f["i"][m]
        if d == "left":   fx[J, I] = sign * qn[m]
        if d == "right":  fx[J, I + 1] = sign * qn[m]
        if d == "bottom": fy[J, I] = sign * qn[m]
        if d == "top":    fy[J + 1, I] = sign * qn[m]
    qx = 0.5 * (fx[:, :-1] + fx[:, 1:])
    qy = 0.5 * (fy[:-1, :] + fy[1:, :])
    qx[~act] = np.nan
    qy[~act] = np.nan

    flows, surface_T = {}, {}
    for bi, bc in enumerate(case.boundaries):
        m = f["bc"] == bi
        flows[bc.name] = float(f["Q"][m].sum())
        if m.any():
            surface_T[bc.name] = (float(f["Ts"][m].min()), float(f["Ts"][m].max()))
    return Result(xl, yl, k, owner, T, qx, qy, f, flows, surface_T, case)


# --------------------------------------------------------------------------- output
def summary(res: Result):
    """Heat flow from the warmest boundary, L2D and fRsi."""
    fixed = [b for b in res.case.boundaries
             if b.kind in ("convective", "temperature") and b.name in res.surface_T]
    Ti, Te = max(b.T for b in fixed), min(b.T for b in fixed)
    warm = [b.name for b in fixed if b.T == Ti]
    phi = sum(res.flows[n] for n in warm)
    tsi = min(res.surface_T[n][0] for n in warm)
    out = {"phi": phi, "Ti": Ti, "Te": Te, "Tsi_min": tsi}
    if Ti > Te:
        out["L2D"] = phi / (Ti - Te)
        out["fRsi"] = (tsi - Te) / (Ti - Te)
    return out


def report(res: Result, title=""):
    ny, nx = res.k.shape
    print(f"\n=== {title} ===")
    print(f"Mesh: {nx} x {ny} = {nx * ny} cells "
          f"(smallest {min(np.diff(res.xl).min(), np.diff(res.yl).min()) * 1000:.2f} mm)")
    print(f"{'boundary':<14}{'heat flow in [W/m]':>20}{'surface T min..max [C]':>26}")
    for b in res.case.boundaries:
        st = res.surface_T.get(b.name)
        s = f"{st[0]:8.2f} .. {st[1]:6.2f}" if st else "(not on any surface)"
        print(f"{b.name:<14}{res.flows[b.name]:>20.4f}{s:>26}")
    unassigned = int((res.faces["bc"] < 0).sum())
    print(f"Adiabatic surface faces (no edge drawn): {unassigned}")
    print(f"Energy balance (should be ~0): {sum(res.flows.values()):.2e} W/m")
    s = summary(res)
    if "L2D" in s:
        print(f"Phi = {s['phi']:.4f} W/m   L2D = {s['L2D']:.4f} W/(m K)   "
              f"Tsi,min = {s['Tsi_min']:.2f} C   fRsi = {s['fRsi']:.3f}")


def plot(res: Result, filename="thermal_bridge.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    from matplotlib.patches import Rectangle

    xl, yl = res.xl, res.yl
    xc, yc = 0.5 * (xl[:-1] + xl[1:]), 0.5 * (yl[:-1] + yl[1:])
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.5), constrained_layout=True)
    mats = list(dict.fromkeys(r.material for r in res.case.rects))
    cmap = plt.get_cmap("tab10")
    matid = np.full(res.owner.shape, np.nan)
    for n, r in enumerate(res.case.rects):
        matid[res.owner == n] = mats.index(r.material)
    ax = axs[0]
    ax.pcolormesh(xl, yl, matid, cmap=cmap, vmin=0, vmax=10)
    ax.vlines(xl, yl[0], yl[-1], colors="k", lw=0.15, alpha=0.4)
    ax.hlines(yl, xl[0], xl[-1], colors="k", lw=0.15, alpha=0.4)
    for n, name in enumerate(mats):
        ax.add_patch(Rectangle((0, 0), 0, 0, color=cmap(n), label=name))
    ax.set_title("Materials, mesh and boundaries")

    ax = axs[1]
    pc = ax.pcolormesh(xl, yl, res.T, cmap="coolwarm")
    cs = ax.contour(xc, yc, res.T, levels=15, colors="k", linewidths=0.5)
    ax.clabel(cs, fontsize=7, fmt="%.1f")
    fig.colorbar(pc, ax=ax, label="Temperature [°C]")
    ax.set_title("Temperature and isotherms")

    ax = axs[2]
    qm = np.hypot(res.qx, res.qy)
    vmin = max(np.nanpercentile(qm, 2), 1e-3)
    pc = ax.pcolormesh(xl, yl, qm, cmap="viridis", norm=LogNorm(vmin=vmin, vmax=np.nanmax(qm)))
    fig.colorbar(pc, ax=ax, label="|q| [W/m²]")
    ax.set_title("Heat flux density")

    colors = plt.get_cmap("Set1")
    for ax in axs:
        for bi, b in enumerate(res.case.boundaries):
            m = res.faces["bc"] == bi
            for x0, y0, x1, y1 in zip(res.faces["x0"][m], res.faces["y0"][m], res.faces["x1"][m], res.faces["y1"][m]):
                ax.plot([x0, x1], [y0, y1], color=colors(bi), lw=3, solid_capstyle="butt")
            ax.plot([], [], color=colors(bi), lw=3, label=b.name)
        m = res.faces["bc"] < 0
        for x0, y0, x1, y1 in zip(res.faces["x0"][m], res.faces["y0"][m], res.faces["x1"][m], res.faces["y1"][m]):
            ax.plot([x0, x1], [y0, y1], color="0.4", lw=1, ls="--")
        ax.set_aspect("equal")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
    axs[0].legend(loc="upper right", fontsize=8)
    fig.savefig(filename, dpi=130)
    plt.close(fig)
    print(f"Plot saved to {filename}")


# --------------------------------------------------------------------------- case files
def load_case(path) -> Case:
    with open(path, encoding="utf-8") as fh:
        c = json.load(fh)
    return case_from_dict(c)


def case_from_dict(c) -> Case:
    rects = [Rect(**r) for r in c["rectangles"]]
    m = c.get("mesh", {})
    mesh = MeshSettings(**{k: v for k, v in m.items() if k in ("h_min", "h_max", "ratio")})
    raw = c.get("boundaries", [])
    if any("side" in b for b in raw):
        # older format: one condition per side of the bounding box
        bx0, bx1 = min(r.x0 for r in rects), max(r.x1 for r in rects)
        by0, by1 = min(r.y0 for r in rects), max(r.y1 for r in rects)
        boundaries, edges = [], []
        for b in raw:
            if b.get("kind", "adiabatic") == "adiabatic":
                continue
            name = b.get("name") or b["side"]
            boundaries.append(Boundary(name, b["kind"], b.get("T", 0.0), b.get("R", 0.13), b.get("q", 0.0)))
            lo, hi = b.get("start", -np.inf), b.get("end", np.inf)
            ylo, yhi, xlo, xhi = max(by0, lo), min(by1, hi), max(bx0, lo), min(bx1, hi)
            edges.append({"left": Edge(name, bx0, ylo, bx0, yhi), "right": Edge(name, bx1, ylo, bx1, yhi),
                          "bottom": Edge(name, xlo, by0, xhi, by0), "top": Edge(name, xlo, by1, xhi, by1)}[b["side"]])
    else:
        boundaries = [Boundary(b["name"], b.get("kind", "convective"), b.get("T", 0.0),
                               b.get("R", 0.13), b.get("q", 0.0)) for b in raw]
        edges = [Edge(**e) for e in c.get("edges", [])]
        names = {b.name for b in boundaries}
        for e in edges:
            if e.boundary not in names:
                raise KeyError(f"edge uses unknown boundary '{e.boundary}'")
    return Case(dict(c["materials"]), rects, boundaries, edges, mesh)


def case_to_dict(case: Case):
    return {
        "materials": case.materials,
        "rectangles": [vars(r) for r in case.rects],
        "boundaries": [{"name": b.name, "kind": b.kind, "T": b.T, "R": b.R, "q": b.q} for b in case.boundaries],
        "edges": [vars(e) for e in case.edges],
        "mesh": vars(case.mesh),
    }


# --------------------------------------------------------------------------- examples
INSIDE = Boundary("Inside", "convective", T=20.0, R=0.13)
OUTSIDE = Boundary("Outside", "convective", T=0.0, R=0.04)


def corner_case():
    """External wall corner in plan: 200 mm concrete with 200 mm insulation outside.
    The room is in the inner corner. The flanking walls are cut 1 m from the inside
    corner; the cut planes have no edge and are therefore adiabatic."""
    return Case(
        materials={"Concrete": 1.7, "Mineral wool": 0.037},
        rects=[Rect(0, 0, 0.2, 1.4, "Mineral wool"), Rect(0, 0, 1.4, 0.2, "Mineral wool"),
               Rect(0.2, 0.2, 0.4, 1.4, "Concrete"), Rect(0.2, 0.2, 1.4, 0.4, "Concrete")],
        boundaries=[INSIDE, OUTSIDE],
        edges=[Edge("Outside", 0, 0, 0, 1.4), Edge("Outside", 0, 0, 1.4, 0),
               Edge("Inside", 0.4, 0.4, 0.4, 1.4), Edge("Inside", 0.4, 0.4, 1.4, 0.4)],
        mesh=MeshSettings(0.002, 0.025, 1.3))


def stud_case(with_stud=True):
    """Light steel-frame wall, 0.6 m stud spacing, inside on the left.
    Gypsum 13 mm | mineral wool 200 mm | wood-fibre board 22 mm, with a steel C-profile
    (1 mm web, 50 mm flanges) drawn on top of the insulation."""
    rects = [Rect(0.000, 0.0, 0.013, 0.6, "Gypsum board"),
             Rect(0.013, 0.0, 0.213, 0.6, "Mineral wool"),
             Rect(0.213, 0.0, 0.235, 0.6, "Wood fibre board")]
    if with_stud:
        rects += [Rect(0.013, 0.2995, 0.213, 0.3005, "Steel"),
                  Rect(0.013, 0.275, 0.014, 0.325, "Steel"),
                  Rect(0.212, 0.275, 0.213, 0.325, "Steel")]
    return Case(
        materials={"Gypsum board": 0.25, "Mineral wool": 0.037, "Wood fibre board": 0.05, "Steel": 50.0},
        rects=rects, boundaries=[INSIDE, OUTSIDE],
        edges=[Edge("Inside", 0, 0, 0, 0.6), Edge("Outside", 0.235, 0, 0.235, 0.6)],
        mesh=MeshSettings(0.0005, 0.01, 1.25))


def demo():
    # wall corner
    res = solve(corner_case())
    report(res, "External wall corner")
    U = 1 / (0.13 + 0.2 / 1.7 + 0.2 / 0.037 + 0.04)
    L2D = summary(res)["L2D"]
    print(f"U of the flanking walls = {U:.4f} W/(m2 K)")
    print(f"psi, inside dimensions (2 x 1.0 m)  = {L2D - 2 * 1.0 * U:+.4f} W/(m K)")
    print(f"psi, outside dimensions (2 x 1.4 m) = {L2D - 2 * 1.4 * U:+.4f} W/(m K)")
    plot(res, "thermal_bridge_corner.png")

    # steel stud
    res = solve(stud_case(True))
    report(res, "Wall with steel stud")
    res0 = solve(stud_case(False))
    s, s0 = summary(res), summary(res0)
    print(f"U (wall without stud) = {s0['L2D'] / 0.6:.4f} W/(m2 K)")
    print(f"psi of the stud       = {s['L2D'] - s0['L2D']:.4f} W/(m K)")
    plot(res, "thermal_bridge_stud.png")


def validate():
    """Two-layer wall, 0.5 m high, insulated top and bottom: the result must equal the
    1D calculation U = 1/(Rsi + d1/l1 + d2/l2 + Rse) exactly, on any mesh."""
    case = Case(materials={"Concrete": 1.7, "Insulation": 0.04},
                rects=[Rect(0, 0, 0.15, 0.5, "Concrete"), Rect(0.15, 0, 0.30, 0.5, "Insulation")],
                boundaries=[Boundary("Inside", "convective", 20, 0.13), Boundary("Outside", "convective", -10, 0.04)],
                edges=[Edge("Inside", 0, 0, 0, 0.5), Edge("Outside", 0.3, 0, 0.3, 0.5)],
                mesh=MeshSettings(0.005, 0.03, 1.3))
    res = solve(case)
    U = 1 / (0.13 + 0.15 / 1.7 + 0.15 / 0.04 + 0.04)
    q_hand, tsi_hand = U * 30 * 0.5, 20 - U * 30 * 0.13
    print(f"Heat flow: FD {res.flows['Inside']:.6f} W/m, hand {q_hand:.6f} W/m")
    print(f"Tsi:       FD {res.surface_T['Inside'][0]:.6f} C,   hand {tsi_hand:.6f} C")
    ok = abs(res.flows["Inside"] - q_hand) < 1e-9 and abs(sum(res.flows.values())) < 1e-9
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        demo()
    elif args[0] == "--validate":
        sys.exit(0 if validate() else 1)
    else:
        r = solve(load_case(args[0]))
        report(r, args[0])
        plot(r, args[0].rsplit(".", 1)[0] + ".png")
