# © initOS GmbH 2017
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "CRM Partner Automatic Merge",
    "version": "12.0.1.0.0",
    "depends": ['crm', 'contacts'
                ],
    'author': "Nitrokey GmbH, Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'website': "https://github.com/OCA/crm_deduplicate_contact",
    'data': [
        'views/base_partner_merge_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
