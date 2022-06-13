{
    'name': 'OSI Address Validation',
    'category': 'Sales',
    'version': '13.02.03.2022',
    'summary': """""",
    'description': """""",
    'depends': ['contacts'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/osi_address_validation.xml',
        'views/res_partner.xml',
	'views/config.xml',
    ],
    'author': 'Open Source Integrators, Odoo Community Association (OCA)',
    'images': [''],
    'maintainer': ['ckolobow'],
    'website': 'www.opensourceintegrators.com',
    'live_test_url': '',
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',

}
# 13.02.03.2022
# fix state code issue
