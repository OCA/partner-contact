# -*- coding: utf-8 -*-
# © 2013 Nicolas Bessi (Camptocamp SA)
# © 2014 Agile Business Group (<http://www.agilebg.com>)
# © 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner first name and last name',
    'summary': "Split first name and last name for non company partners",
    'version': '10.0.2.1.4',
    'author': "Camptocamp, "
              "Grupo ESOC Ingeniería de Servicios, "
              "Tecnativa, "
              "LasLabs, "
              "ACSONE SA/NV, "
              "Odoo Community Association (OCA)",
    'license': "AGPL-3",
    'maintainer': 'Camptocamp, Acsone',
    'category': 'Extra Tools',
    'website': 'https://odoo-community.org/',
    'depends': ['base_setup'],
    'post_init_hook': 'post_init_hook',
    'data': [
        'views/base_config_view.xml',
        'views/res_partner.xml',
        'views/res_user.xml',
    ],
    'auto_install': False,
    'installable': True,
}
