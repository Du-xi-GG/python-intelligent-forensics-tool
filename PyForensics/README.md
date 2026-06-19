# Intelligent Digital Forensics Tool

## Overview

A Python-based digital forensics tool for analyzing files within a selected directory. The application extracts file metadata, calculates SHA-256 hashes, performs entropy analysis, and uses machine learning to identify potentially suspicious files.

## Features

* Recursive directory scanning
* SHA-256 hash generation
* File entropy calculation
* File metadata extraction
* Suspicious file detection using Isolation Forest
* CSV report generation
* PDF report generation

## Technologies

* Python
* Pandas
* NumPy
* Scikit-Learn
* ReportLab

## How It Works

The application scans all files inside a selected directory and collects:

* File name
* File path
* File extension
* File size
* Last modification time
* SHA-256 hash
* Entropy value

After collecting the data, an Isolation Forest machine learning model analyzes the files and labels unusual files as suspicious.

## Machine Learning

The project uses the Isolation Forest algorithm for anomaly detection.

Features used by the model:

* File size
* File entropy
* File extension
* Modification timestamp

Files that significantly differ from the majority are marked as suspicious.

## Reports

The application can generate:

* CSV forensic reports
* PDF forensic reports

Reports contain information about analyzed files, entropy values, file sizes, and anomaly detection results.

## Example Workflow

1. Enter a directory path.
2. Scan files and extract metadata.
3. Calculate SHA-256 hashes.
4. Calculate file entropy.
5. Run anomaly detection.
6. Review suspicious files.
7. Export results as CSV or PDF.

## Author

Dušan Milošević

