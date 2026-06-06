---
name: fda-novel-newly-approved-analysis
description: |
  Execute the clinical evidence aggregator pipeline (pipeline.py) for a target drug in the FDA-novel-newly-approved-analysis project. It automatically scrapes FDA approvals, queries ClinicalTrials.gov, retrieves PubMed publications, and outputs a unified JSON dataset.
allowed-tools: default_api:run_command, default_api:write_to_file
---

# FDA Novel Newly Approved Drug Analysis Skill

This skill allows the agent to run the unified python pipeline (`pipeline.py`) inside the `/Users/ahmadhidayat/claude-code/projects/FDA-novel-newly-approved-analysis` directory. It maps any target drug to its corresponding clinical trials and PubMed literature to assemble a consolidated JSON dataset.

## When to Use This Skill

Trigger this skill when the user requests to:
- Run the clinical trials/PubMed pipeline for a specific drug.
- Gather clinical trial data and peer-reviewed literature for an active ingredient.
- Aggregate new FDA approvals and scientific evidence together.
- Trigger phrases include: *"run the pipeline for [drug]"*, *"execute pipeline.py for [drug]"*, *"collect clinical and pubmed data for [drug]"*, or *"run the drug evidence aggregator"*.

## Pipeline Execution Workflow

### Step 1: Parse the Target Drug
Identify the brand name or active ingredient of the drug requested by the user (e.g. `bulevirtide`, `ensitrelvir`, or `suzetrigine`).

### Step 2: Locate the Project Directory
Navigate to the project root directory:
```
/Users/ahmadhidayat/claude-code/projects/FDA-novel-newly-approved-analysis
```

### Step 3: Run the Pipeline Script
Execute the script using the `uv` tool manager to run in the virtual environment.

```bash
uv run pipeline.py --drug "<drug_name>"
```

#### Optional CLI Arguments
*   `--year <YYYY>`: Scrape FDA approvals for a specific year (default is `2026`).
*   `--output_dir <path>`: Force output destination (defaults to the relative `./data` directory).

### Step 4: Verify the JSON Output Dataset
Ensure that the pipeline completed successfully and wrote the compiled dataset to the relative data folder:
```
/Users/ahmadhidayat/claude-code/projects/FDA-novel-newly-approved-analysis/data/<generic_name>-pipeline-data.json
```

### Step 5: Report Results
Summarize the findings for the user:
*   **Approval details** (Brand, active ingredient, date, sponsor, indication).
*   **Number of clinical trials mapped** from ClinicalTrials.gov.
*   **Number of peer-reviewed articles fetched** from PubMed.
*   Provide a clickable link to the generated JSON data file.
