"""
Simple exhaust-air heat pump model (Nilan Compact P-like) for DHW tank charging.

- Capacity: interpolated from PHI certificate test points (DHW tank heating, 92 m3/h).
- COP: Lorenz model. Heat is delivered over a temperature glide from return to
  supply, so COP depends on BOTH supply and return temperature.
- Source: exhaust air after the counterflow heat exchanger.
"""
import numpy as np

# --- Parameters -------------------------------------------------------------
T_ROOM = 20.0          # extract air temperature [C]
ETA_HX = 0.85          # counterflow heat exchanger temperature efficiency [-]
DT_EVAP = 5.0          # evaporator approach (air -> refrigerant) [K]
DT_COND = 5.0          # condenser approach (refrigerant -> water) [K]
ETA_LORENZ = 0.32      # fraction of ideal Lorenz COP; tuned to ~COP 2.8 at 7 C (PHI cert)

# PHI certificate, DHW tank heating, Compact P @ 92 m3/h
T_OUT_PTS = np.array([-6.9, 1.9, 7.2, 20.2])   # outdoor [C]
P_DHW_PTS = np.array([0.51, 0.72, 0.89, 1.02])  # heat output [kW]


def capacity(t_out):
    """Heat output [kW] vs outdoor temperature (held constant beyond test range)."""
    return np.interp(t_out, T_OUT_PTS, P_DHW_PTS)


def evaporator_temp(t_out):
    """Exhaust air leaving the heat exchanger feeds the evaporator."""
    t_exhaust = T_ROOM - ETA_HX * (T_ROOM - t_out)
    return t_exhaust - DT_EVAP


def log_mean(t_hi, t_lo):
    """Thermodynamic mean temperature [K] of a glide from t_lo to t_hi [C]."""
    a, b = t_hi + 273.15, t_lo + 273.15
    return a if abs(a - b) < 1e-6 else (a - b) / np.log(a / b)


def cop(t_out, t_supply, t_return):
    """Lorenz COP: hot side glides return -> supply, cold side ~isothermal."""
    t_hot = log_mean(t_supply, t_return) + DT_COND
    t_cold = evaporator_temp(t_out) + 273.15
    return ETA_LORENZ * t_hot / (t_hot - t_cold)


def hour(t_out, t_supply, t_return):
    """One hour of tank charging: heat [kWh], electricity [kWh], COP."""
    q = capacity(t_out)
    c = cop(t_out, t_supply, t_return)
    return q, q / c, c


if __name__ == "__main__":
    print("Effect of outdoor temperature (supply 55 C, return 15 C):")
    for t in [-10, -5, 0, 7, 15, 20]:
        q, e, c = hour(t, 55, 15)
        print(f"  T_out {t:>4} C  Q {q:.2f} kW  El {e:.2f} kW  COP {c:.2f}")

    print("\nEffect of return temperature (T_out 7 C, supply 55 C):")
    for tr in [10, 20, 30, 40, 50]:
        q, e, c = hour(7, 55, tr)
        print(f"  T_return {tr:>3} C  COP {c:.2f}")
