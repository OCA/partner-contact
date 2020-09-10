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
        'odoo13-addon-base_location_nuts',
        'odoo13-addon-base_partner_sequence',
        'odoo13-addon-base_vat_sanitized',
        'odoo13-addon-partner_affiliate',
        'odoo13-addon-partner_bank_active',
        'odoo13-addon-partner_coc',
        'odoo13-addon-partner_company_group',
        'odoo13-addon-partner_company_type',
        'odoo13-addon-partner_contact_access_link',
        'odoo13-addon-partner_contact_age_range',
        'odoo13-addon-partner_contact_birthdate',
        'odoo13-addon-partner_contact_department',
        'odoo13-addon-partner_contact_gender',
        'odoo13-addon-partner_contact_job_position',
        'odoo13-addon-partner_contact_lang',
        'odoo13-addon-partner_contact_personal_information_page',
        'odoo13-addon-partner_deduplicate_acl',
        'odoo13-addon-partner_deduplicate_by_ref',
        'odoo13-addon-partner_deduplicate_by_website',
        'odoo13-addon-partner_disable_gravatar',
        'odoo13-addon-partner_employee_quantity',
        'odoo13-addon-partner_fax',
        'odoo13-addon-partner_firstname',
        'odoo13-addon-partner_identification',
        'odoo13-addon-partner_industry_secondary',
        'odoo13-addon-partner_label',
        'odoo13-addon-partner_multi_relation',
        'odoo13-addon-partner_phone_extension',
        'odoo13-addon-partner_phonecall_schedule',
        'odoo13-addon-partner_priority',
        'odoo13-addon-partner_ref_unique',
        'odoo13-addon-partner_vat_unique',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
