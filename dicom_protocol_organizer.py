import os
import re
import shutil
from pathlib import Path
import pydicom
from tqdm import tqdm

def organize_dicoms_by_protocol(base_dir: str):
    """
    Iterates through all subject folders within the specified root directory and
    categorizes DICOM (*.IMA) files in each folder into subfolders based on their MRI protocol (SeriesDescription).
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
        # 2. Search for .IMA files within the subject folder (use rglob('*.IMA') to search subdirectories as well)
        #dicom_files = list(subject_dir.glob('*.IMA'))
        dicom_files = [f for f in subject_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.ima', '.dcm']]
        
        if not dicom_files:
            print(f"Skipping folder [{subject_dir.name}]: No *.IMA files found.")
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
                
                # Create target directory if it doesn't exist (exist_ok=True prevents duplicate creation errors)
                target_dir.mkdir(parents=True, exist_ok=True)
                
                target_file = target_dir / dicom_file.name
                
                # 5. Move the file
                shutil.move(str(dicom_file), str(target_file))
                
            except Exception as e:
                print(f"\nFailed to process file: {dicom_file.name} | Error: {e}")

    print("\nProtocol-based foldering completed for all subjects.")

# Execution Example
if __name__ == "__main__":
    # Specify the path to the root data directory (which contains all subject folders)
    # Example: Assume folders like SUBJ_001, SUBJ_002 are located inside /path/to/your/dataset
    source_directory = r'/path/to/your/dataset'  # REPLACE WITH YOUR ACTUAL PATH BEFORE RUNNING LOCALLY
    organize_dicoms_by_protocol(source_directory)
