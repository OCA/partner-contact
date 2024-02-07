from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    partner_types = env["res.partner"]._fields.get("type").selection
    partner_types.append((False, "No address type set"))

    env["res.partner.sequence.type"].create(
        [
            {
                "name": v,
                "code": k,
            }
            for k, v in dict(partner_types).items()
        ]
    )
