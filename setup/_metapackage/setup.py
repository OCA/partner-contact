import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-base_location',
        'odoo12-addon-base_location_geonames_import',
        'odoo12-addon-base_partner_sequence',
        'odoo12-addon-partner_address_street3',
        'odoo12-addon-partner_affiliate',
        'odoo12-addon-partner_disable_gravatar',
        'odoo12-addon-partner_external_map',
        'odoo12-addon-partner_fax',
        'odoo12-addon-partner_firstname',
        'odoo12-addon-partner_identification',
        'odoo12-addon-partner_multi_relation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
