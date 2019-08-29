import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-base_country_state_translatable',
        'odoo11-addon-base_location',
        'odoo11-addon-base_location_geonames_import',
        'odoo11-addon-base_location_nuts',
        'odoo11-addon-base_partner_merge',
        'odoo11-addon-base_partner_sequence',
        'odoo11-addon-base_vat_sanitized',
        'odoo11-addon-partner_academic_title',
        'odoo11-addon-partner_address_street3',
        'odoo11-addon-partner_affiliate',
        'odoo11-addon-partner_certificate_of_conduct',
        'odoo11-addon-partner_coc',
        'odoo11-addon-partner_company_type',
        'odoo11-addon-partner_contact_birthdate',
        'odoo11-addon-partner_contact_department',
        'odoo11-addon-partner_contact_gender',
        'odoo11-addon-partner_contact_in_several_companies',
        'odoo11-addon-partner_contact_job_position',
        'odoo11-addon-partner_contact_lang',
        'odoo11-addon-partner_contact_personal_information_page',
        'odoo11-addon-partner_email_check',
        'odoo11-addon-partner_employee_quantity',
        'odoo11-addon-partner_external_map',
        'odoo11-addon-partner_fax',
        'odoo11-addon-partner_firstname',
        'odoo11-addon-partner_group',
        'odoo11-addon-partner_identification',
        'odoo11-addon-partner_industry_secondary',
        'odoo11-addon-partner_multi_relation',
        'odoo11-addon-partner_multi_relation_tabs',
        'odoo11-addon-partner_phone_extension',
        'odoo11-addon-partner_phone_search',
        'odoo11-addon-partner_phonecall_schedule',
        'odoo11-addon-partner_ref_unique',
        'odoo11-addon-partner_second_lastname',
        'odoo11-addon-partner_vat_unique',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
