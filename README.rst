.. image:: https://travis-ci.org/tivaliy/validocx.svg?branch=master
    :target: https://travis-ci.org/tivaliy/validocx

.. image:: https://codecov.io/gh/tivaliy/validocx/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/tivaliy/validocx

ValiDocX
========

Docx file validator based on `python-docx <https://python-docx.readthedocs.io/en/latest/>`_

QuickStart
__________

1. Clone `validocx`:

``git clone https://github.com/tivaliy/validocx.git``

2. Create isolated Python environment ``virtualenv venv`` and activate it ``source venv/bin/activte``
3. Install ``validocx`` with all necessary dependencies:

``pip install -r requirements.txt .``

4. Specify file with requirements in YAML or JSON format

.. code-block:: yaml

   ---
   styles:
     heading1:
       font:
         unit: pt
         attributes:
           - 12.0
           - cs_bold
           - Times New Roman
         paragraph:
           unit: cm
           attributes:
           alignment: 0
   sections:
     - unit: cm
       attributes:
         right_margin: 4.4
         start_type: 2
         top_margin: 5.2
         footer_distance: 4.1
         header_distance: 0.0
         left_margin: 4.4
         bottom_margin: 5.2
         orientation: 0
         page_height: 29.7
         page_width: 21.0

5. Run validation from CLI:

``usage: validocx [-h] -r REQUIREMENTS [--log-file LOG_FILE] [-q | -v] docx-file``

positional arguments:
 docx-file             Docx file to be validated.

optional arguments:
 -h, --help            show this help message and exit
 -r REQUIREMENTS, --requirements REQUIREMENTS
                       File with the requirements. In YAML or JSON format.
 --log-file LOG_FILE   Log file to store logs.
 -q, --quiet           Decrease output verbosity.
 -v, --verbose         Increase output verbosity.
