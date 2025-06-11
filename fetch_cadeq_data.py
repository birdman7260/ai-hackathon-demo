"""
CA DEQ Document Downloader

This module downloads official California Department of Environmental Quality (CA DEQ, CalEPA) documents from public sources for use in the
CA DEQ Document Q&A System. It retrieves PDF studies and reports from CalEPA and related agencies.

The downloaded documents are stored in the ./data directory and serve as the
source material for the document ingestion pipeline (ingest.py).

Dependencies:
    - requests: For HTTP downloads
    - os: For directory creation

Usage:
    python fetch_cadeq_data.py

    Or via Makefile:
    make fetch-data

Documents Downloaded:
    - 10 CA DEQ/CalEPA studies and reports (see URLS below)

Author: CA DEQ Q&A System
License: MIT
"""
from typing import Dict
import os
import requests

# =============================================================================
# CA DEQ DOCUMENT SOURCES
# =============================================================================
# Official CA DEQ/CalEPA PDF documents with their download URLs

URLS: Dict[str, str] = {
    "2014_arb_pm_report.pdf": "https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/reports/l3007.pdf",
    "indicators_climate_change_2013.pdf": "https://ww2.arb.ca.gov/sites/default/files/classic/cc/inventory/pubs/reports/indicators/indicators-2013.pdf",
    "california_water_action_plan.pdf": "https://resources.ca.gov/CNRALegacyFiles/docs/california_water_action_plan/Final_California_Water_Action_Plan.pdf",
    "2019_caleap_enforcement_report.pdf": "https://calepa.ca.gov/wp-content/uploads/sites/6/2020/09/Enforcement-Report-2019.pdf",
    "ej_program_update_2016.pdf": "https://calepa.ca.gov/wp-content/uploads/sites/6/2016/06/EnvJustice-Documents-EJ-Update-2016.pdf",
    "refinery_safety_final_report_2014.pdf": "https://calepa.ca.gov/wp-content/uploads/sites/6/2016/10/Refinery-Task-Force-Final-Report.pdf",
    "calenviroscreen2_report.pdf": "https://oehha.ca.gov/media/downloads/ej/report/ces20report.pdf",
    "2013_arb_pm_report.pdf": "https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/reports/l3006.pdf",
    "leaf_blowers_legislature_report.pdf": "https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/reports/l828.pdf",
    "source_apportionment_final_report.pdf": "https://ww2.arb.ca.gov/sites/default/files/classic/research/apr/past/01-306.pdf"
}

def download_cadeq_documents() -> None:
    """
    Download CA DEQ documents from official sources.
    
    This function:
    1. Creates the data directory if it doesn't exist
    2. Downloads each PDF from the official CA DEQ URLs
    3. Saves files locally with descriptive names
    4. Provides progress feedback during download
    
    Raises:
        requests.RequestException: If download fails
        OSError: If file system operations fail
    """
    # Create data directory for storing PDF files
    os.makedirs("data", exist_ok=True)
    print(f"📁 Created/verified data directory: ./data") 
    # Download each CA DEQ document
    print(f"📥 Downloading {len(URLS)} CA DEQ documents...")
    for filename, url in URLS.items():
        try:
            print(f"   ↓ {filename}")

            # Download with timeout to prevent hanging
            response = requests.get(url, timeout=90)
            response.raise_for_status()  # Raise exception for bad status codes

            # Save file to data directory
            filepath = f"data/{filename}"
            with open(filepath, "wb") as f:
                f.write(response.content)
                
            # Show file size for verification
            file_size = len(response.content) / (1024 * 1024)  # Convert to MB
            print(f"     ✅ {file_size:.1f} MB downloaded")
            
        except requests.RequestException as e:
            print(f"     ❌ Failed to download {filename}: {e}")
            raise
        except OSError as e:
            print(f"     ❌ Failed to save {filename}: {e}")
            raise
    
    print("\n🎉 All CA DEQ documents downloaded successfully!")
    print("📂 Files available in: ./data")

if __name__ == "__main__":
    # Main execution when script is run directly
    # Downloads all configured CA DEQ documents to the data directory
    download_cadeq_documents() 