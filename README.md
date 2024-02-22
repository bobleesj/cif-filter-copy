# CIF File Processing Toolkit

## Overview
This Python toolkit provides a set of tools for processing Crystallographic Information File (CIF) files. It allows for moving files based on unsupported formats, unreasonable distances, and specific tags, copying files based on atomic occupancy and mixing, retrieving file information, and checking CIF folder content against an Excel file.

## Features
- **Move Unsupported CIF Files:** Relocate CIF files that do not comply with the expected format.
- **Move CIF Files Based on Distance:** Relocate CIF files containing unreasonable distances between atoms.
- **Move CIF Files Based on Tags:** Relocate CIF files based on specific tags.
- **Copy Files Based on Atomic Occupancy and Mixing:** Copy CIF files that meet criteria for atomic occupancy and atomic mixing.
- **Get File Info:** Retrieve information from CIF files within a folder.
- **Excel Integration:** Check CIF folder content against an Excel file for missing entries.

## Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/bobleesj/cif-filter-copy.git
cd cif-filter-copy
python main.py
```
