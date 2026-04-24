# Edison result: micro-dose-mg-precision-dispensers

- task_id: `8024a567-32b4-4704-aa1c-d623a4c40769`
- submitted_at: 2026-04-24T01:42:41.197324Z
- status: success
- has_successful_answer: True
- total_queries: None

## Query

What commercial instruments can dispense powders at the milligram or sub-milligram scale with high precision? Focus on Mettler Toledo Quantos QX1/QX2, Chemspeed Powdernium / GDU, Freeslate / Unchained Labs Core Module Powder Dispensing, Zinsser Lissy, Analytik Jena CyBio, Hamilton STAR with powder head, and any acoustic or piezo-based micro-powder dispensers. Provide minimum dose, accuracy (±%), powder compatibility, and references to publications using these systems for high-throughput experimentation.

## Formatted answer

Question: What commercial instruments can dispense powders at the milligram or sub-milligram scale with high precision? Focus on Mettler Toledo Quantos QX1/QX2, Chemspeed Powdernium / GDU, Freeslate / Unchained Labs Core Module Powder Dispensing, Zinsser Lissy, Analytik Jena CyBio, Hamilton STAR with powder head, and any acoustic or piezo-based micro-powder dispensers. Provide minimum dose, accuracy (±%), powder compatibility, and references to publications using these systems for high-throughput experimentation.

## Commercial instruments for mg/sub‑mg powder dispensing (high precision)

### Summary
Multiple commercial solid-dispensing platforms can dispense powders in the milligram and (in some cases) sub‑milligram range with gravimetric control, but low-dose performance is strongly powder-dependent (flowability, cohesiveness, particle size, electrostatics, hygroscopicity). The evidence retrieved here contains quantitative performance for (i) Mettler Toledo Quantos on an XPE206 balance (tested down to 20 mg) and (ii) Chemspeed GDU‑Pfd (tested down to 0.5 mg), plus several peer‑reviewed examples of high‑throughput experimentation (HTE) workflows using these systems. For some user‑requested specific product names (Quantos QX1/QX2, Chemspeed “Powdernium”, and “Hamilton STAR powder head”), quantitative specifications were not found in the retrieved sources and are therefore not reported.

