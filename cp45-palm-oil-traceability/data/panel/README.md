# Classifier panel (not supplied)

Notebook Part 5 (and report Chapter 4.2) specify a distress / controversy classifier. It needs a **labelled firm-month panel**, which the
15-Oct-2026 Terminal screens do not provide (21 firm-years, no event history). Until you add one, Part 5 runs on a **synthetic** panel
only to prove the code works; every number it prints is tagged `SYNTHETIC - code test, NOT EVIDENCE`.

**To run it on real data:** copy `spoei_panel_TEMPLATE.csv` to `spoei_panel.csv`, fill it, and re-run the notebook. The file is git-ignored
(Bloomberg-derived history is licensed data).

| Column | Definition | Source |
|---|---|---|
| `firm_id`, `month` | issuer identifier; month `YYYY-MM`, 2016-01 to 2026-09; universe of at least 40 palm-exposed issuers | - |
| `X1_hhi` | Herfindahl index of the issuer's supplier cost shares | Bloomberg SPLC |
| `X2_env_gap`, `X2_env_gap_chg12` | 10 minus the BESG environmental pillar; its 12-month change | Bloomberg ESG |
| `X3_news_z`, `X3_news_vol` | z-score (trailing 90 days) and volatility of news sentiment | Bloomberg CN |
| `X4_cpo_var_x_exposure` | variance of palm oil (CPO) returns x the issuer's palm exposure | Bloomberg GP + company data |
| `X5_int_cover` | operating income / interest expense | Bloomberg FA |
| `X6_flag_share` | share of suppliers carrying Bloomberg risk flags | Bloomberg SPLC |
| `X7_eq_vol` | equity volatility | Bloomberg DES / HP |
| `Y_event_12m` | 1 if in months t+1..t+12 there is (a) an RSPO complaint or membership sanction against the firm or a named subsidiary, (b) a new Bloomberg ESG controversy flag, or (c) a CN headline on deforestation / RSPO / EUDR / NDPE with coded severity >= 3. Source (a) is external to Bloomberg so the target is independent of the features. | RSPO complaints record; ESG; CN |

**Sample size:** about 85 labelled firm-periods with at least 17 events (and at least 40 firms for out-of-firm generalisation) are
needed to show an AUC of 0.70 against chance at 80% power (Hanley-McNeil approximation; `figures/f16_power.png`).
