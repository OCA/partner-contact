# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Personal information page for contacts",
    "summary": "Add a page to contacts form to put personal information",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/partner-contact",
    "author": "Nicolas JEUDY,Odoo Community Association (OCA)",
    "contributors": [
        'EL Hadji DEM <elhadji.dem@savoirfairelinux.com>',
        'Jairo Llopis <j.llopis@grupoesoc.es>',
        'Matjaž Mozetič <m.mozetic@matmoz.si>',
        'Rudolf Schnapka <schnapkar@golive-saar.de>',
        'Richard deMeester <richard@willowit.com.au>',
        'Nicolas JEUDY <https://github.com/njeudy>',
    ],
    "license": "AGPL-3",
    'application': False,
    'installable': True,
    'auto_install': False,
    "depends": [
        "base"
    ],
    "data": [
        "views/res_partner.xml",
    ],
}