| Instrument/system | Dispensing principle | Minimum demonstrated/claimed dose | Accuracy/precision at low doses | Powder compatibility notes | Example HTE/automation publications | Evidence citations |
|---|---|---:|---|---|---|---|
| Mettler Toledo Quantos (XPE206/QX96 family; QX1/QX2 not evidenced in retrieved sources) | Gravimetric hopper/feeder; flow controlled by rotary tapping; QX96 used for automated solid dispensing in 96-well HTE | 20 mg demonstrated in benchmarking; lower dose for QX1/QX2 not found in retrieved sources | At 20 mg, mean errors increased for many powders (examples: Al2O3 −6.00 ± 0.93%; NaNO2 −3.96 ± 2.40%; pectin −5.87 ± 1.37%); at 200–1000 mg many powders were near 0% mean error with small SD; one study reports operation at ±0.1% target-dose tolerance in a biological dosing workflow | Best suited to free-flowing solids; failures/timeouts can occur with flow interruption; challenging materials in benchmarking included potassium acetate, molecular sieves, ammonium acetate; coarse powders can over-dispense | 96-well HTE Suzuki–Miyaura workflow using QX96; HTE survey listing Quantos models as common solid dispensers | (mennen2019theevolutionof pages 19-22, jiang2023autonomousbiomimeticsolid pages 10-10, jiang2023autonomousbiomimeticsolid pages 8-10, christensen2021automationisntautomatic pages 3-6, jiang2023autonomousbiomimeticsolid media f2d8cb27) |
| Chemspeed GDU-S SWILE | Positive-displacement gravimetric dispensing using capillaries with pistons | 0.1 mg to 50 mg evaluated in comparative study; described as effective in sub-mg to low-mg range | Quantitative ±% not found in retrieved sources; comparative review/thesis concludes it was favorable for sub- to low-mg dispensing | Better than hopper systems for wider range of powder properties, including sticky or oily solids; comparative summary says favorable for free-flowing/non-cohesive powders in 0.1–50 mg study | Comparative HTE solid-dispensing evaluation summarized in HTE reviews/thesis | (christensen2021automationisntautomatic pages 3-6, biyani2022highthroughputexperimentation pages 20-24, biyani2021advancementinorganic pages 4-7) |
| Chemspeed GDU-Pfd | Gravimetric fine-powder dosing unit on Chemspeed SWING ISYNTH; extruder partially opens to discharge target mass | 0.5 mg demonstrated | Sub-mg is achievable but variable: at 0.5 mg targets, means typically ~0.4–0.8 mg with RSD roughly ~19–33% for glass-bead examples and as high as ~45–58% for some polystyrene-bead examples; precision improves at 1–10 mg and is best at 50 mg | Material-dependent bias/variability; benchmarking versus Quantos showed large under-dosing or failures for some powders and clogging/closure issues for some challenging solids | ChemBeads submilligram HTE work; commercial benchmark in autonomous solid-dispensing study | (jiang2023autonomousbiomimeticsolid pages 5-7, jiang2023autonomousbiomimeticsolid pages 7-8, jiang2023autonomousbiomimeticsolid pages 10-10, martin2019versatilemethodsto pages 6-8, martin2019versatilemethodsto pages 8-10, martin2019versatilemethodsto pages 1-6, martin2019versatilemethodsto pages 11-14) |
| Zinsser Lissy / VARIX | Vacuum/air-pressure or positive-displacement powder pipetting; gravimetric verification with integrated balance in some systems | VARIX: 1 mg to 2 g; DryPette: 2 mg to 700 mg depending on model; Lissy PTFE tip aspiration limit 65 mg per dosage step | Zinsser test powders: ±5% at 1 mg, ±3% at 10 mg, ±1% at 50 mg; Dinter reports ~4–5% accuracy depending on solid properties; DryPette claims SD <5% for amounts ≥50 mg | Performance depends on particle size distribution, homogeneity, electrostatics, and number of dosing steps; larger targets may require multiple aspiration/dispense cycles; DryPette smallest OD 3.5 mm limits narrow-well access | Customized Zinsser robotic HT reaction screening; formulation/extraction automation using Lissy robot | (bachtler2016extractionofanthocyanins pages 3-5, dinter2004combinationofa pages 1-2, alsenz2011powderpickinganinexpensive pages 4-5, taylor2010productfocusscreening pages 2-5) |
| Unchained Labs / Freeslate Core Module 3 (CM3) solid dispensing | Integrated solid and liquid dispensing on CM3 deck; specific powder-head principle not found in retrieved sources | Not found in retrieved sources | Not found in retrieved sources | Used inside gloveboxes / N2 atmosphere for catalyst library synthesis; performs solid and liquid dispensing plus on-deck stirring | HTE catalyst synthesis workflows in MOF/mixed-oxide/single-atom catalyst studies; HTE survey notes CM3 with QX96 combination | (mennen2019theevolutionof pages 19-22, byron2024singleatommanganesebasedcatalysts pages 3-4) |
| Analytik Jena CyBio | Liquid handling / pipetting platform | Not found in retrieved sources for powder dispensing | Not found in retrieved sources for powder dispensing | Retrieved sources describe CyBio/CyBi liquid handling heads and dispensers, not powder-dosing hardware | Numerous HT liquid-handling assays, but no powder-dispensing evidence in retrieved sources | (taylor2010productfocusscreening pages 2-5) |
| Hamilton STAR | Primarily liquid handling; retrieved source mentions a powder-distribution capability but attribution to Hamilton is unclear | “<1 to 50 mg” reported in product-focus excerpt, but the same excerpt does not explicitly attribute that powder dispenser to Hamilton | Not found in retrieved sources | Treat as unconfirmed for Hamilton-specific powder head based on retrieved evidence; other retrieved STAR papers are liquid-handling only | Automation publications using Hamilton STAR are liquid-handling workflows, not confirmed powder-dispensing HTE in retrieved sources | (taylor2010productfocusscreening pages 2-5) |
| Acoustic/piezo: Labcyte Echo acoustic dispensing; ultrasonic/piezo dry-powder feeders | Echo: acoustic droplet ejection for liquids; ultrasonic/piezo dry-powder feeders: vibration-assisted dry powder flow in research prototypes | Echo: liquid 25 nL increments; direct dry-powder commercial minimum not found; ultrasonic dry-powder research systems report micro-feeding rates as low as 0.2 mg/s | Echo liquid accuracy/precision better than 4% for 5 µL transfers in one study; for direct dry powders, retrieved sources describe research prototypes and material-dependent variability, not commercial validated ±% specs | Echo is for solutions/suspensions, not evidence of direct commercial bulk-powder dispensing; ultrasonic dry-powder feeders depend strongly on density, particle size, distribution, shape, flowability, amplitude/frequency, and are noncommercial prototypes in retrieved sources | Echo-enabled HT screening and picomole-scale synthesis; ultrasonic dry-powder dispensing described in academic prototype literature, not commercial HTE platforms | (pan2015pharmaceuticalpowderdispensing pages 65-71, pan2015pharmaceuticalpowderdispensing pages 79-85, chianrabutra2014adrypowder pages 11-13, pan2015pharmaceuticalpowderdispensing pages 170-173, pan2015pharmaceuticalpowderdispensing pages 11-17) |


