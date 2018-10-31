# SDI
# © 2018 David Juaneda <djuaneda@sdi.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "SDi-CRM: nav to contacts",
    'version': '11.0.1.0.1',
    'category': '',
    'author': 'David Juaneda',
    'summary': """  
        Add navigation from customers to your contacts.""",
    'license': 'AGPL-3',
    'depends': [
        'contacts',
    ],
    'data': [
        'views/inherit_res_partner_views.xml',
    ],
    'installable':True,
}
