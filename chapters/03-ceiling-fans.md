# Ceiling fans

## Introduction

Danish homes are increasingly at risk of overheating. New dwellings are well insulated and airtight, often have large glazed areas, and keep their heat well. That works well in winter, but in summer the same building struggles to get rid of solar and internal gains. Summers are also getting warmer, and heat waves are getting longer and more intense. A row house that is comfortable in today's climate may well overheat in the 2050 climate.

The Danish Building Regulations (BR18) limit overheating in new dwellings to 100 hours per year above 27 °C and 25 hours per year above 28 °C. The easy answer to overheating is air-conditioning, but it adds investment, electricity use, refrigerants and maintenance to buildings that previously needed none. This chapter looks at a cheaper and much more energy-efficient alternative: the ceiling fan.

### Fans cool people, not rooms

A ceiling fan does not lower the air temperature. Its motor even adds a little heat to the room. What it does is raise the air speed around the occupants. Higher air speed increases the heat loss from the skin by convection and evaporation, so people feel cooler at the same temperature. A design air speed of about 0.5 m/s gives a cooling effect of roughly 2 °C {cite:p}`raftery2020`. In other words, a room at 28 °C with a fan running can feel like 26 °C without one.

Two consequences follow:

- A fan only helps when someone is in the room. A fan running in an empty room wastes energy.
- A fan cannot remove heat from the building. Heat must still be kept out or removed by other means, otherwise the temperature keeps rising until the fan is no longer enough.

### Where fans fit in the cooling strategy

Ceiling fans are one step in a cooling hierarchy, where each step is cheaper and simpler than the next:

1. **Reduce the heat gains**: shading, solar-control glazing and sensible window areas (chapter 1).
2. **Remove heat passively**: ventilative cooling with opening windows and night cooling of the thermal mass (chapter 2).
3. **Raise the air speed**: ceiling fans let occupants accept a higher temperature (this chapter).
4. **Cool actively**: mechanical cooling, only for what is left.

Used this way, the fan becomes the first cooling stage that runs before any active cooling starts. It can push the temperature at which air-conditioning is needed up by a couple of degrees, or remove the need for it altogether. The energy saved typically exceeds the fan's own energy use by a factor of 10 to 100 {cite:p}`raftery2020`.

:::{admonition} Learning objectives
:class: tip

After this chapter you can:

- explain how elevated air speed offsets operative temperature, using PMV/SET and the adaptive comfort model
- size and place a ceiling fan for a room from a datasheet
- set up a temperature-stepped control strategy where the fan runs before any active cooling
- estimate the change in PMV and the fan energy for a room, and compare it with air-conditioning
:::

The chapter first explains how air speed affects thermal comfort and how a ceiling fan moves air. It then covers fan performance, sizing and placement, control, and energy use compared with air-conditioning. It ends by showing how to model fans when the simulation tool does not support elevated air speed, with a worked example from the course row house.

## Air speed and thermal comfort

:::{admonition} To be written
:class: dropdown

How the body loses heat, and the cooling effect of air speed. Operative temperature versus PMV versus the adaptive model, and why the adaptive model suits residences. Key number: 0.5 m/s gives about 2 °C cooling effect (SET, ASHRAE 55 Appendix D). Elevated air speed in EN 16798, ASHRAE 55 and ISO 7730, with the CBE comfort tool as a hands-on aid.
:::

## Airflow from a ceiling fan

:::{admonition} To be written
:class: dropdown

The impinging jet (core, expansion and radial floor spread). The highest speeds are under the fan, and a larger diameter relative to the room gives more uniform speeds. Draught from above: mean velocity and turbulence intensity.
:::

## Fan performance

:::{admonition} To be written
:class: dropdown

Fan laws: airflow is proportional to speed and power to speed cubed, so efficacy falls at high speed (median 165 cfm/W at low speed vs 79 cfm/W at high). Compare fans only at equal diameter and airflow. Reading a datasheet, and CFM versus m³/h.
:::

## Sizing and placement

:::{admonition} To be written
:class: dropdown

Diameter of 0.2 to 0.4 times √(floor area). One centred fan serves aspect ratios up to 1.5:1, and larger rooms are split into square fan cells. Clearances: blades at least 2.1 m above the floor, at least 0.2–0.3 m below the ceiling and at least 0.45 m from walls. Coordinate with lighting and sprinklers.
:::

## Control and integration

:::{admonition} To be written
:class: dropdown

The fan is the first cooling stage: the fan starts around 23–24 °C and AC only around 25.5–26.5 °C. Minimum speed should stay below about 0.4 m/s for seated occupants. Occupant control versus automation, interplay with opening windows, and reverse mode for winter destratification.
:::

## Energy and carbon

:::{admonition} To be written
:class: dropdown

Fan energy versus air-conditioning, compared on primary energy as a proxy for carbon. HVAC savings typically exceed fan energy 10 to 100 times.
:::

## Modelling fans

:::{admonition} To be written
:class: dropdown

IDA ICE fixes air speed at 0.1 m/s in its comfort output, so fan effects must be post-processed. The course PMV script with its stepped control is the method.
:::

## Worked example

:::{admonition} To be written
:class: dropdown

One room in the course row house, including a heat-wave year:

1. Pick a fan datasheet and read its diameter, rated airflow and rated power.
2. Check the diameter against the room using the sizing rule and the clearances.
3. Calculate the rated specific fan figure, then air speed and power at low, medium and high, assuming both scale with airflow.
4. Apply the stepped control and compute PMV with and without the fan, plus annual fan energy.
5. Compare with AC using primary energy as a proxy for carbon.
:::

## Summary and exercises

:::{admonition} To be written
:class: dropdown

Rules-of-thumb box, and guiding questions linked to Assignment 04 Q11: How much cooling does a fan give? Is it enough in future Danish summers, including the Annex 80 heat waves? How much energy does a fan in every habitable room use?
:::
