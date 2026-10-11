# Heat pump model

A heat pump moves heat from a cold source to the warm water in a floor heating loop or a hot water tank, and its coefficient of performance (COP) is the heat delivered per unit of electricity used. The model in this appendix, {download}`heatpump_model.py <code/heatpump_model.py>`, describes a compact exhaust-air heat pump of the kind used in Danish low-energy houses, which takes its heat from the exhaust air leaving the ventilation heat exchanger and uses it to charge the hot water tank. Its heat output is interpolated between the test points of its Passive House Institute certificate, from 0.51 kW at −7 °C to 1.02 kW at 20 °C outdoors, and its COP follows a Lorenz model at 32 % of the ideal value, which gives a COP of 2.8 at 7 °C outdoors. Because the condenser heats the water over a glide from the return to the supply temperature, the COP depends on both: at 7 °C outdoors and 55 °C supply it falls from 3.0 with 10 °C return water to 2.0 with 50 °C, which is why a well-stratified tank matters.

```{anywidget} code/heatpump.mjs
{}
```