*Table: This table compares the main commercial and quasi-commercial solid dispensing systems discussed in the evidence set, normalized to dose floor, low-dose performance, compatibility, and example HTE use. It also flags where the retrieved sources did not support quantitative claims, especially for QX1/QX2, CM3 hardware details, CyBio powder handling, and Hamilton-specific powder heads.*

### 1) Mettler Toledo Quantos (evidence in retrieved corpus: XPE206/QX96 family; not QX1/QX2-specific)
**Minimum dose (evidence):** 20 mg demonstrated in an independent benchmarking study across many powders (targets 20–1000 mg). (jiang2023autonomousbiomimeticsolid pages 10-10, jiang2023autonomousbiomimeticsolid pages 8-10, jiang2023autonomousbiomimeticsolid media f2d8cb27)

**Accuracy/precision (evidence):** In the same study, Quantos mean percent error is typically near 0% with small SD at 200–1000 mg for many powders, but performance degrades at 20 mg with larger negative bias and higher variability (e.g., Al2O3 at 20 mg: −6.00 ± 0.93%; NaNO2 at 20 mg: −3.96 ± 2.40%; pectin at 20 mg: −5.87 ± 1.37%). (jiang2023autonomousbiomimeticsolid pages 10-10, jiang2023autonomousbiomimeticsolid media f2d8cb27)

**Powder compatibility (evidence):** A perspective on automation describes Quantos as a hopper/feeder gravimetric module best suited to free‑flowing solids and susceptible to flow interruptions/timeouts; the benchmarking study reported specific “challenging solids” for Quantos including potassium acetate, molecular sieves, and ammonium acetate, and noted coarse powders (e.g., sand) can over‑dispense due to incompatibility with dosing heads. (jiang2023autonomousbiomimeticsolid pages 8-10, christensen2021automationisntautomatic pages 3-6, jiang2023autonomousbiomimeticsolid pages 7-8)

**HTE usage references (evidence):** An HTE survey/perspective lists Quantos platforms among commonly used solid-dispensing tools in pharmaceutical HTE. (mennen2019theevolutionof pages 15-19)

**Caveat:** No quantitative minimum dose or ±% accuracy specification for Quantos **QX1/QX2** specifically was present in the retrieved sources; the quantitative results above are for a Quantos on **XPE206** and an HTE workflow reference for **QX96**. (mennen2019theevolutionof pages 19-22, jiang2023autonomousbiomimeticsolid pages 10-10)

### 2) Chemspeed GDU systems
#### 2.1 Chemspeed GDU‑S SWILE
**Minimum dose (evidence):** A comparative evaluation summarized in an HTE thesis/minireview reports testing automated powder dispensing over **0.1–50 mg** (3240 dispenses across platforms) and concludes the **GDU‑S SWILE** was favorable for sub‑ to low‑mg dispensing (in that study). (biyani2022highthroughputexperimentation pages 20-24, biyani2021advancementinorganic pages 4-7)

**Accuracy/precision (evidence):** The retrieved excerpts summarize outcomes but do not provide numeric ±% or RSD by dose for SWILE; they provide qualitative conclusions (favorable in sub‑ to low‑mg regime). (biyani2022highthroughputexperimentation pages 20-24, biyani2021advancementinorganic pages 4-7)

