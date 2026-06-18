# QMOOD-Based Software Quality Evolution Analysis of Logback with LLM-Supported Evaluation

Selected repository: Logback  
Repository link: https://github.com/qos-ch/logback
Project GitHub repository: https://github.com/hkshakib/qmood-logback-llm-analysis

Purpose: This project studies how Logback quality changes across versions using QMOOD-related object-oriented metrics. The calculated results are also compared with manual evaluations from 3 LLMs.

## Repository Overview

Selected software: Logback

Analyzed modules:
- `logback-core`
- `logback-classic`

Analyzed versions:
- `v_1.5.25` to `v_1.5.34`

Tools used:
- CK Tool
- Python

Main output folders:
- `data/raw_metrics/` - raw CK Tool CSV files
- `data/processed/` - combined metrics, QMOOD-inspired scores, and LLM comparison files
- `graphs/` - generated quality and metric trend graphs
- `prompts/` - LLM prompt and metric input files
- `data/llm_outputs/` - manual ChatGPT, Gemini, and DeepSeek responses
- `report/` - technical report draft

Useful scripts:
- `python scripts/list_logback_tags.py`
- `python scripts/checkout_logback_version.py v_1.5.25`
- `python scripts/run_ck_single_version.py v_1.5.25`
- `python scripts/run_ck_all_versions.py`
- `python scripts/inspect_ck_columns.py`
- `python scripts/calculate_qmood.py`
- `python scripts/generate_graphs.py`

Notes:
- `tools/ck.jar` is needed to run CK extraction locally.
- `tools/ck.jar` is ignored by Git and is not committed.
- The report uses a QMOOD-inspired approximation, not the complete original QMOOD model.
- Presentation slides are a separate task and are not included yet.

## Work Log

Day 1 status:
- Project folders were created.
- Logback was cloned into `versions/logback`.
- Git tags were checked.
- 10 recent stable `1.5.x` versions were selected.
- No metrics were calculated today.

Selected versions:
- v_1.5.25
- v_1.5.26
- v_1.5.27
- v_1.5.28
- v_1.5.29
- v_1.5.30
- v_1.5.31
- v_1.5.32
- v_1.5.33
- v_1.5.34

Day 2 status:
- Selected source folders:
  - `versions/logback/logback-core/src/main/java`
  - `versions/logback/logback-classic/src/main/java`
- Excluded folders: tests, examples, target folders, generated files, documentation, and logback-access.
- CK Tool is expected at `tools/ck.jar`.
- Test version: `v_1.5.25`.
- Checkout worked.
- CK test did not run because `tools/ck.jar` was missing at that time.

Day 3 status:
- CK Tool was prepared as `tools/ck.jar`.
- Java was installed so CK could run.
- CK extraction was tested only for `v_1.5.25`.
- Raw CK output was saved in `data/raw_metrics/v_1.5.25/`.
- No QMOOD calculation, graphs, LLM prompts, report, or slides were created.

Day 4 status:
- CK extraction was completed for all 10 selected versions.
- Raw metric files are saved in `data/raw_metrics/<version>/`.
- Extraction log is saved at `data/raw_metrics/extraction_log.csv`.
- QMOOD calculation had not started yet.
- Graph generation had not started yet.
- LLM evaluation had not started yet.

Day 5.1 status:
- CK class CSV columns were inspected for all 10 versions.
- Column report was saved in `data/processed/ck_column_report.csv`.
- A simple QMOOD-inspired mapping was saved in `data/processed/qmood_metric_mapping.csv`.
- Final QMOOD scores had not been calculated yet.

Day 5.2 status:
- Combined version-level metrics were created in `data/processed/logback_combined_metrics.csv`.
- QMOOD-inspired quality scores were created in `data/processed/logback_qmood_scores.csv`.
- All 10 selected versions were processed.
- Raw CK files were not modified.
- Graphs, LLM evaluation, report, and slides had not started yet.

Day 6.1 status:
- Simple graphs were created in `graphs/`.
- Manual LLM prompt files were prepared in `prompts/`.
- Empty response files were created in `data/llm_outputs/`.
- LLM responses had not been collected yet.
- LLM comparison had not been done yet.

Day 6.2 status:
- Manual responses from ChatGPT, Gemini, and DeepSeek were collected.
- LLM comparison CSV was created in `data/processed/llm_comparison.csv`.
- LLM comparison summary was created in `data/processed/llm_comparison_summary.md`.
- Report and slides were still not final.

Day 7.1 status:
- A complete technical report draft was created in `report/final_report_draft.md`.
- The report uses the existing metrics, graphs, prompt, and LLM comparison files.
- Slides are not finalized yet.
- The project is nearly ready for final packaging.

Day 7.2 status:
- Repository materials were finalized.
- The report draft was reviewed for grammar, clarity, formatting, and simple academic wording.
- README was updated as a clear project overview.
- Presentation slides remain a separate task.
