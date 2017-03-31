# -*- coding: utf-8 -*-
# © 2014 Sébastien BEAU <sebastien.beau@akretion.com>
# © 2017 Angel Moya <angel.moya@pesol.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Partner Helper',
    'version': '8.0.0.1.0',
    'author': "Akretion,Odoo Community Association (OCA)",
    'maintainer': 'Akretion',
    'category': 'Warehouse',
    'depends': [
        'base',
    ],
    'description': """
Partner Helper
==============
The purpose of this module is to gather generic partner methods.
It avoids to grow up excessively the number of modules in Odoo
for small features.

Description
-----------
Add specific helper methods to deal with partners:

* _get_split_address():
    This method allows to get a number of street fields according to
    your choice. 2 fields by default in Odoo with 128 width chars.
    In some countries you have constraints on width of street fields and you
    should use 3 or 4 shorter fields.
    You also need of this feature to avoid headache with overflow printing task

* other_method():

Contributors
------------
* Sébastien BEAU <sebastien.beau@akretion.com>
* David BEAL <david.beal@akretion.com>


    """,
    'website': 'http://www.akretion.com/',
    'data': [],
    'tests': [],
    'installable': False,
    'auto_install': False,
    'license': 'AGPL-3',
    'application': False,
}
