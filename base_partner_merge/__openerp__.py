{
    'name': 'Base Partner Merge',
    'author': "OpenERP S.A.,Odoo Community Association (OCA)",
    'category': 'Generic Modules/Base',
    'version': '8.0.0.1.0',
    'description': """
backport module, to be removed when we switch to saas2 on the private servers
""",
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'base_partner_merge_view.xml',
    ],
    'installable': True,
}
