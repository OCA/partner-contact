# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    company = env["res.company"]
    ir_property = env["ir.property"]
    field = env["ir.model.fields"]._get("res.partner", "property_product_pricelist")
    for record in company.search([]):
        company_default_pricelist = record.default_property_product_pricelist
        if not company_default_pricelist:
            continue
        ppty = ir_property.search(
            [
                ("name", "=", "property_product_pricelist"),
                ("company_id", "=", record.id),
                ("fields_id", "=", field.id),
                ("res_id", "=", False),
                ("value_reference", "!=", False),
            ],
            limit=1,
        )
        if ppty:
            res = ppty.value_reference.split(",")
            res_id = int(res[1])
            if res_id != company_default_pricelist.id:
                ppty.sudo().write(
                    {
                        "value_reference": "product.pricelist,%s"
                        % company_default_pricelist.id
                    }
                )
        else:
            ir_property.sudo().create(
                {
                    "name": "property_product_pricelist",
                    "value_reference": "product.pricelist,%s"
                    % company_default_pricelist.id,
                    "fields_id": field.id,
                    "company_id": record.id,
                }
            )