**Powder compatibility (evidence):** A peer‑reviewed perspective describes SWILE as a **positive‑displacement** (capillary + piston) **gravimetric** approach, effective in “sub‑milligram to low‑milligram” quantities and able to handle a wider range of powder physical properties than hopper-based tools, including **sticky or oily solids**. (christensen2021automationisntautomatic pages 3-6)

#### 2.2 Chemspeed GDU‑Pfd (fine powder dosing)
**Minimum dose (evidence):** **0.5 mg target** dispensing is explicitly reported in ChemBeads supplemental data (sub‑mg dispensing demonstrated). (martin2019versatilemethodsto pages 6-8, martin2019versatilemethodsto pages 8-10)

**Accuracy/precision (evidence, sub‑mg):** At 0.5 mg targets, mean dispensed masses are material-dependent (often ~0.4–0.8 mg) with high relative variability (RSD commonly ~20–33% in one SI table and up to ~45–58% in another, depending on bead type/material). Precision improves markedly at 1–10 mg and is best at ~50 mg (RSD often ~1–2% at 50 mg in examples). (martin2019versatilemethodsto pages 6-8, martin2019versatilemethodsto pages 8-10)

**Powder compatibility (evidence):** Material-dependent clogging/closure failures and large errors were observed in benchmarking versus Quantos for some powders; failures were attributed to issues like compressible solids clogging outlets and mechanical closure problems in cartridges/heads. (jiang2023autonomousbiomimeticsolid pages 10-10, jiang2023autonomousbiomimeticsolid pages 7-8, jiang2023autonomousbiomimeticsolid media f2d8cb27)

**HTE usage reference (evidence):** The ChemBeads paper is explicitly targeted at enabling sub‑milligram solid dispensing for HTE, using Chemspeed dosing hardware in the workflow. (martin2019versatilemethodsto pages 6-8, martin2019versatilemethodsto pages 1-6)

**Caveat:** No quantitative evidence explicitly tied to the Chemspeed product name **“Powdernium”** was present in the retrieved sources.

### 3) Zinsser Lissy / VARIX (Zinsser Analytic)
**Minimum dose / range (evidence):** A high‑throughput reaction screening platform reports solid dosing of **1 mg to 2 g** using two variable solid-dispensing pipets (VARIX) with an integrated balance measuring transferred mass. (dinter2004combinationofa pages 1-2)

**Accuracy/precision (evidence):** 
- Zinsser test powders (narrow particle size distribution) are reported to yield **±5% at 1 mg, ±3% at 10 mg, ±1% at 50 mg** in a Lissy-robot application study. (bachtler2016extractionofanthocyanins pages 3-5)
- The HT reaction screening platform reports approximate accuracy on the order of **~4–5%**, depending on solid physical properties. (dinter2004combinationofa pages 1-2)

**Powder compatibility (evidence):** Performance depends on particle size distribution, homogeneity, electrostatic charging, and the number of aspiration/dispense steps; a disposable PTFE powder tip is described with an aspiration limit of **65 mg per dosing step**, requiring multiple steps for larger target masses. (bachtler2016extractionofanthocyanins pages 3-5)

**HTE/automation publications (evidence):** A peer‑reviewed HT reaction screening study used a customized Zinsser system incorporating LISSY/VARIX components. (dinter2004combinationofa pages 1-2)

### 4) Unchained Labs / Freeslate Core Module 3 (CM3)
**Quantitative dosing specs:** Not found in retrieved sources (minimum dose, ±% accuracy, and solid-dispensing mechanism not reported). (byron2024singleatommanganesebasedcatalysts pages 3-4)

**HTE usage references (evidence):** A peer‑reviewed catalyst synthesis paper reports using a **CM3 Core Module deck (Unchained Labs)** inside an N2-filled glovebox for high‑throughput synthesis (“over 150 catalysts”), where CM3 performed **both solid and liquid dispensing** and on‑deck stirring. (byron2024singleatommanganesebasedcatalysts pages 3-4)

**Related HTE context:** A pharmaceutical HTE survey describes workflows combining an Unchained Labs CM3 deck with automated solid dispensing (e.g., Mettler‑Toledo QX96) in inert gloveboxes. (mennen2019theevolutionof pages 19-22)

