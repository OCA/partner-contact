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
        'odoo13-addon-base_partner_sequence',
        'odoo13-addon-base_vat_sanitized',
        'odoo13-addon-partner_affiliate',
        'odoo13-addon-partner_bank_active',
        'odoo13-addon-partner_coc',
        'odoo13-addon-partner_company_group',
        'odoo13-addon-partner_company_type',
        'odoo13-addon-partner_contact_gender',
        'odoo13-addon-partner_contact_personal_information_page',
        'odoo13-addon-partner_deduplicate_acl',
        'odoo13-addon-partner_deduplicate_by_website',
        'odoo13-addon-partner_fax',
        'odoo13-addon-partner_firstname',
        'odoo13-addon-partner_identification',
        'odoo13-addon-partner_phone_extension',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
