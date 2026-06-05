# FDA Novel Newly Approved Drug Analysis Project

This project compiles the tools, scripts, raw data, and finalized regulatory reports focused on the U.S. FDA's novel drug and biologic approvals during the first half of 2026. The key showcase analysis features **Bulevirtide (Hepcludex)**, mapping it from initial FDA approval to clinical trial evidence and PubMed scientific literature to compile a robust review dossier for international regulatory authorities.

---

## 📁 Project Directory Structure

```
FDA-nove-newly-approved-analysis/
├── README.md                                    # This project overview
├── FDA_Approved_Innovative_Drugs_H1_2026_Report.md # Chronological list and deep dives of H1 2026 approvals
├── pipeline.py                                  # Automated drug aggregator pipeline script
├── data/                                        # Subfolder containing raw JSON data
│   ├── bulevirtide-pipeline-data.json           # Consolidated pipeline data for Bulevirtide
│   └── test_bulevirtide_trials.json             # Cached trials query data
├── scripts/                                     # Subfolder containing scratch & helper scripts
│   ├── generate_report.py                       # Code to generate the FDA approvals list report
│   └── format_apa.py                            # Reference compiler and formatter
└── example/                                     # Subfolder containing example reports
    ├── Ensitrelvir_International_Regulatory_Review_Report.md # Report for Ensitrelvir (COVID-19 PEP)
    └── bulevirtide-2026-05-22X2026-06-05.md     # Report for Bulevirtide (Hepatitis Delta)
```

---

## 📄 Core Project Assets

### 1. Reports
*   **[FDA_Approved_Innovative_Drugs_H1_2026_Report.md](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/FDA_Approved_Innovative_Drugs_H1_2026_Report.md)**: A chronological analysis of the first semester of 2026 novel approvals, highlighting advanced gene therapies (Otarmeni, Kresladi), weight management (Foundayo), post-exposure COVID-19 prophylaxis (Xocova), and chronic hepatitis delta (Hepcludex).
*   **[example/Ensitrelvir_International_Regulatory_Review_Report.md](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/example/Ensitrelvir_International_Regulatory_Review_Report.md)**: A template-driven regulatory review report for Ensitrelvir (Xocova) as post-exposure prophylaxis for COVID-19.
*   **[example/bulevirtide-2026-05-22X2026-06-05.md](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/example/bulevirtide-2026-05-22X2026-06-05.md)**: A template-driven, APA 7th-styled regulatory review report built for non-US international health authorities considering bulevirtide marketing authorization.

### 2. Core Code & Scripts
*   **[pipeline.py](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/pipeline.py)**: The main pipeline script. It performs web scraping of the FDA CDER portal, parses details of a selected drug, calls ClinicalTrials.gov and PubMed CLI wrappers via subprocesses, and aggregates the results.
*   **[scripts/generate_report.py](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/scripts/generate_report.py)**: Helper script used to compile the raw HTML table scraped from the FDA into the structured Markdown table in the main report.
*   **[scripts/format_apa.py](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/scripts/format_apa.py)**: Utility to parse, filter, and format clinical trials and literature metadata into APA 7th Edition style citations.

### 3. Data Directory
*   **[data/bulevirtide-pipeline-data.json](file:///Users/ahmadhidayat/claude-code/projects/FDA-nove-newly-approved-analysis/data/bulevirtide-pipeline-data.json)**: The final compiled database output representing the combined information for bulevirtide from the FDA, ClinicalTrials.gov, and PubMed.

---

## 🚀 How to Run the Pipeline

To execute the data gathering pipeline for a newly approved drug:

```bash
uv run pipeline.py --drug "<drug_name>"
```

### Script Flags
*   `--drug`: Name of the brand or active ingredient to target (e.g., `Hepcludex` or `bulevirtide`).
*   `--year`: The calendar year for the scraper (default: `2026`).
*   `--output_dir`: Target folder for the data file. By default, the script output will save directly to your workspace `claude-code/output/` directory, which you can then copy to the `./data` folder here.
