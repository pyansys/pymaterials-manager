PyMaterials Manager
===================
|pyansys| |python| |pypi| |GH-CI| |codecov| |MIT| |black|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/badge/Python-%3E%3D3.10-blue
   :target: https://pypi.org/project/pymaterials-manager/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-materials-manager.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-materials-manager
   :alt: PyPI

.. |codecov| image:: https://codecov.io/gh/pyansys/pymaterials-manager/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/pyansys/pymaterials-manager
   :alt: Codecov

.. |GH-CI| image:: https://github.com/pyansys/pymaterials-manager/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/pyansys/pymaterials-manager/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat
   :target: https://github.com/psf/black
   :alt: Black


PyMaterials Manager is a Python package for unifying material management across the Ansys portfolio.


Installation
------------

Two installation modes are provided: user and developer.

Install in user mode
^^^^^^^^^^^^^^^^^^^^

Before installing the ``ansys-materials-manager`` package, run this command to
ensure that you have the latest version of `pip`_:

.. code:: bash

    python -m pip install -U pip

Then, install the latest package for use with this command:

.. code:: bash

    poetry run python -m pip install ansys-materials-manager
    
Install in development mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing the ``ansys-materials-manager`` package in developer mode allows
you to modify the source and enhance it.

Before contributing to PyMaterials Manager, see the `PyAnsys Developer's Guide`_.

To install PyMaterials Manager in developer mode, perform these steps:

#. Cloning the repository:

    .. code:: bash

        git clone https://github.com/pyansys/pymaterials-manager

#. Create a fresh-clean Python environment and activate it:

    .. code:: bash

        # Create a virtual environment
        python -m venv .venv

        # Activate it in a POSIX system
        source .venv/bin/activate

        # Activate it in Windows CMD environment
        .venv\Scripts\activate.bat

        # Activate it in Windows Powershell
        .venv\Scripts\Activate.ps1

#. Make sure that you have the latest required build system and doc, testing,
   and CI tools:

    .. code:: bash

        python -m pip install -U pip poetry tox
        python -m pip install -r requirements/requirements_build.txt
        python -m pip install -r requirements/requirements_doc.txt
        python -m pip install -r requirements/requirements_tests.txt


#. Install the project in editable mode:

    .. code:: bash
    
        poetry run python -m pip install ansys-materials-manager
        
#. Verify your development installation:

    .. code:: bash
        
        tox

Testing
-------

This project takes advantage of `tox`_. This tool is used to automate common
development tasks (similar to Makefile), but it is oriented towards Python
development. 

Use ``tox``
^^^^^^^^^^^

`tox`_ uses environments, which are similar to ``Makefile`` rules, to make it highly
customizable. In fact, this tool creates its own virtual environment so that anything
being tested is isolated from the project to guarantee the project's integrity.

Descriptions follow of some of the most widely used environments:

- **tox -e style**: Checks the code style of your project.
- **tox -e py**: Runs your test suite.
- **tox -e py-coverage**: Checks unit tests and code coverage.
- **tox -e doc**: Builds the documentation of your project.


Perform raw testing
^^^^^^^^^^^^^^^^^^^

If required, you can call style commands (such as `black`_, `isort`_,
and `flake8`_) or unit testing commands (such as `pytest`_) from the command
line. However, calling these commands does not guarantee that your project
is being tested in an isolated environment, which is the reason why tools
like `tox`_ exist.


Use pre-commit
^^^^^^^^^^^^^^

The style checks take advantage of `pre-commit`_. Developers are not forced but
encouraged to install this tool by running this command:

.. code:: bash

    python -m pip install pre-commit && pre-commit install

Every time you stage some changes and try to commit them,
``pre-commit`` only allows them to be committed if all defined hooks succeed.

Documentation and issues
------------------------

For comprehensive information on PyMaterials Manager, see the latest release `documentation`_.
On the `PyMaterials Manager Issues`_ page, you can create issues to submit questions,
report bugs, and request new features. This is the best place to post questions and code.

Distribution
------------

If you want to create either source or wheel files, start by installing
the building requirements and then executing the build module:

.. code:: bash

    python -m pip install -r requirements/requirements_build.txt
    python -m build
    python -m twine check dist/*


.. LINKS AND REFERENCES
.. _black: https://github.com/psf/black
.. _flake8: https://flake8.pycqa.org/en/latest/
.. _isort: https://github.com/PyCQA/isort
.. _pip: https://pypi.org/project/pip/
.. _pre-commit: https://pre-commit.com/
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _tox: https://tox.wiki/
.. _PyMaterials Manager Issues: https://github.com/pyansys/pymaterials-manager/issues
.. _documentation: https://manager.materials.docs.pyansys.com/
