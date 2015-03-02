{
    'name': 'Base Partner Merge',
    'author': "OpenERP S.A.,Odoo Community Association (OCA)",
    'category': 'Generic Modules/Base',
    'version': '0.1',
    'description': """
backport module, to be removed when we switch to saas2 on the private servers
""",
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'base_partner_merge_view.xml',
    ],
    'installable': True,
}
