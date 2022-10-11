import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-partner_contact_personal_information_page>=16.0dev,<16.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 16.0',
    ]
)
