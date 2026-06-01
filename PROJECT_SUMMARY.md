# Project Summary — CO₂ Emissions Trajectories Across IPCC and CMIP Scenario Generations

**Author:** Paul J. Durack ([durack1](https://github.com/durack1))  
**Repository:** `git/scenarios`  
**Last updated:** 2026-06-01

---

## Purpose

This project builds and visualises a historical record of future CO₂ emissions scenarios developed across successive generations of IPCC Assessment Reports and the Coupled Model Intercomparison Project (CMIP). The central message is captured in the figure subtitle:

> **"Futures avoided, opportunities lost"**

Each generation of IPCC/CMIP scenarios has progressively narrowed and shifted downward the plausible range of future emissions — reflecting both improved scientific understanding and evolving policy ambition. High-end scenarios that once seemed credible have been retired; low-end mitigation pathways that were once considered achievable have proved elusive. A pivotal and quantifiable milestone: RCP2.6 (2009) was the first scenario in nearly two decades of IPCC scenario-making to require **net-negative CO₂ emissions** at 2100 (−1.5 GtCO₂ yr⁻¹), marking the moment when stabilising the climate shifted from requiring emissions *reductions* to requiring active carbon *removal*.

---

## Scenario Generations Covered

| Generation | IPCC Report | CMIP Connection | Year | Scenarios | Unit |
|---|---|---|---|---|---|
| SA90 | FAR (1990) | None — used with simple models only | 1990 | 5 | PgC yr⁻¹ |
| IS92 | SAR (1995) | Informal — IS92a approximated CMIP2 1pctCO2 | 1992 | 7 | BtC yr⁻¹ |
| SRES | TAR (2001) / AR4 (2007) | CMIP3 — first formal CMIP adoption | 2000 | 40 | GtC yr⁻¹ |
| RCP | AR5 (2013–14) | CMIP5 — co-designed parallel process | 2009 | 4 | PgC yr⁻¹ |
| SSP | AR6 (2021–22) | CMIP6 — fully integrated ScenarioMIP | 2016 | 127 | Gt CO₂ yr⁻¹ |
| ScenarioMIP | AR7 (2027–29) | CMIP7 — emission-driven, harmonised 2023 | 2026 | 7 | Gt CO₂ yr⁻¹ |

Note: SA90, IS92, SRES, and RCP data are stored in carbon units and converted to CO₂ using the factor 44/12 (≈ 3.667). SSP and CMIP7 data are already in Gt CO₂ yr⁻¹.

---

## CMIP-Used Scenarios

The figure highlights the specific scenarios formally adopted to drive CMIP simulations, defined in the `CMIP_USED` dictionary in `makeFig.py`. The highest and lowest of these (ranked by 2100 value) are drawn as bold lines; the shaded band shows the full range of all scenarios in each generation.

| Generation | Scenario(s) used | 2100 CO₂ extremes (GtCO₂ yr⁻¹) |
|---|---|---|
| SA90 / FAR | None prescribed | ~10 to ~82 (full family range) |
| IS92 / SAR | IS92a | ~17 (IS92c) to ~128 (IS92e) |
| SRES / CMIP3 | A1B-AIM (~50), A2-ASF (~107), B1-IMAGE (~16) | ~10 (B1T-MESSAGE) to ~135 (A1C-AIM) |
| RCP / CMIP5 | RCP2.6 (−1.5), RCP4.5 (+15.6), RCP6.0 (+51.1), RCP8.5 (+105.7) | −1.5 to +105.7 |
| SSP / CMIP6 | SSP1-1.9 (−14.3), SSP1-2.6 (−8.3), SSP2-4.5 (+9.1), SSP3-7.0 (+85.2), SSP4-3.4 (−16.0), SSP4-6.0 (+20.6), SSP5-3.4os (−13.6), SSP5-8.5 (+126.1) | −16.0 to +126.1 |
| ScenarioMIP / CMIP7 | All 7 shown as range (no simulations complete as of 2026-06) | −22.5 (verylow-os) to +71.3 (high) |

---

## Data Sources

### Scenario data
All scenario families SA90–SSP are hardcoded as Python dictionaries in `makeFig.py`, transcribed from the primary literature:

- **SA90:** Tirpak and Vellinga (1990), IPCC FAR Working Group III, Chapter 2
- **IS92:** Leggett *et al.* (1992); Pepper *et al.* (1992)
- **SRES:** Nakicenovic and Swart (2000), *Emission Scenarios*, IPCC. doi:[10.1017/CBO9781107415324](https://www.grida.no/climate/ipcc/emission/index.htm)
- **RCP:** van Vuuren *et al.* (2007); Clarke *et al.* (2007); Hijioka *et al.* (2008); Riahi *et al.* (2007); IIASA RCP Database v2.0.4–2.0.5. The 4 RCPs were selected from ~30 candidate scenarios in the published IAM literature; each is an existing published study, not purpose-built.
- **SSP:** Riahi *et al.* (2017), *Global Environmental Change* 42, 153–168. doi:[10.1016/j.gloenvcha.2016.05.009](https://doi.org/10.1016/j.gloenvcha.2016.05.009)
- **ScenarioMIP/CMIP7:** Van Vuuren *et al.* (2026), *Geosci. Model Dev.* 19, 2627–2656. doi:[10.5194/gmd-19-2627-2026](https://doi.org/10.5194/gmd-19-2627-2026). Fetched at runtime from [chrisroadmap/cmip7-scenariomip](https://github.com/chrisroadmap/cmip7-scenariomip).

### Historical emissions
Fetched at runtime from the [Our World in Data CO₂ dataset](https://github.com/owid/co2-data) (GCP/OWID), covering 1950–2024 for World fossil + industrial CO₂ (converted from MtCO₂ to GtCO₂). A hardcoded fallback is used if the fetch fails.

---

## Files

| File | Description |
|---|---|
| `makeFig.py` | Main figure script — all data, interpolation, and plotting logic |
| `buildData.ipynb` | Jupyter notebook documenting data provenance and assembly |
| `Notes.txt` | Development notes and upstream data links |
| `NARRATIVE.md` | Extended narrative: history of IPCC/CMIP scenarios, IAMC formation, zero-crossing insight, key references |
| `PROJECT_SUMMARY.md` | This file — technical documentation of the figure |
| `YYMMDD_scenariosThroughTime.{pdf,svg,png}` | **Dated** main figure — accumulates across runs for version tracking |
| `YYMMDD_scenariosThroughTime_avg.{pdf,svg,png}` | **Dated** average-per-generation figure |
| `scenariosThroughTime.{pdf,svg,png}` | **Stable undated** main figure — used by NARRATIVE.md embed, overwritten each run |
| `scenariosThroughTime_avg.{pdf,svg,png}` | **Stable undated** average figure |
| `LICENSE` | CC BY 4.0 |

---

## Figure Design — `makeFig.py`

### Main figure (`scenariosThroughTime.png`)

**Shaded bands:** For each scenario generation, the **full min–max range** across all scenarios in the family is drawn as a lightly shaded region. Thin coloured lines trace the min and max band edges, making it easy to see where generations overlap. Envelope uses true min/max (not p10/p90) to ensure all scenarios are captured — particularly important for small ensembles such as SA90 (n=5) and RCP (n=4).

**Legend labels:** Correctly reflect the institutional relationship — `SA90 (IPCC FAR, 1990)` and `IS92 (IPCC SAR, 1992)` had no formal CMIP connection; `SRES (IPCC AR4 / CMIP3, 2000)` onward shows both IPCC assessment and CMIP phase.

**Scenario lines:** Only the highest- and lowest-emission CMIP-used scenarios per generation are drawn as bold solid lines, ranked by their 2100 value. Intermediate scenarios are omitted. End-of-line labels use short names from `CMIP_SHORT`; overlapping labels (IS92a/high, A2/RCP8.5) are offset by ±2.5 GtCO₂ for readability.

**CMIP7:** Shown as a shaded band and envelope edge lines only — no bold lines because no CMIP7 simulations are complete. Retained because the lower envelope reinforces the downward trend.

**Historical overlay:** GCP/OWID World CO₂ emissions as a thick black line, providing the observed anchor for all projections.

**Annotations:**
- *"Futures avoided"* — arrow at (2090, 110), pointing into the cluster of SRES A1FI, RCP8.5, and SSP5-8.5 high scenarios
- *"Opportunities lost"* — arrow at (2026, 20), anchored to the present date, pointing below the current historical emissions level

**2100 summary bars:** A column of vertical bars to the right of the main time series (separated by a dotted line at 2102.5) shows six statistics per generation at year 2100:
- Full-width outer ticks: **min** and **max** (matching the full scenario range envelope)
- Shorter inner ticks (solid, slightly faded): **p90** and **p10**
- Shorter inner tick (solid, full opacity): **median** (p50)
- Shorter inner tick (dashed): **mean**
- n= count above each bar in the generation's colour

Reference labels (max/p90/median/mean--/p10/min) are shown alongside the CMIP7 bar; an "at 2100" header labels the column. Note: for CMIP7, p90 = max (both high scenarios share identical 2100 values), so the "p90" label is offset 3 GtCO₂ below "max" to avoid overlap.

### Average figure (`scenariosThroughTime_avg.png`)

A sanity-check plot showing the ensemble mean trajectory per generation as a single coloured line, with the **full scenario range** (min–max) as shading. Labelled with the 2100 mean value for each family.

---

## How to Run

```bash
cd /home/duro/git/scenarios
/home/duro/miniforge3/condabin/mamba run -n xcd0112 python3 makeFig.py
```

Each run fetches CMIP7 and historical emissions data from the internet (~5 seconds) and writes 12 output files: 6 dated (`YYMMDD_` prefix, for version tracking) and 6 undated stable references. The date prefix is set automatically from the system date.

**Known warning:** `RuntimeWarning: Mean of empty slice` is raised for SA90 in the average figure because `CMIP_USED["SA90"] = []`. This is harmless — SA90 had no formally prescribed CMIP scenarios.

---

## Possible Next Steps

- **Suppress the SA90 RuntimeWarning** — guard `family_stats` against an empty selection list
- **CMIP7 simulations** — once a CMIP7 model database is available, revisit `CMIP_USED["CMIP7"]` to highlight the formally adopted driving scenarios and add bold extreme lines
- **Gitignore dated files** — if the repo grows large from accumulated dated outputs, add `[0-9][0-9][0-9][0-9][0-9][0-9]_*.pdf` etc. to `.gitignore` and manage dated copies externally
- **Additional annotations** — consider adding a vertical line or shaded band at the current date (2026) to explicitly mark the historical/projection boundary

---

## References

Durack, P.J., Taylor, K.E., Gleckler, P.J., Meehl, G.A., *et al.* (2025) The Coupled Model Intercomparison Project (CMIP): Reviewing project history, evolution, infrastructure and implementation. *EGUsphere* (preprint). doi:[10.5194/egusphere-2024-3729](https://doi.org/10.5194/egusphere-2024-3729)

Girod, B. *et al.* (2009) The evolution of the IPCC's emissions scenarios. *Environmental Science & Policy* 12(2), 103–118. doi:[10.1016/j.envsci.2008.12.006](https://doi.org/10.1016/j.envsci.2008.12.006)

Meehl, G.A. (2023) The Role of the IPCC in Climate Science. *Oxford Research Encyclopedia of Climate Science*. doi:[10.1093/acrefore/9780190228620.013.933](https://doi.org/10.1093/acrefore/9780190228620.013.933)

Moss, R.H. *et al.* (2010) The next generation of scenarios for climate change research and assessment. *Nature* 463, 747–756. doi:[10.1038/nature08823](https://doi.org/10.1038/nature08823)

O'Neill, B.C. *et al.* (2016) The Scenario Model Intercomparison Project (ScenarioMIP) for CMIP6. *Geosci. Model Dev.* 9, 3461–3482. doi:[10.5194/gmd-9-3461-2016](https://doi.org/10.5194/gmd-9-3461-2016)

Pederson, N. *et al.* (2021) An assessment of the performance of scenarios against historical global emissions for IPCC reports. *Global Environmental Change* 66, 102199. doi:[10.1016/j.gloenvcha.2020.102199](https://doi.org/10.1016/j.gloenvcha.2020.102199)

Riahi, K. *et al.* (2017) The Shared Socioeconomic Pathways and their energy, land use, and greenhouse gas emissions implications. *Global Environmental Change* 42, 153–168. doi:[10.1016/j.gloenvcha.2016.05.009](https://doi.org/10.1016/j.gloenvcha.2016.05.009)

Taylor, K.E., Stouffer, R.J., and Meehl, G.A. (2012) An overview of CMIP5 and the experiment design. *Bull. Am. Meteorol. Soc.* 93, 485–498. doi:[10.1175/BAMS-D-11-00094.1](https://doi.org/10.1175/BAMS-D-11-00094.1)

Van Vuuren, D.P. *et al.* (2011) The representative concentration pathways: an overview. *Climatic Change* 109, 5–31. doi:[10.1007/s10584-011-0148-z](https://doi.org/10.1007/s10584-011-0148-z)

Van Vuuren, D.P. *et al.* (2026) The Scenario Model Intercomparison Project for CMIP7 (ScenarioMIP-CMIP7). *Geosci. Model Dev.* 19, 2627–2656. doi:[10.5194/gmd-19-2627-2026](https://doi.org/10.5194/gmd-19-2627-2026)

*See `NARRATIVE.md` for the full historical account with complete references.*
