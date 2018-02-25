"""
magnolia is a simple package for analyzing the contribution of
magnetic fields to the physics within the cores of galaxy cluster mergers
"""

__version__ = "1.0"

import sys
import os
sys.path.append(os.path.dirname(__file__))

import derived_field_definitions

from dataset_read_write_functions import *
