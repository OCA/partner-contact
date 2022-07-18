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
        'odoo-addon-base_partner_company_group>=15.0dev,<15.1dev',
        'odoo-addon-base_partner_sequence>=15.0dev,<15.1dev',
        'odoo-addon-partner_affiliate>=15.0dev,<15.1dev',
        'odoo-addon-partner_contact_access_link>=15.0dev,<15.1dev',
        'odoo-addon-partner_contact_age_range>=15.0dev,<15.1dev',
        'odoo-addon-partner_contact_birthdate>=15.0dev,<15.1dev',
        'odoo-addon-partner_contact_job_position>=15.0dev,<15.1dev',
        'odoo-addon-partner_contact_personal_information_page>=15.0dev,<15.1dev',
        'odoo-addon-partner_deduplicate_acl>=15.0dev,<15.1dev',
        'odoo-addon-partner_deduplicate_by_ref>=15.0dev,<15.1dev',
        'odoo-addon-partner_employee_quantity>=15.0dev,<15.1dev',
        'odoo-addon-partner_external_map>=15.0dev,<15.1dev',
        'odoo-addon-partner_fax>=15.0dev,<15.1dev',
        'odoo-addon-partner_firstname>=15.0dev,<15.1dev',
        'odoo-addon-partner_industry_secondary>=15.0dev,<15.1dev',
        'odoo-addon-partner_manual_rank>=15.0dev,<15.1dev',
        'odoo-addon-partner_multi_relation>=15.0dev,<15.1dev',
        'odoo-addon-partner_phone_secondary>=15.0dev,<15.1dev',
        'odoo-addon-partner_phonecall_schedule>=15.0dev,<15.1dev',
        'odoo-addon-partner_priority>=15.0dev,<15.1dev',
        'odoo-addon-partner_ref_unique>=15.0dev,<15.1dev',
        'odoo-addon-partner_second_lastname>=15.0dev,<15.1dev',
        'odoo-addon-partner_vat_unique>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
