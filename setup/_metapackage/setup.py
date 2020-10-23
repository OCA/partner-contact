import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-partner_contact_birthdate',
        'odoo14-addon-partner_contact_gender',
        'odoo14-addon-partner_contact_lang',
        'odoo14-addon-partner_contact_nationality',
        'odoo14-addon-partner_contact_personal_information_page',
        'odoo14-addon-partner_fax',
        'odoo14-addon-partner_firstname',
        'odoo14-addon-partner_second_lastname',
        'odoo14-addon-partner_vat_unique',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
