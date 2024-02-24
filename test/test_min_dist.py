import os
import glob
import pytest
import filter.min_distance as min_distance


# For testing, I have a flag called "isInteractiveMode" it is set to False. The default
def test_files_removed():
    # script_directory /Users/imac/Documents/GitHub/cif-filter-copy
    error_dir = "test/bad_cif_files/min_dist"
    min_distance.move_files_based_on_min_dist(error_dir, isInteractiveMode=False)

