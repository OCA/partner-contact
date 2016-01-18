# -*- coding: utf-8 -*-
# © 2014 Agile Business Group (<http://www.agilebg.com>)
# © 2015 Grupo ESOC <www.grupoesoc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner first name and last name',
    'summary': "Split first name and last name for non company partners",
    'version': '9.0.1.0.0',
    'author': "Camptocamp, Odoo Community Association (OCA)",
    'license': "AGPL-3",
    'category': 'Extra Tools',
    'website': 'http://www.camptocamp.com, http://www.acsone.eu',
    'depends': ['base'],
    'data': [
        'views/res_partner.xml',
        'views/res_user.xml',
        'data/res_partner.yml',
    ],
    'auto_install': False,
    'installable': True,
}
