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
| Process raw metrics | Done | Version-level combined metrics were created. |
| Calculate QMOOD scores | Done | QMOOD-inspired scores were calculated for all 10 selected versions. |
| Prepare LLM evaluation prompts | Done | Manual prompt and metric input files were created. |
| Compare CK/QMOOD results with LLMs | Done | Manual responses were collected and compared. |
| Create graphs | Done | Simple QMOOD and metric trend graphs were created. |
| Write report | In progress | A full draft report was created, but it still needs final review. |
| Create slides | Not started | Not started yet. |
