# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerProperty(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.companies = cls.env["res.partner"].create(
            [
                {"name": "Company A", "vat": "ESA58818501"},
                {"name": "Company B", "vat": "ESB99286320"},
            ]
        )
        cls.individuals = cls.env["res.partner"].create(
            [
                {
                    "name": f"Individual {company.name}",
                    "parent_id": company.id,
                }
                for company in cls.companies
            ]
        )
        container = cls.companies[:1].properties_base_definition_id
        container.properties_definition = [
            {"name": "scope_global", "string": "Global", "type": "char"},
            {
                "name": "scope_company",
                "string": "Company",
                "type": "char",
                "partner_scope": "companies",
            },
            {
                "name": "scope_individual",
                "string": "Individual",
                "type": "char",
                "partner_scope": "individuals",
            },
        ]

    def test_property_visibility(self):
        for partner in self.companies | self.individuals:
            with self.subTest(partner=partner.name):
                expected = {
                    "scope_global": True,
                    "scope_company": partner in self.companies,
                    "scope_individual": partner in self.individuals,
                }
                self.browser_js(
                    f"/odoo/contacts/{partner.id}",
                    "const expected = "
                    + json.dumps(expected)
                    + ";\n"
                    + """
                    for (const [name, visible] of Object.entries(expected)) {
                        const element = document.querySelector(
                            `.o_form_view .o_property_field[property-name="${name}"]`
                        );
                        const displayed = Boolean(element?.getClientRects().length);
                        if (displayed !== visible) {
                            throw new Error(
                                `${name}: expected visible=${visible}, got ${displayed}`
                            );
                        }
                    }
                    console.log("test successful");
                    """,
                    ready=(
                        "Boolean(document.querySelector("
                        "'.o_form_view .o_property_field'))"
                    ),
                    login="admin",
                )
