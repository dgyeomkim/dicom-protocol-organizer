import os
import re
import shutil
import argparse
from pathlib import Path
import pydicom
from tqdm import tqdm

def organize_dicoms_by_protocol(base_dir: str):
    """
    Iterates through all subject folders within the specified root directory and
    categorizes DICOM (*.IMA, *.dcm) files in each folder into subfolders based on their MRI protocol (SeriesDescription).
    """
    base_path = Path(base_dir)
    
    if not base_path.exists() or not base_path.is_dir():
        raise FileNotFoundError(f"The specified base directory could not be found: {base_dir}")

    # 1. Search for all subject directories within the root folder
    subject_dirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    if not subject_dirs:
        print(f"Warning: No subject folders found to process in '{base_dir}'.")
        return

    print(f"Found a total of {len(subject_dirs)} subject folders. Starting processing...\n")

    for subject_dir in subject_dirs:
        # 2. Search for DICOM files (.IMA, .dcm) within the subject folder (case-insensitive)
        dicom_files = [f for f in subject_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.ima', '.dcm']]
        
        if not dicom_files:
            print(f"Skipping folder [{subject_dir.name}]: No *.IMA or *.dcm files found.")
            continue

        # Progress bar using tqdm
        for dicom_file in tqdm(dicom_files, desc=f"Sorting [{subject_dir.name}]"):
            try:
                # 3. Optimization: Read only the header (metadata) excluding pixel data to maximize I/O speed
                ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)
                
                # Extract protocol name
                protocol_name = getattr(ds, 'SeriesDescription', 'Unknown_Protocol')
                
                # 4. Remove whitespaces and special characters that are invalid for directory names
                protocol_name = re.sub(r'[\\/*?:"<>|]', '_', str(protocol_name)).strip()
                
                target_dir = subject_dir / protocol_name
                
                # Create target directory if it doesn't exist
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_file = target_dir / dicom_file.name
                
                # 5. Move the file
                shutil.move(str(dicom_file), str(target_file))
                
            except Exception as e:
                print(f"\nFailed to process file: {dicom_file.name} | Error: {e}")

    print("\nProtocol-based foldering completed for all subjects.")

if __name__ == "__main__":
    # Setup command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Fast DICOM Protocol Organizer: Sorts DICOM files (*.IMA, *.dcm) into subfolders by MRI protocol."
    )
    
    parser.add_argument(
        "source_directory",
        type=str,
        help="The absolute path to the root dataset directory containing subject folders."
    )
    
    args = parser.parse_args()
    
    # Execute the function with the provided CLI argument
    organize_dicoms_by_protocol(args.source_directory)
