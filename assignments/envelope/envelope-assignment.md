# Assignment 1: Compactness and building envelope

**This assignment is made in groups of 2.**

## Background and aim

It is essential to minimize space heating consumption in optimized nearly Zero Energy Buildings, onZEBs. Despite the fact that climate change causes shorter heating seasons, space heating remains a significant contributor to the overall energy consumption of buildings and it is difficult to align the heating demand with renewable energy production.

This assignment demonstrates how different components related to the envelope can be optimized to reduce the space heating demand significantly.

The assignment touches upon:

1. Compactness
2. Thermal envelope and thermal bridges
3. Glazings and window frames
4. Cost-optimal insulation levels

Answer the questions (Q1–Q13). Document them in a report.

## Compactness

The compactness plays a significant role on the final energy use and the cost of construction. A more compact building has lower heat loss per livable m² and less material use per m². This is particularly easy to achieve for row-houses or point-houses.

Compactness ratio is defined as the ratio of total insulated building envelope area to the floor area. This is based on *internal* surface areas of the building neglecting effects from partition walls.

The aim of the assignment is to make a fast analysis of the overall geometry of buildings based on archetype spaces, resembling pre-fabricated 3D volumes:

- 4 × 4 × 2.5 m *primary* spaces with one window (habitable rooms)
- 4 × 4 × 2.5 m *secondary* spaces without windows (bathrooms, corridors etc.)

This will show how the compactness ratio influences space heating consumption.

In Appendix A, dwelling 06 and 07 represent fictive, realistic buildings. Dwelling 08 is a realistic type house from Huscompagniet. The houses are numbered in the same order as here: <https://www.huscompagniet.dk/huse/plantegninger>

**Q1.** Calculate the compactness ratio, equal to the ratio of insulated, opaque building envelope to the floor area, for the different examples shown in Appendix A.

### Heat demand

The calculation of the heat demand assumes that the heat demand may be expressed by the simple linear function of the compactness ratio shown below:

$$
q_{heat} = 12 - 5.65 \times (2.69 - c)
$$

where $q_{heat}$ is the heat demand of the dwelling in kWh/m² and $c$ the compactness ratio of the dwelling. This equation is explained in the presentation of the parameter analyses.

**Q2.** Calculate the heat demand for each building type in Appendix A. Evaluate the results: do they match your beliefs?

## Thermal envelope

### Reducing U-value and Ψ-losses

Building façade performance depends on the U-value and the linear thermal losses. It is prudent to develop façades with a U-value of 0.10 W/m²K *including* linear losses.

A wooden skeleton façade is structurally sound and minimizes material use, but could potentially be optimized by increasing the thickness of the insulation and minimizing the effect of the wood profiles by using I-profiles instead of solid wood profiles.

In the sketch below the internal area of the wall is shown by a dashed line. The body of the I-profile is made of a 15 mm OSB plate with top and bottom flanges of 45 × 45 mm battens.

:::{note} Calculation principle
The calculation is based on the *area-weighted average thermal conductivity of layers* with mixed wood and insulation, as shown in DS 418, chapter 6.6. This method ignores the 2D effects of mixed layers, but is acceptable for wood battens (NEVER for metal profiles).

The four layers with 45 × 45 mm wood profiles may be assumed to have 10 % solid wood and 90 % insulation. The centre layer (I-profile body) with a variable thickness X may be assumed to have 3 % wood and 97 % insulation.

Calculate the average U-value of the wall using a thermal conductivity of insulation and wood of 0.037 W/mK and 0.14 W/mK, respectively. Ignore the resistances of gypsum boards, OSB boards, wind barriers and ventilated cavities.

Do not use the sketch to calculate the wood fractions; use the wood fractions given above.
:::

:::{figure} figures/wall-i-profile.png
:label: fig-asg1-wall
:width: 100%

Wooden skeleton façade element with a window opening of 1.2 × 2.67 m (elevation, horizontal section below and vertical section right). The layers are 90 mm, X = 155, 205 or 255 mm, and 90 mm of insulation.
:::

