{
    'name': 'Partner CoC',
    'summary': "Adds a field 'Chamber Of Commerce Registration Number' to "
               "partner",
    'version': '10.0.1.0.0',
    'category': 'Web',
    'author': 'Onestein,Odoo Community Association (OCA)',
    'website': 'http://www.onestein.eu',
    'license': 'AGPL-3',
    'depends': [
        'partner_identification',
    ],
    'data': [
        'data/res_partner_id_category_data.xml',
        'views/res_partner_view.xml'
    ],
    'installable': True,
    'application': False,
}
