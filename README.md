# dicom-protocol-organizer
A high-speed Python script designed to automatically categorize large-scale neuroimaging DICOM files based on their MRI protocols (`SeriesDescription`). 

## Introduction
Legacy MATLAB-based processing pipelines often induce severe I/O bottlenecks when handling large cohort datasets because they load the entire image volume into memory. This project resolves that inefficiency by leveraging `pydicom` to selectively parse only the metadata (Header) while excluding the pixel data. It is optimized to perform batch processing across multiple subject directories rather than a single subject, resulting in exponentially faster classification of tens of thousands of DICOM files.

## Key Features
- **High Performance (I/O Optimization):** Utilizes the `stop_before_pixels=True` parameter to bypass heavy image decoding, reading only the header to maximize processing speed.
- **Batch Processing:** Automatically iterates through all subject folders within a designated root directory to execute hierarchical foldering.
- **Robust Path Handling:** Implements regex-based sanitization to remove special characters that are invalid for directory names, ensuring safe path generation.
- **Progress Tracking:** Integrates the `tqdm` library for intuitive real-time monitoring of progress and error logging per subject.

## Prerequisites
This script requires Python 3.7 or higher. For reproducibility and to avoid dependency conflicts, it is highly recommended to run this script within a Python virtual environment.

```bash
# Create and activate a virtual environment (Optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Install required packages
pip install pydicom tqdm
```

## Usage

### 1. Configuration
Open `organize_dicoms_by_protocol.py` (or copy the source code below) and navigate to the bottom of the script. Update the `source_directory` variable with the absolute path to the root folder containing your subject data.

```python
if __name__ == "__main__":
    # Replace this string with the absolute path to your clinical dataset
    source_directory = r'/absolute/path/to/your/dataset' 
    organize_dicoms_by_protocol(source_directory)
```

### 2. Execution
Run the script from your terminal. The `tqdm` progress bar will display the sorting status for each subject in real-time.

```bash
python organize_dicoms_by_protocol.py
```

## Directory Structure
This script acts on a root directory that contains individual subject folders. It scans each subject folder and reorganizes the unsorted DICOM (`*.IMA`) files into distinct sub-directories named after their respective MRI protocol.

**Before Execution (Raw Data)**
```text
/path/to/your/dataset/
├── SUBJ_001/                  
│   ├── 0001.IMA               
│   ├── 0002.IMA
│   └── ...
└── SUBJ_002/
    ├── 0001.IMA
    └── ...
```

**After Execution (Organized Data)**
```text
/path/to/your/dataset/
├── SUBJ_001/
│   ├── T1_MPRAGE_SAG/         
│   │   ├── 0001.IMA
│   │   └── ...
│   └── DTI_64DIR_b1000/       
│       ├── 0050.IMA
│       └── ...
└── SUBJ_002/
    ├── T1_MPRAGE_SAG/
    └── ...
```

## ⚠️ Data Integrity Warning
By default, this script uses `shutil.move` to physically relocate files, which is efficient for managing local disk space. However, to prevent any potential data loss during unexpected interruptions, **backing up your raw data** before execution is strongly recommended. For pipelines where strict preservation of the original data is mandatory, modify the script to use `shutil.copy` instead of `shutil.move`.
