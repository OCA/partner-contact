import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-base_location',
        'odoo13-addon-base_location_geonames_import',
        'odoo13-addon-partner_company_group',
        'odoo13-addon-partner_company_type',
        'odoo13-addon-partner_contact_personal_information_page',
        'odoo13-addon-partner_fax',
        'odoo13-addon-partner_firstname',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
