dj5-starter
===========

|pre-commit.ci status| |Code style: black| |Imports: isort|

A starter project for Django 5 with allauth (formerly
`starter-fullstack <https://github.com/andywar65/starter-fullstack>`__)

Stack
-----

-  Postgres
-  Python 3.13.1
-  Django 5.2
-  Bootstrap 5
-  HTMX
-  (check requirements.txt for actual installs)

Features
--------

-  Authentication with allauth and socialaccount (Google)
-  Environs for storing secrets
-  User model with profile extension
-  Model translation ready
-  Django Filer ready
-  FlatPages with tinymce editor (start url with "/en/" if language is
   english, "/it/" if it's italian)
-  Interactive search bar with Hyperscript
-  Styled with Bootstrap 5
-  Some interaction with HTMX, avoiding full page reload
-  Incorporating Neapolitan with HTMX behaviour (use project.HxCRUDView)

Tests
-----

Unittests, coverage 98%

Working on:
-----------

-  Hyperscript for local interactions

.. |pre-commit.ci status| image:: https://results.pre-commit.ci/badge/github/andywar65/dj5-starter/main.svg
   :target: https://results.pre-commit.ci/latest/github/andywar65/dj5-starter/main
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |Imports: isort| image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
   :target: https://pycqa.github.io/isort/