**Q3.** Calculate the average U-value of the wall for different heights of the body of the I-profile (marked X on the sketch). Do it for bodies of 155 mm, 205 mm and 255 mm (corresponding to standard I-profile dimensions of 245 mm, 295 mm and 345 mm).

**Q4.** For comparison, make the same calculations with solid wood profiles of 45 × 245 mm, 45 × 295 mm and 45 × 345 mm replacing the I-profiles, resulting in 10 % wood and 90 % insulation in all layers. Calculate the average U-value of the wall with the three profiles.

**Q5.** Calculate the U-value reductions (in percent) when moving from solid profiles to I-profiles.

**Q6.** Which combination comes closest to a U-value of 0.10 W/m²K?

**Q7.** Using the Q6 solution as example, how many cm of insulation does using the I-profile instead of the solid profile save (equal U-value)?

:::{admonition} Q7b. Extra for the nerdy ones
:class: tip
Very often, in bigger projects, light façades are made with slotted metal profiles instead of wood profiles. Slotted metal profiles require meticulous calculations, but fortunately we can be inspired by example 4.3 in DS/INF 418-1:2013 and quickly recalculate the Q6 solution with slotted metal profiles. Try to calculate the average U-value of the wall, but now with slotted metal profiles. Use approximate lengths from the sketch.
:::

## Glazings and frames

Triple glazings are now the standard for windows in new buildings in Denmark. But improvement of the energy performance of glazing units is an ongoing process, and therefore it is important to keep searching for the best products on the market.

The glazing units should have the specific required functions, like an anti-condensation coating on the outside, and be based on a gas filling of 90 % argon to avoid a very costly gas filling such as krypton.

The energy performance of glazing units should have a low U-value and a high LT-value (light transmittance). The g-value should be selected to avoid overheating, but without compromising LT. The theoretical LT/g ratio is approx. 2 (= the maximum *selectivity* is 2).

On-line programs with product databases:

- Spectrum from Pilkington: <https://spectrum.pilkington.com/>
- Calumen from Saint-Gobain: <https://calumen.com/>

**Register with your name in the program** and select DK as country, English as language and 2 decimals (if possible). Always use EN standards for calculations if there is a choice.

It is recommended to start by looking at an overview of products (glass and coatings) and their performance data from the companies, to have the basic information on the different elements of the glazing unit that can be used in the programs. Pilkington has the "Glasfakta" handbook, and Calumen has online guidance, but the tools may not include the very best coatings, like anti-reflective and anti-condensation coatings.

The guide to building the best glazing units is to select:

- 4 mm low-iron glass (product names like Diamant, Optiwhite)
- 18–20 mm gaps with 90 % argon. Don't use krypton, as it is too expensive
- a low-emissivity coating on one of the surfaces in each cavity; choose the type that gives the lowest U-value and highest LT-value
- an anti-condensation coating on the outside; this may be part of a self-cleaning coating
- anti-reflection coatings on all possible surfaces to increase the LT-value

**Q8.** Assemble the best 3-layer glazing that can be made with and without anti-condensation (AC) coating, and report the U-, g- and LT-values in the table below.

| | U [W/m²K] | g [-] | LT [-] |
|---|---|---|---|
| Reference S3 | 0.6 | 0.49 | 0.71 |
| Improved without AC | | | |
| Improved with AC | | | |

The solar transmittance of the glazing unit is called TE in Calumen, ET in Spectrum and Te in IDA ICE.

The emissivities in the input for glazings in IDA ICE are the emissivities of the inside surface and the outside surface of the glazing unit, not of the internal surfaces. You may therefore typically keep the default values.

### Best performing operable and fixed window frames on the market

In general, the best frame is the product with the smallest total heat loss per metre length of the profile (W/mK). The total heat loss of the frame per metre length, L (W/mK), may be found in two ways:

