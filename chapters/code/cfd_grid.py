"""Grid study for the room CFD appendix: highest floor speed (0.1 m) for a 0.1 m slot at 2.3-2.4 m,
16 °C supply, 6 ACH, gains for a well-mixed 26 °C room, on four grids, k-epsilon with TVD and upwind.

    python cfd_grid.py

Contact: Christian Hviid, cahv@dtu.dk. Use at own risk; see the disclaimer in room_cfd.py.
"""
from room_cfd import Case, Opening, HeatBlock, run, occupied_zone

for nx, ny in ((60, 30), (100, 50), (150, 75), (200, 100)):
    for adv in ("upwind", "tvd"):
        c = Case(nx=nx, ny=ny, inlet=Opening("left", 2.3, 2.4), outlet=Opening("right", 2.3, 2.4),
                 T_in=16.0, ach=6, advection=adv, t_end=1800, t_avg=600)
        c.heat = [HeatBlock(2.3, 2.7, 0.0, 1.2, 1.2 * 1005 * c.q * (26.0 - 16.0) / c.W)]
        oz = occupied_zone(run(c))
        print(f"{nx} x {ny}  {adv:6s}  v_max {oz['v_max']:.3f} m/s at x {oz['x_at']:.2f}  DR {oz['DR']:.0f} %", flush=True)
