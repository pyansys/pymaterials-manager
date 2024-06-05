"""Sphinx documentation configuration file."""
from datetime import datetime
import os

from ansys_sphinx_theme import ansys_favicon, get_version_match, pyansys_logo_black

from ansys.materials.manager import __version__

cname = os.getenv("DOCUMENTATION_CNAME", default="https://manager.materials.docs.pyansys.com/")

# Project information
project = "ansys-materials-manager"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__

# Select desired logo, theme, and declare the html title
html_logo = pyansys_logo_black
html_favicon = ansys_favicon
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = "pymaterials-manager"

# specify the location of your github repo
html_theme_options = {
    "github_url": "https://github.com/ansys/pymaterials-manager",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "additional_breadcrumbs": [
        ("PyAnsys", "https://docs.pyansys.com/"),
    ],
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "autoapi.extension",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/dev", None),
    # kept here as an example
    # "numpy": ("https://numpy.org/devdocs", None),
    # "matplotlib": ("https://matplotlib.org/stable", None),
    # "pyvista": ("https://docs.pyvista.org/", None),
    # "grpc": ("https://grpc.github.io/grpc/python/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}


# static path
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"


# The suffix(es) of source filenames.
source_suffix = {
    ".rst": "restructuredtext",
    ".mystnb": "jupyter_notebook",
    ".md": "markdown",
}

# Configuration for Sphinx autoapi
autoapi_type = "python"
autoapi_dirs = ["../../src/ansys"]
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_template_dir = "_autoapi_templates"
suppress_warnings = ["autoapi"]
exclude_patterns = ["_autoapi_templates/index.rst"]
autoapi_python_use_implicit_namespaces = True
autoapi_python_class_content = "both"
