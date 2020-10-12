import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-partner-contact",
    description="Meta package for oca-partner-contact Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-partner_firstname',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
