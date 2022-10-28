import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_location>=16.0dev,<16.1dev',
        'odoo-addon-base_location_geonames_import>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_birthdate>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_gender>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_job_position>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_lang>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_personal_information_page>=16.0dev,<16.1dev',
        'odoo-addon-partner_disable_gravatar>=16.0dev,<16.1dev',
        'odoo-addon-partner_firstname>=16.0dev,<16.1dev',
        'odoo-addon-partner_vat_unique>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
