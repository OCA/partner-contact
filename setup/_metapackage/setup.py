import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-base_country_state_translatable',
        'odoo12-addon-base_location',
        'odoo12-addon-base_location_geonames_import',
        'odoo12-addon-base_location_nuts',
        'odoo12-addon-base_partner_sequence',
        'odoo12-addon-base_vat_sanitized',
        'odoo12-addon-partner_address_street3',
        'odoo12-addon-partner_affiliate',
        'odoo12-addon-partner_bank_active',
        'odoo12-addon-partner_brand',
        'odoo12-addon-partner_capital',
        'odoo12-addon-partner_coc',
        'odoo12-addon-partner_company_group',
        'odoo12-addon-partner_company_type',
        'odoo12-addon-partner_contact_birthdate',
        'odoo12-addon-partner_contact_department',
        'odoo12-addon-partner_contact_gender',
        'odoo12-addon-partner_contact_job_position',
        'odoo12-addon-partner_contact_personal_information_page',
        'odoo12-addon-partner_deduplicate_acl',
        'odoo12-addon-partner_deduplicate_filter',
        'odoo12-addon-partner_disable_gravatar',
        'odoo12-addon-partner_employee_quantity',
        'odoo12-addon-partner_external_map',
        'odoo12-addon-partner_fax',
        'odoo12-addon-partner_firstname',
        'odoo12-addon-partner_helper',
        'odoo12-addon-partner_identification',
        'odoo12-addon-partner_industry_secondary',
        'odoo12-addon-partner_multi_relation',
        'odoo12-addon-partner_phone_extension',
        'odoo12-addon-partner_phonecall_schedule',
        'odoo12-addon-partner_priority',
        'odoo12-addon-partner_ref_unique',
        'odoo12-addon-partner_second_lastname',
        'odoo12-addon-partner_vat_unique',
        'odoo12-addon-portal_partner_select_all',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
