# © 2018 Apruzzese Francesco <f.apruzzese@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner fax',
    'category': 'Extra Tools',
    'summary': 'Add fax number on partner',
    'version': '11.0.1.1.0',
    'license': 'AGPL-3',
    'author': 'Francesco Apruzzese, '
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'depends': [
        'base_setup'
        ],
    'data': [
        'views/res_partner.xml',
        ],
    'installable': True,
}
