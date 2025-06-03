# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os, sys
PROJECT_FOLDER = "tkinter_tools"
PATH = os.path.abspath(os.path.join("ENTER_DIRECTORY", PROJECT_FOLDER))

def add_files(topDir):
    for lDirPaths, lDirNames, lFileNames in os.walk(topDir):
        for dirName in lDirNames:
            if dirName not in ["__pycache__"]:
                sys.path.insert(0, os.path.join(topDir, dirName))
                add_files(os.path.join(topDir, dirName))
        for fileName in lFileNames:
            if fileName.endswith(".py") and fileName not in ["__init__.py"]:
                sys.path.insert(0, os.path.join(topDir, fileName))
                
add_files(os.path.join(PATH, PROJECT_FOLDER))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'tkinter tools'
copyright = '2023, Arjan lemmens'
author = 'Arjan lemmens'
release = '1.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
