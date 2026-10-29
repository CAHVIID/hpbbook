"""Steady-state model of a shower with drain water heat recovery (DWHR).

Counterflow heat exchanger, epsilon-NTU. UA is fitted to the certified
effectiveness at 8 L/min (balanced flow, PHI test) and scaled with flow as
UA ~ V^m (m = 0.5 assumed). Three connections:
  1 preheated water to the shower mixer only
  2 preheated water to the water heater only
  3 preheated water to both (balanced, equal flow)
"""
import math

RHO_CP = 994 * 4.182 / 3600  # Wh/(L K), mean 10-55 C
V_TEST = 8.0                 # L/min, PHI test flow
M_UA = 0.5                   # UA ~ V_drain^M_UA (assumption)


def eps_cf(ntu, cr):
    """Counterflow effectiveness."""
    if abs(1 - cr) < 1e-9:
        return ntu / (1 + ntu)
    e = math.exp(-ntu * (1 - cr))
    return (1 - e) / (1 - cr * e)


def ua_rel(eps_rated, v_drain):
    """UA/(rho cp) in L/min, fitted to balanced eps at V_TEST."""
    ntu0 = eps_rated / (1 - eps_rated)
    return ntu0 * V_TEST * (v_drain / V_TEST) ** M_UA


def shower(eps_rated, conn, v=8.0, t_mix=40.0, t_drain=37.0, t_c=10.0, t_h=55.0):
    """Return dict with preheat temp, heater load (W) and saving fraction."""
    ua = ua_rel(eps_rated, v)
    q_ref = v * (t_mix - t_c)                     # L/min*K without DWHR
    if conn == 0:
        return dict(t_p=t_c, v_cold_side=0, eps=0, saving=0.0)
    if conn == 3:
        vc = v
        eps = eps_cf(ua / v, 1.0)
        t_p = t_c + eps * (t_drain - t_c)
        q = v * (t_mix - t_p)
    elif conn == 2:
        vc = v * (t_mix - t_c) / (t_h - t_c)          # hot fraction, fixed
        eps = eps_cf(ua / vc, vc / v)                 # cold side is C_min
        t_p = t_c + eps * (t_drain - t_c)
        q = vc * (t_h - t_p)
    elif conn == 1:
        t_p = t_c
        for _ in range(200):                          # mixing ratio feedback
            vc = v * (t_h - t_mix) / (t_h - t_p)      # cold fraction at mixer
            eps = eps_cf(ua / vc, vc / v)
            t_p_new = t_c + eps * (t_drain - t_c)
            if abs(t_p_new - t_p) < 1e-9:
                break
            t_p = t_p_new
        vh = v - vc
        q = vh * (t_h - t_c)
    return dict(t_p=t_p, v_cold_side=vc, eps=eps, saving=1 - q / q_ref,
                load_kW=q * RHO_CP * 60 / 1000)


PRODUCTS = [  # name, type, PHI nominal efficiency at 8 L/min
    ("Showersave QB1-21XE", "vertical", 0.70),
    ("ACO ShowerDrain X2.2 PHI", "channel", 0.60),
    ("Zypho Slim 50 DW", "tray", 0.54),
    ("Zypho PiPe 60 DW", "vertical", 0.53),
    ("Joulia-Inline 5", "channel", 0.41),
]

if __name__ == "__main__":
    for name, typ, e in PRODUCTS:
        r = [shower(e, c) for c in (1, 2, 3)]
        print(f"{name:26s} eps={e:.2f}  " + "  ".join(
            f"c{c}: tp={x['t_p']:.1f} eps={x['eps']:.2f} save={x['saving']:.3f}"
            for c, x in zip((1, 2, 3), r)))
    print("no DWHR load kW", 8 * 30 * RHO_CP * 60 / 1000)
    for v in (5, 8, 12):
        print(v, [round(shower(0.7, 3, v=v)['eps'], 3) for _ in [0]],
              round(shower(0.41, 3, v=v)['eps'], 3))
    # seasonal
    for tc in (5, 10, 15):
        x = shower(0.5, 3, t_c=tc)
        print("tc", tc, round(x['saving'], 3), round(x['t_p'] - tc, 2))