- From a detailed calculation or information: the U-value of the frame and the linear loss coefficient of the glazing–frame assembly, the Ψ-value (W/mK): $L = U_f \, w + \Psi$, where $w$ is the width of the frame.
- From whole-window information and areas: the total equivalent $U_f$-value of the frame (from energy labelling tables) and the specific width of the frame, $w$ (from data sheets on the products referred to in the energy labelling, energivinduer.dk): $L = U_f \, w$.

Note that the total (window) U-value is interchangeably called $U_w$ and $U_{tot}$.

**Best operable window.** Data for the best operable frame on the market in Denmark can be found in the list of products at <https://www.energivinduer.dk>. $U_f$ represents the total heat loss of the frame (in W/K), including the effect of the U-value of the frame and the effect of the linear loss coefficient of the glazing–frame assembly, divided by the frame area.

In the product list, $1-F_f$ is the ratio of glazing area to total window area of a reference window of 1.23 × 1.48 m (in the individual certificates it is $F_f$, so beware). So $F_f$ is the ratio of frame area to total window area. The product list does not give the frame width, but $F_f$ is proportional to it.

The product with the smallest value of $U_f F_f$ may be used to find the best frame. Also consider the $T_{oi}$ temperature: well-insulating frames have a higher $T_{oi}$.

When the best frame is found, the data sheet for the product can be found through the link in the energivinduer.dk database. Find the width of the frame, $w$ (m), on the drawings of the profiles on the producer's homepage, and calculate $w \, U_f$. The name of the producer is in the energivinduer.dk database.

**Best fixed window.** Search in Denmark and globally for frame profiles for fixed windows with triple glazing. A very useful source of documented frame data is <https://www.passivehouse.com>. Some of the slim operable frames may also be used as fixed window frames with the same energy data. When comparing energy data, it is important to find either the total U-value of the frame *or* both the U-value and the Ψ-value of the frame.

**Q9.** Document the parameters of the best fixed and the best operable window frame in a table like the one below.

| Product | Type | Documentation | Width [m] | $U_f$ [W/m²K] | Width × $U_f$ [W/mK] |
|---|---|---|---|---|---|
| Reference | Operable | Screenshot | 0.094 | 1.56 | 0.15 |
| NN (a) | Best operable | Screenshot | | | |
| NN (b) | Best fixed | Screenshot | | | |

(a) Based on the list of windows at energivinduer.dk.
(b) Based on your search for the best fixed window frame profile with triple glazing.

Despite the advances in the thermal properties of windows, the heat loss is still much higher than through the insulated wall next to the window. When the light transmittance of a glazing is improved, the glazing area can be reduced while maintaining the same daylight: high heat loss glazing is replaced by low heat loss insulated façade.

- Adjust the *glazing* area for the new light transmittance: $A_{g,new} = \dfrac{LT_{ref}}{LT_{new}} A_{g,ref}$
- Calculate the *frame area* $A_f$ from the width of your best operable frame.
- Calculate the new *window area* $A_w = A_f + A_g$.
- Calculate the *frame fraction* for the new glazing area: $F_f = 1 - A_g / A_w$.

**Q10.** Given the improved glazing from Q8 and the improved frame from Q9, calculate the new glazing area, window area, frame area and total U-value of the improved window. Document the parameters of the improved glazing first, then of the improved glazing + frame, in a table like the one below.

| Product | Type | LT [-] | $A_w$ [m²] | $A_g$ [m²] | $A_f$ [m²] | $1-F_f$ [-] | $U_f$ [W/m²K] | $U_w$ [W/m²K] |
|---|---|---|---|---|---|---|---|---|
| Reference | Operable | 0.71 | 3.2 | 2.56 | 0.64 | 0.8 | 2.1 | 1.3 |
| Improved glazing | Best triple-layer | | | | 0.64 | | 2.1 | |
| Improved frame + glazing | Best operable | | | | | | | |

## Cost-optimal insulation

Reducing the cost of the building envelope by:

- using cheaper insulation material
- optimizing the insulation thickness in the floor, roof and wall to achieve equal CCE, and to achieve a CCE equal to the cost of renewable energy.

