"""
magnolia is a simple package for analyzing the contribution of
magnetic fields to the physics within the cores of galaxy cluster mergers
"""

__version__ = "1.0"

import sys
import os
sys.path.append(os.path.dirname(__file__))

import derived_field_definitions

from store_dataset_info import *

from retrieve_dataset_info import *

from plot_dataset_info import *
