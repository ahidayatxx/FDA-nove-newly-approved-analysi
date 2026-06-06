#!/usr/bin/env python3
"""
FDA Approval & Clinical Evidence Aggregator Pipeline
===================================================
A reusable pipeline script that fetches FDA CDER approvals, maps a selected molecule
to its clinical trials, retrieves related PubMed scientific evidence, and outputs
a unified JSON dataset for regulatory report generation.

Author: Antigravity AI, Clinical & Regulatory Intelligence Unit
Date: June 5, 2026
"""

import os
import sys
import json
import argparse
import subprocess
import urllib.request
import ssl
import re
from datetime import datetime

# Setup directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data")
CLINICAL_TRIALS_API_PATH = os.path.join(SCRIPT_DIR, "scripts", "clinical_trials_api.py")
PUBMED_API_PATH = os.path.join(SCRIPT_DIR, "scripts", "pubmed_api.py")

# Pre-compiled database of H1 2026 innovative approvals as a robust fallback
H1_2026_FALLBACK_DB = [
    {
        "approval_date": "2026-01-14",
        "brand_name": "Zycubo",
        "generic_name": "copper histidinate",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Menkes disease",
        "sponsor": "Cyprium Therapeutics"
    },
    {
        "approval_date": "2026-02-12",
        "brand_name": "Adquey",
        "generic_name": "difamilast",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Mild to moderate atopic dermatitis",
        "sponsor": "Otsuka Pharmaceutical"
    },
    {
        "approval_date": "2026-02-20",
        "brand_name": "Bysanti",
        "generic_name": "milsaperidone",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Schizophrenia & bipolar I disorder",
        "sponsor": "Bausch Health"
    },
    {
        "approval_date": "2026-02-23",
        "brand_name": "Loargys",
        "generic_name": "pegzilarginase",
        "regulation_center": "CDER",
        "drug_type": "BLA",
        "indication": "Arginase 1 Deficiency",
        "sponsor": "Immedica"
    },
    {
        "approval_date": "2026-02-27",
        "brand_name": "Yuviwel",
        "generic_name": "navepegritide",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Achondroplasia in pediatric patients",
        "sponsor": "Ascendis Pharma"
    },
    {
        "approval_date": "2026-03-17",
        "brand_name": "Lynavoy",
        "generic_name": "linerixibat",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Cholestatic pruritus in Primary Biliary Cholangitis",
        "sponsor": "GlaxoSmithKline"
    },
    {
        "approval_date": "2026-03-17",
        "brand_name": "Icotyde",
        "generic_name": "icotrokinra",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Moderate-to-severe plaque psoriasis",
        "sponsor": "Johnson & Johnson"
    },
    {
        "approval_date": "2026-03-24",
        "brand_name": "Avlayah",
        "generic_name": "tividenofusp alfa",
        "regulation_center": "CDER",
        "drug_type": "BLA",
        "indication": "Hunter syndrome (Mucopolysaccharidosis Type II)",
        "sponsor": "Denali Therapeutics"
    },
    {
        "approval_date": "2026-03-25",
        "brand_name": "Lifyorli",
        "generic_name": "relacorilant",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Platinum-resistant epithelial ovarian/peritoneal cancer",
        "sponsor": "Corcept Therapeutics"
    },
    {
        "approval_date": "2026-04-01",
        "brand_name": "Foundayo",
        "generic_name": "orforglipron",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Chronic weight management in adults with obesity",
        "sponsor": "Eli Lilly"
    },
    {
        "approval_date": "2026-04-20",
        "brand_name": "Idvynso",
        "generic_name": "doravirine/islatravir",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "HIV-1 infection in suppressed adults",
        "sponsor": "Merck & Co."
    },
    {
        "approval_date": "2026-05-01",
        "brand_name": "Veppanu",
        "generic_name": "vepdegestrant",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "ER+/HER2- ESR1-mutated breast cancer",
        "sponsor": "Pfizer"
    },
    {
        "approval_date": "2026-05-13",
        "brand_name": "Beqalzi",
        "generic_name": "sonrotoclax",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Relapsed or refractory mantle cell lymphoma",
        "sponsor": "BeiGene"
    },
    {
        "approval_date": "2026-05-15",
        "brand_name": "Baxfendy",
        "generic_name": "baxdrostat",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Treatment of hypertension",
        "sponsor": "AstraZeneca"
    },
    {
        "approval_date": "2026-05-22",
        "brand_name": "Hepcludex",
        "generic_name": "bulevirtide",
        "regulation_center": "CDER",
        "drug_type": "BLA",
        "indication": "Chronic hepatitis delta virus (HDV) infection",
        "sponsor": "Gilead Sciences"
    },
    {
        "approval_date": "2026-05-27",
        "brand_name": "Decnupaz",
        "generic_name": "pivekimab sunirine",
        "regulation_center": "CDER",
        "drug_type": "BLA",
        "indication": "Blastic plasmacytoid dendritic cell neoplasm",
        "sponsor": "AbbVie"
    },
    {
        "approval_date": "2026-05-29",
        "brand_name": "Zaynich",
        "generic_name": "cefepime/zidebactam",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Complicated urinary tract infections (cUTIs)",
        "sponsor": "Wockhardt"
    },
    {
        "approval_date": "2026-05-29",
        "brand_name": "Cypsedo",
        "generic_name": "cipepofol",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "General anesthesia in adults",
        "sponsor": "SciClone"
    },
    {
        "approval_date": "2026-06-01",
        "brand_name": "Xocova",
        "generic_name": "ensitrelvir",
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": "Post-exposure prophylaxis of COVID-19",
        "sponsor": "Shionogi"
    }
]

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch FDA novel approvals, clinical trials, and PubMed evidence for a molecule.")
    parser.add_argument("--drug", type=str, help="Specific brand name or active ingredient to target.")
    parser.add_argument("--year", type=int, default=2026, help="Calendar year for FDA approvals list (default: 2026).")
    parser.add_argument("--output_dir", type=str, default=DEFAULT_OUTPUT_DIR, help=f"Directory to save JSON output (default: {DEFAULT_OUTPUT_DIR}).")
    return parser.parse_args()

