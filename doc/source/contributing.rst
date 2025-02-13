.. _ref_contributing:

==========
Contribute
==========

Overall guidance on contributing to a PyAnsys library appears in the
`Contribute <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyMaterials Manager.
 
The following contribution information is specific to PyMaterials Manager.


Clone the repository and install the package
============================================

To clone the PyMaterials Manager repository and install the latest release
in development mode, run this code:

.. code:: console

    git clone https://github.com/ansys/pymaterials-manager
    cd pymaterials-manager
    pip install poetry
    poetry install


Post issues
===========

Use the `PyMaterials Manager Issues`_ page to submit questions, report bugs,
and request new features. When possible, use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

View documentation
==================

Documentation for the latest stable release of PyMaterials Manager is hosted at
`PyMaterials Manager Documentation <Pymaterials-manager_docs_>`_.

Adhere to code style
====================

PyMaterials Manager follows the PEP8 standard as outlined in the `PyAnsys Development Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit`_.

To ensure your code meets minimum code styling standards, run this code::

    pip install pre-commit
    pre-commit run --all-files

You can also install this as a pre-commit hook by running this code::

    pre-commit install

This way, it's not possible for you to push code that fails the style checks::

    $ pre-commit install
    $ git commit -am "added my cool feature"
    black....................................................................Passed
    isort....................................................................Passed
    flake8...................................................................Passed
    codespell................................................................Passed
    check for merge conflicts................................................Passed
    debug statements (python)................................................Passed
    fix requirements.txt.....................................................Passed
    Validate GitHub Workflows................................................Passed
    pydocstyle...............................................................Passed


.. LINKS AND REFERENCES
.. _pre-commit: https://pre-commit.com/
.. _pyansys_support: pyansys.support@ansys.com
.. _dev_guide_pyansys: https://dev.docs.pyansys.com/
.. _dev_guide_contributing: https://dev.docs.pyansys.com/how-to/contributing.html
.. _dev_guide_coding_style: https://dev.docs.pyansys.com/coding-style/index.html
.. _PyMaterials Manager Issues: https://github.com/ansys/pymaterials-manager/issues
.. _Pymaterials-manager_docs: https://manager.materials.docs.pyansys.com/