### 5) Analytik Jena CyBio platforms
The retrieved corpus supports CyBio as **liquid-handling/pipetting automation**, but contains **no evidence of a CyBio-branded powder dispensing module** or quantitative powder-dosing specs; therefore it should not be treated as a powder dispenser based on the retrieved documents. (taylor2010productfocusscreening pages 2-5)

### 6) Hamilton STAR (powder dispensing head/module)
The retrieved corpus contains multiple Hamilton STAR automation examples for **liquid handling**, but **no evidence** for a Hamilton STAR powder-dispensing head/module (minimum dose, ±% accuracy, powder compatibility) in the retrieved sources. (taylor2010productfocusscreening pages 2-5)

### 7) Acoustic/piezo approaches (micro‑powder dispensing)
**Commercial acoustic dispensing (Echo/Labcyte family):** Retrieved documents show extensive HTE use of acoustic droplet ejection for *liquid* dosing (e.g., Echo 550/650 used for miniaturized synthesis/screening), but they do not provide evidence that these commercial acoustic instruments dispense *dry powders directly* in the workflows captured here. (pan2015pharmaceuticalpowderdispensing pages 65-71, pan2015pharmaceuticalpowderdispensing pages 11-17)

**Direct acoustic/piezo dry‑powder micro‑feeders:** A dissertation-like technical document reviews multiple **ultrasonic/piezoelectric vibration** approaches to dispense **dry powders**, including reports of micro-feeding rates as low as **0.2 mg/s** for some powders and strong dependence on powder properties and actuation parameters; however, these are presented as research/prototype systems rather than clearly identified commercial HTE powder dispensers in the retrieved sources. (pan2015pharmaceuticalpowderdispensing pages 65-71, pan2015pharmaceuticalpowderdispensing pages 79-85, pan2015pharmaceuticalpowderdispensing pages 170-173)

## Visual evidence
A quantitative cross-platform comparison table (Quantos vs Chemspeed vs a dual-arm robot, targets 20–1000 mg across 13 powders) is available as a cropped table image from Jiang et al. (Digital Discovery 2023). (jiang2023autonomousbiomimeticsolid media f2d8cb27)

## Key limitations of this evidence set (important for interpretation)
1) **Quantos QX1/QX2**: no QX1/QX2-specific minimum dose or accuracy specifications were retrievable here; the quantitative Quantos results are for XPE206-based Quantos tests and QX96 HTE usage. (mennen2019theevolutionof pages 19-22, jiang2023autonomousbiomimeticsolid pages 10-10)
2) **Chemspeed “Powdernium”**: not evidenced as a distinct spec-bearing product name in the retrieved sources; Chemspeed evidence is for GDU-S SWILE and GDU‑Pfd. (biyani2022highthroughputexperimentation pages 20-24, martin2019versatilemethodsto pages 6-8)
3) **Hamilton STAR powder head**: no powder-dispensing head/module evidence was found in the retrieved sources. (taylor2010productfocusscreening pages 2-5)

References

1. (mennen2019theevolutionof pages 19-22): Steven M. Mennen, Carolina Alhambra, C. Liana Allen, Mario Barberis, Simon Berritt, Thomas A. Brandt, Andrew D. Campbell, Jesús Castañón, Alan H. Cherney, Melodie Christensen, David B. Damon, J. Eugenio de Diego, Susana García-Cerrada, Pablo García-Losada, Rubén Haro, Jacob Janey, David C. Leitch, Ling Li, Fangfang Liu, Paul C. Lobben, David W. C. MacMillan, Javier Magano, Emma McInturff, Sebastien Monfette, Ronald J. Post, Danielle Schultz, Barbara J. Sitter, Jason M. Stevens, Iulia I. Strambeanu, Jack Twilton, Ke Wang, and Matthew A. Zajac. The evolution of high-throughput experimentation in pharmaceutical development and perspectives on the future. Organic Process Research & Development, 23:1213-1242, May 2019. URL: https://doi.org/10.1021/acs.oprd.9b00140, doi:10.1021/acs.oprd.9b00140. This article has 573 citations and is from a peer-reviewed journal.

2. (jiang2023autonomousbiomimeticsolid pages 10-10): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

3. (jiang2023autonomousbiomimeticsolid pages 8-10): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

