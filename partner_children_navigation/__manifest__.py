# SDI
# © 2018 David Juaneda <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Navigate to a partner's contacts",
    'version': '11.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Partners',
    'website': 'https://github.com/OCA/social',
    'author': 'SDi, David Juaneda, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/inherit_res_partner_views.xml',
    ],
    'installable': True,
}
