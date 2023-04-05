:orphan:

API reference
=============

This section provides descriptions of classes, functions, and attributes for the
PyMaterials Manager API. Use the search feature or click links to view API documentation.

.. toctree::
   :titlesonly:
   :maxdepth: 3

   {% for page in pages %}
   {% if (page.top_level_object or page.name.split('.') | length == 3) and page.display %}
   {{ page.include_path }}
   {% endif %}
   {% endfor %}