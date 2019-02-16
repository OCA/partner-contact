# © 2014-2016 Camptocamp SA
# @author: Nicolas Bessi
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Street3 in addresses',
    'summary': 'Add a third address line on partners',
    'license': 'AGPL-3',
    'version': '12.0.1.0.0',
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'maintainer': 'Camptocamp',
    'category': 'Sales',
    'depends': ['base'],
    'website': 'https://github.com/OCA/partner-contact',
    'data': ['view/partner_view.xml'],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
}
