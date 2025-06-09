#!/usr/bin/env python3
"""
NASA Document Downloader

This module downloads official NASA documents from public sources for use in the
NASA Document Q&A System. It retrieves PDF documents including technical handbooks,
mission press kits, and other official NASA publications.

The downloaded documents are stored in the ./data directory and serve as the
source material for the document ingestion pipeline (ingest.py).

Dependencies:
    - requests: For HTTP downloads
    - os: For directory creation

Usage:
    python fetch_nasa_data.py

    Or via Makefile:
    make fetch-data

Documents Downloaded:
    - NASA Systems Engineering Handbook (technical reference)
    - Artemis I Press Kit (mission documentation)
    - CLPS Press Kit (commercial lunar payload services)

Author: NASA Q&A System
License: MIT
"""
from typing import Dict
import os
import requests

# =============================================================================
# NASA DOCUMENT SOURCES
# =============================================================================
# Official NASA PDF documents with their download URLs
# These are publicly available documents from nasa.gov

URLS: Dict[str, str] = {
    "nasa_se_handbook.pdf": (
        "https://www.nasa.gov/wp-content/uploads/2018/09/"
        "nasa_systems_engineering_handbook_0.pdf"
    ),
    "artemis_i_press_kit.pdf": (
        "https://www.nasa.gov/wp-content/uploads/static/artemis-i-press-kit/"
        "img/Artemis%20I_Press%20Kit.pdf"
    ),
    "clps_press_kit.pdf": (
        "https://www.nasa.gov/wp-content/uploads/2024/01/"
        "np-2023-12-016-jsc-clps-im-press-kit-web-508.pdf"
    ),
}

def download_nasa_documents() -> None:
    """
    Download NASA documents from official sources.
    
    This function:
    1. Creates the data directory if it doesn't exist
    2. Downloads each PDF from the official NASA URLs
    3. Saves files locally with descriptive names
    4. Provides progress feedback during download
    
    Raises:
        requests.RequestException: If download fails
        OSError: If file system operations fail
    """
    # Create data directory for storing PDF files
    os.makedirs("data", exist_ok=True)
    print(f"📁 Created/verified data directory: ./data") 
    # Download each NASA document
    print(f"📥 Downloading {len(URLS)} NASA documents...")
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
    
    print("\n🎉 All NASA documents downloaded successfully!")
    print("📂 Files available in: ./data")

if __name__ == "__main__":
    # Main execution when script is run directly
    # Downloads all configured NASA documents to the data directory
    download_nasa_documents()