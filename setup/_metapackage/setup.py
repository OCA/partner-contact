import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-base_country_state_translatable>=16.0dev,<16.1dev',
        'odoo-addon-base_location>=16.0dev,<16.1dev',
        'odoo-addon-base_location_geonames_import>=16.0dev,<16.1dev',
        'odoo-addon-base_partner_sequence>=16.0dev,<16.1dev',
        'odoo-addon-partner_accreditation>=16.0dev,<16.1dev',
        'odoo-addon-partner_address_street3>=16.0dev,<16.1dev',
        'odoo-addon-partner_address_two_lines>=16.0dev,<16.1dev',
        'odoo-addon-partner_affiliate>=16.0dev,<16.1dev',
        'odoo-addon-partner_company_type>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_access_link>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_address_default>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_birthdate>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_gender>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_job_position>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_lang>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_nationality>=16.0dev,<16.1dev',
        'odoo-addon-partner_contact_personal_information_page>=16.0dev,<16.1dev',
        'odoo-addon-partner_disable_gravatar>=16.0dev,<16.1dev',
        'odoo-addon-partner_email_duplicate_warn>=16.0dev,<16.1dev',
        'odoo-addon-partner_external_map>=16.0dev,<16.1dev',
        'odoo-addon-partner_fax>=16.0dev,<16.1dev',
        'odoo-addon-partner_firstname>=16.0dev,<16.1dev',
        'odoo-addon-partner_identification>=16.0dev,<16.1dev',
        'odoo-addon-partner_manual_rank>=16.0dev,<16.1dev',
        'odoo-addon-partner_multi_relation>=16.0dev,<16.1dev',
        'odoo-addon-partner_second_lastname>=16.0dev,<16.1dev',
        'odoo-addon-partner_tz>=16.0dev,<16.1dev',
        'odoo-addon-partner_vat_unique>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
