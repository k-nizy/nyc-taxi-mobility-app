"""
Script to download NYC Taxi data from official source.
Downloads a sample month of data for testing.
"""

import requests
import os
from pathlib import Path

def download_taxi_data(year=2023, month=1):
    """
    Download NYC Yellow Taxi trip data.
    
    Args:
        year: Year of data (default 2023)
        month: Month of data (default 1)
    """
    # Create data directory
    data_dir = Path(__file__).parent.parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    # Construct URL
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:02d}.parquet"
    output_file = data_dir / f"yellow_tripdata_{year}-{month:02d}.parquet"
    
    print(f"Downloading NYC Taxi data for {year}-{month:02d}...")
    print(f"URL: {url}")
    print(f"Output: {output_file}")
    
    # Check if file already exists
    if output_file.exists():
        print(f"File already exists: {output_file}")
        response = input("Redownload? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return str(output_file)
    
    try:
        # Download with progress
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress indicator
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f} MB)", end='')
        
        print(f"\n✓ Download complete: {output_file}")
        print(f"File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")
        return str(output_file)
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Download failed: {e}")
        return None


def download_sample_data():
    """Download a smaller sample for testing."""
    print("For full dataset, this will download ~40-50 MB")
    print("This contains approximately 3 million trip records.")
    
    proceed = input("\nProceed with download? (y/n): ")
    if proceed.lower() == 'y':
        return download_taxi_data(2023, 1)
    else:
        print("Download cancelled.")
        print("\nAlternative: You can manually download from:")
        print("https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page")
        return None


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 2:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        download_taxi_data(year, month)
    else:
        print("NYC Taxi Data Downloader")
        print("=" * 50)
        download_sample_data()
