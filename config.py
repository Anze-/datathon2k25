""" This script contains the project configuration. """

import os

# PATHS
PROJECT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(PROJECT_FOLDER_PATH, 'data')


# ONTOLOGY
ONTOLOGY_FILE = os.path.join(DATASET_PATH, 'SupplyChain.rdf')
