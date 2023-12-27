This module assigns default company to res.parnter.

Background
~~~~~~~~~~

Up to 12.0, Odoo used to assign a company by default when partner was added,
however the default company proposal has been removed since 13.0 with multi-company refactoring.
This causes inconveniences to users who want to seggregate partner records between companies.

ref. https://github.com/odoo/odoo/commit/25714692b23624d04a43862db26ebcf802b89399
