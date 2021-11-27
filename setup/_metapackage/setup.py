import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-animal>=15.0dev,<15.1dev',
        'odoo-addon-base_country_state_translatable>=15.0dev,<15.1dev',
        'odoo-addon-base_location>=15.0dev,<15.1dev',
        'odoo-addon-base_location_geonames_import>=15.0dev,<15.1dev',
        'odoo-addon-partner_fax>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
