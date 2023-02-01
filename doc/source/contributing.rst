.. _ref_contributing:

============
Contributing
============

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Coding style <dev_guide_coding_style_>`_ before attempting to
contribute to Pymaterials-manager.
 
The following contribution information is specific to Pymaterials-manager.


Cloning the pymaterials-manager repository
==========================================

Run this code to clone and install the latest version of Pymaterials-manager in development mode:

.. code:: console

    git clone https://github.com/pyansys/pymaterials-manager
    cd pymaterials-manager
    pip install poetry
    poetry install


Posting issues
==============

Use the `Pymaterials-manager Issues <Pymaterials-manager_issues_>`_
page to submit questions, report bugs, and request new features. When possible,
use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `pyansys.support@ansys.com <pyansys_support_>`_.

Viewing pymaterials-manager documentation
==========================================

Documentation for the latest stable release of Pymaterials-manager is hosted at
`Pymaterials-manager Documentation <Pymaterials-manager_docs_>`_.

Code style
==========

Pymaterials-manager follows PEP8 standard as outlined in the `PyAnsys Development Guide
<dev_guide_pyansys_>`_ and implements style checking using
`pre-commit <precommit_>`_.

To ensure your code meets minimum code styling standards, run::

    pip install pre-commit
    pre-commit run --all-files

You can also install this as a pre-commit hook by running::

    pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

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
.. _dev_guide_contributing: https://dev.docs.pyansys.com/dev/how-to/contributing.html
.. _dev_guide_coding_style: https://dev.docs.pyansys.com/dev/coding-style/index.html
.. _Pymaterials-manager_issues: https://github.com/pyansys/pymaterials-manager/issues
.. _Pymaterials-manager_docs: https://manager.materials.docs.pyansys.com/