# CIF File Processing Toolkit

## Overview
This Python toolkit provides a set of tools for processing Crystallographic Information File (CIF) files. It allows for moving files based on unsupported formats, unreasonable distances, and specific tags, copying files based on atomic occupancy and mixing, retrieving file information, and checking CIF folder content against an Excel file.

When you run `python main.py`, a prompt below will appear. 
```
Welcome! Please choose an option to proceed:
[1] Move files based on unsupported CIF format
[2] Move files based on unreasonable distance
[3] Move files based on tags
[4] Copy files based on atomic occupancy and mixing
[5] Get file info in the folder
[6] Check CIF folder content against Excel file
Enter your choice (1-6): 
```

No need to import packages or *write a line of code*. One can simply drag and drop CIF files to have all the features below.

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

## Test

```
python -m pytest           
```

README is to be updated once the code becomes more robust. If you have any further suggestions or ideas, please feel free to make an issue.