One IDA ICE model is uploaded, representing the row house in Appendix B:

- *Model B. Realistic energy use*: space heating / cooling set points are 22/25 °C and the internal heat gain is 4 W/m².

Remember to make the changes to the window size, glazing U-value and frame from Q10.

To simplify, the model has active mechanical cooling instead of passive cooling measures like venting and/or shading. The active cooling ensures that the space heating demand is not artificially reduced because the indoor temperature is allowed to rise high above the heating set point. Future assignments will show how passive cooling measures can replace active cooling in residences.

### Reduce air leakage by use of perfect air sealing systems

The Danish low-energy class building code requires a maximum air leakage of the building envelope of 0.7 L/(s·m²) at 50 Pa. By designing and producing the prefabricated modules with a high focus on the air sealing system, it is possible to reduce the air leakage to 0.2 L/(s·m²) at 50 Pa.

Use the IDA ICE model "Model B. Realistic energy use" with all of the building envelope set to U = 0.1 W/m²K, and simulate the difference in heating energy between an infiltration of 0.7 and 0.2 L/(s·m²) at 50 Pa.

**Q11.** Compare the heating energy with infiltration 0.7 and 0.2. Report both numbers in kWh/m².

### Reducing the cost of the building envelope

In the real row house the insulation of the floor construction is placed below the box, and no insulation is placed inside the floor construction. This keeps the floor construction warm and dry. The insulation is typically 30 cm of expanded polystyrene, EPS. But as the insulation is not exposed to any load from the floor of the box, it may be replaced with low-density insulation.

Find prices of EPS and mineral wool insulation online and calculate the initial cost saving for one row house when the 30 cm EPS is replaced with 30 cm standard low-density mineral wool insulation (λ = 0.037 W/mK).

#### Optimizing the insulation thickness in the floor, roof and wall using CCE

The cost of conserved energy, CCE, can be calculated for each of the building envelope constructions by increasing the thickness of insulation in the constructions one at a time in IDA ICE.

Use the IDA ICE model "Model B. Realistic energy use" with U = 0.1 W/m²K *and* 0.2 L/(s·m²) at 50 Pa from the air leakage section above. Change the thermal conductivity of the floor insulation to 0.037 W/mK and adjust the insulation thickness to get a U-value of 0.1 W/m²K.

Use this model to calculate the reduction in space heating when the insulation thickness is increased by 5 cm in one of the building envelope constructions (floor, wall or roof), *one envelope construction at a time*.

Then find the corresponding change in investment cost of insulation (based on mineral wool with λ = 0.037 W/mK) for each envelope construction *and* the change in energy use for heating over 100 years. This is the way to calculate the marginal CCE.

You may repeat the calculations a few times, increasing the insulation thickness by 5 cm each time, but to be realistic you can stop when the insulation thickness exceeds 50 cm. Use the provided Excel template "Marginal CCE" to help you.

By comparing and recalculating the CCE for the floor, wall and roof, you find the insulation thickness of each construction that results in the same CCE. Use all three insulation thicknesses as a combined input to your IDA ICE model and calculate the space heating demand for *the optimal insulation combination*.

**Q12.** Show the CCE optimization (Excel screenshot) and the heating energy demand for the optimal insulation solution. Comment on the results.

#### CCE equal to the cost of renewable energy

As long as your CCE is lower than the cost of buying energy, it is still cheaper to insulate more. Try to see if it is possible and realistic (within the maximum of 50 cm of insulation) to achieve a CCE equal to the cost of renewable energy. Calculate the heating energy use for the absolute optimal solution by selecting 3–4 CCE values, reading the corresponding insulation thicknesses and *changing the insulation thickness in all three building envelope constructions at the same time*. Find the CCE that comes close to the heating price of 0.6 DKK/kWh.

**Q13.** How much insulation should the owner buy and still have a cheaper solution? Should the owner buy more expensive insulation (with better insulating properties)? Report the results in a short memo and comment on what you learned. Reflect back on the previous results.

