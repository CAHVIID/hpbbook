# Cost of conserved energy

:::{warning} Under revision
This chapter is being reworked and may change substantially.
:::

An energy saving measure costs money once and saves energy every year of its life. The cost of conserved energy (CCE) converts the investment into a cost per kWh saved, which can be compared directly with the price of the energy the measure saves {cite:p}`meier1982`.

The investment is spread over the lifetime of the measure as an annual payment,

$$
a = \frac{r}{1-(1+r)^{-n}}
$$ (eq-cce-annuity)

where $a$ is the annuity factor, $r$ the real discount rate and $n$ the lifetime in years. The cost of conserved energy is

$$
CCE = \frac{I\,a}{\Delta E}
$$ (eq-cce)

where $I$ is the investment and $\Delta E$ the energy saved per year, compared with a reference solution. This book uses $r$ = 2.5 %. {numref}`tab-cce-annuity` gives the annuity factor for typical lifetimes.

:::{table} Annuity factor at a real discount rate of 2.5 %.
:label: tab-cce-annuity

| Lifetime $n$, years | 10 | 20 | 30 | 40 |
|---|---|---|---|---|
| Annuity factor $a$ | 0.114 | 0.064 | 0.048 | 0.040 |
:::

A measure is profitable when its CCE is lower than the price of the energy it saves. Measures can be ranked by their CCE, and the cheapest saving is taken first. The CCE does not depend on the energy price, so the ranking holds when the price changes. It does not include savings other than energy, such as water, and it does not include maintenance unless that is added to $I$ as a present value.

% REVIEW LATER (Christian, 2026-10-15): check the choice of r = 2.5 % and add a source for it, and decide whether maintenance should be part of the definition.