def scrape_fda_approvals(year):
    """
    Attempts to fetch and parse CDER novel approvals for a given year.
    Falls back to pre-compiled H1 2026 list or local cache if FDA page is unavailable (404/SSL error).
    """
    print(f"[*] Attempting to fetch FDA novel drug approvals for {year}...")
    url = f"https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-{year}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context, timeout=15) as response:
            html = response.read().decode("utf-8")
        
        print(f"[+] Successfully fetched FDA page. Parsing table...")
        tables = re.findall(r'<table[^>]*>.*?</table>', html, re.DOTALL)
        if not tables:
            print("[-] No table found in HTML. Falling back to local database.")
            return H1_2026_FALLBACK_DB if year == 2026 else []
        
        # Simple regex-based HTML table parser
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tables[0], re.DOTALL)
        approvals = []
        for row in rows[1:]:  # skip header row
            cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cols) >= 3:
                # Clean HTML tags and whitespace
                clean_cols = [re.sub(r'<[^>]*>', '', c).strip() for c in cols]
                
                # Column 1 usually contains "Brand (generic)" or "Brand / generic"
                drug_text = clean_cols[0]
                brand_name = drug_text
                generic_name = drug_text.lower()
                
                match = re.search(r'([^(]+)\(([^)]+)\)', drug_text)
                if match:
                    brand_name = match.group(1).strip()
                    generic_name = match.group(2).strip().lower()
                
                indication = clean_cols[1]
                approval_date_str = clean_cols[2]
                
                # Convert date if possible
                try:
                    approval_date = datetime.strptime(approval_date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
                except ValueError:
                    approval_date = approval_date_str
                
                approvals.append({
                    "approval_date": approval_date,
                    "brand_name": brand_name,
                    "generic_name": generic_name,
                    "regulation_center": "CDER",
                    "drug_type": "NME",
                    "indication": indication,
                    "sponsor": "Unknown"
                })
        
        print(f"[+] Scraped {len(approvals)} approvals from FDA website.")
        return approvals
    except Exception as e:
        print(f"[!] Warning: Failed to fetch FDA website ({e}).")
        print("[*] Falling back to pre-compiled H1 2026 innovative approvals list...")
        return H1_2026_FALLBACK_DB if year == 2026 else []

def find_target_drug(approvals_list, search_name):
    """
    Search for a drug in the list. Prompts user for details if not found.
    """
    if not search_name:
        # Pick the most recent approved drug
        sorted_approvals = sorted(approvals_list, key=lambda x: x["approval_date"], reverse=True)
        if sorted_approvals:
            print(f"[+] No drug specified. Selecting the most recent approval: {sorted_approvals[0]['brand_name']} ({sorted_approvals[0]['generic_name']})")
            return sorted_approvals[0]
        else:
            print("[-] No approvals found in list.")
            sys.exit(1)
            
    search_lower = search_name.lower().strip()
    for drug in approvals_list:
        if search_lower in drug["brand_name"].lower() or search_lower in drug["generic_name"].lower():
            print(f"[+] Found matching drug in approvals list: {drug['brand_name']} ({drug['generic_name']})")
            return drug
            
    # Fallback: drug not in scraped list, prompt or manually construct
    print(f"[!] Target drug '{search_name}' not found in approvals database.")
    print("[*] Proceeding with manual metadata definition...")
    
    # Generate generic active ingredient name from input
    generic_input = input(f"Enter active ingredient (generic name) for '{search_name}' [default: {search_name}]: ").strip()
    generic_name = generic_input.lower() if generic_input else search_name.lower()
    
    brand_input = input(f"Enter brand name for '{search_name}' [default: {search_name}]: ").strip()
    brand_name = brand_input if brand_input else search_name
    
    app_date = input("Enter approval date (YYYY-MM-DD) [default: 2026-06-01]: ").strip()
    approval_date = app_date if app_date else "2026-06-01"
    
    indication = input("Enter approved indication: ").strip()
    sponsor = input("Enter developer/sponsor: ").strip()
    
    return {
        "approval_date": approval_date,
        "brand_name": brand_name,
        "generic_name": generic_name,
        "regulation_center": "CDER",
        "drug_type": "NME",
        "indication": indication,
        "sponsor": sponsor
    }

def run_clinical_trials_search(generic_name, output_dir):
    """
    Invokes the clinical-trials-database skill wrapper via subprocess.
    """
    print(f"[*] Querying ClinicalTrials.gov for '{generic_name}'...")
    os.makedirs(output_dir, exist_ok=True)
    temp_output_path = os.path.join(output_dir, "temp_trials.json")
    
    skill_dir = os.path.dirname(os.path.dirname(CLINICAL_TRIALS_API_PATH))
    # Build CLI command
    cmd = [
        "uv", "run", "--no-cache",
        "scripts/clinical_trials_api.py", "search",
        "--intervention", generic_name,
        "--fields", "NCTId,BriefTitle,OverallStatus,Phase,BriefSummary,ArmsInterventionsModule,EligibilityModule",
        "--limit", "10",
        "--output", temp_output_path
    ]
    
    try:
        # Run command
        print(f"Running command: {' '.join(cmd)} (in {skill_dir})")
        result = subprocess.run(cmd, cwd=skill_dir, capture_output=True, text=True, check=True)
        
        # Load output
        if os.path.exists(temp_output_path):
            with open(temp_output_path, "r") as f:
                data = json.load(f)
            os.remove(temp_output_path) # clean up
            studies = data.get("studies", [])
            print(f"[+] Mapped {len(studies)} clinical trials.")
            return studies
        else:
            print("[-] Error: Clinical trials output file not created.")
            return []
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running clinical trials CLI: {e.stderr}")
        return []
    except Exception as e:
        print(f"[!] Unexpected error during clinical trials fetch: {e}")
        return []

def run_pubmed_search(generic_name, output_dir):
    """
    Invokes the pubmed-database skill wrapper via subprocess (search + fetch).
    """
    print(f"[*] Querying PubMed for scientific evidence matching '{generic_name}'...")
    os.makedirs(output_dir, exist_ok=True)
    temp_search_path = os.path.join(output_dir, "temp_pubmed_search.json")
    temp_abstracts_path = os.path.join(output_dir, "temp_pubmed_abstracts.json")
    
    skill_dir = os.path.dirname(os.path.dirname(PUBMED_API_PATH))
    # Step 1: Search PubMed
    cmd_search = [
        "uv", "run", "--no-cache",
        "scripts/pubmed_api.py", temp_search_path,
        "search_pubmed", generic_name,
        "--max_results", "15"
    ]
    
    try:
        print(f"Running command: {' '.join(cmd_search)} (in {skill_dir})")
        subprocess.run(cmd_search, cwd=skill_dir, capture_output=True, text=True, check=True)
        
        if not os.path.exists(temp_search_path):
            print("[-] PubMed search failed to generate results file.")
            return []
            
        with open(temp_search_path, "r") as f:
            pmids = json.load(f)
        os.remove(temp_search_path) # clean up
        
        if not pmids:
            print("[-] No PubMed articles found for query.")
            return []
            
        print(f"[+] Found {len(pmids)} PubMed articles. Fetching abstracts...")
        pmids_str = ",".join([str(p) for p in pmids])
        
        # Step 2: Fetch Abstracts
        cmd_fetch = [
            "uv", "run", "--no-cache",
            "scripts/pubmed_api.py", temp_abstracts_path,
            "fetch_article_abstracts", pmids_str
        ]
        
        print(f"Running command: {' '.join(cmd_fetch)} (in {skill_dir})")
        subprocess.run(cmd_fetch, cwd=skill_dir, capture_output=True, text=True, check=True)
        
        if os.path.exists(temp_abstracts_path):
            with open(temp_abstracts_path, "r") as f:
                articles = json.load(f)
            os.remove(temp_abstracts_path) # clean up
            
            # Slim down abstracts to conserve context window
            slim_articles = []
            for art in articles:
                if not art or not isinstance(art, dict):
                    continue
                slim_articles.append({
                    "pmid": art.get("pmid"),
                    "title": art.get("title"),
                    "authors": art.get("authors", []),
                    "journal": art.get("journal"),
                    "pubdate": art.get("pubdate"),
                    "doi": art.get("doi"),
                    "abstract": (art.get("abstract") or "")[:1200]  # truncate very long abstracts
                })
            
            print(f"[+] Fetched {len(slim_articles)} abstracts.")
            return slim_articles
        else:
            print("[-] PubMed abstracts fetch failed to create file.")
            return []
            
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running PubMed CLI: {e.stderr}")
        return []
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[!] Unexpected error during PubMed evidence fetch: {e}")
        return []

def main():
    args = parse_args()
    
    # 1. Scrape approvals
    approvals = scrape_fda_approvals(args.year)
    
    # 2. Find target drug
    target_drug = find_target_drug(approvals, args.drug)
    generic_name = target_drug["generic_name"]
    brand_name = target_drug["brand_name"]
    
    print("\n" + "="*50)
    print(f"Selected Drug: {brand_name} ({generic_name})")
    print(f"Approval Date: {target_drug['approval_date']}")
    print(f"Indication:    {target_drug['indication']}")
    print(f"Sponsor:       {target_drug['sponsor']}")
    print("="*50 + "\n")
    
    # 3. Query Clinical Trials
    trials = run_clinical_trials_search(generic_name, args.output_dir)
    
    # 4. Query PubMed
    publications = run_pubmed_search(generic_name, args.output_dir)
    
    # 5. Output unified dataset
    pipeline_data = {
        "metadata": {
            "generic_name": generic_name,
            "brand_name": brand_name,
            "approval_date": target_drug["approval_date"],
            "regulation_center": target_drug["regulation_center"],
            "drug_type": target_drug["drug_type"],
            "indication": target_drug["indication"],
            "sponsor": target_drug["sponsor"],
            "pipeline_date": datetime.now().strftime("%Y-%m-%d")
        },
        "clinical_trials": trials,
        "pubmed_publications": publications
    }
    
    os.makedirs(args.output_dir, exist_ok=True)
    # Generic format matching: generic-pipeline-data.json
    output_filename = f"{generic_name.replace('/', '_')}-pipeline-data.json"
    output_path = os.path.join(args.output_dir, output_filename)
    
    with open(output_path, "w") as f:
        json.dump(pipeline_data, f, indent=2)
        
    print(f"\n[+] PIPELINE SUCCESS: Structured dataset written to {output_path}")
    print("[*] Next Step: Antigravity AI will read this JSON file to synthesize a comprehensive")
    print("    APA 7th-style international regulatory review report for other national authorities.")

if __name__ == "__main__":
    main()
