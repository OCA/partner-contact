{
    "name": "Partner Delivery Link",
    "version": "15.0.1.0.0",
    "category": "Tools",
    "author": "ERP Harbor Consulting Services,"
    "Odoo Community Association (OCA),"
    "Nitrokey GmbH",
    "website": "https://github.com/OCA/partner-contact",
    "license": "AGPL-3",
    "summary": """
    Partner Delivery Link
    This module adds a smart button in Partner form to open and redirect to the Delivery
    Orders of the related partner. If the partner do not have any delivery order then it will
    by default "0" Will show delivery order.
     """,
    "depends": ["stock"],
    "data": [
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