4. (christensen2021automationisntautomatic pages 3-6): Melodie Christensen, Lars P. E. Yunker, Parisa Shiri, Tara Zepel, Paloma L. Prieto, Shad Grunert, Finn Bork, and Jason E. Hein. Automation isn't automatic. Chemical Science, 12:15473-15490, Oct 2021. URL: https://doi.org/10.1039/d1sc04588a, doi:10.1039/d1sc04588a. This article has 160 citations and is from a highest quality peer-reviewed journal.

5. (jiang2023autonomousbiomimeticsolid media f2d8cb27): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

6. (biyani2022highthroughputexperimentation pages 20-24): Shruti Biyani. High throughput experimentation and continuous flow synthesis of active pharmaceutical ingredients. Text, Jan 2022. URL: https://doi.org/10.25394/pgs.20081318, doi:10.25394/pgs.20081318. This article has 0 citations and is from a peer-reviewed journal.

7. (biyani2021advancementinorganic pages 4-7): Shruti A. Biyani, Yuta W. Moriuchi, and David H. Thompson. Advancement in organic synthesis through high throughput experimentation. Chemistry methods : new approaches to solving problems in chemistry, 1 7:323-339, Jul 2021. URL: https://doi.org/10.1002/cmtd.202100023, doi:10.1002/cmtd.202100023. This article has 48 citations.

8. (jiang2023autonomousbiomimeticsolid pages 5-7): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

9. (jiang2023autonomousbiomimeticsolid pages 7-8): Ying Jiang, Hatem Fakhruldeen, Gabriella Pizzuto, Louis Longley, Ai He, Tianwei Dai, Rob Clowes, Nicola Rankin, and Andrew I. Cooper. Autonomous biomimetic solid dispensing using a dual-arm robotic manipulator. Digital Discovery, 2:1733-1744, Jan 2023. URL: https://doi.org/10.1039/d3dd00075c, doi:10.1039/d3dd00075c. This article has 58 citations and is from a peer-reviewed journal.

10. (martin2019versatilemethodsto pages 6-8): M. Cynthia Martin, Gashaw M. Goshu, Jeffery R. Hartnell, Collin D. Morris, Ying Wang, and Noah P. Tu. Versatile methods to dispense submilligram quantities of solids using chemical-coated beads for high-throughput experimentation. Organic Process Research & Development, 23:1900-1907, Jul 2019. URL: https://doi.org/10.1021/acs.oprd.9b00213, doi:10.1021/acs.oprd.9b00213. This article has 34 citations and is from a peer-reviewed journal.

11. (martin2019versatilemethodsto pages 8-10): M. Cynthia Martin, Gashaw M. Goshu, Jeffery R. Hartnell, Collin D. Morris, Ying Wang, and Noah P. Tu. Versatile methods to dispense submilligram quantities of solids using chemical-coated beads for high-throughput experimentation. Organic Process Research & Development, 23:1900-1907, Jul 2019. URL: https://doi.org/10.1021/acs.oprd.9b00213, doi:10.1021/acs.oprd.9b00213. This article has 34 citations and is from a peer-reviewed journal.

12. (martin2019versatilemethodsto pages 1-6): M. Cynthia Martin, Gashaw M. Goshu, Jeffery R. Hartnell, Collin D. Morris, Ying Wang, and Noah P. Tu. Versatile methods to dispense submilligram quantities of solids using chemical-coated beads for high-throughput experimentation. Organic Process Research & Development, 23:1900-1907, Jul 2019. URL: https://doi.org/10.1021/acs.oprd.9b00213, doi:10.1021/acs.oprd.9b00213. This article has 34 citations and is from a peer-reviewed journal.

13. (martin2019versatilemethodsto pages 11-14): M. Cynthia Martin, Gashaw M. Goshu, Jeffery R. Hartnell, Collin D. Morris, Ying Wang, and Noah P. Tu. Versatile methods to dispense submilligram quantities of solids using chemical-coated beads for high-throughput experimentation. Organic Process Research & Development, 23:1900-1907, Jul 2019. URL: https://doi.org/10.1021/acs.oprd.9b00213, doi:10.1021/acs.oprd.9b00213. This article has 34 citations and is from a peer-reviewed journal.