## Appendix A: Example of submission layout

A room may function as a *primary room* (P) with long-term use by people.

A room may function as a *secondary room* (S) with short-term use (bathroom, kitchen, technical room), with no windows and no façade.

Primary rooms have a window area of 4 m² in the façade or in the flat roof.

Area of external wall without window: 4 m × 2.5 m = 10 m². Area of external wall with window: 10 − 4 = 6 m².

For the last example dwelling (No 8), realistic dimensions of type house floor plans must be used; see "Dwellings No 8". There is one numbered floor plan for each group. Garages and sheds are not heated and are therefore disregarded.

Unknown dimensions must be estimated, e.g. by scale measuring in a PDF program. *Use internal dimensions.*

:::{figure} figures/legend-modules.png
:label: fig-asg1-legend
:width: 70%

Explanation of the sketches. P: primary room, S: secondary room, w: window in façade or roof (4 m²), A: area surrounded by boxes, gw: glass wall 4 m × 2.5 m.
:::

Ratio of insulated building envelope surface area to floor area for some examples. All areas in m². Wall ww: wall with window, 10 − 4 = 6 m² per module face. Wall wow: wall without window, 4 × 2.5 = 10 m² per module face.

| Residential example | Storeys | Floor area | Slab | Roof | Wall ww | Wall wow | Surface total | Surface to floor ratio | Space heating [kWh/m²] | Comment |
|---|---|---|---|---|---|---|---|---|---|---|
| No 1 | 1 | 16 | 16 | 16 | 6 | 30 | 68 | 4.25 | | Max possible |
| No 2 | 1 | 16 | 0 | 0 | 6 | 0 | 6 | 0.38 | | Min possible |
| No 3 | | | | | | | | | | |
| No 4 | | | | | | | | | | |
| No 5 | | | | | | | | | | |
| No 6 | | | | | | | | | | |
| No 7 | | | | | | | | | | |
| No 8 | | | | | | | | | | |

**No 1. One module, all surfaces external.** A free-standing micro house, 4 m × 4 m × 2.5 m, with a window in one façade.

```{image} figures/no1-micro-house.png
:width: 15%
```

**No 2. One module, only the wall with the window is external.** A room in a very large multistorey building.

**No 3. 12 modules. Detached long house.**

```{image} figures/no3-long-house.png
:width: 45%
```

**No 4. 12 modules. Detached angle house.**

```{image} figures/no4-angle-house.png
:width: 45%
```

**No 5. 12 modules forming an open space A with 4 roof windows. Detached house.**

```{image} figures/no5-open-space.png
:width: 45%
```

**No 6. N × 9 modules in a 3-storey terraced house or row house.** Floor plan and gable view. Gables are neglected in the calculations.

```{image} figures/no6-row-house-plan.png
:width: 20%
```

```{image} figures/no6-row-house-facade.png
:width: 15%
```

**No 7. Dormitory with 32 m² rooms on 3 floors.** A U-shaped building where the rooms form a shared kitchen area with a glass façade. Total dimensions 24 m × 24 m × 7.5 m.

```{image} figures/no7-dormitory.png
:width: 50%
```

**No 8. Type house floor plan no XX** from <https://www.huscompagniet.dk/huse/plantegninger>. Floor plans are numbered for each group. Assumptions for the compactness ratio, building envelope area based on:

- internal lengths = external lengths − 2 × 0.40 m
- an internal height of 2.5 m.

## Appendix B: Examples of real buildings similar to buildings No 6 and No 7

**Building 6. Row house.** See the description in the file "Bachelor - Energianalyse …" in the Background folder on DTU Learn.

```{image} figures/b6-row-house-photo.jpg
:width: 35%
```

```{image} figures/b6-row-house-section.jpg
:width: 45%
```

**Building 7. Dormitory, Lundtoftevej 160.** See the description in the file "Presentation - Lundtoftevej" in the Background folder on DTU Learn.

```{image} figures/b7-lundtoftevej.jpg
:width: 70%
```
