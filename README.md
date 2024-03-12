# CIF Cleaner

[![codecov](https://codecov.io/gh/bobleesj/cif-cleaner/graph/badge.svg?token=3KDQ4344V5)](https://codecov.io/gh/bobleesj/cif-cleaner)

Interactive and codeless program for sorting, pre-processing, sorting CIF (Crystallographic Information File) files

## Overview

This Python toolkit provides a set of tools for processing Crystallographic Information File (CIF) files. It allows for moving files based on unsupported formats, unreasonable distances, and specific tags, copying files based on atomic occupancy and mixing, retrieving file information, and checking CIF folder content against an Excel file.

When you run `python main.py`, a prompt below will appear. 

```text
Welcome! Please choose an option to proceed:
[1] Move files based on unsupported CIF format
[2] Move files based on unreasonable distance
[3] Move files based on tags
[4] Move files based on supercell atom count
[5] Copy files based on atomic occupancy and mixing
[6] Get file info in the folder
[7] Check CIF folder content against Excel file
Enter your choice (1-7): 
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

Simply copy and paste the following block.

```bash
git clone https://github.com/bobleesj/cif-cleaner.git
cd cif-cleaner
pip install pandas click gemmi matplotlib pytest scipy sympy openpyxl
python main.py
```

The above method had no issue so far. But If you are interested in using `Conda` with a fresh new environment

```bash
git clone https://github.com/bobleesj/cif-cleaner.git
cd cif-cleaner
conda create -n cif python=3.12
conda activate cif
pip install -r requirements.txt
python main.py
```

## Tutorial

> If you are new to Conda (Python package manager), I have written a tutorial for you here [Intro to Python package manager for beginners (Ft. Conda with Cheatsheet](https://bobleesj.github.io/tutorial/2024/02/26/intro-to-python-package-manager.html).

## Test

```bash
python -m pytest           
```

README is to be updated once the code becomes more robust. If you have any further suggestions or ideas, please feel free to make an issue. If you have any questions, please feel free to send me an email at sl5400@columbia.edu

## Changelog

- 20240311 implementing Flake8 linting requirement
- 20240303 added GitHub CI integration
