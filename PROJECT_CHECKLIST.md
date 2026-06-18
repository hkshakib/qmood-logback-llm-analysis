# Project Checklist

| Requirement | Status | Notes |
| --- | --- | --- |
| Create project folder structure | Done | Completed on Day 1. |
| Clone Logback repository | Done | Stored in `versions/logback`. |
| Select 10 Logback versions | Done | Selected `v_1.5.25` to `v_1.5.34`. |
| Choose source folders for metrics | Done | Using only `logback-core` and `logback-classic` main Java code. |
| Prepare version checkout script | Done | `scripts/checkout_logback_version.py` |
| Prepare single-version CK script | Done | `scripts/run_ck_single_version.py` |
| Prepare CK Tool jar | Done | Local jar is expected at `tools/ck.jar`. |
| Validate CK extraction for `v_1.5.25` | Done | Raw CK CSV files were created. |
| Run CK extraction for all selected versions | Done | Raw CK CSV files were created for all 10 selected versions. |
| Process raw metrics | In progress | CK columns were inspected and a QMOOD-inspired mapping was drafted. |
| Calculate QMOOD scores | Not started | Planned after metric extraction. |
| Prepare LLM evaluation prompts | Not started | Not started yet. |
| Compare CK/QMOOD results with LLMs | Not started | Not started yet. |
| Create graphs | Not started | Not started yet. |
| Write report | Not started | Not started yet. |
| Create slides | Not started | Not started yet. |
