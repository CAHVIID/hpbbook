# Recirculating showers

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

Drain water heat recovery ([Drain water heat recovery](c3-drain-water-heat-recovery.md)) takes heat from shower water on its way to the sewer. A recirculating shower keeps the water itself. It collects the water from the shower floor, cleans it and sends it back to the shower head. Only a small amount of fresh water is needed to fill the loop and to replace what is lost, so both water and heat stay in the loop.

The example in this chapter is the Orbital Shower from Orbital Systems, Sweden. All data for it come from the manufacturer. No independent measurement of its water or energy use has been published.

## How a unit works

{numref}`fig-recirc-shower` shows the principle. The shower starts on fresh water, mixed from the central hot and cold water supply. The water that falls on the shower floor is collected, passed through a filter and a UV lamp, and checked by water quality sensors 20 times a second. If the quality is poor, the water goes to the drain and is replaced by fresh water. An electric heater brings the recirculated water back to the set temperature, and a pump returns it to the shower head.

:::{figure} figures/c4/recirc-shower-schematic.*
:label: fig-recirc-shower
:alt: Schematic of a recirculating shower. Water from the shower head is collected in the shower floor and flows through a filter, a UV lamp and water quality sensors, then up through an electric heater of 2.5 kW and a pump back to the shower head at 40 °C. Fresh water from the central hot water system, about 15 L, enters at the heater. A dashed arrow from the sensors leads to the drain when the water quality is poor.
:width: 100%

Principle of a recirculating shower. The order of the components is simplified. [View script](https://github.com/CAHVIID/hpbbook/blob/main/chapters/code/recirc_shower_schematic.py)
:::

The data sheet gives a supply of up to 9 L/min on each of the hot and cold inlets, and an electrical power of typically 2.5 kW and at most 3.7 kW on a 16 A circuit. The filter capsule lasts 20,000 L and the UV lamp 8,000 hours. Every night the unit runs a cleaning cycle with 60 s at 72 °C {cite:p}`orbital-datasheet`.

## Water and energy balance

The heat needed for a shower of volume $V$ at temperature $\theta_s$, heated from the cold water temperature $\theta_c$, is

$$
Q_{shower} = \rho c_p V (\theta_s - \theta_c) = Q_{central} + Q_{unit} + Q_{rec}
$$ (eq-recirc-balance)

where $Q_{central} = \rho c_p V_{fresh} (\theta_s - \theta_c)$ is the heat in the fresh water from the central hot water system, $Q_{unit} = P\,t$ the electric reheating in the unit at power $P$ over the shower time $t$, and $Q_{rec}$ the heat kept in the recirculated water.

The manufacturer states a water saving of 60 % for a 5-minute shower, 75 % for a 10-minute shower and 90 % for a 15-minute shower. In all three cases, the fresh water corresponds to about 2 minutes of a conventional shower. The fresh water is mostly the volume that fills the loop, and it depends little on the length of the shower.

% REVIEW LATER (Christian, 2026-10-15): check the CCE assumptions (price without installation, 0.68 DKK/SEK, n = 10 years). All data on the recirculating shower are from the manufacturer. Add the source of the 60/75/90 % water savings, and check the 2.5 kW reheating power, which is the largest uncertainty in the table.

## Electricity use compared with other heat sources

{numref}`tab-recirc-shower` compares the shower of the family of four in [Domestic hot water](c2-domestic-hot-water.md) with three heat sources.

:::{table} Heat and electricity for one shower of 6 minutes, and electricity for 3 showers a day over a year.
:label: tab-recirc-shower

| System | Heat supplied per shower, kWh | Heated centrally | Heated by the unit | Electricity per shower, kWh | Electricity per year, kWh | CCE, DKK/kWh |
|---|---|---|---|---|---|---|
| Direct electric | 1.46 | 100 % | 0 % | 1.46 | 1,590 | reference |
| Heat pump, COP 2.5 | 1.46 | 100 % | 0 % | 0.58 | 640 | – |
| Recirculating shower, electric heater | 0.79 | 68 % | 32 % | 0.79 | 860 | 4.2 |
:::

The shower is 6 minutes at 7 L/min, 42 L at 40 °C, heated from 10 °C, which is 1.46 kWh. The year has 3 showers a day. Interpolated between 5 and 10 minutes, the water saving of the recirculating shower at 6 minutes is 63 %, so the shower uses 42 × 0.37 = 15.5 L of fresh water. The heat supplied to the recirculating shower is then:

- **Central:** 15.5 L of fresh water heated from 10 to 40 °C, 15.5 L × 4.16 kJ/(L·K) × 30 K = 0.54 kWh.
- **Unit:** the electric reheating at a typical power of 2.5 kW for 6 minutes, 0.25 kWh.
- **Share:** 0.54/(0.54 + 0.25) = 68 % central and 32 % by the unit.

The rest of the 1.46 kWh, 0.67 kWh, is not supplied. It stays in the recirculated water.

The cost of conserved energy (CCE) is defined in [Cost of conserved energy](a4-cost-of-conserved-energy.md). The reference is a conventional shower with direct electric water heating. The investment is the price of the Orbital Shower Basic, 39,345 SEK including VAT {cite:p}`orbital-configurator`, or about 26,800 DKK at 0.68 DKK/SEK. Installation and shipping are not included. With $r$ = 2.5 % and $n$ = 10 years, the period of the manufacturer's warranty, the annuity factor is 0.114, and the saving of 1,590 − 860 = 730 kWh a year gives a CCE of 26,800 × 0.114 / 730 = 4.2 DKK/kWh. This is almost twice the 2.38 DKK/kWh that the family of four pays for electricity for hot water on the day shown in [Domestic hot water](c2-domestic-hot-water.md). That value is the electricity price weighted by the hot water drawn in each hour of the day; the daily average price is 1.89 DKK/kWh. The saving of water is not included in the CCE.

With direct electric water heating, the recirculating shower reduces the electricity for showering by 46 %. A conventional shower supplied by a heat pump with a COP of 2.5 uses less electricity than the recirculating shower. The water use falls from 42 to 15.5 L per shower, or by 29 m³ a year for the family of four.

The table does not include the nightly cleaning cycle and the standby power of the unit, because neither is published. The water savings are given for a conventional shower of unknown flow rate. If that flow rate is higher than 7 L/min, the fresh water volume for the 6-minute shower is larger than 15.5 L.
