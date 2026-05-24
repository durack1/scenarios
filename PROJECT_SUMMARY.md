# Project Summary — CO₂ Emissions Trajectories Across CMIP Scenario Generations

**Author:** Paul J. Durack ([durack1](https://github.com/durack1))  
**Repository:** `git/scenarios`  
**Last updated:** 2026-05-24

---

## Purpose

This project builds and visualises a historical record of future CO₂ emissions scenarios developed to drive successive generations of the Coupled Model Intercomparison Project (CMIP). The central message is captured in the figure subtitle:

> **"Futures avoided, opportunities lost"**

Each generation of IPCC scenarios has progressively narrowed and shifted downward the plausible range of future emissions — reflecting both improved scientific understanding and evolving policy ambition. High-end scenarios that once seemed credible have been retired; low-end mitigation pathways that were once considered achievable have proved elusive.

---

## Scenario Generations Covered

| Generation | CMIP Phase | Year | Scenarios | Unit |
|---|---|---|---|---|
| SA90 | CMIP1 | 1990 | 5 | PgC yr⁻¹ |
| IS92 | CMIP2 | 1992 | 7 | BtC yr⁻¹ |
| SRES | CMIP3 | 2000 | 40 | GtC yr⁻¹ |
| RCP | CMIP5 | 2009 | 4 | PgC yr⁻¹ |
| SSP | CMIP6 | 2016 | 127 | Gt CO₂ yr⁻¹ |
| ScenarioMIP | CMIP7 | 2026 | 7 | Gt CO₂ yr⁻¹ |

Note: SA90, IS92, SRES, and RCP data are stored in carbon units (C) and converted to CO₂ using the factor 44/12 (≈ 3.667). SSP and CMIP7 data are already in Gt CO₂ yr⁻¹.

---

## CMIP-Used Scenarios

The figure highlights the specific scenarios that were formally adopted to drive CMIP simulations, rather than showing all scenarios in each family. These are defined in the `CMIP_USED` dictionary in `makeFig.py`.

| Generation | Scenario(s) used to drive CMIP |
|---|---|
| SA90 / CMIP1 | None prescribed |
| IS92 / CMIP2 | IS92a |
| SRES / CMIP3 | A1B-AIM, A2-ASF, B1-IMAGE |
| RCP / CMIP5 | RCP2.6 (IMAGE), RCP4.5 (MiniCAM), RCP6.0 (AIM), RCP8.5 (MESSAGE) |
| SSP / CMIP6 | SSP1-1.9 (IMAGE), SSP1-2.6 (IMAGE), SSP2-4.5 (MESSAGE-GLOBIOM), SSP3-7.0 (AIM/CGE), SSP4-3.4 (GCAM4), SSP4-6.0 (GCAM4), SSP5-3.4os (REMIND-MAGPIE), SSP5-8.5 (REMIND-MAGPIE) |
| ScenarioMIP / CMIP7 | All 7 scenarios shown as range (no simulations complete as of 2026-05) |

---

## Data Sources

### Scenario data
All scenario families SA90–SSP are hardcoded as Python dictionaries in `makeFig.py`, transcribed from the primary literature:

- **SA90:** Tirpak and Vellinga (1990), IPCC FAR Working Group III, Chapter 2
- **IS92:** Leggett *et al.* (1992); Pepper *et al.* (1992); Mitchell and Gregory (1992)
- **SRES:** Nakicenovic and Swart (2000), *Emission Scenarios*, IPCC
- **RCP:** van Vuuren *et al.* (2007); Clarke *et al.* (2007); Hijioka *et al.* (2008); Riahi and Nakicenovic (2007); RCP Database v2.0.4–2.0.5, IIASA
- **SSP:** IIASA SSP Scenario Database; Riahi *et al.* (2017)
- **ScenarioMIP/CMIP7:** Van Vuuren *et al.* (2026), *Geosci. Model Dev.*, 19(7), 2627–2656. doi:[10.5194/gmd-19-2627-2026](https://doi.org/10.5194/gmd-19-2627-2026). Data fetched at runtime from [chrisroadmap/cmip7-scenariomip](https://github.com/chrisroadmap/cmip7-scenariomip).

### Historical emissions
Fetched at runtime from the [Our World in Data CO₂ dataset](https://github.com/owid/co2-data) (GCP/OWID), covering 1950–2024 for World fossil + industrial CO₂ (converted from MtCO₂ to GtCO₂). A hardcoded fallback is used if the fetch fails.

---

## Files

| File | Description |
|---|---|
| `makeFig.py` | Main figure script — all data, interpolation, and plotting logic |
| `buildData.ipynb` | Jupyter notebook documenting data provenance and assembly |
| `Notes.txt` | Development notes and upstream data links |
| `makeFig.png/pdf/svg` | Main figure outputs |
| `makeFig_avg.png/pdf/svg` | Sanity-check figure: mean trajectory per generation with p10–p90 shading |
| `LICENSE` | CC BY 4.0 |

---

## Figure Design — `makeFig.py`

### Main figure (`makeFig.png`)

**Shaded bands:** For each scenario generation, the full p10–p90 range across all scenarios in the family is drawn as a lightly shaded region. Thin coloured lines trace the p10 and p90 band edges, making it easy to see where generations overlap.

**Scenario lines:** Only the highest- and lowest-emission CMIP-used scenarios per generation are drawn as bold solid lines, ranked by their 2100 value. Intermediate scenarios are omitted to reduce clutter. End-of-line labels identify each extreme using short names from `CMIP_SHORT`.

**CMIP7:** Shown as a shaded band and envelope edge lines only. No bold lines are drawn because no CMIP7 simulations are complete; the band is retained because it continues and reinforces the downward trend in the scenario envelope.

**Historical overlay:** GCP/OWID World CO₂ emissions plotted as a thick black line, providing the observed anchor for all projections.

**2100 summary bars:** A column of vertical error bars to the right of the main time series (separated by a dotted line at 2102.5) shows, for each generation at year 2100:
- Top and bottom ticks: p90 and p10 (matching the envelope edges)
- Solid inner tick: median (p50)
- Dashed inner tick: mean

This allows direct y-axis comparison of the scenario spread across generations.

**Annotations:** "Futures avoided" (pointing to the high-end region that successive generations have retired) and "Opportunities lost" (pointing to the low-end region that has proved unattainable).

### Average figure (`makeFig_avg.png`)

A simpler sanity-check plot showing the ensemble mean trajectory per generation as a single coloured line, with p10–p90 shading. Labelled with the 2100 mean value and scenario count (n) for each family.

---

## How to Run

```bash
cd /home/duro/git/scenarios
/home/duro/miniforge3/condabin/mamba run -n xcd0112 python3 makeFig.py
```

The script fetches CMIP7 and historical data from the internet on each run (~5 seconds). Outputs are written to the repo directory.

**Known warning:** `RuntimeWarning: Mean of empty slice` is raised for SA90 in the average figure because SA90 has no CMIP-used scenarios defined (`CMIP_USED["SA90"] = []`). This is harmless.

---

## Possible Next Steps

- **Suppress the SA90 RuntimeWarning** — guard `family_stats` against an empty selection list
- **Label the 2100 summary bar column** — add a small header or x-axis annotation to identify it as a 2100 cross-section
- **Refine annotations** — the "Futures avoided / Opportunities lost" arrow positions may need adjustment as the layout evolves
- **CMIP7 simulations** — once a CMIP7 model database is available, revisit `CMIP_USED["CMIP7"]` to highlight the formally adopted driving scenarios
- **Add CMIP4 note** — the sequence jumps IS92 (CMIP2) → SRES (CMIP3) → RCP (CMIP5), skipping CMIP4; a figure note may be warranted
- **Commit to GitHub remote** — `git push` when ready to share

---

## References

Girod *et al.* (2009) The evolution of the IPCC's emissions scenarios. *Environmental Science & Policy*, 12(2), 103–118. doi:[10.1016/j.envsci.2008.12.006](https://doi.org/10.1016/j.envsci.2008.12.006)

Pederson *et al.* (2021) An assessment of the performance of scenarios against historical global emissions for IPCC reports. *Global Environmental Change*, 66, 102199. doi:[10.1016/j.gloenvcha.2020.102199](https://doi.org/10.1016/j.gloenvcha.2020.102199)

Van Vuuren *et al.* (2026) The Scenario Model Intercomparison Project for CMIP7 (ScenarioMIP-CMIP7). *Geoscientific Model Development*, 19(7), 2627–2656. doi:[10.5194/gmd-19-2627-2026](https://doi.org/10.5194/gmd-19-2627-2026)
