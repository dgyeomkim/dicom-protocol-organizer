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
This script requires Python 3.7 or higher. You can install the required dependencies using the following command:

```bash
pip install pydicom tqdm