14. (bachtler2016extractionofanthocyanins pages 3-5): Simone Bachtler and Hans‐Jörg Bart. Extraction of anthocyanins using a laboratory robot and innovative extraction technologies. Chemical Engineering & Technology, 39:1875-1883, Oct 2016. URL: https://doi.org/10.1002/ceat.201600087, doi:10.1002/ceat.201600087. This article has 6 citations and is from a peer-reviewed journal.

15. (dinter2004combinationofa pages 1-2): Christian Dinter, Hilmar Weinmann, Claudia Merten, Armin Schütz, Thorsten Blume, Michael Sander, Michael Harre, and Harribert Neh. Combination of a customized robotic system with a tlc scanner for high-throughput reaction screening. Organic Process Research & Development, 8:482-487, Apr 2004. URL: https://doi.org/10.1021/op0341972, doi:10.1021/op0341972. This article has 11 citations and is from a peer-reviewed journal.

16. (alsenz2011powderpickinganinexpensive pages 4-5): Jochem Alsenz. Powderpicking: an inexpensive, manual, medium-throughput method for powder dispensing. Powder Technology, 209:152-157, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.014, doi:10.1016/j.powtec.2011.02.014. This article has 16 citations and is from a domain leading peer-reviewed journal.

17. (taylor2010productfocusscreening pages 2-5): P. Taylor. Product focus: screening robotics and automation. Journal of Biomolecular Screening, 15:710-714, Jul 2010. URL: https://doi.org/10.1177/1087057110373266, doi:10.1177/1087057110373266. This article has 0 citations.

18. (byron2024singleatommanganesebasedcatalysts pages 3-4): Carly Byron, Patricia Anne Ignacio-de Leon, Jacob Bryant, Ryan Langeslay, Louisa Savereide, Jianguo Wen, Jeffrey Camacho-Bunquin, Justin M. Notestein, Massimiliano Delferro, and Magali Ferrandon. Single-atom manganese-based catalysts for the oxidative dehydrogenation of propane. ACS Catalysis, 14:16698-16711, Oct 2024. URL: https://doi.org/10.1021/acscatal.4c06021, doi:10.1021/acscatal.4c06021. This article has 7 citations and is from a highest quality peer-reviewed journal.

19. (pan2015pharmaceuticalpowderdispensing pages 65-71): L Pan. Pharmaceutical powder dispensing by ultrasonic vibration dosing system. Unknown journal, 2015.

20. (pan2015pharmaceuticalpowderdispensing pages 79-85): L Pan. Pharmaceutical powder dispensing by ultrasonic vibration dosing system. Unknown journal, 2015.

21. (chianrabutra2014adrypowder pages 11-13): S. Chianrabutra, B.G. Mellor, and S. Yang. A dry powder material delivery device for multiple material additive manufacturing. Unknown, Jan 2014. URL: https://doi.org/10.26153/tsw/15662, doi:10.26153/tsw/15662. This article has 53 citations.

22. (pan2015pharmaceuticalpowderdispensing pages 170-173): L Pan. Pharmaceutical powder dispensing by ultrasonic vibration dosing system. Unknown journal, 2015.

23. (pan2015pharmaceuticalpowderdispensing pages 11-17): L Pan. Pharmaceutical powder dispensing by ultrasonic vibration dosing system. Unknown journal, 2015.

24. (mennen2019theevolutionof pages 15-19): Steven M. Mennen, Carolina Alhambra, C. Liana Allen, Mario Barberis, Simon Berritt, Thomas A. Brandt, Andrew D. Campbell, Jesús Castañón, Alan H. Cherney, Melodie Christensen, David B. Damon, J. Eugenio de Diego, Susana García-Cerrada, Pablo García-Losada, Rubén Haro, Jacob Janey, David C. Leitch, Ling Li, Fangfang Liu, Paul C. Lobben, David W. C. MacMillan, Javier Magano, Emma McInturff, Sebastien Monfette, Ronald J. Post, Danielle Schultz, Barbara J. Sitter, Jason M. Stevens, Iulia I. Strambeanu, Jack Twilton, Ke Wang, and Matthew A. Zajac. The evolution of high-throughput experimentation in pharmaceutical development and perspectives on the future. Organic Process Research & Development, 23:1213-1242, May 2019. URL: https://doi.org/10.1021/acs.oprd.9b00140, doi:10.1021/acs.oprd.9b00140. This article has 573 citations and is from a peer-reviewed journal.
